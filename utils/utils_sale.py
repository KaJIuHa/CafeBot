from Database.database import db


def sale_count(tg_id):
    count = db.check_count(tg_id)[0]
    if count < 5:
        return 0
    elif 5 <= count <= 15:
        return 5
    elif 15 <= count <= 30:
        return 7
    elif count >= 30:
        return 10


def info_for_next(tg_id):
    count = db.check_count(tg_id)[0]
    if count < 5:
        return f'До скидки в 5% вам осталось {5 - count} посещений'
    elif 5 <= count <= 15:
        return f'До скидки в 7% вам осталось {15 - count} посещений'
    elif 15< count < 30:
        return f'До скидки в 10% вам осталось {30 - count} посещений'
    else:
        return 'У Вас максимальная скидка в 10%'


