In the case of updating SQLAlchemy models, need to update tables in database via Alembic CLI tool

  ---
  Analogy

  | Component  | Analogy                                                                  |
  |------------|--------------------------------------------------------------------------|
  | PostgreSQL | A physical library building that stores books                            |
  | SQLAlchemy | A librarian who speaks your language and fetches books for you           |
  | Alembic    | A construction crew that renovates the library when you need new shelves |

  ---


What it does:
1. Creates a python script that modifies the database
2. Creates migration files that tracks updates to the database
3. Allows for rollbacks

Steps for migration

Step 1: PostgreSQL is running
```bash
sudo service postgresql start # to run postgres
sudo service postgresql status # to check if postgres is running

psql -U habit_user -d habit_tracker # Connect to DB
```

```psql
/dt # List tables
/d habit_cycles # Describe table
```

Step 2: Modify SQLAlchemy model
Make modifications to model
Make sure that the model is exported in /models/__init__.py and /alembic/env.py

Step 3: Alembic detects the change - Create migration
```bash
alembic revision --autogenerate -m "add description field <or any other message that describes the change>"

# Alembic compares SQLAlchemy models to current PostgeSQL schema
# Generates a migration file
```

Step 4: Alembic applies the migration
```bash
alembic upgrade head

# Alembic sends SQL to PostgreSQL
```


Rollbacks
```bash
alembic downgrade -1
```

Check current version
```bash
alembic current
```