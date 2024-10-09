# app/main.py
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, database, auth
from .auth import create_access_token, get_password_hash, authenticate_user, get_current_user
from .database import engine

# Crée les tables de la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency pour obtenir une session DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour créer un nouvel utilisateur
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        Nom=user.Nom,
        Prenom=user.Prenom,
        email=user.email,
        password=hashed_password,
        role=user.role,
        health_conditions_id=user.health_conditions_id,
        id_kine=user.id_kine
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Route pour obtenir un token JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # Utilisation de l'email et du mot de passe pour authentifier
    user = authenticate_user(db, login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crée un token d'accès qui expire dans un certain temps
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # Retourne le token d'accès et le type
    return {"access_token": access_token, "token_type": "bearer"}

# Route pour obtenir les informations de l'utilisateur authentifié
@app.get("/users/me/", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Route GET /users
@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    users = db.query(models.User).all()
    return users

# Route GET /exercices
@app.get("/exercices", response_model=list[schemas.ExerciceResponse])
def get_exercices(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    exercices = db.query(models.Exercice).all()
    return exercices

# Route POST /exercices pour ajouter un nouvel exercice
@app.post("/exercices/", response_model=schemas.ExerciceResponse)
def create_exercice(exercice: schemas.ExerciceCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_exercice = models.Exercice(
        Nom_exo=exercice.Nom_exo,
        description=exercice.description,
        Difficulte=exercice.Difficulte,
        video_link=exercice.video_link
    )
    db.add(new_exercice)
    db.commit()
    db.refresh(new_exercice)
    return new_exercice
