from typing import List, Optional
from repositories.level_repository import LevelRepository
from models.level import Level
from loguru import logger
from helper.dependencies import db
from loguru import logger

TAG = "LevelService"

class LevelService:
    def __init__(self):
        self.db = db
        self.level_repository = LevelRepository(db)


    def create_level(self, name: str, min_points: int, max_points: int = None) -> Level:
        logger.info(f"{TAG} - create_level() called")

        return self.level_repository.create_level(name, min_points, max_points)


    def get_level_by_name(self, name: str) -> Optional[Level]:
        logger.info(f"{TAG} - get_level_by_name() called")

        return self.level_repository.get_level_by_name(name)


    def get_level_by_id(self, level_id: int) -> Optional[Level]:
        logger.info(f"{TAG} - get_level_by_id() called")

        return self.level_repository.get_level_by_id(level_id)
    
    def get_level_by_points(self, points: int) -> Optional[Level]:
        logger.info(f"{TAG} - get_level_by_points() called")

        return self.level_repository.get_level_by_points(points)
    

    def get_all_levels(self) -> List[Level]:
        logger.info(f"{TAG} - get_all_levels() called")

        return self.level_repository.get_all_levels()


    def update_level(self, level_id: int, name: str = None, min_points: int = None, max_points: int = None) -> Optional[Level]:
        logger.info(f"{TAG} - update_level() called")

        return self.level_repository.update_level(level_id, name, min_points, max_points)


    def delete_level(self, level_id: int) -> Optional[Level]:
        logger.info(f"{TAG} - delete_level() called")

        return self.level_repository.delete_level(level_id)
