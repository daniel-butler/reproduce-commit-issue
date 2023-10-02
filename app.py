import datetime
from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


# Database
class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class TableTwo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


DATABASE_URL = "sqlite+aiosqlite:///./test.db"
connect_args = {"check_same_thread": False}  # Required for SQLite
engine = create_async_engine(DATABASE_URL, echo=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


class Input(BaseModel):
    content: str


# API
app = FastAPI()
app.on_event("startup")(create_db_and_tables)


@app.post("/")
async def root(input: Input, db: AsyncSession = Depends(get_db)):
    print(f"Received: {input}")

    table_two = TableTwo(content="\n")
    db.add(table_two)
    await db.commit()
    await db.refresh(table_two)
    print(f"Created table two with id: {table_two.id}")

    entry = Entry(content=''.join(input.content))
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    print(f"Created entry with id: {entry.id}")

    table_two.content = input.content
    entry_id = entry.id   # <--- This makes it work
    await db.commit()
    return {
        "new_entry": {
            "id": entry.id,
        }
    }

