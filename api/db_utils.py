import sqlite3
from datetime import datetime
from contextlib import contextmanager


DB_NAME = "rag_app.db"

@contextmanager
def get_db_connection():
    """Context manager for SQLite connection with ROW Factory enabled"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row #Return structured results (dicts) using row_factory.
    try:
        yield conn
        conn.commit() # auto-commit on success
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

# Schema Initialization
def init_db():
    """Initialize required tables if they don't exist."""
    with get_db_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS application_logs(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_id TEXT,
                            user_query TEXT,
                            gpt_response TEXT,
                            model TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS document_store(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT,
                            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )""")

# Application logs
def insert_application_logs(session_id, user_query,gpt_response,model):
    with get_db_connection() as conn:
        conn.execute("""INSERT INTO application_logs (session_id, user_query, gpt_response, model)
                        VALUES (?,?,?,?)""", (session_id,user_query,gpt_response,model))
        
def get_chat_history(session_id):
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at",(session_id,))
        messages = []
        for row in cursor.fetchall():
            messages.extend([
                {'role':"human","content":row["user_query"]},
                {"role":"ai","content":row["gpt_response"]}
            ])
        return messages
    

# Document Store
def insert_document_record(filename):
    with get_db_connection() as conn:
        cursor = conn.execute("INSERT INTO document_store (filename) VALUES (?)",(filename,))
        return cursor.lastrowid
    
def delete_document_record(file_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM document_store WHERE id = ?",(file_id,))
        return True
    
def get_all_documents():
    with get_db_connection() as conn:
        cursor = conn.execute("""SELECT id, filename, upload_timestamp
                                FROM document_store
                                ORDER BY upload_timestamp DESC""")
        return [dict(row) for row in cursor.fetchall()]


# Initialize the database table
init_db()