# SQLite in Python — Complete Tutorial

---

## What is SQLite?

SQLite is a **file-based relational database**. Unlike MySQL or PostgreSQL, it has no separate server process — the entire database lives in a single `.db` file on disk. Python ships with `sqlite3` in its standard library, so you need **zero installations**.

### When to use SQLite vs PostgreSQL/MySQL

| Situation | SQLite | PostgreSQL/MySQL |
|---|---|---|
| Local dev / prototyping | ✅ Perfect | Overkill |
| Embedded in desktop/mobile apps | ✅ Perfect | ❌ Needs server |
| Single-user apps | ✅ Fine | Overkill |
| Multi-user web apps | ❌ Not ideal | ✅ Use this |
| Learning SQL concepts | ✅ Best place to start | Fine too |
| Production backend with concurrent writes | ❌ Avoid | ✅ Use this |

SQLite is excellent for **LangGraph checkpointing** (SqliteSaver), local job queues, CLI tools, testing, and any time you want SQL without spinning up a server.

---

## 1. Connecting to a Database

```python
import sqlite3

# Creates the file if it doesn't exist, opens it if it does
conn = sqlite3.connect("mydb.db")

# In-memory database — lives only in RAM, gone when connection closes
# Great for tests and temporary processing
conn = sqlite3.connect(":memory:")

# Always close your connection when done
conn.close()
```

### The Cursor

Every SQL operation goes through a **cursor** — think of it as the "execution pen" you hand to the database.

```python
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# cursor executes SQL
# conn manages transactions (commit / rollback)
```

---

## 2. Creating Tables

```python
import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT    NOT NULL,
        email   TEXT    UNIQUE NOT NULL,
        age     INTEGER,
        created_at TEXT DEFAULT (datetime('now'))
    )
""")

conn.commit()  # Save the change to disk
conn.close()
```

**Key concepts:**
- `INTEGER PRIMARY KEY AUTOINCREMENT` — auto-incrementing ID
- `IF NOT EXISTS` — safe to run multiple times without error
- `conn.commit()` — SQLite uses **transactions**; nothing is saved until you commit

---

## 3. Inserting Data

### Single insert

```python
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# ALWAYS use parameterized queries — never f-strings with user input
# The ? placeholders are SQLite's way; prevents SQL injection
cursor.execute(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    ("Samyak", "samyak@example.com", 20)
)

conn.commit()
print("Inserted row ID:", cursor.lastrowid)  # ID of the row just inserted
conn.close()
```

### Bulk insert

```python
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

users = [
    ("Alice", "alice@example.com", 25),
    ("Bob",   "bob@example.com",   30),
    ("Carol", "carol@example.com", 22),
]

# executemany — one round trip for all rows
cursor.executemany(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    users
)

conn.commit()
conn.close()
```

---

## 4. Querying Data

```python
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# Fetch all rows
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()  # list of tuples
for row in rows:
    print(row)
# Output: (1, 'Samyak', 'samyak@example.com', 20, '2025-05-03 ...')

# Fetch one row
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
row = cursor.fetchone()  # single tuple or None
print(row)

# Fetch N rows
cursor.execute("SELECT * FROM users")
rows = cursor.fetchmany(2)  # first 2 rows

# Iterate directly (memory efficient for large results)
cursor.execute("SELECT name, email FROM users")
for name, email in cursor:
    print(f"{name} → {email}")

conn.close()
```

### Why tuples by default?

SQLite returns rows as tuples. To access `row[0]`, `row[1]` is awkward. Fix this with `row_factory`.

---

## 5. Row Factory — Access Columns by Name

```python
conn = sqlite3.connect("mydb.db")

# This single line makes rows behave like dictionaries
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
row = cursor.fetchone()

# Now access by column name
print(row["name"])   # "Samyak"
print(row["email"])  # "samyak@example.com"

# Convert to a real dict if needed
print(dict(row))
# {'id': 1, 'name': 'Samyak', 'email': 'samyak@example.com', 'age': 20, ...}

conn.close()
```

This is the pattern you'll use in real projects — always set `row_factory`.

---

## 6. Updating Data

```python
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

cursor.execute(
    "UPDATE users SET age = ? WHERE email = ?",
    (21, "samyak@example.com")
)

print("Rows affected:", cursor.rowcount)  # how many rows changed
conn.commit()
conn.close()
```

---

## 7. Deleting Data

```python
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM users WHERE id = ?", (3,))
print("Rows deleted:", cursor.rowcount)

conn.commit()
conn.close()
```

---

## 8. Transactions — The Most Important Concept

SQLite wraps everything in transactions. This matters for **data integrity**.

```python
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

try:
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Dave", "dave@x.com"))
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Eve", "dave@x.com"))  # duplicate email → FAIL
    conn.commit()  # only reaches here if both succeed
except sqlite3.IntegrityError as e:
    conn.rollback()  # undo everything — Dave is NOT inserted either
    print("Transaction failed, rolled back:", e)
finally:
    conn.close()
```

**Rule:** Either all operations succeed together, or none of them do. This is the "A" in ACID.

---

## 9. Context Manager — The Clean Pattern

Python's `with` block handles `commit` and `close` automatically.

```python
import sqlite3

# Preferred pattern in production code
with sqlite3.connect("mydb.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(dict(row))

# conn.commit() called automatically on exit
# conn.close() NOT called — you need to call it manually or use conn as context manager properly
```

