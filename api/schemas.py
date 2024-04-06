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


class TagsBase(BaseModel):
    title: str


class TagsCreate(TagsBase):
    pass


class Tags(TagsBase):
    id: int

    class Config:
        from_attributes = True


class TaskDescriptionListBase(BaseModel):
    title: str


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
    tag_id: int


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    description_lists: list[TaskDescriptionList] | None = None
    tags: list[Tags] | None = None

    class Config:
        from_attributes = True
