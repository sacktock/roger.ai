from __future__ import annotations
import os
from dotenv import load_dotenv
from openai import OpenAI

from .prompts import INSTRUCTIONS

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

def get_ai(
    model: str | None = OPENAI_MODEL,
    api_key: str | None = OPENAI_API_KEY
) -> ResponseModel:
    if not api_key or not model:
        raise ValueError("Both API key and model need to be set in .env")
    return ResponseModel(api_key, model)

class ResponseModel:

    def __init__(self, api_key: str, model: str):
        self.model = model
        self._client = OpenAI(api_key=api_key)

    def response(self, input_text: str) -> str:
        return self._client.responses.create(
            model=self.model,
            #response_format={"type", "json_object"},
            input=input_text,
            instructions=INSTRUCTIONS,
        )


    

