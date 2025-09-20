from fastapi import FastAPI,Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel
import pandas as pd
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the root directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.ml.insurance import insur

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/submit/")
async def submit_insurance_form(
    age: Annotated[int, Form()],
    sex: Annotated[str, Form()],
    bmi: Annotated[float, Form()],
    children: Annotated[int, Form()],
    smoker: Annotated[str, Form()],
    region: Annotated[str, Form()],
):
    try:
        val = pd.DataFrame({
            "age": [age],
            "sex": [sex],
            "bmi": [bmi],
            "children": [children],
            "smoker": [smoker],
            "region": [region]
        })
        
        result = insur(val)
        return result
        
    except Exception as e:
        return {"error": str(e)}
