import os
import requests
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Configuration
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps"
TARGET_ROADMAPS = ["cyber-security", "frontend", "backend", "devops", "python", "javascript", "react"]
DB_DIR = "./backend/vector_db"

def fetch_roadmap_data(roadmap_id):
    """Fetches key topics from a specific roadmap JSON."""
    # Structure found: src/data/roadmaps/<id>/<id>.json
    url = f"{GITHUB_RAW_BASE}/{roadmap_id}/{roadmap_id}.json"
    try:
        print(f"📥 Fetching: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"❌ Failed to fetch {roadmap_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Error fetching {roadmap_id}: {e}")
        return None

def process_node(node, roadmap_title, documents):
    """Recursively extracts text from roadmap nodes."""
    # Extract Topic title and description
    # Some nodes might be just a string ID, others objects
    title = node.get("title", "")
    description = node.get("description", "")
    
    if title or description:
        content = f"Roadmap: {roadmap_title}\nTopic: {title}\nDescription: {description}"
        metadata = {"source": roadmap_title, "topic": title}
        documents.append(Document(page_content=content, metadata=metadata))

    # Check for children
    children = node.get("children", [])
    for child in children:
        process_node(child, roadmap_title, documents)

def ingest_data():
    """
    1. Read Roadmaps from GitHub.
    2. Split text into chunks.
    3. Generate embeddings using SentenceTransformers.
    4. Store in ChromaDB.
    """
    print("🔄 Starting Data Ingestion...")
    
    all_documents = []

    for roadmap_id in TARGET_ROADMAPS:
        data = fetch_roadmap_data(roadmap_id)
        if not data:
            continue
            
        # The JSON structure usually has a 'json' key containing the nodes tree, or it IS the tree
        # Based on research, it seems structure varies, but let's try to parse the 'json' field if present or the list
        
        # NOTE: Simple traversal - specific structure depends on exact JSON format
        # We will assume a flexible extraction strategy
        
        content_text = json.dumps(data) # Fallback: Embed the whole JSON string if parsing fails? No, too big.
        
        # Let's try to extract specific relevant sections if possible, otherwise use a generic JSON loader approach
        # For now, we'll treat each roadmap as a large text and split it, 
        # as complex tree traversal might fail without exact schema knowledge.
        
        # Better approach: Convert JSON to a text representation
        text_content = f"Roadmap: {roadmap_id.replace('-', ' ').title()}\n\n"
        
        # Simply dump the JSON to string for now, but cleaner.
        # Capturing "title" and "description" fields via regex or iteration would be better but
        # JSON text splitting is a decent MVP.
        
        text_content += json.dumps(data, indent=2)
        
        metadata = {"source": roadmap_id}
        doc = Document(page_content=text_content, metadata=metadata)
        all_documents.append(doc)

    if not all_documents:
        print("⚠️ No documents to ingest.")
        return

    # Text Splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(all_documents)
    
    print(f"🧩 Split into {len(split_docs)} chunks.")

    # Embeddings
    print("🧠 Generating Embeddings (all-MiniLM-L6-v2)...")
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Store in ChromaDB
    print(f"💾 Saving to ChromaDB at {DB_DIR}...")
    db = Chroma.from_documents(
        documents=split_docs, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    db.persist()
    print("✅ Ingestion Complete!")

if __name__ == "__main__":
    ingest_data()
