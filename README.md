# 🤖 AI-ChatBot: Advanced RAG Pipeline

A sophisticated, containerized Natural Language Processing AI ChatBot integrated with a Retrieval-Augmented Generation (RAG) pipeline and high-performance Redis context memory.

---

## 💎 Features

- **Context-Aware Memory**: Integrates an advanced Redis backend to persist and map context history to individual user sessions.
- **RAG Engine**: Incorporates Retrieval-Augmented Generation principles.
- **Microservice Architecture**: Fully decoupled backend (Python/FastAPI-styled) and frontend (React/Vanilla) interconnected via REST.
- **Universal Containerization**: Built purely on Docker, ensuring no environment configuration or dependency management errors.

---

## 🛠️ Automated Zero-Touch Deployment

Deploy the AI-ChatBot seamlessly on Windows or Linux. These scripts will automatically install **Docker**, clone the repository, prompt for your OpenRouter API Key, and start the system via `docker-compose`.

### 🪟 Windows (PowerShell)
Run this command from an elevated PowerShell command prompt:
```powershell
irm https://raw.githubusercontent.com/1Z4t-R3p0/AI-ChatBot/main/win-setup.ps1 | iex
```

### 🐧 WSL / Linux
Run this command from your terminal:
```bash
curl -fsSL https://raw.githubusercontent.com/1Z4t-R3p0/AI-ChatBot/main/wsl-setup.sh | bash
```

---

## 🚀 Manual Local Setup (Docker)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/1Z4t-R3p0/AI-ChatBot.git
   cd AI-ChatBot
   ```

2. **Configure Authentication**:
   Create a `.env` file in the root directory and add your OpenRouter API Key:
   ```bash
   OPENROUTER_API_KEY=your_key_here
   ```

3. **Launch the Infrastructure**:
   ```bash
   docker compose up -d --build
   ```

4. **Access the Microservices**:
   - **User Interface (Frontend)**: [http://localhost:8080](http://localhost:8080)
   - **Backend API Engine**: [http://localhost:8001](http://localhost:8001)
   - **Redis Store**: `localhost:6380`

---
*Created by [1Z4t](https://github.com/1Z4t-R3p0)*
# AI-Projects
