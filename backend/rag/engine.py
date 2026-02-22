import os
from typing import Dict, Any


from duckduckgo_search import DDGS
from typing import List, Dict, Any

import os
import json
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

from backend.storage.redis_client import RedisClient

class RAGEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        self.redis = RedisClient()
        
        # Initialize Vector DB for Retrieval
        self.db_dir = "./backend/vector_db"
        try:
            self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            self.vector_db = Chroma(persist_directory=self.db_dir, embedding_function=self.embeddings)
            print("✅ Vector DB Loaded.")
        except Exception as e:
            print(f"⚠️ Vector DB Load Error: {e}")
            self.vector_db = None
        
        # Priority list of free models to try
        self.models = [
            "deepseek/deepseek-r1:free",
            "google/gemini-2.0-flash-lite-preview-02-05:free",
            "meta-llama/llama-3-8b-instruct:free",
            "mistralai/mistral-7b-instruct:free",
            "microsoft/phi-3-medium-128k-instruct:free",
            "openrouter/auto:free"
        ]
        self.current_model_index = 0
        self.model = self.models[0]

    def search_web(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """Tool: Real-time Web Search"""
        results = []
        try:
            with DDGS() as ddgs:
                search_query = f"{query} geeksforgeeks free tutorial documentation"
                for r in ddgs.text(search_query, max_results=max_results):
                    results.append({
                        "title": r['title'],
                        "link": r['href'],
                        "snippet": r['body']
                    })
        except Exception as e:
            print(f"Search Error: {e}")
        
        if not results:
            results.append({
                "title": "Google Search",
                "link": f"https://www.google.com/search?q={query}",
                "snippet": "Fallback: Click to search manually."
            })
        return results

    def _classify_intent(self, user_query: str) -> str:
        """Step 1: Identify/Classify Intent"""
        if not self.api_key:
            return "chat"
            
        system_prompt = (
            "You are the 'Brain' of an educational chatbot. "
            "Classify the user's input into exactly one of these categories:\n"
            "1. 'roadmap': If user wants a study plan, path, or curriculum.\n"
            "2. 'search': If user asks for specific resources, links, or factual lookup.\n"
            "3. 'chat': General conversation, greeting, or philosophical questions.\n"
            "Output ONLY the category name."
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )
            intent = response.choices[0].message.content.strip().lower()
            if "roadmap" in intent: return "roadmap"
            if "search" in intent: return "search"
            return "chat"
        except Exception as e:
            print(f"Classification Error: {e}")
            # Fallback Logic
            q = user_query.lower()
            if "roadmap" in q or "plan" in q or "path" in q: return "roadmap"
            if "find" in q or "search" in q or "tutorial" in q or "resource" in q: return "search"
            return "chat"

    async def process_query(self, query: str, department: str, session_id: str = None) -> str:
        """
        Pipeline: Input -> Context -> Classify -> Function Call -> Response
        """
        if not self.api_key:
             return "⚠️ API Key missing. Please check .env file."

        print(f"🧠 Processing: '{query}' for {department} (Session: {session_id})")
        
        # 0. Retrieve Context
        history = self.redis.get_context(session_id) if session_id else []
        context_block = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
        
        # 1. Classify
        intent = self._classify_intent(query)
        print(f"👉 Intent Detected: {intent}")
        
        external_context = ""
        system_instruction = ""
        
        # 2. Function Call logic
        if intent == "search":
            # Web Search
            results = self.search_web(f"{department} {query}")
            external_context = "Web Search Results:\n" + "\n".join([f"- {r['title']}: {r['snippet']} ({r['link']})" for r in results])
            system_instruction = "You are a helpful assistant. Use the provided Search Results to answer the user."
            
        elif intent == "roadmap":
            # RAG Retrieval
            system_instruction = "You are a mentor. Use the provided Roadmap Context to outline a learning path."
            external_context = f"User wants a roadmap for {department}."
            
            if self.vector_db:
                try:
                    print("🔍 Searching Vector DB...")
                    docs = self.vector_db.similarity_search(query, k=3)
                    retrieved_text = "\n\n".join([f"[Source: {d.metadata.get('source', 'Unknown')}]\n{d.page_content}" for d in docs])
                    external_context += f"\n\nRoadmap Context (Retrieved):\n{retrieved_text}"
                except Exception as e:
                    print(f"⚠️ Retrieval Error: {e}")
            
        else: # Chat
            system_instruction = "You are a friendly AI mentor. Answer directly, using the conversation history for context."
            external_context = "General conversation."
            
            # Optional: Also try retrieval for chat if it seems technical
            if self.vector_db:
                 try:
                    docs = self.vector_db.similarity_search(query, k=2)
                    retrieved_text = "\n".join([d.page_content for d in docs])
                    external_context += f"\n\nRelevant Context:\n{retrieved_text}"
                 except: pass

        # 3. Final Response Generation
        full_prompt = f"History:\n{context_block}\n\nContext:\n{external_context}\n\nUser Query: {query}"
        
        for attempt in range(len(self.models)):
            try:
                print(f"🤖 Using Model: {self.model}")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": full_prompt}
                    ]
                )
                ai_response = response.choices[0].message.content
                
                # 4. Save to Redis
                if session_id:
                    self.redis.add_message(session_id, "user", query)
                    self.redis.add_message(session_id, "assistant", ai_response)
                    
                return ai_response

            except Exception as e:
                print(f"⚠️ Error with {self.model}: {e}")
                # Switch to next model
                self.current_model_index = (self.current_model_index + 1) % len(self.models)
                self.model = self.models[self.current_model_index]
                continue
        
        # Fallback if all models fail
        fallback = f"AI Error: All models failed. Please try again later.\n\nBased on my search:\n\n{external_context}"
        if session_id:
            self.redis.add_message(session_id, "user", query)
            self.redis.add_message(session_id, "assistant", fallback)
        return fallback

    async def generate_roadmap(self, department: str, level: str) -> Dict[str, Any]:
        """
        Generates structured JSON roadmap using LLM.
        """
        if not self.api_key:
            return {"title": "Error", "modules": []}

        prompt = (
            f"Generate a detailed 4-week structured learning roadmap for {department} at {level} level. "
            "Ensure you provide content for ALL 4 WEEKS. "
            "For 'resources', prioritize **GeeksforGeeks (GFG)**, **Official Documentation**, and **FreeCodeCamp** articles. "
            "**DO NOT** generate specific YouTube video URLs (like 'youtube.com/watch?v=...') as they often break. "
            "Instead, link to the YouTube **Channel** or a generic Search URL (e.g., 'https://www.youtube.com/results?search_query=...'). "
            "Output strictly valid JSON with this structure: "
            "{'title': '...', 'modules': [{'week': 1, 'topic': '...', 'description': '...', 'resources': [{'title': '...', 'link': '...'}]}]}. "
            "Do not add markdown formatting like ```json, just return the raw JSON object."
        )

        for attempt in range(len(self.models)):
            try:
                print(f"🗺️  Generating Roadmap with {self.model}...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.choices[0].message.content.strip()
                
                # Cleanup potential markdown wrapper if present
                if content.startswith("```"):
                    # Find the first and last backticks to extract content
                    start = content.find("```") + 3
                    if content[start:].startswith("json"):
                        start += 4
                    end = content.rfind("```")
                    content = content[start:end].strip()
                
                return json.loads(content)
            
            except Exception as e:
                print(f"⚠️ Roadmap Gen Error ({self.model}): {e}")
                # Switch to next model
                self.current_model_index = (self.current_model_index + 1) % len(self.models)
                self.model = self.models[self.current_model_index]
                continue

        # Fallback if all models fail
        return {
            "title": f"{department} (Fallback)",
            "modules": [{"week": 1, "topic": "Basics", "description": "AI generation failed, please try again.", "resources": []}]
        }

rag_engine = RAGEngine()
