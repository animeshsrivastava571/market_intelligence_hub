# app/main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from app.api.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Market Intelligence Hub")

app.include_router(router)

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "Market Intelligence Hub is running"}
