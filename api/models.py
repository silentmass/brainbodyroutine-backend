from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from typing_extensions import Annotated


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


str50 = Annotated[str, mapped_column(String(50))]

intpk = Annotated[int, mapped_column(primary_key=True)]
task_fk = Annotated[int, mapped_column(ForeignKey("task.id"))]
tag_fk = Annotated[int, mapped_column(ForeignKey("tag.id"))]
task_category_fk = Annotated[int, mapped_column(ForeignKey("taskcategory.id"))]
task_description_list_fk = Annotated[
    int, mapped_column(ForeignKey("taskdescriptionlist.id"))
]


class TaskCategory(Base):
    __tablename__ = "taskcategory"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(30), index=True)
    description: Mapped[Optional[str]] = mapped_column(default=None)


class TaskDescription(Base):
    __tablename__ = "taskdescription"

    id: Mapped[intpk] = mapped_column(init=False)
    description: Mapped[str] = mapped_column(index=True)
    description_list_id: Mapped[task_description_list_fk]

    description_owner: Mapped["TaskDescriptionList"] = relationship(
        back_populates="descriptions"
    )


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(30), index=True)

    tag_owner: Mapped["Task"] = relationship(back_populates="tags")


class TaskDescriptionList(Base):
    __tablename__ = "taskdescriptionlist"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str50] = mapped_column(index=True)
    task_id: Mapped[task_fk]

    description_list_owner: Mapped["Task"] = relationship(
        back_populates="description_lists"
    )
    descriptions: Mapped[List["TaskDescription"]] = relationship(
        back_populates="description_owner"
    )


class Task(Base):
    __tablename__ = "task"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(index=True)
    task_category_id: Mapped[task_category_fk]
    is_active: Mapped[bool] = mapped_column(default=True)
    tag_id: Mapped[Optional[tag_fk]] = mapped_column(default=None)

    description_lists: Mapped[Optional[List["TaskDescriptionList"]]] = relationship(
        back_populates="description_list_owner", default=None
    )
    tags: Mapped[Optional[List["Tag"]]] = relationship(
        back_populates="tag_owner", default=None
    )
