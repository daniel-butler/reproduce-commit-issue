import datetime
from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field
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
async def root(inpt: Input, db: AsyncSession = Depends(get_db)):
    entry = Entry(content=inpt.content)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    print(f"Created entry with id: {entry.id}")  # Can access the id here!

    table_two = TableTwo(content="")
    db.add(table_two)
    entry_id = entry.id   # <--- Using this variable in the response will avoid the error
    await db.commit()
    return {"id": entry.id}
