from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, HTTPException
import sys
sys.path.append('../')



router = APIRouter(
    prefix="", tags=["user"]
)

@router.get("/")
async def read_root():
    return {"message": "Hello, World"}

@router.get("/database")
async def connect_to_database():
    return "connected"
