from pydantic import BaseModel


class TaskDescriptionBase(BaseModel):
    description: str
    description_list_id: int


class TaskDescriptionCreate(TaskDescriptionBase):
    pass


class TaskDescription(TaskDescriptionBase):
    id: int

    class Config:
        from_attributes = True
