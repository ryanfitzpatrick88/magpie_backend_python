from sqlalchemy.orm import Session
from app.db.models.user import UserAccount
from app.schemas.user import UserAccountCreate, UserAccountUpdate

def create_user_account(db: Session, user_account: UserAccountCreate) -> UserAccount:
    db_user_account = UserAccount(database=user_account.database)
    db.add(db_user_account)
    db.commit()
    db.refresh(db_user_account)
    return db_user_account

def get_user_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[UserAccount]:
    return db.query(UserAccount).offset(skip).limit(limit).all()

def get_user_account(db: Session, user_account_id: int) -> Optional[UserAccount]:
    return db.query(UserAccount).filter(UserAccount.id == user_account_id).first()

def update_user_account(db: Session, user_account_id: int, user_account: UserAccountUpdate) -> Optional[UserAccount]:
    db_user_account = get_user_account(db, user_account_id)
    if db_user_account:
        for field, value in user_account.dict(exclude_unset=True).items():
            setattr(db_user_account, field, value)
        db.commit()
        db.refresh(db_user_account)
    return db_user_account

def delete_user_account(db: Session, user_account_id: int) -> bool:
    db_user_account = get_user_account(db, user_account_id)
    if db_user_account:
        db.delete(db_user_account)
        db.commit()
        return True
    return False
