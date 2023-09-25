from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from Keyboards.keybord import in_admin, in_admin_cat, choise_2, no_add
from create_bot import bot,CHAT
from Database.database import db
from Handlers.client import validate_user_status


class FSMAdmin(StatesGroup):
    take_cat = State()
    take_id = State()
    add_photo = State()
    add_cat = State()
    confirm = State()


class FSMSpam(StatesGroup):
    text = State()


async def add_admin(message: types.Message):
    """Команда вызова админ панели"""
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=message.from_user.id)
    if validate_user_status(user_status['status']):
        await bot.send_message(message.from_user.id,
                               "Опять работа((((\n"
                               "Выбери что делаем",
                               reply_markup=in_admin)
    else:
        await bot.send_message(message.from_user.id,
                               "Ты не админ, давай не балуйся😎")


# Запуск машины
async def add_cart_start(callback: types.CallbackQuery):
    """Добавляем товар"""
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=callback.from_user.id)
    if validate_user_status(user_status['status']):
        await FSMAdmin.add_photo.set()
        await bot.send_message(callback.from_user.id, 'Загрузи фото')


async def add_photo(message: types.Message, state: FSMContext):
    """Добавляем фото товара"""
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=message.from_user.id)
    if validate_user_status(user_status['status']):
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await bot.send_message(message.from_user.id,
                               "Выбери категорию",
                               reply_markup=in_admin_cat)


async def add_category(callback_query: types.CallbackQuery, state: FSMContext):
    """Добавялем категорию"""
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=callback_query.from_user.id)
    if validate_user_status(user_status['status']):
        async with state.proxy() as data:
            data['category'] = callback_query.data
        await FSMAdmin.next()
        await bot.send_message(callback_query.from_user.id,
                               "Жми 👌 Подтвердить чтобы запиcать\n"
                               "или ⛔ Отмена ",
                               reply_markup=choise_2)


async def add_menu_finish(callback_query: types.CallbackQuery, state: FSMContext):
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=callback_query.from_user.id)
    if validate_user_status(user_status['status']):
        if callback_query.data == "Yes":
            await db.add_menu(state)
            await bot.send_message(callback_query.from_user.id,
                                   "Добавил")
            await callback_query.answer(cache_time=3)
    elif callback_query.data == "No":
        await bot.send_message(callback_query.from_user.id,
                               "Отменил")
        await callback_query.answer(cache_time=3)

    await state.finish()


async def spam_start(callback_query: types.CallbackQuery):
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=callback_query.from_user.id)
    if validate_user_status(user_status['status']):
        await bot.send_message(callback_query.from_user.id,
                               'Введите текст рассылки или фото для рассылки',
                               reply_markup=no_add)
        await FSMSpam.text.set()
        await callback_query.answer(cache_time=3)


async def spam_finish(message: types.Message, state: FSMContext):
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=message.from_user.id)
    if validate_user_status(user_status['status']):
        if message.content_type == 'photo':
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            for ret in db.spam():
                try:
                    await bot.send_photo(chat_id=ret[0],
                                         photo=data['photo'])
                except Exception as e:
                    print(e)
                    continue
        if message.content_type == 'text':
            async with state.proxy() as data:
                data['text'] = message.text
            for ret in db.spam():
                try:
                    await bot.send_message(chat_id=ret[0],
                                           text=data['text'])
                except Exception as e:
                    print(e)
                    continue
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'Рассылка успешно завершина')


async def del_from_menu(callback: types.CallbackQuery):
    """Хендлер удаления из базы карточки меню"""
    item: str = callback.message.text.split('.')[0]
    print(item)
    await db.del_from_menu(item)
    await callback.answer(cache_time=3,
                          text='Успешно удалено',
                          show_alert=True)


def register_message_admin(dp: Dispatcher):
    dp.register_message_handler(add_admin,
                                commands=['admin'])
    dp.register_callback_query_handler(add_cart_start,
                                       text='add_menu')
    dp.register_message_handler(add_photo,
                                content_types=['photo'],
                                state=FSMAdmin.add_photo)
    dp.register_callback_query_handler(add_category,
                                       state=FSMAdmin.add_cat)
    dp.register_callback_query_handler(add_menu_finish,
                                       state=FSMAdmin.confirm)
    dp.register_callback_query_handler(spam_start,
                                       text='spam')
    dp.register_message_handler(spam_finish,
                                content_types=['photo', 'text'],
                                state=FSMSpam.text)
    dp.register_callback_query_handler(del_from_menu,
                                       text='delete_menu')
