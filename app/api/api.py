from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.dependencies.dependecies import get_user_db, get_current_user
from app.api.routes import auth, budget, category, transaction, user, import_batch, user_account, merchant, bill, bank_account
from app.db.models import User

router = APIRouter()

@router.get("/app-info")
def get_app_info(db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    try:
        app_info = db.execute(text("SELECT * FROM alembic_version")).fetchone()
        return {"username": current_user.username,
                "database": current_user.user_account.database,
                "alias": current_user.user_account.alias,
                "version": app_info[0]}
    except Exception as e:
        raise HTTPException(status_code=400)


router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(budget.router, prefix="/budgets", tags=["budgets"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(user_account.router, prefix="/user-accounts", tags=["user-accounts"])
router.include_router(category.router, prefix="/categories", tags=["categories"])
router.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
router.include_router(import_batch.router, prefix="/import-batches", tags=["import-batches"])
router.include_router(merchant.router, prefix="/merchants", tags=["merchants"])
router.include_router(bill.router, prefix="/bills", tags=["bills"])
router.include_router(bank_account.router, prefix="/bank-accounts", tags=["bank-accounts"])

