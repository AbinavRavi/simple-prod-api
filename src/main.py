from fastapi import FastAPI, status
from typing import List, Dict
import random
import hashlib

app = FastAPI()


@app.get("/health_check", status_code=status.HTTP_200_OK)
def health_check() -> Dict:
    return {"status": "ok"}


@app.post("/", status_code=status.HTTP_201_CREATED)
def get_array(sentence: str) -> List[float]:
    seed = int(hashlib.sha256(sentence.encode()).hexdigest(), 16)
    random.seed(seed)
    array_length = 500
    random_floats = [random.uniform(1.0, 1000.0) for _ in range(array_length)]
    return random_floats
