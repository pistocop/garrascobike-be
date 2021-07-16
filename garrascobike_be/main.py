import os
from datetime import datetime

import uvicorn as uvicorn
from dotenv import find_dotenv
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException

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


supported_bikes = ["canyon", "stoic"]


@app.get("/recommender/{bike_name}")
def recommender(bike_name: str):
    if bike_name not in supported_bikes:
        raise HTTPException(status_code=404, detail=f"Bike `{bike_name}` not found")
    return "canyon spectral"


if __name__ == "__main__":
    # noinspection PyTypeChecker
    uvicorn.run(app, host="0.0.0.0", port=8888)
