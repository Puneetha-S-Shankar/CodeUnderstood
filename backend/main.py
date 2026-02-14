from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
from google import genai


load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.INFO)

# Configure Gemini client
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options={"api_version": "v1beta"}
)


class CodeRequest(BaseModel):
    code: str


@app.get("/")
def read_root():
    return {"message": "Concept Extractor Backend (Gemini) is running 🚀"}


@app.post("/analyze")
def analyze_code(request: CodeRequest):

    prompt = f"""
You are a computer science concept extraction engine.

You MUST return valid JSON only.
Do NOT include markdown.
Do NOT include explanation outside JSON.
Do NOT wrap in backticks.

If any field is not applicable, return "N/A" or [].

Return JSON with EXACT structure:

{{
  "language": "",
  "domain": "",
  "primary_concepts": [],
  "secondary_concepts": [],
  "design_patterns": [],
  "architectural_layer": "",
  "time_complexity": "",
  "space_complexity": "",
  "execution_flow": "",
  "why_abstraction_exists": "",
  "prerequisite_concepts": []
}}


Code:
{request.code}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text

        logging.info("=== GEMINI RAW TEXT ===")
        logging.info(text)
        logging.info("=======================")

        return {
            "raw": text
        }

    except Exception as e:
        logging.error("GEMINI ERROR:")
        logging.error(str(e))

        return {
            "error": str(e)
        }
    