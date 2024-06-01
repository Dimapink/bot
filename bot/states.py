from aiogram.fsm.state import StatesGroup, State


class AddWordStates(StatesGroup):
    user_id = State()
    ru = State()
    en = State()


class DeleteWord(StatesGroup):
    asked = State()


class WordGame(StatesGroup):
    asked = State()
    right = State()
    wrong = State()
    q = State()
    target = State()


