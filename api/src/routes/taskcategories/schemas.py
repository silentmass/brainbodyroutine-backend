from typing import Optional

from pydantic import BaseModel


class TaskCategoryBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCategoryCreate(TaskCategoryBase):
    pass


class TaskCategory(TaskCategoryBase):
    id: int

    class Config:
        from_attributes = True
