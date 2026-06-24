import os
import sqlite3
import hashlib
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per hour"])
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def init_db():
    conn = sqlite3.connect('audit.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS decisions
                 (content_id TEXT PRIMARY KEY, creator_id TEXT, timestamp TEXT, content_hash TEXT, 
                  llm_score REAL, stylo_score REAL, confidence REAL, label TEXT, 
                  signals TEXT, appeal_reason TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_content_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def stylometric_analysis(text):
    words = text.split()
    sentences = text.split('.')
    unique_words = len(set(words))
    vocab_diversity = unique_words / len(words) if words else 0
    avg_sent_len = len(words) / len(sentences) if sentences else 0
    score = 0.5
    if vocab_diversity < 0.4: score += 0.3
    if 15 < avg_sent_len < 25: score += 0.2
    return min(1.0, score)

def llm_analysis(text):
    prompt = f"Analyze if this text is likely AI-generated. Return only a score 0-1 (1=AI) and reason. Text: {text[:2000]} Score:"
    try:
        completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        response = completion.choices[0].message.content.strip()
        import re
        score_match = re.search(r'([0-9]*\.?[0-9]+)', response)
        return min(1.0, max(0.0, float(score_match.group(1)))) if score_match else 0.5
    except: return 0.5

@app.route('/submit', methods=['POST'])
@limiter.limit("10 per hour")
def submit_content():
    data = request.json
    if not data or 'text' not in data or 'creator_id' not in data:
        return jsonify({"error": "text and creator_id required"}), 400
    text, creator_id = data['text'], data['creator_id']
    content_hash = get_content_hash(text)
    llm_score = llm_analysis(text)
    stylo_score = stylometric_analysis(text)
    confidence = round(0.6 * llm_score + 0.4 * stylo_score, 2)
    label = "likely_ai" if confidence > 0.8 else "likely_human" if confidence < 0.3 else "uncertain"
    display_text = f"Attribution {'AI-generated' if label=='likely_ai' else 'human-written' if label=='likely_human' else 'uncertain'} (Confidence: {int(confidence*100)}%). {'Could be either; creator may appeal.' if label == 'uncertain' else ''}"
    content_id = str(uuid.uuid4())
    conn = sqlite3.connect('audit.db')
    c = conn.cursor()
    c.execute("INSERT INTO decisions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
              (content_id, creator_id, datetime.now().isoformat() + "Z", content_hash, llm_score, stylo_score, confidence, label, json.dumps({"llm": llm_score, "stylo": stylo_score}), None, "classified"))
    conn.commit()
    conn.close()
    return jsonify({"content_id": content_id, "attribution": label, "confidence": confidence, "label": display_text})

@app.route('/appeal', methods=['POST'])
def appeal():
    data = request.json
    if not data or 'content_id' not in data or 'reason' not in data: return jsonify({"error": "content_id and reason required"}), 400
    conn = sqlite3.connect('audit.db')
    c = conn.cursor()
    c.execute("UPDATE decisions SET appeal_reason=?, status='under_review' WHERE content_id=?", (data['reason'], data['content_id']))
    conn.commit()
    updated = c.rowcount > 0
    conn.close()
    return jsonify({"status": "appeal logged" if updated else "not found"})

@app.route('/log', methods=['GET'])
def get_log():
    conn = sqlite3.connect('audit.db')
    c = conn.cursor()
    c.execute("SELECT content_id, creator_id, timestamp, label, confidence, llm_score, status FROM decisions ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"content_id": r[0], "creator_id": r[1], "timestamp": r[2], "attribution": r[3], "confidence": r[4], "llm_score": r[5], "status": r[6]} for r in rows])

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Provenance Guard API is running. Use /submit, /appeal, or /log."})

if __name__ == '__main__': app.run(debug=True)
