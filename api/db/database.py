from pathlib import Path
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DB_NAME = 'cook.db'
DB_PATH = Path(__file__).parent / 'main_db' / DB_NAME

Base = declarative_base()

engine_main = create_async_engine('sqlite+aiosqlite:///{db}'.format(db=DB_PATH))

async_session = sessionmaker(
    bind=engine_main,
    expire_on_commit=False,
    class_=AsyncSession
)

a_session_main = async_session()
