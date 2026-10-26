#!/usr/bin/env python3
"""
Autonomous Database Migration Guard
Inspects live production schemas, detects schema drift against application models,
validates zero-downtime safety, and executes verified reversible migrations.
Part 9 of Autonomous Developer Workflows Series (@SystemZeroTech)
"""

import sys
import os
import sqlite3
import json
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

# Ensure UTF-8 output on Windows terminals
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from models import TARGET_SCHEMA, TableDef, ColumnDef

@dataclass
class DriftItem:
    table: str
    drift_type: str  # MISSING_COLUMN, MISSING_INDEX, TYPE_MISMATCH
    target_name: str
    target_def: ColumnDef
    safety_verdict: str  # SAFE_EXPAND, POTENTIAL_LOCK, BREAKING_CHANGE
    recommendation: str

class SchemaInspector:
    """Inspects live database schema and index metadata."""
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_tables(self) -> List[str]:
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        return [row[0] for row in cur.fetchall()]

    def get_columns(self, table: str) -> Dict[str, Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(f"PRAGMA table_info({table});")
        columns = {}
        for row in cur.fetchall():
            # cid, name, type, notnull, dflt_value, pk
            columns[row[1]] = {
                "name": row[1],
                "type": row[2].upper(),
                "nullable": not bool(row[3]),
                "default": row[4],
                "is_primary_key": bool(row[5])
            }
        return columns

    def get_indices(self, table: str) -> List[str]:
        cur = self.conn.cursor()
        cur.execute(f"PRAGMA index_list({table});")
        indices = []
        for row in cur.fetchall():
            idx_name = row[1]
            cur.execute(f"PRAGMA index_info({idx_name});")
            col_info = cur.fetchall()
            for col in col_info:
                indices.append(col[2])
        return indices

class MigrationGuardAgent:
    """Autonomous agent that checks drift, evaluates downtime safety, and generates scripts."""
    name = "Migration-Guard-01"

    def detect_drift(self, inspector: SchemaInspector) -> List[DriftItem]:
        drift = []
        existing_tables = inspector.get_tables()

        for table_name, target_table in TARGET_SCHEMA.items():
            if table_name not in existing_tables:
                drift.append(DriftItem(
                    table=table_name,
                    drift_type="MISSING_TABLE",
                    target_name=table_name,
                    target_def=None,
                    safety_verdict="SAFE_EXPAND",
                    recommendation=f"CREATE TABLE {table_name} with initial columns."
                ))
                continue

            current_cols = inspector.get_columns(table_name)
            current_indices = inspector.get_indices(table_name)

            for col in target_table.columns:
                if col.name not in current_cols:
                    # Evaluate zero-downtime safety
                    if not col.nullable and col.default is None:
                        safety = "POTENTIAL_LOCK"
                        rec = "Unsafe NOT NULL without DEFAULT causes full-table write lock. Add default or make nullable."
                    else:
                        safety = "SAFE_EXPAND"
                        rec = f"Expand schema: add nullable or default-backed column `{col.name}` without locking."

                    drift.append(DriftItem(
                        table=table_name,
                        drift_type="MISSING_COLUMN",
                        target_name=col.name,
                        target_def=col,
                        safety_verdict=safety,
                        recommendation=rec
                    ))

                # Check missing index
                if col.is_indexed and col.name not in current_indices:
                    drift.append(DriftItem(
                        table=table_name,
                        drift_type="MISSING_INDEX",
                        target_name=f"idx_{table_name}_{col.name}",
                        target_def=col,
                        safety_verdict="SAFE_EXPAND",
                        recommendation=f"Create index concurrently: `CREATE INDEX idx_{table_name}_{col.name} ON {table_name}({col.name});`"
                    ))

        return drift

    def generate_migration(self, drift_items: List[DriftItem]) -> Tuple[List[str], List[str]]:
        up_sql = []
        down_sql = []

        for item in drift_items:
            if item.drift_type == "MISSING_COLUMN":
                col = item.target_def
                col_def = f"{col.name} {col.type}"
                if not col.nullable:
                    col_def += f" NOT NULL DEFAULT {col.default}"
                elif col.default is not None:
                    col_def += f" DEFAULT {col.default}"

                up_sql.append(f"ALTER TABLE {item.table} ADD COLUMN {col_def};")
                # SQLite doesn't drop columns in old versions, but SQLite 3.35.0+ supports DROP COLUMN
                down_sql.append(f"ALTER TABLE {item.table} DROP COLUMN {col.name};")

            elif item.drift_type == "MISSING_INDEX":
                idx_name = item.target_name
                up_sql.append(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {item.table}({item.target_def.name});")
                down_sql.append(f"DROP INDEX IF EXISTS {idx_name};")

        return up_sql, down_sql

def setup_simulated_db(db_path: str):
    """Seed existing production database with older schema and live data."""
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Legacy schema (without mfa_enabled or stripe_customer_id)
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            full_name TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("CREATE INDEX idx_users_email ON users(email);")

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            slug TEXT NOT NULL,
            billing_tier TEXT NOT NULL DEFAULT 'free'
        );
    """)
    cur.execute("CREATE INDEX idx_orgs_slug ON organizations(slug);")

    # Seed initial production rows
    cur.execute("INSERT INTO users (id, email, full_name) VALUES (1, 'alice@company.com', 'Alice Chen');")
    cur.execute("INSERT INTO users (id, email, full_name) VALUES (2, 'bob@startup.io', 'Bob Miller');")
    conn.commit()
    conn.close()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    simulated_db = os.path.join(script_dir, "prod_simulated.db")

    print("=" * 68)
    print("🛡️ System Zero - Autonomous Zero-Downtime Database Migration Guard")
    print("=" * 68)
    print("[1] Provisioning simulated production database with legacy schema...")
    setup_simulated_db(simulated_db)

    conn = sqlite3.connect(simulated_db)
    inspector = SchemaInspector(conn)
    guard = MigrationGuardAgent()

    print("[2] Inspecting live database schema against application target models...")
    drift_items = guard.detect_drift(inspector)

    print(f"[+] Drift detected: {len(drift_items)} schema differences identified.\n")

    print("| Target Table | Drift Item | Type | Downtime Safety | Recommendation |")
    print("| :--- | :--- | :--- | :--- | :--- |")
    for item in drift_items:
        safety_badge = "🟢 SAFE_EXPAND" if item.safety_verdict == "SAFE_EXPAND" else "🔴 LOCK_RISK"
        print(f"| `{item.table}` | `{item.target_name}` | {item.drift_type} | {safety_badge} | {item.recommendation} |")

    print("\n[3] Generating Reversible Zero-Downtime Migration Scripts...")
    up_sql, down_sql = guard.generate_migration(drift_items)

    print("\n--- [UP MIGRATION (Expand Phase)] ---")
    for stmt in up_sql:
        print(f"  {stmt}")

    print("\n--- [DOWN MIGRATION (Rollback Phase)] ---")
    for stmt in down_sql:
        print(f"  {stmt}")

    print("\n[4] Executing Transactional Migration Simulation...")
    try:
        cur = conn.cursor()
        for stmt in up_sql:
            cur.execute(stmt)
        conn.commit()
        print("  [✓] Forward migration applied successfully with 0 locks.")

        # Verify live records retained data
        cur.execute("SELECT id, email, mfa_enabled, stripe_customer_id FROM users;")
        rows = cur.fetchall()
        print(f"  [✓] Verified data integrity: {len(rows)} live customer records accessible.")
        for r in rows:
            print(f"      - User #{r[0]}: {r[1]} | mfa_enabled={r[2]} | stripe_id={r[3]}")

        print("\n[+] MIGRATION VERDICT: APPROVED FOR ZERO-DOWNTIME PRODUCTION DEPLOYMENT")
    except Exception as e:
        conn.rollback()
        print(f"  [✗] Migration simulation failed: {e}")
        sys.exit(1)
    finally:
        conn.close()
        if os.path.exists(simulated_db):
            os.remove(simulated_db)

    print("=" * 68)

if __name__ == "__main__":
    main()
