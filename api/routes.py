from typing import List
from sqlalchemy import select, desc, update

from db import RecipesTable, a_session_main, engine_main, init_main_db
from loader import app, settings
from utils.sort import sort
from schemas.api_models import RecipeOut, DumpModel, ResultsModel, DumpObj, RecipeDetailOut
from handlers.exceptions import APIException


@app.on_event('startup')
async def _startup():
    await init_main_db()


@app.on_event('shutdown')
async def _shutdown():
    await a_session_main.close()
    await engine_main.dispose()


@app.get('/recipes', response_model=DumpModel, response_model_exclude_unset=True)
@app.get('/recipes/{idx}', response_model=DumpModel, response_model_exclude_unset=True)
async def recipes(idx: int | None = None) -> DumpObj | List[DumpObj]:
    if idx:
        stmt = select(
            RecipesTable.ingredients,
            RecipesTable.name,
            RecipesTable.cooking_time,
            RecipesTable.description,
            RecipesTable.id,
            RecipesTable.views
        ).filter(RecipesTable.id == idx)

        db_res = await a_session_main.execute(stmt)
        row = db_res.one_or_none()

        if row:
            id_ = row.id
            views_ = row.views + 1

            update_stmt = update(RecipesTable).filter(RecipesTable.id == id_).values(views=views_)

            recipe = RecipeDetailOut(**row)
            result = ResultsModel(result=[recipe])
            dump = DumpObj(data=result)

            await a_session_main.execute(update_stmt)
            await a_session_main.commit()

            return dump

        else:
            type_ = 'NotFoundError'
            title_ = 'Not found'
            detail_ = f'Recipe with id=`{idx}` not found'
            status_ = 404
            instance_ = f'/recipes/{idx}'

            raise APIException(
                type_=type_,
                title_=title_,
                status_=status_,
                detail_=detail_,
                instance_=instance_,
            )

    else:
        stmt = select(RecipesTable).order_by(desc(RecipesTable.views))
        res = await a_session_main.execute(stmt)
        rows = res.all()

        items = sort(rows)

        if items:
            recipes_ = [
                RecipeOut(
                    **item
                ) for item in items
            ]

            result = ResultsModel(result=recipes_)
            dump = DumpObj(data=result)

            return dump
        else:
            type_ = 'NotFoundError'
            title_ = 'Not found'
            detail_ = f'Recipes not found'
            status_ = 404
            instance_ = '/recipes'

            raise APIException(
                type_=type_,
                title_=title_,
                status_=status_,
                detail_=detail_,
                instance_=instance_,
            )


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
    }
