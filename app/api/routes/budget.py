from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetInDB
from app.db.models.user import User
from app.services.budget import create_budget, get_budgets, get_budget, update_budget, delete_budget
from app.depdendencies import get_db
from app.api.dependencies import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()


@router.post("/", response_model=BudgetInDB)
def create_budget_item(budget: BudgetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_budget(db, budget)

@router.get("/", response_model=List[BudgetInDB])
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budgets = get_budgets(db, skip=skip, limit=limit)
    return budgets

@router.get("/{budget_id}", response_model=BudgetInDB)
def read_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = get_budget(db, budget_id=budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget

@router.put("/{budget_id}", response_model=BudgetInDB)
def update_budget_item(budget_id: int, budget: BudgetUpdate, db: Session = Depends(get_db)):
    updated_budget = update_budget(db, budget_id, budget)
    if updated_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return updated_budget

@router.delete("/{budget_id}")
def delete_budget_item(budget_id: int, db: Session = Depends(get_db)):
    deleted = delete_budget(db, budget_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"detail": "Budget deleted successfully"}
