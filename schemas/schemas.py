from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    """
    Base schema for a task.

    Attributes:
        title (str): The title of the task.
        description (Optional[str]): A description of the task.
        completed (Optional[bool]): A flag indicating whether the task is completed.
        list_id (int): The ID of the list to which the task belongs.
    """
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    list_id: int


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.

    Inherits all attributes from TaskBase.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Attributes:
        title (Optional[str]): The updated title of the task.
        description (Optional[str]): The updated description of the task.
        completed (Optional[bool]): The updated completion status of the task.
        list_id (Optional[int]): The updated ID of the list to which the task belongs.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    list_id: Optional[int] = None


class ListBase(BaseModel):
    """
    Base schema for a list.

    Attributes:
        name (str): The name of the list.
        description (Optional[str]): A description of the list.
    """
    name: str
    description: Optional[str] = None


class ListCreate(ListBase):
    """
    Schema for creating a new list.

    Inherits all attributes from ListBase.
    """
    pass


class ListUpdate(BaseModel):
    """
    Schema for updating an existing list.

    Attributes:
        name (Optional[str]): The updated name of the list.
        description (Optional[str]): The updated description of the list.
    """
    name: Optional[str] = None
    description: Optional[str] = None
