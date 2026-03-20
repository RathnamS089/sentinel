
**The Sentinel** is an AI-powered security auditor designed to scan GitHub repositories for dependency vulnerabilities. By analyzing files like `requirements.txt` or `pyproject.toml`, it uses the **Gemini 3 Flash Preview** model to provide a categorized security report, a letter-grade rating, and a health score. It features a persistent scan history, allowing users to track the security evolution of multiple projects in a single session.

# 🛡️ The Sentinel: AI Dependency Auditor

The Sentinel is a specialized security tool that leverages Generative AI to audit Python dependency files for known vulnerabilities and best-practice violations.

## ✨ Features
* **AI-Powered Analysis:** Uses Google Gemini 3 Flash Preview  for deep security insights.
* **Instant Scoring:** Provides a numerical health score and a letter grade (A-F).
* **Scan History:** Keep track of all repository audits in a sidebar for quick navigation.
* **Dockerized:** Ready for consistent deployment across any environment.
* **Modern UI:** A clean, responsive dashboard built with Tailwind CSS.

## 🚀 Getting Started

### Prerequisites
* Docker Desktop 🐳
* Google Gemini API Key 🔑

### Local Setup (Using Docker)
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/the-sentinel.git](https://github.com/your-username/the-sentinel.git)
   cd the-sentinel

```

2. Create a `.env` file and add your API key:
```env
GOOGLE_API_KEY=your_key_here

```


3. Build and run the container:
```bash
docker build -t sentinel-app .
docker run -p 8000:8000 --env-file .env sentinel-app

```

4. Open your browser to `http://localhost:8000`

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **AI Engine:** Google GenAI (Gemini 3 Flash Preview)
* **Frontend:** Jinja2 Templates & Tailwind CSS
* **Deployment:** Docker
