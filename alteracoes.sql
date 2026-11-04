-- UPDATE: mover a issue 2 para "doing" e dar um responsável
UPDATE issues SET status = 'doing', assignee_id = 3 WHERE id = 2;
SELECT id, title, status, assignee_id FROM issues WHERE id = 2;
-- ON DELETE SET NULL: apagar a Carla deixa a issue 2 sem responsável
DELETE FROM users WHERE id = 3;
SELECT id, title, assignee_id FROM issues WHERE id = 2;
-- ON DELETE CASCADE: apagar o projeto API apaga as issues dele
SELECT COUNT(*) AS antes FROM issues;
DELETE FROM projects WHERE id = 2;
SELECT COUNT(*) AS depois FROM issues;