from sqlalchemy.orm import Session
from app.db.models.budget import Budget as BudgetModel
from app.schemas.budget import BudgetCreate, BudgetUpdate

def create_budget(db: Session, budget: BudgetCreate) -> BudgetModel:
    db_budget = BudgetModel(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budgets(db: Session, skip: int = 0, limit: int = 100) -> list[BudgetModel]:
    return db.query(BudgetModel).offset(skip).limit(limit).all()

def get_budget(db: Session, budget_id: int) -> BudgetModel:
    return db.query(BudgetModel).filter(BudgetModel.id == budget_id).first()

def update_budget(db: Session, budget_id: int, budget: BudgetUpdate) -> BudgetModel:
    db_budget = db.query(BudgetModel).filter(BudgetModel.id == budget_id).first()
    if db_budget is None:
        return None

    for key, value in budget.dict().items():
        if value is not None:
            setattr(db_budget, key, value)

    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int) -> bool:
    db_budget = db.query(BudgetModel).filter(BudgetModel.id == budget_id).first()
    if db_budget is None:
        return False

    db.delete(db_budget)
    db.commit()
    return True
