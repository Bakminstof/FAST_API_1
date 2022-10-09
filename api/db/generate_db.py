import random
import string

from .schemas import RecipesTable


def generate() -> list:
    data = []

    for _ in range(random.randint(20, 30)):
        views = random.randint(0, 50)
        cooking_time = random.randint(10, 500)

        name = __gen_word()

        description = ' '.join([__gen_word() for _ in range(random.randint(1, 6))]) \
            if random.choice((True, False)) \
            else None
        ingredients = ' '.join([__gen_word() for _ in range(random.randint(1, 4))])

        inst = RecipesTable(
            name=name,
            cooking_time=cooking_time,
            ingredients=ingredients,
            description=description,
            views=views,
        )

        data.append(inst)

    return data


def __gen_word() -> str:
    word = ''

    for _ in range(random.randint(4, 12)):
        letter = random.choice(string.ascii_letters)
        word += letter

    return word
