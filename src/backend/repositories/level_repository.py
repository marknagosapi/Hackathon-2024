from sqlalchemy.orm import Session
from models.level import Level
from loguru import logger

TAG = "LevelRepository"

class LevelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_level(self, name: str, min_points: int, max_points: int = None):
        logger.info(f"{TAG} - create_level() called")
        level = Level(name=name, min_points=min_points, max_points=max_points)
        self.db.add(level)
        self.db.commit()
        return level

    def get_level_by_name(self, name: str):
        logger.info(f"{TAG} - get_level_by_name() called")

        return self.db.query(Level).filter(Level.name == name).first()
    
    def get_level_by_points(self, points:int):
        logger.info(f"{TAG} - get_level_by_points() called")

        return self.db.query(Level.id).filter(Level.min_points <= points, (Level.max_points == None) | (Level.max_points >= points)).first()



    def get_level_by_id(self, level_id: int):
        logger.info(f"{TAG} - get_level_by_id() called")

        return self.db.query(Level).filter(Level.id == level_id).first()
    

    def get_all_levels(self):
        logger.info(f"{TAG} - get_all_levels() called")

        return self.db.query(Level).all()
    

    def update_level(self, level_id: int, name: str = None, min_points: int = None, max_points: int = None):
        logger.info(f"{TAG} - update_level() called")

        level = self.get_level_by_id(level_id)
        if level:
            if name:
                level.name = name
            if min_points:
                level.min_points = min_points
            if max_points:
                level.max_points = max_points
            self.db.commit()
        return level
    

    def delete_level(self, level_id: int):
        logger.info(f"{TAG} - delete_level() called")
        
        level = self.get_level_by_id(level_id)
        if level:
            self.db.delete(level)
            self.db.commit()
        return level
