# Connect to PostgreSQL in your container

```bash
sudo docker exec -it todos_db psql -U todos_user -d todos
```

e.g.
```bash
sudo docker exec -it todos_db psql -U todos_user -d todos
```

Once inside, useful commands:

```sql
-- list all tables
\dt

-- see users table
SELECT * FROM users;

-- see todos table
SELECT * FROM todos;

-- exit
\q
```