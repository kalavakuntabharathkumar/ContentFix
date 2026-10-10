import sqlite3
from pathlib import Path

def connect(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS fix_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page TEXT NOT NULL,
        issue_type TEXT NOT NULL,
        detail TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    return conn

def sync_issues(conn, issues):
    for issue in issues:
        conn.execute(
            "INSERT INTO fix_requests(page, issue_type, detail) VALUES (?, ?, ?)",
            (issue["page"], issue["issue_type"], issue["detail"])
        )
    conn.commit()

def fetch_requests(conn):
    return conn.execute(
        "SELECT id, page, issue_type, detail, status, created_at FROM fix_requests ORDER BY id DESC"
    ).fetchall()

def update_status(conn, request_id: int, status: str):
    if status not in {"open", "in_progress", "resolved"}:
        raise ValueError("Unsupported status")
    conn.execute("UPDATE fix_requests SET status=? WHERE id=?", (status, request_id))
    conn.commit()
