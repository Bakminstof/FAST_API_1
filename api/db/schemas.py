from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TEXT

from .database import Base


# table
class RecipesTable(Base):
    __tablename__ = 'recipes'

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    cooking_time = Column(SMALLINT(unsigned=True), nullable=False)
    ingredients = Column(VARCHAR(300), nullable=False)
    description = Column(TEXT)
    views = Column(INTEGER(unsigned=True), default=0)

    def __repr__(self) -> str:
        return '<id: {id}, ' \
               'name: {name}, ' \
               'cooking_time: {cooking_time}, ' \
               'ingredients: {ingredients}, ' \
               'description: {description}, ' \
               'views: {views}>'.format(
            id=self.id,
            name=self.name,
            cooking_time=self.cooking_time,
            ingredients=self.ingredients,
            description=self.description,
            views=self.views,
        )
