from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional
try:
    from count_table import Base, CountTable
except Exception:
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String, DateTime, func

    Base = declarative_base()

    class CountTable(Base):
        __tablename__ = "counts"
        id = Column(Integer, primary_key=True, index=True)
        count_number = Column(Integer, default=0)
        description = Column(String, nullable=True)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

# Configuration de la base de données SQLite
DATABASE_URL = "sqlite:///./counter.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables
Base.metadata.create_all(bind=engine)

# Initialiser FastAPI
app = FastAPI(
    title="Counter API",
    description="API pour gérer et incrémenter un compteur",
    version="1.0.0"
)


# Modèles Pydantic pour les requêtes/réponses
class CounterCreate(BaseModel):
    """Modèle pour créer un nouveau compteur"""
    description: Optional[str] = None
    initial_value: int = 0


class CounterResponse(BaseModel):
    """Modèle de réponse pour un compteur"""
    id: int
    count_number: int
    description: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


# Dépendance pour obtenir la session de base de données
def get_db():
    """Obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    """Endpoint racine"""
    return {
        "message": "Bienvenue sur l'API Counter",
        "endpoints": {
            "POST /counter": "Créer un nouveau compteur",
            "GET /counter/{counter_id}": "Obtenir un compteur",
            "POST /counter/{counter_id}/increment": "Incrémenter un compteur",
            "GET /counters": "Liste tous les compteurs"
        }
    }


@app.post("/counter", response_model=CounterResponse, status_code=201)
def create_counter(
    counter: CounterCreate,
    db: Session = Depends(get_db)
):
    """
    Créer un nouveau compteur

    Args:
        counter: Données du compteur à créer
        db: Session de base de données

    Returns:
        Le compteur créé
    """
    new_counter = CountTable(
        count_number=counter.initial_value,
        description=counter.description
    )
    db.add(new_counter)
    db.commit()
    db.refresh(new_counter)

    return CounterResponse(
        id=new_counter.id,
        count_number=new_counter.count_number,
        description=new_counter.description,
        created_at=new_counter.created_at.isoformat(),
        updated_at=new_counter.updated_at.isoformat() if new_counter.updated_at else None
    )


@app.get("/counter/{counter_id}", response_model=CounterResponse)
def get_counter(counter_id: int, db: Session = Depends(get_db)):
    """
    Obtenir un compteur par son ID

    Args:
        counter_id: ID du compteur
        db: Session de base de données

    Returns:
        Le compteur demandé

    Raises:
        HTTPException: Si le compteur n'existe pas
    """
    counter = db.query(CountTable).filter(CountTable.id == counter_id).first()

    if not counter:
        raise HTTPException(status_code=404, detail=f"Compteur {counter_id} non trouvé")

    return CounterResponse(
        id=counter.id,
        count_number=counter.count_number,
        description=counter.description,
        created_at=counter.created_at.isoformat(),
        updated_at=counter.updated_at.isoformat() if counter.updated_at else None
    )


@app.post("/counter/{counter_id}/increment", response_model=CounterResponse)
def increment_counter(
    counter_id: int,
    increment_by: int = 1,
    db: Session = Depends(get_db)
):
    """
    Incrémenter un compteur

    Args:
        counter_id: ID du compteur à incrémenter
        increment_by: Valeur d'incrémentation (par défaut 1)
        db: Session de base de données

    Returns:
        Le compteur avec sa nouvelle valeur

    Raises:
        HTTPException: Si le compteur n'existe pas
    """
    counter = db.query(CountTable).filter(CountTable.id == counter_id).first()

    if not counter:
        raise HTTPException(status_code=404, detail=f"Compteur {counter_id} non trouvé")

    # Incrémenter le compteur
    counter.count_number += increment_by
    db.commit()
    db.refresh(counter)

    return CounterResponse(
        id=counter.id,
        count_number=counter.count_number,
        description=counter.description,
        created_at=counter.created_at.isoformat(),
        updated_at=counter.updated_at.isoformat() if counter.updated_at else None
    )


@app.get("/counters", response_model=list[CounterResponse])
def list_counters(db: Session = Depends(get_db)):
    """
    Liste tous les compteurs

    Args:
        db: Session de base de données

    Returns:
        Liste de tous les compteurs
    """
    counters = db.query(CountTable).all()

    return [
        CounterResponse(
            id=counter.id,
            count_number=counter.count_number,
            description=counter.description,
            created_at=counter.created_at.isoformat(),
            updated_at=counter.updated_at.isoformat() if counter.updated_at else None
        )
        for counter in counters
    ]


@app.delete("/counter/{counter_id}")
def delete_counter(counter_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un compteur

    Args:
        counter_id: ID du compteur à supprimer
        db: Session de base de données

    Returns:
        Message de confirmation

    Raises:
        HTTPException: Si le compteur n'existe pas
    """
    counter = db.query(CountTable).filter(CountTable.id == counter_id).first()

    if not counter:
        raise HTTPException(status_code=404, detail=f"Compteur {counter_id} non trouvé")

    db.delete(counter)
    db.commit()

    return {"message": f"Compteur {counter_id} supprimé avec succès"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)