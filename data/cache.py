import sqlite3
import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Any

class QueryCache:
    """SQLite-based query result cache with TTL."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'query_cache.db')
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_cache (
                    id TEXT PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ttl_seconds INTEGER DEFAULT 900
                )
            """)

    def _generate_id(self, query_text: str, filters: dict) -> str:
        """Generates a SHA256 hash for a query and its filters."""
        data = f"{query_text}:{json.dumps(filters, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()

    def get(self, query_text: str, filters: dict) -> Optional[Any]:
        """Retrieves a cached result if valid and not expired."""
        cache_id = self._generate_id(query_text, filters)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT result_json, created_at, ttl_seconds 
                FROM query_cache 
                WHERE id = ?
            """, (cache_id,))
            row = cursor.fetchone()
            
            if row:
                result_json, created_at, ttl_seconds = row
                created_dt = datetime.fromisoformat(created_at)
                if datetime.now() < created_dt + timedelta(seconds=ttl_seconds):
                    return json.loads(result_json)
                else:
                    self.delete(cache_id)
        return None

    def set(self, query_text: str, filters: dict, result: Any, ttl_seconds: int = 900):
        """Stores a result in the cache."""
        cache_id = self._generate_id(query_text, filters)
        result_json = json.dumps(result)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO query_cache (id, query_text, result_json, created_at, ttl_seconds)
                VALUES (?, ?, ?, ?, ?)
            """, (cache_id, query_text, result_json, datetime.now().isoformat(), ttl_seconds))

    def delete(self, cache_id: str):
        """Deletes an entry from the cache."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM query_cache WHERE id = ?", (cache_id,))

    def clear(self):
        """Clears the entire cache."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM query_cache")
