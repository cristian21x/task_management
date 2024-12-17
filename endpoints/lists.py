from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from models.models import List
from db.database import get_db
from schemas.schemas import ListCreate, ListUpdate

router = APIRouter()


@router.get("/lists")
async def get_lists(db: Session = Depends(get_db)):
    """
    Retrieve all lists from the database, including their associated tasks.

    Args:
        db (Session): Database session dependency.

    Returns:
        dict: A dictionary containing a list of lists with their tasks.

    Raises:
        HTTPException: If an error occurs during the database query.
    """
    try:
        lists = db.query(List).options(joinedload(List.tasks)).all()
        return {"lists": lists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/lists")
async def create_list(list: ListCreate, db: Session = Depends(get_db)):
    """
    Create a new list in the database.

    Args:
        list (ListCreate): The list data to create.
        db (Session): Database session dependency.

    Returns:
        List: The created list object.

    Raises:
        HTTPException: If an error occurs during the list creation.
    """
    try:
        db_list = List(**list.dict())
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
        return db_list
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/lists/{list_id}")
async def update_list(list_id: int, list: ListUpdate, db: Session = Depends(get_db)):
    """
    Update an existing list in the database.

    Args:
        list_id (int): The ID of the list to update.
        list (ListUpdate): The updated list data.
        db (Session): Database session dependency.

    Returns:
        List: The updated list object.

    Raises:
        HTTPException: If the list is not found or an error occurs during the update.
    """
    try:
        db_list = db.query(List).filter(List.id == list_id).first()
        if not db_list:
            raise HTTPException(status_code=404, detail="List not found")
        
        update_data = list.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_list, key, value)
        
        db.commit()
        db.refresh(db_list)
        return db_list
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/lists/{list_id}")
async def delete_list(list_id: int, db: Session = Depends(get_db)):
    """
    Delete a list from the database.

    Args:
        list_id (int): The ID of the list to delete.
        db (Session): Database session dependency.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the list is not found or an error occurs during the deletion.
    """
    try:
        db_list = db.query(List).filter(List.id == list_id).first()
        if not db_list:
            raise HTTPException(status_code=404, detail="List not found")
        
        db.delete(db_list)
        db.commit()
        return {"message": "List deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))