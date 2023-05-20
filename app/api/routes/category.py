from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryInDB
from app.db.models.user import User
from app.services.category import create_category, get_categories, get_category, update_category, delete_category
from app.dependencies.dependecies import get_current_user, get_user_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()

@router.post("/", response_model=CategoryInDB)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    return create_category(db=db, category=category)


@router.get("/", response_model=List[CategoryInDB])
def read_categories(
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    return get_categories(db=db)


@router.get("/{category_id}", response_model=CategoryInDB)
def read_category(
    category_id: int,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_category = get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.put("/{category_id}", response_model=CategoryInDB)
def update_existing_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_category = update_category(db=db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/{category_id}")
def delete_existing_category(
    category_id: int,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_category = delete_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted"}


