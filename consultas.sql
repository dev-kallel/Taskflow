-- JOIN: issue + nome do projeto
SELECT i.id, p.key, i.title FROM issues i JOIN projects p ON p.id = i.project_id;
-- JOIN com users: só aparecem issues COM responsável
SELECT i.id, i.title, u.name FROM issues i JOIN users u ON u.id = i.assignee_id;
-- LEFT JOIN: todas as issues, com ou sem responsável
SELECT i.id, i.title, u.name AS responsavel FROM issues i LEFT JOIN users u ON u.id = i.assignee_id;
-- GROUP BY: quantas issues e quantos pontos por status
SELECT status, COUNT(*) AS qtd, SUM(story_points) AS pontos FROM issues GROUP BY status;
-- LIKE: busca por texto
SELECT id, title FROM issues WHERE title LIKE '%pix%';
-- ORDER BY: prioridade mais alta primeiro
SELECT id, title, priority FROM issues ORDER BY priority ASC, id DESC;