from typing import List, Optional

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


class TaskDescriptionBase(BaseModel):
    description: str
    description_list_id: int


class TaskDescriptionCreate(TaskDescriptionBase):
    pass


class TaskDescription(TaskDescriptionBase):
    id: int

    class Config:
        from_attributes = True


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


class TaskBase(BaseModel):
    title: str
    task_category_id: int
    is_active: bool


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    tags: Optional[List[Tag]] = None
    description_lists: Optional[List[TaskDescriptionList]] = None

    class Config:
        from_attributes = True
