from typing import List, Optional

from sqlalchemy import Column, ForeignKey, String, Table
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


# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
association_table_tag = Table(
    "association_table_tag",
    Base.metadata,
    Column("task_id", ForeignKey("task.id")),
    Column("tag_id", ForeignKey("tag.id")),
)

association_table_description_list = Table(
    "association_table_description_list",
    Base.metadata,
    Column("task_id", ForeignKey("task.id")),
    Column("description_list_id", ForeignKey("taskdescriptionlist.id")),
)

association_table_description = Table(
    "association_table_description",
    Base.metadata,
    Column("task_description_list_id", ForeignKey("taskdescriptionlist.id")),
    Column("task_description_id", ForeignKey("taskdescription.id")),
)


str50 = Annotated[str, mapped_column(String(50))]

intpk = Annotated[int, mapped_column(primary_key=True)]
task_fk = Annotated[int, mapped_column(ForeignKey("task.id"))]
tag_fk = Annotated[int, mapped_column(ForeignKey("tag.id"))]
task_category_fk = Annotated[int, mapped_column(ForeignKey("taskcategory.id"))]
task_description_list_fk = Annotated[
    int, mapped_column(ForeignKey("taskdescriptionlist.id"))
]


class Task(Base):
    __tablename__ = "task"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(index=True)
    task_category_id: Mapped[task_category_fk]
    is_active: Mapped[bool] = mapped_column(default=True)

    tags: Mapped[List["Tag"] | None] = relationship(
        secondary=association_table_tag, default_factory=list)
    description_lists: Mapped[List["TaskDescriptionList"] | None] = (
        relationship(
            secondary=association_table_description_list,
            default_factory=list)
    )


class TaskCategory(Base):
    __tablename__ = "taskcategory"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(30), index=True)
    description: Mapped[Optional[str]] = mapped_column(default=None)


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(30), index=True)


class TaskDescriptionList(Base):
    __tablename__ = "taskdescriptionlist"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str50] = mapped_column(index=True)
    task_id: Mapped[task_fk]

    descriptions: Mapped[List["TaskDescription"] | None] = (
        relationship(
            secondary=association_table_description,
            default_factory=list
        )
    )


class TaskDescription(Base):
    __tablename__ = "taskdescription"

    id: Mapped[intpk] = mapped_column(init=False)
    description: Mapped[str] = mapped_column(index=True)
    description_list_id: Mapped[task_description_list_fk]
