from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import crud, schemas, utils, auth, requests
import os

# ---------------- CREATE TABLES -----------------
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Research AI Backend")
COLAB_API_URL = os.getenv("COLAB_API_URL")

# ---------------- AUTH ROUTES ------------------
@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = crud.create_user(db, user.username, user.email, user.password)
    return db_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

# ---------------- PAPER GENERATION -----------------
@app.post("/generate-paper")
def generate_paper(paper_req: schemas.PaperRequest, db: Session = Depends(get_db)):
    # Send request to Colab AI
    response = requests.post(f"{COLAB_API_URL}/generate_paper", json=paper_req.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Colab API error")
    
    paper_text = response.json().get("paper_text", "")
    
    # Save locally and upload to S3
    file_name = f"{paper_req.title.replace(' ', '_')}.txt"
    with open(file_name, "w") as f:
        f.write(paper_text)
    s3_url = utils.upload_to_s3(file_name, file_name)
    
    # Save in DB (owner_id=1 for demo)
    db_paper = crud.create_paper(db, paper_req.title, s3_url, owner_id=1)
    return {"paper_text": paper_text, "s3_url": s3_url, "paper_id": db_paper.id}

# ---------------- PLAGIARISM CHECK -----------------
@app.post("/plagiarism-check")
def plagiarism_check(plag_req: schemas.PlagiarismRequest):
    response = requests.post(f"{COLAB_API_URL}/plagiarism_check", json=plag_req.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Colab API error")
    return response.json()
