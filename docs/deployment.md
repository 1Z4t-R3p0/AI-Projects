# Deployment Instructions (Ubuntu)

## Prerequisites
- Ubuntu 20.04/22.04 LTS
- Python 3.8+
- Node.js 16+ (or via NVM)

## 1. System Setup
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git
```

## 2. Clone & Backend Setup
```bash
git clone <repo-url>
cd AI-Learning-Roadmap
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
echo "OPENROUTER_API_KEY=your_key_here" > .env
```

## 3. Frontend Setup
```bash
cd frontend
npm install
npm run build
```

## 4. Serving the Application

### Option A: Development Mode (easiest for Viva)
Terminal 1 (Backend):
```bash
uvicorn backend.main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
npm run dev
```

### Option B: Production (Nginx + PM2)
1. Install Nginx & PM2:
   `sudo apt installnginx`
   `sudo npm install -g pm2`

2. Start Backend:
   `pm2 start "uvicorn backend.main:app --port 8000" --name backend`

3. Serve Frontend with Nginx (Copy build to /var/www/html).
