import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Keyboards.keybord import choise_main, \
    choise_kat, \
    choise_back_in_fag, \
    back_menu, \
    back_main_menu, \
    no_add, \
    phone_contact, \
    del_menu, \
    info_kb
from utils import utils_sale
from create_bot import bot, CHAT
from Database.database import db


class FSMClientRegister(StatesGroup):
    name = State()
    phone_number = State()
    confirm = State()


def validate_user_status(user_status):
    if user_status == "left":
        return False
    if user_status == "canceled":
        return False
    else:
        return True


async def command_start(message: types.Message):
    """Стартовая команда"""
    await message.answer('Добро пожаловать в Loft, здесь\n'
                         'вы можете посмотреть меню или забронировать столик\n'
                         'А также вы можете оставить отзыв или задать вопрос\n'
                         'Мы работаем для Вас с 14:00 до 2:00',
                         reply_markup=choise_main)


async def command_info(message: types.Message):
    await message.answer('Мы работаем для Вас ежедневнно\n'
                         'с 14:00 до 02:00\n'
                         '<a href="https://yandex.ru/navi/?whatshere%5Bpoint%5D=30.50191817985902%2C59.84026131145099&whatshere%5Bzoom%5D=18">'
                         'Наш адрес: СПб. пр.Рыбацкий 23 корпус 2</a>',
                         disable_web_page_preview=True,
                         reply_markup=info_kb)


async def main(callback: types.CallbackQuery):
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Добро пожаловать в Loft, здесь\n'
                                          'вы можете посмотреть меню или забронировать столик\n'
                                          'А также вы можете оставить отзыв или задать вопрос\n'
                                          'Мы работаем для Вас с 14:00 до 2:00',
                                     reply_markup=choise_main)


async def menu(callback: types.CallbackQuery):
    """Хендлер меню"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Пожалуйстя выберите категорию:',
                                     reply_markup=choise_kat)


async def show_card_menu(callback: types.CallbackQuery):
    """Получение карточек меню"""
    media = types.MediaGroup()
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=callback.from_user.id)
    print(user_status['status'])
    if validate_user_status(user_status['status']):
        for ret in db.show_menu(callback.data[2::1]):
            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=ret[0])
            await bot.send_message(callback.from_user.id,
                                   f'{ret[1]}.^^^^Удалить',
                                   reply_markup=del_menu)
    else:
        await callback.answer(cache_time=3)
        for ret in db.show_menu(callback.data[2::1]):
            # photo = []
            # photo.append(ret[0])
            media.attach_photo(ret[0])
        await types.ChatActions.upload_photo()  # Установка action "Отправка фотографии..."
        await asyncio.sleep(1)
        await bot.send_media_group(callback.from_user.id, media=media)  # Отправка фото
        # await bot.send_photo(chat_id=callback.from_user.id,
        #                      photo=ret[0])
        await bot.send_message(callback.from_user.id,
                               text='_________Наслаждайтесь________',
                               reply_markup=back_menu)


async def call(callback: types.CallbackQuery):
    """Хендлер Позвонить нам """
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Вы всегда можете позвонить нам по телефону:\n'
                                          '<b>+79217779913</b>',
                                     reply_markup=choise_back_in_fag)


async def start_register(message: types.Message):
    """Запуск регистрации и проврка пользователя"""
    if db.check_user(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               text=f'Ваша скидка: {utils_sale.sale_count(message.from_user.id)}%\n'
                                    f'{utils_sale.info_for_next(message.from_user.id)}',
                               reply_markup=back_main_menu)
    else:
        await FSMClientRegister.name.set()
        await bot.send_message(message.from_user.id, 'Пожалуйста укажите ваше имя',
                               reply_markup=no_add)


async def add_register_name(message: types.Message, state: FSMContext):
    """Ловим имя пользователя"""
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClientRegister.next()
    await bot.send_message(message.from_user.id,
                           'Отлично, теперь укажите номер телефона.\n'
                           'Просто нажмите кнопку внизу',
                           reply_markup=phone_contact)


async def add_phone_register(message: types.Message, state: FSMContext):
    """Ловим телефон и id """
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
        data['id'] = message.contact.user_id
        data['count'] = 0
    await db.add_user(state)
    await bot.send_message(message.from_user.id, 'Отлично теперь у Вас есть наша\n'
                                                 'Карта Лояльности',
                           reply_markup=back_main_menu)
    await state.finish()


async def check_in(message: types.Message):
    """Хендлер команды Чек-ИН"""
    if db.check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Отлично!!!!\n'
                                                     'Ожидайте подтверждения')
        await bot.send_message(chat_id=CHAT,
                               text=f'Клиент:{db.check_count(message.from_user.id)[1]}.\n'
                                    f'Посетил нас: {db.check_count(message.from_user.id)[0]}\n'
                                    f'Скидка: {utils_sale.sale_count(message.from_user.id)}%\n'
                                    f'хочет зачекиниться',
                               reply_markup=InlineKeyboardMarkup().
                               add(InlineKeyboardButton(
                                   '✔️ Подтвердить', callback_data=f'confirm{message.from_user.id}')))
    else:
        await bot.send_message(message.from_user.id,
                               'Сначала получи карту лояльности /card')


async def check_in_confirm(callback: types.CallbackQuery):
    """Подтверждение команды Чек-ИН"""
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(cache_time=3)
    db.add_chek_in(callback.data[7::1])
    await bot.send_message(chat_id=callback.data[7::1],
                           text='Ваше посещение подтверждено 🤙')


def register_message_client(dp: Dispatcher):
    """Регистрация хендлеров"""
    dp.register_message_handler(command_start,
                                commands=['start', 'help'])
    dp.register_message_handler(command_info,
                                commands=['info'])
    dp.register_callback_query_handler(main,
                                       text="main")
    dp.register_callback_query_handler(menu,
                                       text="menu")
    dp.register_callback_query_handler(call,
                                       text="call")
    dp.register_callback_query_handler(show_card_menu,
                                       Text(startswith='m_'))
    dp.register_message_handler(start_register,
                                commands=['card'])
    dp.register_message_handler(add_register_name,
                                state=FSMClientRegister.name)
    dp.register_message_handler(add_phone_register,
                                content_types=types.ContentType.CONTACT,
                                state=FSMClientRegister.phone_number)
    dp.register_message_handler(check_in,
                                commands=['check_in'])
    dp.register_callback_query_handler(check_in_confirm,
                                       Text(startswith='confirm'))
