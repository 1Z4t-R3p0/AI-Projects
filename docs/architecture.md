# System Architecture: AI Learning Roadmap Assistant

## 1. High-Level Overview
The AI Learning Roadmap Assistant is a 3-tier web application designed to provide personalized educational guidance. It leverages **Retrieval Augmented Generation (RAG)** to provide accurate, context-aware responses and structured learning paths without hallucinating core facts.

### System Diagram
```mermaid
graph TD
    User[Student] -->|Interact via UI| frontend[Frontend (React + Tailwind)]
    frontend -->|HTTP REST API| backend[Backend API (FastAPI)]
    
    subgraph Backend System
        backend -->|Auth & Session| SessionMgr[Session Manager]
        backend -->|Query| RAG[RAG Engine]
        backend -->|Schedule| Scheduler[Reminder Service]
        
        RAG -->|Retrieve Context| VectorDB[(ChromaDB - Local)]
        RAG -->|Generate Answer| LLM[OpenRouter / Local LLM]
        
        SessionMgr -->|Read/Write| LocalDB[(SQLite/JSON)]
    end
    
    subgraph Data Sources
        Ingest[Ingestion Script] -->|Process| PDF[PDF Resources]
        Ingest -->|Process| Web[Web Resources]
        Ingest -->|Embed| VectorDB
    end
```

## 2. Technology Stack

### Frontend (Client-Side)
- **Framework**: React.js (Vite Bundle)
- **Styling**: Tailwind CSS (Modern, responsive)
- **State Management**: React Context API
- **Icons**: Lucide-React

### Backend (Server-Side)
- **Framework**: FastAPI (Python) - High performance, easy async support.
- **AI Orchestration**: LangChain or direct API integration.
- **Vector Database**: ChromaDB (Running locally in-process or via lightweight server).
- **Scheduler**: `APScheduler` for background tasks (reminders).

### AI & Data
- **LLM**: Models via OpenRouter (e.g., Mistral 7B, Llama 3) for free tier access.
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (Local execution, no API cost).

## 3. Data Flow

### A. Chat & Question Answering
1. **Input**: User asks "What is a neural network?"
2. **Embed**: Backend generates embedding for the query using local model.
3. **Retrieve**: ChromaDB finds relevant documents (textbook snippets, tutorials).
4. **Augment**: The retrieved context + original question are sent to the LLM.
5. **Generate**: LLM provides an answer citing the resources.

### B. Roadmap Generation
1. **Trigger**: User selects "Cyber Security" -> "Beginner".
2. **Template Retrieval**: System fetches the base structure for Cyber Sec.
3. **Customization**: LLM tailors the weekly plan based on user constraints (e.g., "I have 5 hours/week").
4. **Response**: structured JSON returned to frontend to render a Timeline UI.

## 4. Key Design Decisions for "Final Year Project"
- **Zero Cost Architecture**: By using local embeddings and free-tier LLMs, the project fits the student budget constraint.
- **Offline Capability**: The core application logic and vector DB are local. Only the final inference step requires internet (unless a local LLM is swapped in).
- **Scalability**: The modular folder structure allows easy addition of new Departments or Resource types.
