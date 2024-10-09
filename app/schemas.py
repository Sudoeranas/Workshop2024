# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    Nom: str
    Prenom: str
    email: EmailStr
    role: str
    health_conditions_id: Optional[int] = None
    id_kine: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class ExerciceBase(BaseModel):
    Nom_exo: str
    description: str
    Difficulte: str
    video_link: str

class ExerciceCreate(ExerciceBase):
    pass

class ExerciceResponse(ExerciceBase):
    id_exercice: int

    class Config:
        orm_mode = True
        
class UserExerciceCreate(BaseModel):
    user_id: int
    exercice_id: int
    date: date
    Optional: bool = False
    Checked: bool = False

class UserExerciceResponse(BaseModel):
    id: int
    user_id: int
    exercice_id: int
    date: date
    Optional: bool
    Checked: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
class UserLogin(BaseModel):
    email: str
    password: str
    
# HealthConditionResponseclass 
class HealthConditionBase(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

class HealthConditionCreate(BaseModel):
    name: str
    description: str
