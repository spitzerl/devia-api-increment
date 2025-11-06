from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
from app.count_table import CountTable, Base
from schemas import CountTableCreate, CountTableUpdate, CountTableResponse


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Back FastAPI")

# Enable CORS for local development (vite front-end)
app.add_middleware(
    CORSMiddleware,
    # Allow common dev origins (Vite default 5173, Create React App 3000) and localhost
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI (app.main)"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Minimal API expected by the front-end in the project:
# - GET  /api/count                -> { "count": number }
# - POST /api/count/increment      -> { "count": number, "message": str }


def _get_or_create_counter(db: Session) -> CountTable:
    """Return the latest counter row or create one if missing."""
    counter = db.query(CountTable).order_by(CountTable.id.desc()).first()
    if counter is None:
        counter = CountTable(count_number=1)
        db.add(counter)
        db.commit()
        db.refresh(counter)
    return counter


@app.get("/api/count")
def api_get_count(db: Session = Depends(get_db)):
    counter = _get_or_create_counter(db)
    return {"count": counter.count_number}


@app.post("/api/count/increment")
def api_increment_count(db: Session = Depends(get_db)):
    # Simple increment logic. For Postgres this is safe enough inside a transaction
    # For high-concurrency production use consider SELECT ... FOR UPDATE or an atomic DB statement.
    counter = _get_or_create_counter(db)
    counter.count_number = (counter.count_number or 0) + 1
    db.add(counter)
    db.commit()
    db.refresh(counter)
    return {"count": counter.count_number, "message": "Count incrémenté avec succès"}


@app.post("/counts/", response_model=CountTableResponse, status_code=201)
def create_count(count: CountTableCreate, db: Session = Depends(get_db)):
    db_count = CountTable(**count.model_dump())
    db.add(db_count)
    db.commit()
    db.refresh(db_count)
    return db_count


@app.get("/counts/", response_model=List[CountTableResponse])
def read_counts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    counts = db.query(CountTable).offset(skip).limit(limit).all()
    return counts


@app.get("/counts/{count_id}", response_model=CountTableResponse)
def read_count(count_id: int, db: Session = Depends(get_db)):
    db_count = db.query(CountTable).filter(CountTable.id == count_id).first()
    if db_count is None:
        raise HTTPException(status_code=404, detail="Count not found")
    return db_count


@app.put("/counts/{count_id}", response_model=CountTableResponse)
def update_count(count_id: int, count: CountTableUpdate, db: Session = Depends(get_db)):
    db_count = db.query(CountTable).filter(CountTable.id == count_id).first()
    if db_count is None:
        raise HTTPException(status_code=404, detail="Count not found")

    update_data = count.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_count, key, value)

    db.commit()
    db.refresh(db_count)
    return db_count


@app.delete("/counts/{count_id}", status_code=204)
def delete_count(count_id: int, db: Session = Depends(get_db)):
    db_count = db.query(CountTable).filter(CountTable.id == count_id).first()
    if db_count is None:
        raise HTTPException(status_code=404, detail="Count not found")

    db.delete(db_count)
    db.commit()
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
