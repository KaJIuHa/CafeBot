from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from aiogram.dispatcher.filters import Text

from create_bot import bot, CHAT

from Keyboards.keybord import choise_faq, back_main, no_add,in_date_cl,choise_2


class FSMfag(StatesGroup):
    title = State()
    date = State()
    persons = State()
    time = State()
    finish = State()


async def get_admin(callback: types.CallbackQuery):
    """Обработка раздела FAQ"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Вы в разделе вопросов, выберите что хотите сделать\n'
                                          'Чтобы вернуться в главное меню /start',
                                     reply_markup=choise_faq)


async def question(callback: types.CallbackQuery):
    """Нажата кнопка (Задать вопрос)"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text="Спасибо за обращение, сейчас с вами свяжится Администратор ресторана",
                                     reply_markup=InlineKeyboardMarkup().add(back_main))
    await bot.send_message(
        chat_id=CHAT,
        text=f'Клиент {callback.from_user.first_name},'
             f' хочет связаться с Администратором\n',
        reply_markup=InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True).add(
            InlineKeyboardButton('❗ Связаться',
                                 url=f'https://t.me/{callback.from_user.username}')))


# Нажата кнопка (отсавить отзыв)-> Запуск FSM для отзыва
async def feedback(callback: types.CallbackQuery):
    """Нажата кнопка (отсавить отзыв)-> Запуск FSM для отзыва"""
    await FSMfag.title.set()
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text="Напишите Ваш отзыв", reply_markup=no_add)


async def feedback_finish(message: types.Message, state: FSMContext):
    """Обрабатываем отзыв клиента и добавляем в БД"""
    async with state.proxy() as data:
        data['tg_user_id'] = message.from_user.id
        data['user_name'] = message.from_user.username
        data['description'] = message.text
    await bot.send_message(
        chat_id=CHAT,
        text=f'Клиент {message.from_user.first_name} оставил отзыв\n'
             f'{message.text}',
        reply_markup=InlineKeyboardMarkup(
            row_width=2).add(
            InlineKeyboardButton('❗ Связаться',
                                 url=f'https://t.me/{message.from_user.username}'
                                 )))

    await state.finish()
    await bot.send_message(message.from_user.id,
                           'Спасибо за Ваш отзыв, я его уже передал Администраторам',
                           reply_markup=InlineKeyboardMarkup().add(back_main))


# async def get_table_new(callback: types.CallbackQuery):
#     await callback.answer(cache_time=3)
#     await callback.message.edit_text(text="Чтобы забранировать столик напишите нам,нажав кнопку внизу",
#                                      reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('❗ Связаться',
#                                                                                                   url=f'https://t.me/Loft_ryb'
#                                                                                                   )).add(back_main))


