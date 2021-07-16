import os
from datetime import datetime

import uvicorn as uvicorn
from dotenv import find_dotenv
from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger

from .submodules.knn_manager import KnnManager

load_dotenv(find_dotenv())
prefix = os.getenv("CLUSTER_ROUTE_PREFIX", "").rstrip("/")

model_local_path = "./garrascobike_be/ml_model/20210625162104"
knn_mng = KnnManager()
logger.info("Loading ML model...")
knn_mng.load_model(model_local_path)
logger.info("ML model loaded!")

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
    suggestions = knn_mng.get_prediction(bike_name)
    results = []
    for score, bike in suggestions:
        results.append({"score": score, "bike": bike})
    return results


if __name__ == "__main__":
    # noinspection PyTypeChecker
    uvicorn.run(app, host="0.0.0.0", port=8888)
