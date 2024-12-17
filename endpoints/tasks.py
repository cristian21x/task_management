from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import Task
from db.database import get_db
from schemas.schemas import TaskCreate, TaskUpdate

router = APIRouter()


@router.get("/tasks")
async def get_tasks(db: Session = Depends(get_db)):
    """
    Retrieve all tasks from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        dict: A dictionary containing a list of tasks.

    Raises:
        HTTPException: If an error occurs during the database query.
    """
    try:
        tasks = db.query(Task).all()
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task in the database.

    Args:
        task (TaskCreate): The task data to create.
        db (Session): Database session dependency.

    Returns:
        Task: The created task object.

    Raises:
        HTTPException: If an error occurs during the task creation.
    """
    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing task in the database.

    Args:
        task_id (int): The ID of the task to update.
        task (TaskUpdate): The updated task data.
        db (Session): Database session dependency.

    Returns:
        Task: The updated task object.

    Raises:
        HTTPException: If the task is not found or an error occurs during the update.
    """
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        update_data = task.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task from the database.

    Args:
        task_id (int): The ID of the task to delete.
        db (Session): Database session dependency.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the task is not found or an error occurs during the deletion.
    """
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(db_task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))