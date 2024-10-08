from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    Nom: str
    Prenom: str
    email: str
    password: str
    role: str
    health_conditions_id: Optional[int] = None
    id_kine: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    Nom: str
    Prenom: str
    email: str
    role: str

    class Config:
        orm_mode = True

class ExerciceCreate(BaseModel):
    Nom_exo: str
    description: str
    Difficulte: str
    video_link: str

class ExerciceResponse(BaseModel):
    id_exercice: int
    Nom_exo: str
    description: str
    Difficulte: str
    video_link: str

    class Config:
        orm_mode = True
