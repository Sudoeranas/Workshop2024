from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Remplace cette URL par l'URL de ta propre base de données (ex: PostgreSQL, MySQL, etc.)
# Exemple pour SQLite :
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"  # Chemin vers ta base de données SQLite

# Pour PostgreSQL, cela ressemblerait à :
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Crée l'engine SQLAlchemy (la connexion à la base de données)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Utilisé pour SQLite
)

# Crée une session locale qui interagira avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles
Base = declarative_base()

# Fonction de dépendance pour récupérer la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
