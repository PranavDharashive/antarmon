from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

class Metrics(BaseModel):
    metrics: Dict[str, Any]

@app.get("/")
def read_root():
    return {"message": "AntarMon Server is running"}

@app.post("/metrics")
def receive_metrics(metrics: Metrics):
    print("Received metrics:", metrics.dict())
    return {"status": "success", "data_received": metrics.dict()}
