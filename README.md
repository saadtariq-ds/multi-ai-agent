# 🤖 Multi AI Agent

Multi AI Agent is a **multi-agent Generative AI application** that coordinates multiple specialized agents to solve tasks collaboratively. It uses  **LangChain** to interface with LLM tooling, **Groq** for fast LLM inference, and **Tavily** for real-time web search grounding.

The system exposes APIs via FastAPI, includes a Streamlit UI, is containerized with Docker, validated by SonarQube for code quality/security, automated with Jenkins CI/CD, and deployed on AWS ECS Fargate (serverless containers).

---

## 🚀 Features

- ⚡ Fast LLM responses using Groq
- 🌍 Web-grounded responses using Tavily search
- 🔗 Tool + prompt orchestration with LangChain
- 🌐 FastAPI backend for agent execution and task APIs
- 🎨 Streamlit frontend for interactive multi-agent runs
- 🐳 Dockerized for consistent local + cloud execution
- ✅ SonarQube checks for bugs, vulnerabilities, and bad practices
- 🔁 Jenkins pipelines for build → test → scan → deploy
- ☁️ Runs on AWS ECS Fargate (no server management)

---

## 🧱 High-Level Architecture

1. User enters a task in Streamlit UI (or via API)
2. FastAPI receives the request and triggers agent workflow
3. Agents call Groq LLM for reasoning and generation
4. Agents use Tavily to search the web when external facts are needed
5. Final answer is returned to UI/API
6. CI/CD builds Docker image, runs SonarQube analysis, and deploys to ECS Fargate

---

## 🛠️ Tech Stack

| Category | Tools |
|---------|------|
| LLM | Groq |
| Search Tool | Tavily |
| GenAI Framework | LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
| Containerization | Docker |
| Quality & Security | SonarQube |
| CI/CD | Jenkins |
| Cloud Deployment | AWS ECS Fargate |
| SCM | GitHub |

---

# ⚙️ Local Setup

## 1️⃣ Clone
```bash
git clone https://github.com/your-username/multi-ai-agent.git
cd multi-ai-agent
```

## 2️⃣ Create venv
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

## 3️⃣ Install dependencies
```bash
pip install -e .
```

## 4️⃣ Run App
```bash
python src/main.py
```
