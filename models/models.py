from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class List(Base):
    """
    Represents a task list in the database.

    Attributes:
        id (int): The unique identifier for the list.
        name (str): The name of the list.
        description (str): A description of the list.
        created_at (datetime): The timestamp when the list was created.
        tasks (relationship): A relationship to the Task model, representing
            the tasks associated with this list.
    """
    __tablename__ = "list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    tasks = relationship("Task", back_populates="list", cascade="all, delete-orphan")

class Task(Base):
    """
    Represents a task in the database.

    Attributes:
        id (int): The unique identifier for the task.
        title (str): The title of the task.
        description (str): A description of the task.
        completed (bool): A flag indicating whether the task is completed.
        created_at (datetime): The timestamp when the task was created.
        list_id (int): The foreign key referencing the associated list.
        list (relationship): A relationship to the List model, representing
            the list to which this task belongs.
    """
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    list_id = Column(Integer, ForeignKey("list.id"), nullable=False)
    list = relationship("List", back_populates="tasks") 