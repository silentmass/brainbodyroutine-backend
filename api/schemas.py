from pydantic import BaseModel


class TaskCategoryBase(BaseModel):
    title: str
    description: str | None = None


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
    descriptions: list[TaskDescription] | None = None

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    is_active: bool
    task_category_id: int
    tag_id: int | None = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    description_lists: list[TaskDescriptionList] | None = None
    tags: list[Tag] | None = None

    class Config:
        from_attributes = True
