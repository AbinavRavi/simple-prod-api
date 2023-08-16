from pydantic import BaseModel
from typing import List


class SentenceInput(BaseModel):
    sentence: str


class OutputModel(BaseModel):
    output: List[float]