# Раздел заказа столика
async def get_table_start(callback: types.CallbackQuery):
    """Выбор даты"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text="Выберите когда нас хотите посетить:", reply_markup=in_date_cl)


async def another_date(callback: types.CallbackQuery):
    """Хендлер запуска после выбора другой даты """
    await callback.answer(cache_time=3)
    await FSMfag.date.set()
    await callback.message.edit_text(text="Укажите дату в формате ДД.ММ.ГГГГ", reply_markup=no_add)


async def get_date(message: types.Message, state: FSMContext):
    """Ловим дату от пользователя"""
    await FSMfag.date.set()
    try:
        datetime.strptime(message.text, "%d.%m.%Y")
        async with state.proxy() as data:
            data['date'] = message.text
        await FSMfag.next()
        await bot.send_message(message.from_user.id, 'Укажите сколько будет человек',
                               reply_markup=no_add)
    except ValueError:
        await bot.send_message(message.from_user.id,
                               '🤔 По-моему что-то не то, укажите снова', reply_markup=no_add)


async def get_date_cb(callback: types.CallbackQuery, state: FSMContext):
    """Нажата кнопка сегодня"""
    await FSMfag.date.set()
    async with state.proxy() as data:
        data['date'] = 'сегодня'
    await callback.answer(cache_time=3)
    await FSMfag.next()
    await callback.message.edit_text(text='Укажите сколько будет человек', reply_markup=no_add)


async def table_per(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['persons'] = message.text
        await FSMfag.next()
        await bot.send_message(message.from_user.id,
                               '⏰Пожалуйста укажите время в формате ЧЧ:ММ',
                               reply_markup=no_add)

    else:
        await bot.send_message(message.from_user.id,
                               '🤔 По-моему что-то не то, укажите снова',
                               reply_markup=no_add)


async def get_time(message: types.Message, state: FSMContext):
    """Получает время от пользователя"""
    if message.text[2] == ':':
        if message.text.replace(":", "").isdigit():
            async with state.proxy() as data:
                data['time'] = message.text
            await FSMfag.next()
            await bot.send_message(message.from_user.id,
                                   "Жми 👌 Подтвердить, чтобы забронировать \n"
                                   "или ⛔ Отмена, чтобы отменить бронирование",
                                   reply_markup=choise_2)
        else:
            await bot.send_message(message.from_user.id,
                                   '🤔 По-моему что-то не то, укажите снова',
                                   reply_markup=no_add)
    else:
        await bot.send_message(message.from_user.id,
                               '🤔 По-моему что-то не то, укажите снова',
                               reply_markup=no_add)


async def table_finish(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждает заказ"""
    if callback.data == "Yes":
        async with state.proxy() as data:
            data['name'] = callback.from_user.first_name
            data['user'] = callback.from_user.id

        await bot.send_message(
            chat_id=CHAT,
            text=f"Клиент {data['name']} заказал столик на "
                 f"{data['persons']} человек\n"
                 f"на {data['date']} к {data['time']}\n"
                 f"Ссылка для связи: @{callback.from_user.username}",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    '❗ Связаться',
                    url=f'https://t.me/{callback.from_user.username}'
                )).add(
                InlineKeyboardButton(
                    '✔️ Подтвердить',
                    callback_data=f'answer{data["user"]}')))
        await bot.send_message(callback.from_user.id,
                               'Отправил вашу бронь Администратору\n'
                               'Ожидайте сообщение с подтверждением',
                               reply_markup=InlineKeyboardMarkup().add(back_main)
                               )

        await state.finish()
    elif callback.data == "No":
        await bot.send_message(callback.from_user.id,
                               "Отменил",
                               reply_markup=InlineKeyboardMarkup().add(back_main))
    await state.finish()
    await bot.answer_callback_query(callback.id)


async def confirm_table(callback: types.CallbackQuery):
    chat = callback.data[6::1]
    await bot.send_message(chat_id=chat,
                           text='Ваш заказ подтвержден. Будем ждать Вас в Loft',
                           reply_markup=InlineKeyboardMarkup().add(
                               back_main))
    await callback.message.edit_reply_markup(reply_markup=None)


async def cancel(callback: types.CallbackQuery, state: FSMContext):
    """Отмена действий"""
    await state.finish()
    await callback.answer(cache_time=3, show_alert=True, text='Отменено')
    await callback.message.edit_text(text='Чтобы вернуться в главное меню нажмите на кнопку',
                                     reply_markup=InlineKeyboardMarkup().add(
                                         back_main))


# Регистрация хендлеров
def register_message_other(dp: Dispatcher):
    dp.register_callback_query_handler(get_admin,
                                       text='get_admin')
    dp.register_callback_query_handler(question,
                                       text="have_question")
    dp.register_callback_query_handler(feedback,
                                       text='get_feedback',
                                       state=None)
    dp.register_message_handler(feedback_finish,
                                state=FSMfag.title)
    # dp.register_callback_query_handler(get_table_new, text='get_table')
    dp.register_callback_query_handler(get_table_start,
                                       text='get_table',
                                       state=None)
    dp.register_callback_query_handler(another_date,
                                       text='another_day',
                                       state=None)
    dp.register_callback_query_handler(get_date_cb,
                                       text='today',
                                       state='*')
    dp.register_message_handler(get_date,
                                state=FSMfag.date)
    dp.register_message_handler(table_per,
                                state=FSMfag.persons)
    dp.register_message_handler(get_time,
                                state=FSMfag.time)
    dp.register_callback_query_handler(table_finish,
                                       state=FSMfag.finish)
    dp.register_callback_query_handler(cancel,
                                       text='no',
                                       state="*")
    dp.register_callback_query_handler(confirm_table,
                                       Text(startswith='answer'))
