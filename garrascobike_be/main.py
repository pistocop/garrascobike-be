import os
from datetime import datetime

import uvicorn as uvicorn
from dotenv import find_dotenv
from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger

from garrascobike_be.submodules.knn_manager import KnnManager
from garrascobike_be.utils.backblaze import download_garrascobike_model

# Load resources
load_dotenv(find_dotenv())
local_models_folder = "./garrascobike_be/ml_model/"
models_host_info = "./garrascobike_be/ml_model/hosted-model-info.json"
local_model_path = download_garrascobike_model(local_path=local_models_folder,
                                               model_info_path=models_host_info,
                                               app_key_id=os.getenv("BB_APP_KEY_ID"),
                                               app_key=os.getenv("BB_APP_KEY"))
app = FastAPI(
    title="garrascobike-be",
    version="1.0",
    description="Back-end services for garrascobike App",
)
knn_mng = KnnManager()
knn_mng.load_model(local_model_path)


# Define endpoints
@app.get("/health")
def health_check():
    return f"{datetime.utcnow()}"


@app.get("/recommender/{bike_name}")
def recommender(bike_name: str):
    try:
        suggestions = knn_mng.get_prediction(bike_name)
        results = []
        for score, bike in suggestions:
            results.append({"score": score, "bike": bike})
        return results
    except Exception:
        msg = f"Bike {bike_name} not found"
        logger.info(msg)
        return msg


if __name__ == "__main__":
    # noinspection PyTypeChecker
    uvicorn.run(app, host="0.0.0.0", port=8888)
