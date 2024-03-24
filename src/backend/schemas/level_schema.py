from pydantic import BaseModel
from typing import Optional


class LevelBase(BaseModel):
    name: str
    min_points: int
    max_points: int | None = None
