from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from services.level_service import LevelService
from models.level import Level
from schemas.level_schema import LevelBase
from typing import List

router = APIRouter(prefix="/levels")

level_service = LevelService()

@router.post("/")
async def create_level(level_data: LevelBase):
    return level_service.create_level(level_data.name, level_data.min_points, level_data.max_points)

@router.get("/", response_model=List[LevelBase])
async def find_all_levels():
    return level_service.get_all_levels()

@router.get("/get_by_id", response_model=LevelBase)
async def find_level(level_id: int):
    level = level_service.get_level_by_id(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level

@router.get("/get_by_points", response_model=LevelBase)
async def find_level_by_points(level_id: int):
    level = level_service.get_level_by_points(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level



@router.put("/update", response_model=LevelBase)
async def update_level(level_id: int, level_data: LevelBase):
    level = level_service.update_level(level_id, level_data.name, level_data.min_points, level_data.max_points)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level

@router.delete("/delete")
async def delete_level(level_id: int):
    level = level_service.delete_level(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return {"message": "Level deleted successfully"}
