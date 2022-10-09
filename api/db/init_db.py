from os.path import isfile

from .generate_db import generate
from .database import engine_main, Base, a_session_main, DB_PATH


async def init_main_db() -> None:
    if not isfile(DB_PATH):
        async with engine_main.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

            save = generate()
            a_session_main.add_all(save)

            await a_session_main.commit()
            await engine_main.dispose()
