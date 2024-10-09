# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class HealthCondition(Base):
    __tablename__ = "healthconditions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    users = relationship("User", back_populates="healthconditions")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    Nom = Column(String(50))
    Prenom = Column(String(50))
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(50))
    health_conditions_id = Column(Integer, ForeignKey("healthconditions.id"))
    id_kine = Column(Integer, nullable=True)
    # Relation entre les utilisateurs et les conditions de santé
    healthconditions = relationship("HealthCondition", back_populates="users")
    user_exercices = relationship("UserExercice", back_populates="user")

class Exercice(Base):
    __tablename__ = "exercices"

    id_exercice = Column(Integer, primary_key=True, index=True)
    Nom_exo = Column(String(50))
    description = Column(String(255))
    Difficulte = Column(String(50))
    video_link = Column(String(255))
    user_exercices = relationship("UserExercice", back_populates="exercice")

class UserExercice(Base):
    __tablename__ = "userexercice"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercice_id = Column(Integer, ForeignKey("exercices.id_exercice"))
    date = Column(Date)
    Optional = Column(Boolean, default=False)
    Checked = Column(Boolean, default=False)

    user = relationship("User", back_populates="user_exercices")
    exercice = relationship("Exercice", back_populates="user_exercices")