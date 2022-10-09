from typing import List, Union

from pydantic import BaseModel
from pydantic.fields import Field


class RecipeIn(BaseModel):
    id: int = Field(
        ...,
        title='Recipe\'s ID',
    )

    name: str = Field(
        ...,
        title='Recipe\'s name',
        min_length=1,
        max_length=50
    )
    cooking_time: int = Field(
        ...,
        title='Cooking time min.',
        ge=1,
        le=1000
    )
    ingredients: str = Field(
        ...,
        title='List of ingredients',
        min_length=1,
        max_length=300
    )
    description: str = Field(
        None,
        title='Recipe\'s description'
    )
    views: int = Field(
        0,
        title='Views count'
    )

    class Config:
        orm_mode = True


class RecipeOut(BaseModel):
    id: int
    name: str
    cooking_time: int
    views: int

    class Config:
        orm_mode = True


class RecipeDetailOut(BaseModel):
    id: int
    name: str
    cooking_time: int
    ingredients: str
    description: str | None

    class Config:
        orm_mode = True


class ResultsModel(BaseModel):
    result: List[RecipeOut | RecipeDetailOut]

    class Config:
        orm_mode = True


class DumpModel(BaseModel):
    data: ResultsModel
    meta: dict | str | None = None

    class Config:
        orm_mode = True


# class for dumping any obj
class DumpObj:
    def __init__(self, **atr):
        for key, val in atr.items():
            self.__setattr__(key, val)

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)

    def __repr__(self):
        return "{name_cls}({args})".format(
            name_cls=self.__class__.__name__,
            args=', '.join(
                [
                    "{k}={v}".format(
                        k=k, v=v if type(v) is not str else f"'{v}'"
                    )
                    for k, v in self.__dict__.items()
                ]
            )
        )

    def __str__(self):
        return self.__repr__()
