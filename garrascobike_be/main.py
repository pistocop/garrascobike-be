import os
from datetime import datetime

from dotenv import find_dotenv
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv(find_dotenv())
prefix = os.getenv("CLUSTER_ROUTE_PREFIX", "").rstrip("/")

app = FastAPI(
    title="garrascobike-be",
    version="1.0",
    description="Back-end services for garrascobike App",
    openapi_prefix=prefix,
)


@app.get("/health")
def health_check():
    return f"{datetime.utcnow()}"


@app.get("/hello")
def hello_world():
    return f"world"
