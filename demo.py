import sqlite3
from datetime import datetime
print("Provenance Guard Demo")

conn = sqlite3.connect('audit.db')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM decisions")
if c.fetchone()[0] == 0:
    samples = [
        (datetime.now().isoformat(), "hash1", 0.9, 0.8, 0.86, "high-confidence-ai", "{}", "processed"),
        (datetime.now().isoformat(), "hash2", 0.2, 0.3, 0.24, "high-confidence-human", "{}", "processed"),
        (datetime.now().isoformat(), "hash3", 0.5, 0.6, 0.54, "uncertain", "{}", "under_review"),
    ]
    c.executemany("INSERT INTO decisions (timestamp, content_hash, llm_score, stylo_score, confidence, label, signals, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", samples)
    conn.commit()
c.execute("SELECT * FROM decisions LIMIT 3")
print("Sample Audit Log:")
for row in c.fetchall():
    print(row)
conn.close()
