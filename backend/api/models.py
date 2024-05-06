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


# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column


str50 = Annotated[str, mapped_column(String(50))]

intpk = Annotated[int, mapped_column(primary_key=True)]
user_fk = Annotated[
    int,
    mapped_column(ForeignKey("BBR_users.id"), index=True, nullable=True),
]
task_fk = Annotated[int, mapped_column(ForeignKey("BBR_tasks.id"))]
tag_fk = Annotated[int, mapped_column(ForeignKey("BBR_tags.id"))]
task_category_fk = Annotated[
    int, mapped_column(ForeignKey("BBR_taskcategories.id"))
]
task_description_list_fk = Annotated[
    int, mapped_column(ForeignKey("BBR_taskdescriptionlists.id"))
]


class BBR_User(Base):
    __tablename__ = "BBR_users"
    id: Mapped[intpk] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(
        index=True, unique=True, nullable=False
    )
    email: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[Optional[bool]] = mapped_column(
        nullable=True, default=False
    )
    tasks: Mapped[Optional[List["BBR_Task"]]] = relationship(
        argument="BBR_Task",
        default_factory=list,
        cascade="all, delete",
    )


class BBR_Task(Base):
    __tablename__ = "BBR_tasks"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(index=True)
    task_category_id: Mapped[task_category_fk]
    is_active: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[user_fk] = mapped_column(default=None)
    sort_order: Mapped[int] = mapped_column(
        default=None, index=True, nullable=True
    )

    tags: Mapped[Optional[List["BBR_Tag"]]] = relationship(
        argument="BBR_Tag", default_factory=list, cascade="all, delete"
    )
    description_lists: Mapped[Optional[List["BBR_TaskDescriptionList"]]] = (
        relationship(
            argument="BBR_TaskDescriptionList",
            default_factory=list,
            cascade="all, delete",
        )
    )


class BBR_TaskCategory(Base):
    __tablename__ = "BBR_taskcategories"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(30), index=True)
    description: Mapped[Optional[str]] = mapped_column(default=None)


class BBR_Tag(Base):
    __tablename__ = "BBR_tags"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(30), index=True)
    task_id: Mapped[task_fk]


class BBR_TaskDescriptionList(Base):
    __tablename__ = "BBR_taskdescriptionlists"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str50] = mapped_column(index=True)
    task_id: Mapped[task_fk]

    descriptions: Mapped[Optional[List["BBR_TaskDescription"]]] = relationship(
        argument="BBR_TaskDescription",
        default_factory=list,
        cascade="all, delete",
    )


class BBR_TaskDescription(Base):
    __tablename__ = "BBR_taskdescriptions"

    id: Mapped[intpk] = mapped_column(init=False)
    description: Mapped[str] = mapped_column(index=True)
    description_list_id: Mapped[task_description_list_fk]
