from typing import List, Optional

from pydantic import BaseModel

from api.src.routes.descriptionlists.schemas import Tag, TaskDescriptionList


class TaskBase(BaseModel):
    title: str
    task_category_id: int
    is_active: bool
    user_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    sort_order: Optional[int] = None
    tags: Optional[List[Tag]] = None
    description_lists: Optional[List[TaskDescriptionList]] = None

    class Config:
        from_attributes = True
