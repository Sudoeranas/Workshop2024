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
    series: int
    repetitions: int 

class UserExerciceResponse(BaseModel):
    id: int
    user_id: int
    exercice_id: int
    date: date
    Optional: bool
    Checked: bool
    series: int
    repetitions: int

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


class LoginRequest(BaseModel):
    email: str
    password: str

class ExerciceByUserResponse(BaseModel):
    id_exercice: int
    Nom_exo: str
    description: str
    date: date
    userId: int
    checked: bool
    series: int
    repetitions: int
    optional: bool
    video_id: str