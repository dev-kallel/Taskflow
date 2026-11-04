-- USUÁRIOS
INSERT INTO users (name, email) VALUES ('Ana Souza', 'ana@exemplo.com');
INSERT INTO users (name, email) VALUES ('Bruno Lima', 'bruno@exemplo.com');
INSERT INTO users (name, email) VALUES ('Carla Dias', 'carla@exemplo.com');
-- PROJETOS
INSERT INTO projects (key, name, description) VALUES ('APP', 'App Mobile da Cantina', 'Pedir lanche sem
fila');
INSERT INTO projects (key, name, description) VALUES ('API', 'API de Pagamentos', 'Processa PIX e cartão');
-- ISSUES
INSERT INTO issues (project_id, title, type, status, priority, story_points, assignee_id)
VALUES (1, 'Tela de login trava no Android', 'bug', 'doing', 1, 3, 1);
INSERT INTO issues (project_id, title, type, priority, story_points)
VALUES (1, 'Carrinho de compras', 'feature', 2, 8);
INSERT INTO issues (project_id, title, type, status, priority, story_points, assignee_id)
VALUES (2, 'Webhook do PIX duplica pagamentos', 'bug', 'review', 1, 5, 2);
-- CONFERINDO
SELECT id, name, email FROM users;
SELECT id, key, name FROM projects;
SELECT id, project_id, title, status, priority, assignee_id FROM issues;