from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import Dict

main_keys = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Давай другое 🔄"), KeyboardButton(text="Добавить слово 📖")],
    [KeyboardButton(text="Удалить слово ❌")]],
    resize_keyboard=True, input_field_placeholder="Выберите вариант", is_persistent=True)

start_inline_keys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать учиться", callback_data="start_learn")],
    [InlineKeyboardButton(text="Статистика", callback_data="show_statistic")]
])

statistic_inline_keys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мой словарь", callback_data="show_vocabulary")],
    [InlineKeyboardButton(text="Прогресс обучения", callback_data="show_stat")]
])

answer_keys = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Прогресс обучения")], [KeyboardButton(text="Давай еще!")]],
    resize_keyboard=True, input_field_placeholder="Выберите вариант", is_persistent=True)


async def true_answer_keys():
    payload = ReplyKeyboardBuilder()
    payload.attach(ReplyKeyboardBuilder.from_markup(markup=answer_keys))
    payload.attach(ReplyKeyboardBuilder.from_markup(markup=main_keys))
    return payload.adjust(2).as_markup()


async def word_variants_builder(words: Dict.values):
    """
    Метод для создания динамического формирования кнопок клавиатуры во время тренировки
    :param words: список вариантов
    :return:
    """
    payload = ReplyKeyboardBuilder()
    for word in set(words):
        payload.add(KeyboardButton(text=word))
    payload.attach((ReplyKeyboardBuilder().from_markup(markup=main_keys)))
    return payload.adjust(2).as_markup()
