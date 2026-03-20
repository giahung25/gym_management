import sqlite3
from contextlib import contextmanager
from app.core.config import DB_PATH


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    # Dùng connection trực tiếp thay vì get_db() context manager,
    # vì executescript() tự commit ngầm — không tương thích với context manager.
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                gender TEXT,
                date_of_birth TEXT,
                address TEXT,
                emergency_contact TEXT,
                photo TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS membership_plans (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                duration_days INTEGER NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id TEXT PRIMARY KEY,
                member_id TEXT NOT NULL,
                plan_id TEXT NOT NULL,
                price_paid REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (member_id) REFERENCES members(id),
                FOREIGN KEY (plan_id) REFERENCES membership_plans(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'working',
                purchase_date TEXT,
                location TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)
        # Indexes để tăng tốc query phổ biến
        conn.execute("CREATE INDEX IF NOT EXISTS idx_members_phone ON members(phone)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_members_is_active ON members(is_active)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subs_member_id ON subscriptions(member_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subs_plan_id ON subscriptions(plan_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subs_status ON subscriptions(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_equipment_status ON equipment(status)")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
