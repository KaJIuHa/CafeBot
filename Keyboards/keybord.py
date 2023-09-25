from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           KeyboardButton,
                           ReplyKeyboardMarkup
                           )

# Кнопки для первоначального выбора пользователя
choise_menu = InlineKeyboardButton('🍔 Меню',
                                   callback_data='menu')
kat_ph = InlineKeyboardButton('🌆 Фото',
                              callback_data='m_photo')
choise_table = InlineKeyboardButton('🍽️ Заказать столик',
                                    callback_data='get_table')
choise_admin = InlineKeyboardButton('❓ Связаться с нами или оставить отзыв',
                                    callback_data='get_admin')
choise_coocke = InlineKeyboardButton('💳 Оставить чаевые',
                                     url='https://netmonet.co/tip/group/430254?o=4')
choise_main = InlineKeyboardMarkup(row_width=3).row(
    choise_menu, kat_ph).add(
    choise_table).add(choise_admin).add(choise_coocke)

"""Конпки выбора категории меню"""
kat_1 = InlineKeyboardButton('💨 Кальян',
                             callback_data='m_hookah')
kat_2 = InlineKeyboardButton('🍝 Кухня',
                             callback_data='m_kitchen')
kat_3 = InlineKeyboardButton('🍹 Бар',
                             callback_data='m_bar')
kat_4 = InlineKeyboardButton('🔥 Акции',
                             callback_data='m_sale')
kat_b = InlineKeyboardButton('⬅ Вернуться в предыдущее меню',
                             callback_data='menu')
back_main = InlineKeyboardButton('🏠 Вернуться в главное меню',
                                 callback_data='main')
back_main_menu = InlineKeyboardMarkup().add(
    back_main)
choise_kat = InlineKeyboardMarkup().row(kat_1, kat_2, kat_3, kat_4).row(
    back_main)
"""Кнопки в подразделе отображения меню"""
back_menu = InlineKeyboardMarkup().add(
    kat_b).add(
    back_main)

# Кнопки для выбора в разделе FAQ
choise_admin = InlineKeyboardButton("Задать вопрос",
                                    callback_data="have_question")
choise_feedback = InlineKeyboardButton('Оставить отзыв',
                                       callback_data='get_feedback')
choise_call = InlineKeyboardButton('☎️ Позвонить Нам',
                                   callback_data='call')
choise_faq = InlineKeyboardMarkup().row(choise_feedback, choise_admin).add(
    choise_call).add(
    back_main)
back_in_faq = InlineKeyboardButton('⬅ Вернуться в предыдущее меню',
                                   callback_data='get_admin')
choise_back_in_fag = InlineKeyboardMarkup().add(
    back_in_faq).add(
    back_main)
# Кнопки заказа столика
in_kb_no = InlineKeyboardButton("⛔ Отмена",
                                callback_data="No")
in_kb_yes = InlineKeyboardButton("👌 Подтвердить",
                                 callback_data="Yes")
choise_2 = InlineKeyboardMarkup(row_width=2).row(in_kb_yes, in_kb_no)
"""Кнопка отмены"""
in_no_ad = InlineKeyboardButton('❌ Отмена',
                                callback_data='no')
no_add = InlineKeyboardMarkup().add(in_no_ad)
"""Кнопка добавление даты"""
in_date = InlineKeyboardButton('🕞 На сегодня',
                               callback_data='today')
in_date_another = InlineKeyboardButton('📅 Другой день',
                                       callback_data='another_day')
in_date_cl = InlineKeyboardMarkup().row(
    in_date, in_date_another).add(in_no_ad)
"""Кнопки в меню админа"""
in_1_ad = InlineKeyboardButton('Загрзить меню',
                               callback_data='add_menu')
in_2_ad = InlineKeyboardButton('Сделать массовую рассылку',
                               callback_data='spam')
in_admin = InlineKeyboardMarkup().add(in_1_ad).add(in_2_ad)

"""Конопки категорий для добавления меню"""
kat_1_ad = InlineKeyboardButton('💨 Кальян',
                                callback_data='hookah')
kat_2_ad = InlineKeyboardButton('🍝 Кухня',
                                callback_data='kitchen')
kat_3_ad = InlineKeyboardButton('🍹 Бар',
                                callback_data='bar')
kat_4_ad = InlineKeyboardButton('🔥 Акции',
                                callback_data='sale')
kat_ph_add = InlineKeyboardButton('🌆 Фото',
                                  callback_data='photo')
in_admin_cat = InlineKeyboardMarkup().row(
    kat_1_ad, kat_2_ad, kat_3_ad).add(kat_4_ad, kat_ph_add).add(in_no_ad)
"""Кнопка номера телефона"""
phone = KeyboardButton('📱 Телефон',
                       request_contact=True)
phone_contact = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True).add(phone)
"""Кнопка удалить из меню"""
del_1 = InlineKeyboardButton('❌ Удалить',
                             callback_data='delete_menu')
del_menu = InlineKeyboardMarkup().add(del_1)
"""Кнопки в информации"""
info_1 = InlineKeyboardButton('Наш ВК',
                              url='https://vk.com/club178848703')
info_2 = InlineKeyboardButton('Наш Instagram',
                              url='https://instagram.com/loft_ribatskoe?igshid=ZDdkNTZiNTM=')
info_kb = InlineKeyboardMarkup().row(info_1,
                                     info_2).add(back_main)
