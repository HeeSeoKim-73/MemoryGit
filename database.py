import sqlite3
from datetime import datetime


DB_NAME = "memorygit.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_id TEXT UNIQUE NOT NULL,
            branch TEXT NOT NULL,
            content TEXT NOT NULL,
            status TEXT NOT NULL,
            memory_hash TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_parents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_memory_id TEXT NOT NULL,
            parent_memory_id TEXT NOT NULL
        )
    """)

    conn.commit()

    cursor.execute("PRAGMA table_info(memories)")
    columns = [column[1] for column in cursor.fetchall()]

    if "memory_hash" not in columns:
        cursor.execute("""
            ALTER TABLE memories
            ADD COLUMN memory_hash TEXT
        """)

    conn.commit()
    conn.close()


def get_next_memory_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT memory_id
        FROM memories
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return "M001"

    last_id = int(row[0][1:])

    return f"M{last_id + 1:03d}"


def save_memory(branch, content, status, memory_hash=None):
    memory_id = get_next_memory_id()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memories (
            memory_id,
            branch,
            content,
            status,
            memory_hash,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        memory_id,
        branch,
        content,
        status,
        memory_hash,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

    return memory_id


def save_parent(child_memory_id, parent_memory_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memory_parents (
            child_memory_id,
            parent_memory_id
        )
        VALUES (?, ?)
    """, (
        child_memory_id,
        parent_memory_id
    ))

    conn.commit()
    conn.close()


def get_all_memories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            memory_id,
            branch,
            content,
            status,
            memory_hash,
            created_at
        FROM memories
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_parents(memory_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT parent_memory_id
        FROM memory_parents
        WHERE child_memory_id = ?
    """, (
        memory_id,
    ))

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]