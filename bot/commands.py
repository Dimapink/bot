"""
Модуль содержащий все доступные боту команды
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import bot.keyboards as keys
from bot.logic import prepare_questions
from database.queries import Queries
from bot.states import AddWordStates, DeleteWord, WordGame
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import random

router = Router()


@router.message(CommandStart())
async def cmd_start(massage: Message):
    user_id = massage.from_user.id
    first_name = massage.from_user.first_name
    last_name = massage.from_user.last_name
    Queries.add_user(user_id, first_name, last_name)
    await massage.answer(f"Привет *{first_name}* 👋 Давай попрактикуемся в английском языке\\. "
                         f"Тренировки можешь проходить в удобном для себя темпе\\."
                         f"У тебя есть возможность использовать тренажёр, как конструктор\\, "
                         f"и собирать свою собственную базу для обучения\\. "
                         f"Для этого воспрользуйся инструментами\\:\\!",
                         reply_markup=keys.start_inline_keys,
                         parse_mode=ParseMode.MARKDOWN_V2,
                         disable_notification=True)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Тут help", disable_notification=True)


@router.message(F.text == "Добавить слово 📖")
@router.message(Command("add", prefix='!'))
async def cmd_add_word(message: Message, state: FSMContext):
    await state.set_state(AddWordStates.ru)
    await message.answer("Напиши слово на русском", disable_notification=True)


@router.message(F.text == "Удалить слово ❌")
async def cmd_delete_word(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DeleteWord.asked)
    await message.answer("Напиши слово которое хотите удалить", disable_notification=True)


@router.message(DeleteWord.asked)
async def cmd_answer(message: Message, state: FSMContext):
    user_id = message.from_user.id
    word = message.text
    result = Queries.delete_word(user_id, word)
    await state.clear()
    if result == 1:
        await message.answer(f"Слово {word} удалено из вашего словаря",
                             reply_markup=keys.start_inline_keys,
                             disable_notification=True)
    else:
        await message.answer(f"Слова {word} нет в вашем словаре, удалить общие слова нельзя",
                             reply_markup=keys.start_inline_keys,
                             disable_notification=True)


@router.message(AddWordStates.ru)
async def cmd_add_word_ru(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id, ru=message.text)
    await state.set_state(AddWordStates.en)
    await message.answer("Напиши слово на английском", disable_notification=True)


@router.message(AddWordStates.en)
async def cmd_add_word_en(message: Message, state: FSMContext):
    await state.update_data(en=message.text)
    data = await state.get_data()
    Queries.add_word(ru=data.get("ru"), en=data.get("en"), user=data.get("user_id"))
    await message.answer(f"Слово добавлено 🇷🇺{data.get('ru')} - 🇺🇸{data.get('en')}",
                         reply_markup=keys.start_inline_keys,
                         disable_notification=True)
    await state.clear()


@router.message(F.text == "Давай еще!")
@router.message(F.text == "Давай другое 🔄")
@router.callback_query(F.data == "start_learn")
async def cmd_start_learn(callback: CallbackQuery | Message, state: FSMContext):
    user_id = callback.from_user.id

    await state.set_state(WordGame.asked)
    question = prepare_questions(Queries.get_word_variants(user_id))
    target = random.choice(list(question.keys()))
    await state.set_data({"q": question, "t": target})
    await callback.answer("Думаю...", disable_notification=True)
    if isinstance(callback, CallbackQuery):
        Queries.add_lesson(user_id)
        await callback.message.answer(f"Как переводится слово: {target} ",
                                      reply_markup=await keys.word_variants_builder(
                                          question.values()), disable_notification=True)
    else:
        await callback.answer(f"Как переводится слово: {target} ",
                              reply_markup=await keys.word_variants_builder(
                                  question.values()), disable_notification=True)


@router.message(WordGame.asked)
async def cmd_answer(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    question = data.get("q")
    target = data.get("t")
    answer = question.get(target)

    if message.text == answer:
        await message.answer(f"Правильно\\! Слово *{answer}* означает *{target}*",
                             parse_mode=ParseMode.MARKDOWN_V2, reply_markup=await keys.true_answer_keys(),
                             disable_notification=True)
        Queries.add_right(user_id)
        await state.clear()
    else:
        for word, translate in question.items():
            if translate == message.text:
                question[word] = "⛔️ " + translate
        await message.answer(f"Пока неправильно, попробуйте еще раз",
                             parse_mode=ParseMode.MARKDOWN_V2,
                             reply_markup=await keys.word_variants_builder(question.values()),
                             disable_notification=True)
        Queries.add_wrong(user_id)


@router.callback_query(F.data == "show_statistic")
async def cmd_show_status(callback: CallbackQuery | Message):
    await callback.message.answer(text="Могу рассказать", reply_markup=keys.statistic_inline_keys,
                                  disable_notification=True)


@router.message(F.text == "Прогресс обучения")
@router.callback_query(F.data == "show_stat")
async def cmd_show_stat(callback: CallbackQuery | Message):
    user_id = callback.from_user.id
    stat = Queries.show_stat(user_id)
    if isinstance(callback, CallbackQuery):
        await callback.message.answer(text=f"Всего уроков начато: {stat.total_lessons}\n"
                                           f"Правильных ответов: {stat.right_answer}\n"
                                           f"Неправильных ответов: {stat.wrong_answer}",
                                      reply_markup=keys.start_inline_keys,
                                      disable_notification=True)
    else:
        await callback.answer(text=f"Всего уроков начато: {stat.total_lessons}\n"
                                   f"Правильных ответов: {stat.right_answer}\n"
                                   f"Неправильных ответов: {stat.wrong_answer}",
                              reply_markup=keys.start_inline_keys,
                              disable_notification=True)


@router.callback_query(F.data == "show_vocabulary")
async def cmd_show_vocabulary(callback: CallbackQuery):
    user_id = callback.from_user.id
    vocabulary = Queries.show_vocabulary(user_id)
    if vocabulary:
        await callback.message.answer(text="\n".join(vocabulary), reply_markup=keys.start_inline_keys,
                                      disable_notification=True)
    else:
        await callback.message.answer(text="Ваш личный словарь пока пуст", reply_markup=keys.start_inline_keys,
                                      disable_notification=True)
