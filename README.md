# Relationship Counseling AI 🧠❤️

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_App-green?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

A **production-grade, privacy-first AI system** designed for supportive relationship counseling. Built with a rigorous 3-layer safety architecture, this system prioritizes user safety, data privacy, and epistemic humility.

> **Note**: This AI is a tool for reflection, *not* a replacement for professional therapy. It is programmed to strictly refuse crisis scenarios and direct users to emergency resources.

---

## 🚀 Key Features

### 🛡️ 3-Layer Safety Architecture
1.  **Input Risk Detection**: Instantly flags crisis keywords (`suicide`, `self-harm`) and blocked topics before they reach the LLM.
2.  **Safety Classification**: Uses a dedicated LLM pass to categorize inputs into `CRISIS`, `HIGH`, `MEDIUM`, or `LOW` risk levels.
3.  **Response Guardrails**: Validates the AI's output to prevent harmful advice, false certainty ("He definitely loves you"), or amateur medical diagnoses.

### 🔒 Privacy-First "Gist" Memory
We **never** store raw conversation logs permanently. The system uses a sophisticated summarization engine to retain only anonymized contexts:
*   ✅ **Stored**: "User is navigating trust issues after a long-distance move."
*   ❌ **Discarded**: "My boyfriend John Smith (555-0199) hit me yesterday at 123 Main St."

### 💰 Cost & Intelligence Routing
The system dynamically selects the best model for the job:
*   **High Risk/Complexity** → Routes to **GPT-4o / Llama 3 70B** for maximum nuance.
*   **Low Risk/Casual** → Routes to **GPT-4o-mini / Llama 3 8B** for speed and cost-efficiency.

---

## 🛠️ Tech Stack

*   **Backend**: Python, Flask (Async support with `asgiref`)
*   **Frontend**: HTML5, TailwindCSS, Vanilla JS (Clean, soothing UI)
*   **AI Providers**: Switchable support for **OpenAI** (native) or **Groq** (high-speed fallback).
*   **Database**: PostgreSQL (JSONB for flexible memory schemas).
*   **Cache**: Redis (for caching low-risk responses and rate limiting).

---

## 🏁 Quick Start

### Prerequisites
*   Python 3.10+
*   PostgreSQL & Redis

### 1. Clone & Setup
```bash
git clone https://github.com/umairinayat/relationship-counseling-cloud.git
cd relationship-counseling-cloud

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r deploy/requirements.txt
```

### 2. Configuration
Rename `.env.example` to `.env` and add your keys:
```ini
# Choose ONE (or both, OpenAI takes precedence)
OPENAI_API_KEY=
GROQ_API_KEY=gsk_your_groq_key_here

# Database Config (ensure DB exists)
DATABASE_URL=postgresql://user:password@localhost:5432/relationship_ai
REDIS_URL=redis://localhost:6379/0
```

### 3. Run the App
```bash
# Easy start script
python start.py
```
Open **http://localhost:8000** in your browser.

---

## 🏗️ Architecture

![Architecture](docs/image.png)



## ⚠️ Limitations
*   **No Diagnosis**: The AI explicitly refuses to diagnose conditions like Narcissism or BPD.
*   **No Directives**: It will not tell a user to "break up" or "stay". It only helps them explore their own decision-making.

---

## 📄 License
MIT License. See `LICENSE` for details.
