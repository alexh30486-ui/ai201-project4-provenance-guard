# 🛡️ Provenance Guard

An AI attribution detection system for creative writing platforms. It analyzes submitted text to determine if it is likely human-written or AI-generated, provides a meaningful confidence score, shows a clear transparency label to readers, and supports creator appeals.

## ✨ Core Features Implemented

- **Content Submission Endpoint** (`POST /submit`): Accepts text content and returns attribution result, confidence score (0-1), and user-facing transparency label.
- **Multi-Signal Detection Pipeline**:
  - **Signal 1: Groq LLM** (`llama-3.3-70b-versatile`) — analyzes semantic patterns and AI-like phrasing.
  - **Signal 2: Stylometric Heuristics** — measures vocabulary diversity and sentence length uniformity.
- **Confidence Scoring**: Weighted average `(0.6 × LLM score) + (0.4 × Stylometric score)`.
- **Transparency Labels**: Three clear variants based on confidence level.
- **Appeals Workflow**: Creators can contest decisions with reasoning.
- **Rate Limiting**: 10 requests per hour per IP.
- **Audit Log**: Full SQLite database logging every decision and appeal.

---

## 🚀 Installation & Setup

```bash
cd ai201-project4-provenance-guard
source .venv/bin/activate
pip install -r requirements.txt

# Setup API key
cp .env.example .env
nano .env