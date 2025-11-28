## Instruções para Rodar via Docker

1. Instale o Docker.
2. Puxe a imagem: `docker pull arthurprioli/t2-backend:latest`
3. Rode: `docker run -p 8000:8000 arthurprioli/t2-backend:latest`
4. Acesse http://localhost:8000 (para Swagger, acesse /api-docs ou o endpoint configurado).
5. Para CRUD: use ferramentas como Postman ou o frontend.
6. Nota: Use credenciais de teste (ex: user: admin, pass: 123). Dados SQLite não persistem após stop.