**Important nuance:** `with conn:` handles the **transaction** (commit/rollback on exception) but does NOT close the connection. Call `conn.close()` explicitly or nest with a `try/finally`.

---

## 10. Building a Reusable Database Class

This is how you'd structure SQLite in a real project:

```python
import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self._init_tables()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  # enforce FK constraints
        return conn

    @contextmanager
    def _cursor(self):
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_tables(self):
        with self._cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    name  TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)

    def create_user(self, name: str, email: str) -> int:
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            return cur.lastrowid

    def get_user(self, user_id: int) -> dict | None:
        with self._cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def list_users(self) -> list[dict]:
        with self._cursor() as cur:
            cur.execute("SELECT * FROM users")
            return [dict(r) for r in cur.fetchall()]

    def delete_user(self, user_id: int) -> bool:
        with self._cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cur.rowcount > 0


# Usage
db = Database("myapp.db")
uid = db.create_user("Samyak", "samyak@example.com")
print(db.get_user(uid))      # {'id': 1, 'name': 'Samyak', 'email': '...'}
print(db.list_users())
print(db.delete_user(uid))   # True
```

---

## 11. Common SQLite-Specific Things

### PRAGMA statements (SQLite config)

```python
cursor.execute("PRAGMA foreign_keys = ON")   # enable FK enforcement (OFF by default!)
cursor.execute("PRAGMA journal_mode = WAL")  # better concurrent read performance
cursor.execute("PRAGMA cache_size = -64000") # 64MB cache
```

### Named placeholders (alternative to ?)

```python
cursor.execute(
    "INSERT INTO users (name, email) VALUES (:name, :email)",
    {"name": "Samyak", "email": "s@x.com"}
)
```

### Check if table exists

```python
cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name='users'
""")
print(cursor.fetchone())  # None if doesn't exist
```

### Get all tables in the database

```python
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())
```

---

## 12. SQLite in Testing (In-Memory)

This is one of SQLite's superpowers — use `:memory:` for fast, isolated tests.

```python
import sqlite3
import pytest

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    yield conn
    conn.close()

def test_insert_user(db):
    db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    db.commit()
    row = db.execute("SELECT * FROM users WHERE name = 'Alice'").fetchone()
    assert row["name"] == "Alice"
```

Each test gets a fresh in-memory database — no cleanup needed, blazing fast.

---

## 13. SQLite with LangGraph (SqliteSaver)

Since you're using LangGraph — here's how SQLite fits in:

```python
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# LangGraph uses SQLite to persist agent state across turns
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)

graph = graph_builder.compile(checkpointer=memory)

# Same thread_id = same conversation, state is loaded from SQLite
config = {"configurable": {"thread_id": "user-123"}}
result = graph.invoke({"messages": [...]}, config=config)
```

This is exactly how SqliteSaver stores your TypedDict state between calls.

---

## 14. Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `OperationalError: no such table` | Table not created yet | Run `CREATE TABLE IF NOT EXISTS` first |
| `IntegrityError: UNIQUE constraint failed` | Duplicate value in UNIQUE column | Handle with try/except or use `INSERT OR IGNORE` |
| `ProgrammingError: Incorrect number of bindings` | Wrong number of `?` vs values | Count your `?` placeholders |
| `OperationalError: database is locked` | Multiple connections writing simultaneously | Use WAL mode or switch to PostgreSQL for concurrency |
| Data not saved after insert | Forgot `conn.commit()` | Always commit after writes |

```python
# INSERT OR IGNORE — skip duplicates silently
cursor.execute(
    "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
    ("Alice", "alice@x.com")
)

# INSERT OR REPLACE — upsert (delete + reinsert)
cursor.execute(
    "INSERT OR REPLACE INTO users (name, email) VALUES (?, ?)",
    ("Alice", "alice@x.com")
)
```

---

## Quick Reference

```python
import sqlite3

conn = sqlite3.connect("db.db")
conn.row_factory = sqlite3.Row          # rows as dict-like objects

cursor = conn.cursor()

# Create
cursor.execute("CREATE TABLE IF NOT EXISTS t (id INTEGER PRIMARY KEY, val TEXT)")

# Insert
cursor.execute("INSERT INTO t (val) VALUES (?)", ("hello",))
conn.commit()

# Read
cursor.execute("SELECT * FROM t WHERE id = ?", (1,))
row = cursor.fetchone()
print(dict(row))

# Update
cursor.execute("UPDATE t SET val = ? WHERE id = ?", ("world", 1))
conn.commit()

# Delete
cursor.execute("DELETE FROM t WHERE id = ?", (1,))
conn.commit()

conn.close()
```

---

## What's Next After SQLite?

Since your goal is backend mastery:

1. **SQLAlchemy Core** — SQL toolkit that works with SQLite, PostgreSQL, MySQL using the same Python API
2. **SQLAlchemy ORM** — map Python classes to tables (like Mongoose but for SQL)
3. **Alembic** — database migrations (schema versioning, like Git for your DB schema)
4. **asyncio + aiosqlite** — async SQLite for FastAPI (drop-in async replacement)
5. **PostgreSQL via asyncpg** — when you graduate to production-grade SQL

SQLite is the perfect place to lock in SQL fundamentals before integrating PostgreSQL into your FastAPI projects.
