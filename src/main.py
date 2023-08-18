from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from src.model import SentenceInput, OutputModel
from typing import List, Dict
import random
import hashlib

app = FastAPI()

# can add other frontend urls as well here now allowing all ports from frontend
origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health_check", status_code=status.HTTP_200_OK)
def health_check() -> Dict:
    return {"status": "ok"}


@app.post("/get_array", status_code=status.HTTP_200_OK, response_model=OutputModel)
def get_array(inp: SentenceInput) -> List[float]:
    sentence = inp.sentence
    seed = int(hashlib.sha256(sentence.encode()).hexdigest(), 16)
    random.seed(seed)
    array_length = 500
    random_floats = [random.uniform(1.0, 1000.0) for _ in range(array_length)]
    response = {"output": random_floats}
    return response
