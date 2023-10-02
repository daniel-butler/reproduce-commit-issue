import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app import app, get_db


DATABASE_URL = "sqlite+aiosqlite:///:memory:"
connect_args = {"check_same_thread": False}
engine = create_async_engine(DATABASE_URL, echo=True, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='session')
async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture()
async def async_client(init_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_insert_new_entry_that_starts_at_the_beginning_of_the_file(async_client: AsyncClient):
    response = await async_client.post("/", json={
        "content": 'Example content',
    }, headers={"content-type": "application/json"})

    # THEN the response is successful
    assert response.status_code == 200

