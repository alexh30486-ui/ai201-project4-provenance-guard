cat > README.md << 'EOF'
# 🛡️ Provenance Guard

An AI attribution detection system for creative writing platforms. It analyzes submitted text to determine if it is likely human-written or AI-generated, provides a meaningful confidence score, shows a clear transparency label to readers, and supports creator appeals.

## ✨ Core Features Implemented
- **Content Submission Endpoint** (`POST /submit`): Accepts text content and returns attribution result, confidence score (0-1), and user-facing transparency label.
- **Multi-Signal Detection Pipeline**:
  - **Signal 1: Groq LLM** (`llama-3.3-70b-versatile`) — analyzes semantic patterns and AI-like phrasing.
  - **Signal 2: Stylometric Heuristics** — measures vocabulary diversity and sentence length uniformity.
- **Confidence Scoring**: Weighted average `(0.6 × LLM score) + (0.4 × Stylometric score)`.
- **Transparency Labels**: Three clear variants based on confidence level (`likely_ai`, `likely_human`, `uncertain`).
- **Appeals Workflow**: Creators can contest decisions with reasoning via `POST /appeal`.
- **Rate Limiting**: 10 requests per hour per IP.
- **Audit Log**: Full SQLite database (`audit.db`) logging every decision and appeal, utilizing UUIDs and content hashing for privacy.

---

## 🚀 Installation & Setup

```bash
# 1. Navigate to project directory and activate virtual environment
cd ai201-project4-provenance-guard
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup API key
# (Copy the example file, open it, and paste your GROQ_API_KEY)
cp .env.example .env
nano .env

# 4. Run the server
python app.py
