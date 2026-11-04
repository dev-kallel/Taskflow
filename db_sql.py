"""Camada de acesso ao banco RELACIONAL (SQLite)."""
import sqlite3
from pathlib import Path
from flask import current_app, g
SCHEMA_FILE = Path(__file__).with_name("schema.sql")

def get_db():
    """Uma conexão por requisição, guardada em g."""
    if "sql" not in g:
        g.sql = sqlite3.connect(current_app.config["SQL_DATABASE"])
        g.sql.row_factory = sqlite3.Row # permite row["title"]
        g.sql.execute("PRAGMA foreign_keys = ON")
    return g.sql

def close_db(_exc=None):
    conn = g.pop("sql", None)
    if conn is not None:
        conn.close()

def init_db():
    """Cria (ou recria) as tabelas a partir de schema.sql."""
    db = get_db()
    db.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
    db.commit()