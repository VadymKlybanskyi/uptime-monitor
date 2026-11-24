import os

import psycopg
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Uptime Monitor API")

DATABASE_URL = os.getenv("DATABASE_URL")


@app.get("/")
def root():
    return {
        "service": "uptime-monitor",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health():
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()

        return {"database": "connected"}

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )
