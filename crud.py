from models import User, Paper
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------- USER --------------------
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, email: str, password: str):
    hashed = pwd_context.hash(password)
    db_user = User(username=username, email=email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# -------------------- PAPER --------------------
def create_paper(db: Session, title: str, s3_url: str, owner_id: int):
    db_paper = Paper(title=title, s3_url=s3_url, owner_id=owner_id)
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper
