from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Banco SQLite
DATABASE_URL = "sqlite:///ti.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
