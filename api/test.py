import asyncio
import datetime

from sqlalchemy import select, desc
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from db import DB_PATH, RecipesTable
from api_wsgi import app
from utils.sort import sort

client = TestClient(app)


class DB:
    def __init__(self):
        self.path = DB_PATH
        self.session: AsyncSession | None = None
        self.__connect_db()

    def __connect_db(self):
        engine_main = create_async_engine('sqlite+aiosqlite:///{db}'.format(db=self.path))

        async_session = sessionmaker(
            bind=engine_main,
            expire_on_commit=False,
            class_=AsyncSession
        )

        self.session = async_session()

    async def get_all_recipes(self) -> dict[str, dict[str, list[dict[str, str | int]]]]:
        stmt = select(RecipesTable).order_by(desc(RecipesTable.views))
        res = await self.session.execute(stmt)
        rows = res.all()

        items = sort(rows)

        result = {'data': {'result': [item for item in items]}}

        return result

    async def get_one_recipe(self, idx: int) -> dict[str, dict[str, list[dict[str, str | int]]]]:
        stmt = select(
            RecipesTable.ingredients,
            RecipesTable.name,
            RecipesTable.cooking_time,
            RecipesTable.description,
            RecipesTable.id,
        ).filter(RecipesTable.id == idx)

        db_res = await self.session.execute(stmt)
        row = db_res.one_or_none()

        result = {
            'data': {
                'result': [
                    {
                        **row
                    }
                ]
            }
        }

        return result


db = DB()


def test_valid__recipes():
    url = "/recipes"

    data = asyncio.run(db.get_all_recipes())

    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == data


def test_invalid__zero_recipes():
    # need clear table `recipes` in db and uncomment lines 108 - 109
    url = "/recipes"

    type_ = 'NotFoundError'
    title_ = 'Not found'
    detail_ = f'Recipes not found'
    status_ = 404
    instance_ = '/recipes'

    exc = {
        'type': type_,
        'title': title_,
        'status': status_,
        'detail': detail_,
        'instance': instance_,
        'timestamp': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    }

    error = {
        'error': exc
    }

    response = client.get(url)

    # assert response.status_code == status_
    # assert response.json() == error


def test_valid__recipes_with_id():
    # In order to pass this test, you need to comment out lines 48-49 in 1routes.py`.
    # To avoid trying to make changes to the database

    idx = 1

    url = f"/recipes/{idx}"

    data = asyncio.run(db.get_one_recipe(idx))

    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == data


def test_invalid__string_idx():
    msg = {
        "detail":
            [
                {
                    "loc": [
                        "path",
                        "idx"
                    ],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer"
                }
            ]
    }

    url = "/recipes/some_string"

    response = client.get(url)

    assert response.status_code == 422
    assert response.json() == msg


def test_invalid__not_found_idx():
    idx = 100000

    url = f"/recipes/{idx}"

    type_ = 'NotFoundError'
    title_ = 'Not found'
    detail_ = f'Recipe with id=`{idx}` not found'
    status_ = 404
    instance_ = f'/recipes/{idx}'

    exc = {
        'type': type_,
        'title': title_,
        'status': status_,
        'detail': detail_,
        'instance': instance_,
        'timestamp': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    }

    error = {
        'error': exc
    }

    response = client.get(url)

    assert response.status_code == 404
    assert response.json() == error
