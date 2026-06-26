# 🛡️ Provenance Guard CODE PATH Project

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

## 🏗️ Architecture
The system uses a hybrid detection engine combining LLM semantic analysis and local stylometric heuristics.

```text
[User Input] --> [Flask /submit] --> [LLM Signal: Groq Llama 3]
                     |                        |
                     +--> [Stylometric Signal] --+--> [Confidence Engine]
                     |     (Heuristics)               (Weighted Avg)
                     |                                      |
            [Audit Log / SQLite] <--------------------------+
🔍 Detection Pipeline Details
We use a weighted ensemble approach: (0.6 × LLM score) + (0.4 × Stylometric score).

Signal	What it Measures	What it Misses
Groq LLM	Semantic patterns and "AI-voice" markers.	Can be fooled by highly creative human writing.
Stylometric	Vocabulary diversity, sentence structure, and length uniformity.	Misses nuance; can misclassify technical manuals as "robotic."
🏷️ Transparency Labels
We provide three tiers of attribution based on the final confidence score.

Label Type	Threshold	Transparency Text
likely_ai	> 0.8	"This content appears to be AI-generated. Our system detected strong AI patterns."
likely_human	< 0.3	"This content appears to be human-written."
uncertain	0.3 - 0.8	"Attribution uncertain. Could be either; creator may appeal."
⚠️ Known Limitations
The system relies on stylistic heuristics that assume "standard" human writing patterns. Consequently, creative poetry, experimental literature, or highly specific technical documentation may be misclassified. Because these formats often use irregular sentence lengths or repetitive vocabulary, the Stylometric signal may incorrectly label them as AI-generated.

📝 Spec Reflection
The original plan was to build the audit log using a standard JSON file. However, during implementation, I diverged by switching to SQLite. This was necessary because a flat JSON file would become a bottleneck for concurrent read/write operations and would not support the efficient relational queries required for the /log and /appeal endpoints.

🤖 AI Usage

Detection Logic Optimization: I directed the AI to write the stylometric_analysis function. The AI initially suggested a simple average, but I overrode this by adding a conditional check for vocabulary diversity. This ensured the signal captures word variety rather than just length, significantly improving accuracy on short inputs.
Rate Limiting Implementation: I requested a Flask-Limiter boilerplate. The AI suggested a default 200/day limit, which I rejected. I manually revised this to 10/hour to better align with the project's goal of detecting malicious bulk-generation behavior on a writing platform.
🚀 Installation & Setup

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
📚 API Reference

Submit Content
POST /submit
Payload: {"text": "string", "creator_id": "string"}
View Audit Log
GET /log
Submit Appeal
POST /appeal
Payload: {"content_id": "uuid", "reason": "string"}
EOF
**After pasting the above**, run these commands to verify and commit:

```bash
cat README.md          # Check it looks good
git add README.md
git commit -m "Final polished README for submission"
git push
You're all set! Let me know if you need any small changes.
Detection Pipeline Details
We use a weighted ensemble approach: (0.6 × LLM score) + (0.4 × Stylometric score).
 

| Signal | What it Measures | What it Misses |
| --- | --- | --- |
| Groq LLM | Semantic patterns and "AI-voice" markers. | Can be fooled by highly creative human writing. |
| Stylometric | Vocabulary diversity, sentence structure, and length uniformity. | Misses nuance; can misclassify technical manuals as "robotic." |
🏷️ Transparency Labels
We provide three tiers of attribution based on the final confidence score.
 

| Label Type | Threshold | Transparency Text |
| --- | --- | --- |
| likely_ai | > 0.8 | "This content appears to be AI-generated. Our system detected strong AI patterns." |
| likely_human | < 0.3 | "This content appears to be human-written." |
| uncertain | 0.3 - 0.8 | "Attribution uncertain. Could be either; creator may appeal." |
⚠️ Known Limitations
The system relies on stylistic heuristics that assume "standard" human writing patterns. Consequently, creative poetry, experimental literature, or highly specific technical documentation may be misclassified. Because these formats often use irregular sentence lengths or repetitive vocabulary, the Stylometric signal may incorrectly label them as AI-generated.
📝 Spec Reflection
The original plan was to build the audit log using a standard JSON file. However, during implementation, I diverged by switching to SQLite. This was necessary because a flat JSON file would become a bottleneck for concurrent read/write operations and would not support the efficient relational queries required for the /log and /appeal endpoints.
🤖 AI Usage

Detection Logic Optimization: I directed the AI to write the stylometric_analysis function. The AI initially suggested a simple average, but I overrode this by adding a conditional check for vocabulary diversity. This ensured the signal captures word variety rather than just length, significantly improving accuracy on short inputs.
Rate Limiting Implementation: I requested a Flask-Limiter boilerplate. The AI suggested a default 200/day limit, which I rejected. I manually revised this to 10/hour to better align with the project's goal of detecting malicious bulk-generation behavior on a writing platform.

                 
