import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import re
from scout import scout

app = FastAPI()

# config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Welcome to the Scout Crawler API"}

@app.get("/scout/{cas_or_name}")
async def run_scout(cas_or_name: str):
    if not cas_or_name:
        raise HTTPException(status_code=400, detail="No input provided.")
    cas_pattern = r'^\d{2,7}-\d{2}-\d$'
    match = re.match(cas_pattern, cas_or_name)
    try:
        if match:
            response = await scout(cas=cas_or_name, name=None)
        else:
            response = await scout(cas=None, name=cas_or_name)
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
