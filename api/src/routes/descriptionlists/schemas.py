from typing import List, Optional

from pydantic import BaseModel

from api.src.routes.descriptions.schemas import TaskDescription


class TagBase(BaseModel):
    title: str
    task_id: int


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True


class TaskDescriptionListBase(BaseModel):
    title: str
    task_id: int


class TaskDescriptionListCreate(TaskDescriptionListBase):
    pass


class TaskDescriptionList(TaskDescriptionListBase):
    id: int
    descriptions: Optional[List[TaskDescription]] = None

    class Config:
        from_attributes = True
