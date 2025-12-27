# Relationship Counseling AI (Production System)

A privacy-first, safety-critical AI system designed for supportive relationship conversations.

## Key Features
- **Privacy-First Memory**: No raw conversation text is ever stored. Only anonymized "gists" (themes, context) are retained.
- **3-Layer Safety System**: Input risk detection, prohibited topic filtering, and strict crisis protocols.
- **Cost-Optimized**: Automatic model routing (GPT-4o vs 4o-mini) based on risk validation.
- **Epistemic Humility**: Enforced non-directive language and avoided diagnostic claims.

## Quick Start (Docker)

1. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY to .env
   ```

2. **Run with Docker Compose**
   ```bash
   cd deploy
   docker-compose up --build
   ```

3. **Access the Interface**
   Open http://localhost:8000 in your browser.

## Project Structure
- `src/web/`: Flask application and UI templates.
- `src/orchestration/`: Main logic flow and safety guardrails.
- `src/memory/`: Privacy-preserving summarization and retrieval.
- `src/cost/`: Model routing and token budgeting.
- `src/llm/`: Prompts and robust client.
- `docs/`: Detailed design and safety documentation.
