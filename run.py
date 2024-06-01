import logging
import asyncio
from bot.bot import start
from database.database import Database
from database.queries import Queries

if __name__ == "__main__":
    Database.create_tables()
    Queries.add_word("Белый", "White")
    Queries.add_word("Черный", "Black")
    Queries.add_word("Желтый", "Yellow")
    Queries.add_word("Красный", "Red")
    Queries.add_word("Синий", "Blue")
    Queries.add_word("Зеленый", "Green")
    Queries.add_word("Поезд", "Train")
    Queries.add_word("Машина", "Car")
    Queries.add_word("Самолет", "Plane")
    Queries.add_word("Велосипед", "Bike")
    Queries.add_word("Лодка", "Boat")

    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(start())

