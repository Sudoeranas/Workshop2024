# app/main.py
from datetime import date, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, database, auth
from .auth import create_access_token, get_password_hash, authenticate_user, get_current_user
from .database import engine
from fastapi.middleware.cors import CORSMiddleware

# Crée les tables de la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurer CORS
origins = [
    "http://localhost:5173",  # Remplace par l'URL de ton frontend
    "http://127.0.0.1:5173",  # Inclure aussi cette adresse
    # Ajoute d'autres origines si nécessaire
]

# Ajoutez le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permet uniquement les origines spécifiées
    allow_credentials=True,  # Autorise l'envoi des cookies ou des identifiants
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les en-têtes
)

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

@app.post("/token")
def login_for_access_token():
    # Simuler une réponse de connexion sans authentification
    return {"access_token": "no-token-needed", "token_type": "none"}

# Exemple d'une route qui n'utilise plus de tokens
@app.get("/users/{user_id}")
def read_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return {"id": user.id, "email": user.email, "nom": user.Nom, "Prenom" : user.Prenom, "role" : user.role, "kine" : user.id_kine}  # Renvoie les informations que tu veux

@app.get("/items/")
def read_items():
    # Simplement retourner les items sans vérifier de token
    return {"items": ["item1", "item2"]}


# Route GET /users
@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Route GET /exercices
@app.get("/exercices", response_model=list[schemas.ExerciceResponse])
def get_exercices(db: Session = Depends(get_db)):
    # Récupérer tous les exercices sans authentification
    exercices = db.query(models.Exercice).all()
    return exercices


# Route POST /exercices pour ajouter un nouvel exercice
@app.post("/exercices/", response_model=schemas.ExerciceResponse)
def create_exercice(exercice: schemas.ExerciceCreate, db: Session = Depends(get_db)):
    # Créer un nouvel exercice sans authentification
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

# Route de connexion qui utilise un body JSON
@app.post("/login")
def login(
    login_data: schemas.LoginRequest,  # Le body est automatiquement converti via LoginRequest
    db: Session = Depends(database.get_db)
):
    email = login_data.email
    password = login_data.password

    # Authentification de l'utilisateur
    user = authenticate_user(db, email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )

    return {"message": "Connexion réussie", "user_id": user.id, "role": user.role, "nom": user.Nom, "prenom": user.Prenom, "email": user.email}

@app.get("/users/{user_id}/healthconditions", response_model=list[schemas.HealthConditionBase])
def get_healthconditions_for_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Récupérer les conditions de santé de cet utilisateur
    healthconditions = db.query(models.HealthCondition).filter(models.HealthCondition.user_id == user_id).all()
    
    if not healthconditions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune condition de santé trouvée pour cet utilisateur"
        )
    
    return healthconditions

@app.post("/users/{user_id}/healthconditions", response_model=schemas.HealthConditionBase)
def create_healthcondition_for_user(
    user_id: int, 
    healthcondition: schemas.HealthConditionCreate, 
    db: Session = Depends(database.get_db)
):
    # Vérifier si l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Créer une nouvelle condition de santé pour cet utilisateur
    new_healthcondition = models.HealthCondition(
        name=healthcondition.name,
        description=healthcondition.description,
        user_id=user_id  # Lier la condition à l'utilisateur via user_id
    )
    
    db.add(new_healthcondition)
    db.commit()
    db.refresh(new_healthcondition)
    
    return new_healthcondition

@app.get("/exercices/{id}", response_model=schemas.ExerciceResponse)
def get_exercice_by_id(id: int, db: Session = Depends(get_db)):
    exercice = db.query(models.Exercice).filter(models.Exercice.id_exercice == id).first()
    
    if not exercice:
        raise HTTPException(status_code=404, detail="Exercice not found")
    
    return exercice

# Route POST /userexercice/ pour ajouter un exercice à un utilisateur
@app.post("/userexercice/", response_model=schemas.UserExerciceResponse)
def create_user_exercice(user_exercice: schemas.UserExerciceCreate, db: Session = Depends(get_db)):
    new_user_exercice = models.UserExercice(
        user_id=user_exercice.user_id,
        exercice_id=user_exercice.exercice_id,
        date=user_exercice.date,
        Optional=user_exercice.Optional,
        Checked=user_exercice.Checked
    )
    db.add(new_user_exercice)
    db.commit()
    db.refresh(new_user_exercice)
    return new_user_exercice

# Route GET /userexercice/{user_id} pour obtenir tous les exercices d'un utilisateur spécifique
@app.get("/userexercice/{user_id}")
def read_user_exercises_by_id(
    user_id: int,
    date: Optional[date] = None,  # Ajout du paramètre de requête pour la date
    db: Session = Depends(get_db)
):
    query = db.query(models.UserExercice).filter(models.UserExercice.user_id == user_id)

    # Si une date est fournie, filtrer par date
    if date:
        query = query.filter(models.UserExercice.date == date)

    user_exercices = query.all()

    if not user_exercices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun exercice trouvé pour cet utilisateur"
        )
    
    return user_exercices  # Renvoie la liste des exercices de l'utilisateur
