import os
import json
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import vertexai
from vertexai.generative_models import GenerativeModel

# =============================
# Logging setup
# =============================

logging.basicConfig(level=logging.INFO)

# =============================
# FastAPI app
# =============================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# Request model
# =============================

class CodeRequest(BaseModel):
    code: str

# =============================
# Load Google credentials from Render env
# =============================

try:
    creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

    if not creds_json:
        raise Exception("Missing GOOGLE_APPLICATION_CREDENTIALS_JSON")

    creds_dict = json.loads(creds_json)

    creds_path = "/tmp/gcp-creds.json"

    with open(creds_path, "w") as f:
        json.dump(creds_dict, f)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

    # Initialize Vertex AI
    vertexai.init(
        project=creds_dict["project_id"],
        location="us-central1"
    )

    # Load Gemini model
    model = GenerativeModel("gemini-live-2.5-flash-native-audio")

    logging.info("Vertex AI Gemini initialized successfully")

except Exception as e:
    logging.error("Failed to initialize Vertex AI")
    logging.error(str(e))
    model = None

# =============================
# Health check route
# =============================

@app.get("/")
def root():
    return {"status": "CodeUnderstood backend running"}

# =============================
# Analyze endpoint
# =============================

@app.post("/analyze")
def analyze_code(request: CodeRequest):

    if not model:
        return {
            "error": "Gemini model not initialized"
        }

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

        response = model.generate_content(prompt)

        text = response.text.strip()

        logging.info("Gemini response received")

        # Try parsing JSON
        try:
            parsed = json.loads(text)
            return parsed
        except:
            return {
                "raw": text
            }

    except Exception as e:

        logging.error("Gemini error")
        logging.error(str(e))

        return {
            "error": str(e)
        }
