from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from models.models import List, Task
from db.database import get_db
from fastapi.responses import JSONResponse
import json

router = APIRouter()


@router.post("/import")
async def import_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Import data from a JSON file and store it in the database.

    Args:
        file (UploadFile): The uploaded JSON file containing lists and tasks.
        db (Session): Database session dependency.

    Returns:
        dict: A message indicating successful data import.

    Raises:
        HTTPException: If an error occurs during the import process.
    """
    try:
        content = await file.read()
        data = json.loads(content)
        
        if "lists" in data:
            for list_data in data["lists"]:
                db_list = List(name=list_data["name"], description=list_data.get("description", ""))
                db.add(db_list)
                db.commit()
                db.refresh(db_list)
                
                for task_data in list_data.get("tasks", []):
                    db_task = Task(
                        title=task_data["title"],
                        description=task_data.get("description", ""),
                        completed=task_data.get("completed", False),
                        list_id=db_list.id
                    )
                    db.add(db_task)
                db.commit()
        return {"message": "Data imported successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export", response_class=JSONResponse)
async def export_data(db: Session = Depends(get_db)):
    """
    Export all lists and their tasks from the database to a JSON response.

    Args:
        db (Session): Database session dependency.

    Returns:
        JSONResponse: A JSON response containing all lists and their tasks.

    Raises:
        HTTPException: If an error occurs during the export process.
    """
    try:
        lists = db.query(List).options(joinedload(List.tasks)).all()
        data = {
            "lists": [
                {
                    "name": list.name,
                    "description": list.description,
                    "tasks": [
                        {
                            "title": task.title,
                            "description": task.description,
                            "completed": task.completed
                        } for task in list.tasks
                    ]
                } for list in lists
            ]
        }
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))