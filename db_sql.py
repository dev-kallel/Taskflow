"""Camada de acesso ao banco RELACIONAL (SQLite)."""
import email
from os import name
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

    STATUSES = ["todo", "doing", "review", "done"]
    TYPES = ["bug", "task", "feature"]
    # ------------------------------------------------------------------ USERS
def list_users():
    return get_db().execute("SELECT * FROM users ORDER BY name").fetchall()
def create_user(name, email):
    db = get_db()
    cur = db.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    db.commit()
    return cur.lastrowid
    # ------------------------------------------------------------------ PROJECTS
def list_projects():
    # LEFT JOIN + GROUP BY: cada projeto com o total de issues e quantas estão "done"
    sql = """
    SELECT p.*,
    COUNT(i.id) AS total,
    SUM(CASE WHEN i.status = 'done' THEN 1 ELSE 0 END) AS done
    FROM projects p
    LEFT JOIN issues i ON i.project_id = p.id
    GROUP BY p.id
    ORDER BY p.name
    """
    return get_db().execute(sql).fetchall()
    # ------------------------------------------------------------------ PROJECTS
def get_project(project_id):
    return get_db().execute(
    "SELECT * FROM projects WHERE id = ?", (project_id,)
    ).fetchone()
    # ------------------------------------------------------------------ PROJECTS
def create_project(key, name, description):
    db = get_db()
    cur = db.execute(
    "INSERT INTO projects (key, name, description) VALUES (?, ?, ?)",
    (key.upper(), name, description),
    )
    db.commit()
    return cur.lastrowid
    # ------------------------------------------------------------------ PROJECTS
def update_project(project_id, name, description):
    db = get_db()
    db.execute(
    "UPDATE projects SET name = ?, description = ? WHERE id = ?",
    (name, description, project_id),
    )
    db.commit()
def delete_project(project_id):
    """O ON DELETE CASCADE apaga as issues do projeto junto."""
    db = get_db()
    issue_ids = [r["id"] for r in db.execute(
    "SELECT id FROM issues WHERE project_id = ?", (project_id,))]
    db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    db.commit()
    return issue_ids # na aula 6 usaremos esta lista para limpar o MongoDB