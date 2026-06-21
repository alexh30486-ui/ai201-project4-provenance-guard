# Provenance Guard - Planning Document

## Architecture Narrative
After reading the full project spec, I took time to sketch how the whole system should work together.

A submitted text goes through this path:
POST /submit → Rate Limiter → Groq LLM Signal + Stylometric Signal → Combine scores into confidence → Generate transparency label → Save everything to SQLite audit log → Return JSON response to user.

For appeals: POST /appeal with decision_id + reason → find the record → change status to "under_review" → save appeal reason in audit log.

## Detection Signals
I chose two distinct signals after thinking about their strengths and weaknesses.

**1. Groq LLM (llama-3.3-70b-versatile)**
- What it measures: Semantic patterns, AI-like phrasing, and stylistic uniformity.
- Output: Score between 0.0 and 1.0 (1.0 = very likely AI).
- Why I chose it: It can understand meaning and subtle patterns that numbers alone can't catch.
- What it misses: Heavily edited AI text or very creative human writing.

**2. Stylometric Heuristics**
- What it measures: Vocabulary diversity (type-token ratio) and average sentence length.
- Output: Score between 0.0 and 1.0 (higher = more uniform, more AI-like).
- Why I chose it: Simple, fast, pure Python, and looks at completely different things (structure).
- What it misses: Short texts and poems that use repetition on purpose.

**Combination**: I used 0.6 * LLM score + 0.4 * Stylometric score.

## Uncertainty Representation
I wanted the confidence score to feel real.
A score of 0.6 means the two signals are not agreeing — we are genuinely uncertain.

Final thresholds I decided on:
- < 0.30 → High-confidence Human
- 0.30 – 0.79 → Uncertain
- ≥ 0.80 → High-confidence AI

## Transparency Label Design
Here are the exact texts I designed:

- **High-confidence AI** (≥ 0.80):  
  "This content appears to be AI-generated (Confidence: XX%). Our system detected strong AI patterns."

- **High-confidence Human** (< 0.30):  
  "This content appears to be human-written (Confidence: XX%)."

- **Uncertain** (0.30–0.79):  
  "Attribution uncertain (Confidence: XX%). Could be either; creator may appeal."

## Appeals Workflow
Any creator can appeal by sending the decision_id and their reasoning. The system updates the status to "under_review" and saves the reason in the audit log so a reviewer can see the full history.

## Anticipated Edge Cases
- A short poem with lots of repetition (stylometrics may wrongly flag as AI).
- Text that was AI-generated but then heavily edited by a human (LLM may return uncertain).

## Architecture Diagram


## AI Tool Plan
- M3: Gave Grok the detection signals section + diagram to generate Flask app skeleton + Groq function.
- M4: Used signals + uncertainty section to generate stylometric function and scoring logic.
- M5: Used label variants + appeals section to generate label logic and /appeal endpoint.

I took time to think through each section carefully before starting to code. This planning step really helped everything connect properly at the end.
