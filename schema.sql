-- TaskFlow - Esquema RELACIONAL (SQL)
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE projects (
id INTEGER PRIMARY KEY AUTOINCREMENT,
key TEXT NOT NULL UNIQUE,
name TEXT NOT NULL,
description TEXT,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE issues (
id INTEGER PRIMARY KEY AUTOINCREMENT,
project_id INTEGER NOT NULL,
title TEXT NOT NULL,
description TEXT,
type TEXT NOT NULL DEFAULT 'task'
CHECK (type IN ('bug', 'task', 'feature')),
status TEXT NOT NULL DEFAULT 'todo'
CHECK (status IN ('todo', 'doing', 'review', 'done')),
priority INTEGER NOT NULL DEFAULT 3
CHECK (priority BETWEEN 1 AND 5),
story_points INTEGER CHECK (story_points IS NULL OR story_points >= 0),
assignee_id INTEGER,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_issues_project ON issues(project_id);
CREATE INDEX idx_issues_status ON issues(status);