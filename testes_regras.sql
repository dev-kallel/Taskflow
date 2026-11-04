-- 1) CHECK: status que não existe
INSERT INTO issues (project_id, title, status) VALUES (1, 'Teste', 'pronto');
-- 2) CHECK: prioridade fora de 1..5
INSERT INTO issues (project_id, title, priority) VALUES (1, 'Teste', 9);
-- 3) NOT NULL: issue sem título
INSERT INTO issues (project_id) VALUES (1);
-- 4) UNIQUE: e-mail repetido
INSERT INTO users (name, email) VALUES ('Outra Ana', 'ana@exemplo.com');
-- 5) FOREIGN KEY: projeto 99 não existe
INSERT INTO issues (project_id, title) VALUES (99, 'Issue órfã');
-- 6) Valores padrão (DEFAULT): só título e projeto
INSERT INTO issues (project_id, title) VALUES (2, 'Documentar endpoints');
SELECT id, title, type, status, priority, created_at FROM issues WHERE id = last_insert_rowid();