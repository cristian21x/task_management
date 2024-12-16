from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from models import List
from database import get_db
from schemas import ListCreate, ListUpdate

router = APIRouter()


@router.get("/lists")
async def get_lists(db: Session = Depends(get_db)):
    try:
        lists = db.query(List).options(joinedload(List.tasks)).all()
        return {"lists": lists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lists")
async def create_list(list: ListCreate, db: Session = Depends(get_db)):
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