"""
etl_pipeline_mssql.py
---------------------
ETL pipeline for the Website Analytics & Conversion Optimization project,
loading into Microsoft SQL Server (MSSQL) and querying it with T-SQL.

    EXTRACT   -> read raw sessions from data/website_sessions.csv
    TRANSFORM -> validate, clean, type-cast and enrich the data with Pandas
    LOAD      -> write the clean data into SQL Server table: dbo.website_sessions
    ANALYSE   -> run the T-SQL files in /sql_mssql and save the results as CSV

Setup:
    pip install pandas sqlalchemy pyodbc
    Install "ODBC Driver 18 for SQL Server" and SQL Server (Express/Developer).
    Create the database once:  CREATE DATABASE WebsiteAnalytics;

Run from the project root:
    python python/etl_pipeline_mssql.py
"""

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import BigInteger, Boolean, Date, Float, String

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_CSV = BASE_DIR / "data" / "website_sessions.csv"
SQL_DIR = BASE_DIR / "sql_mssql"
OUTPUT_DIR = BASE_DIR / "data" / "sql_results_mssql"

# ---- CONNECTION: change SERVER to your SQL Server instance name -----------
# Express edition  : localhost\SQLEXPRESS
# Developer edition: localhost
SERVER = r"localhost\SQLEXPRESS"
DATABASE = "WebsiteAnalytics"
DRIVER = "ODBC Driver 18 for SQL Server"

DEFAULT_URL = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    f"?driver={DRIVER.replace(' ', '+')}"
    "&trusted_connection=yes&TrustServerCertificate=yes"
)
# Optional override (for example a SQL login): set the DB_URL environment variable
DB_URL = os.environ.get("DB_URL", DEFAULT_URL)

TABLE_NAME = "website_sessions"
REQUIRED_COLUMNS = [
    "session_id", "date", "month", "month_num", "year", "year_month",
    "day_of_week", "traffic_source", "landing_page", "device", "location",
    "pages_viewed", "session_duration_s", "bounced", "converted", "new_user",
]
BOOL_COLUMNS = ["bounced", "converted", "new_user"]

# Column types for SQL Server (BIT for flags, proper VARCHAR sizes, DATE)
SQL_TYPES = {
    "session_id": String(20),
    "date": Date(),
    "month": String(15),
    "month_num": BigInteger(),
    "year": BigInteger(),
    "year_month": String(7),
    "day_of_week": String(15),
    "traffic_source": String(40),
    "landing_page": String(60),
    "device": String(20),
    "location": String(60),
    "pages_viewed": BigInteger(),
    "session_duration_s": Float(),
    "bounced": Boolean(),
    "converted": Boolean(),
    "new_user": Boolean(),
    "session_duration_min": Float(),
}


# --------------------------------------------------------------------------
# EXTRACT
# --------------------------------------------------------------------------
def extract(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw data file not found: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"[EXTRACT]   {len(df):,} rows, {df.shape[1]} columns read from {csv_path.name}")
    return df


# --------------------------------------------------------------------------
# TRANSFORM
# --------------------------------------------------------------------------
def to_bool(series: pd.Series) -> pd.Series:
    mapping = {"true": True, "false": False, "1": True, "0": False,
               "yes": True, "no": False}
    return series.astype(str).str.strip().str.lower().map(mapping)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    rows_in = len(df)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df = df[REQUIRED_COLUMNS].copy()

    dupes = df.duplicated(subset="session_id").sum()
    df = df.drop_duplicates(subset="session_id", keep="first")

    text_cols = ["session_id", "month", "day_of_week", "traffic_source",
                 "landing_page", "device", "location", "year_month"]
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["month_num", "year", "pages_viewed", "session_duration_s"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in BOOL_COLUMNS:
        df[col] = to_bool(df[col])

    critical = ["session_id", "date", "traffic_source", "device", "year_month",
                "bounced", "converted"]
    null_rows = df[critical].isna().any(axis=1).sum()
    df = df.dropna(subset=critical)

    invalid_mask = (df["session_duration_s"] < 0) | (df["pages_viewed"] < 1)
    invalid_rows = invalid_mask.sum()
    df = df[~invalid_mask]

    df["session_duration_min"] = (df["session_duration_s"] / 60).round(2)

    for col in ["month_num", "year", "pages_viewed"]:
        df[col] = df[col].astype("int64")
    for col in BOOL_COLUMNS:
        df[col] = df[col].astype(bool)
    df["date"] = df["date"].dt.date

    print(f"[TRANSFORM] duplicates removed : {dupes}")
    print(f"[TRANSFORM] rows with nulls    : {null_rows}")
    print(f"[TRANSFORM] invalid rows       : {invalid_rows}")
    print(f"[TRANSFORM] {rows_in:,} rows in -> {len(df):,} clean rows out")
    return df.reset_index(drop=True)


# --------------------------------------------------------------------------
# LOAD
# --------------------------------------------------------------------------
def load(df: pd.DataFrame, engine) -> None:
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False,
              dtype=SQL_TYPES, chunksize=2000, schema="dbo")

    with engine.begin() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM dbo.{TABLE_NAME}")).scalar()
    print(f"[LOAD]      {count:,} rows loaded into table '{TABLE_NAME}' ({DATABASE})")

    if count != len(df):
        raise RuntimeError("Row count mismatch between DataFrame and database table")


# --------------------------------------------------------------------------
# ANALYSE (run the T-SQL files on the loaded table)
# --------------------------------------------------------------------------
def run_sql_files(engine, sql_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sql_files = sorted(sql_dir.glob("*.sql"))
    if not sql_files:
        print("[ANALYSE]   No .sql files found, skipping.")
        return

    for sql_file in sql_files:
        query = sql_file.read_text(encoding="utf-8")
        with engine.connect() as conn:
            result = pd.read_sql_query(text(query), conn)
        out_file = output_dir / f"{sql_file.stem}_result.csv"
        result.to_csv(out_file, index=False)
        print(f"\n[ANALYSE]   {sql_file.name} -> {out_file.name}")
        print(result.head(6).to_string(index=False))


def main() -> None:
    kwargs = {"fast_executemany": True} if DB_URL.startswith("mssql") else {}
    engine = create_engine(DB_URL, **kwargs)

    raw = extract(RAW_CSV)
    clean = transform(raw)
    load(clean, engine)
    run_sql_files(engine, SQL_DIR, OUTPUT_DIR)
    print("\nETL pipeline (MSSQL) completed successfully.")


if __name__ == "__main__":
    main()
