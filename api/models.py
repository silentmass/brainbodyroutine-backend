from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class TaskCategory(Base):
    __tablename__ = "taskcategories"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)


class TaskDescription(Base):
    __tablename__ = "taskdescription"
    id = Column(Integer, primary_key=True)
    description = Column(String, index=True)
    description_list_id = Column(Integer, ForeignKey("taskdescriptionlist.id"))

    description_owner = relationship(
        "TaskDescriptionList", back_populates="descriptions"
    )


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)

    tag_owner = relationship("Task", back_populates="tags")


class TaskDescriptionList(Base):
    __tablename__ = "taskdescriptionlist"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)

    description_list_owner = relationship("Task", back_populates="description_lists")
    descriptions = relationship("TaskDescription", back_populates="description_owner")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    task_category_id = Column(Integer, ForeignKey("taskcategories.id"))
    task_description_list_id = Column(Integer, ForeignKey("taskdescriptionlist.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    description_lists = relationship(
        "TaskDescriptionList", back_populates="description_list_owner"
    )
    tags = relationship("Tags", back_populates="tag_owner")
