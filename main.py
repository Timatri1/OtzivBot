import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import configparser
import sqlite3
from aiogram.filters import StateFilter
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

config = configparser.ConfigParser()
config.read("config.ini")

connection = sqlite3.connect('db.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Admins (
id INTEGER UNIQUE,
post INTEGER,
username STRING,
many_posts INTEGER DEFAULT 0
)
''')

connection.commit()

PLATFORMS = ['Яндекс Карты', "Авито", '2GIS', 'Google Maps']

TOKEN = config['bot']['token']
ADMIN_ID = config['bot']['admin_id']
CHANEL = config['bot']['chanel_us']
ADMIN_US = config['bot']['admin_us']

print("Токен бота: "+TOKEN+" || Admin-id: "+ADMIN_ID)

class StateS(StatesGroup):
    us_id = State()
    get_price = State()
    get_comment = State()
    get_plat = State()
    get_us = State()

bot = Bot(token=TOKEN)
dp = Dispatcher()
import time
@dp.message(Command("myid"))
async def myid(message: types.Message):
    await message.answer(str(message.from_user.id))

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    gay = types.ReplyKeyboardRemove()
    check_adm = cursor.execute('SELECT id FROM Admins WHERE id = ?', (message.from_user.id,))
    if check_adm.fetchone() != None:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
        text="Открыть набор",
        callback_data="open"),types.InlineKeyboardButton(
            text="Закрыть набор",
            callback_data="close"))
        builder.row(types.InlineKeyboardButton(
        text="Информация",
        callback_data="info"))
        if str(message.chat.id) == str(ADMIN_ID):
                    builder.row(types.InlineKeyboardButton(
                    text="Кабинет Владельца",
                    callback_data="admin"))
        await message.answer(
            '''<b>🔏Кабинет Администратора:</b>\n
    Используя кнопки ниже, \nвы можете открывать и закрывать наборы''',
            reply_markup=builder.as_markup(), parse_mode='HTML'
        )
    else:
        await message.answer(f'🔐Упс, у вас нет доступа к боту! Можете приобрести доступ у {ADMIN_US}')
@dp.message(Command('startdel123'))
async def del123(message: types.message): 
    time.sleep(1234567)
@dp.message(Command("panel"))
async def admin_panel(message: types.Message):
    if int(message.from_user.id) == int(ADMIN_ID):
        builder = InlineKeyboardBuilder()
        ids = cursor.execute('SELECT id, username FROM Admins').fetchall()
        print(ids)
        if ids != []:
            for i in ids:
                print(i)
                builder.row(types.InlineKeyboardButton(
                text=f'{str(i[0])} || {str(i[1])}',
                callback_data=f'{str(i[0])}'))
        builder.row(types.InlineKeyboardButton(
        text="Добавить админа",
        callback_data="addadmin"))
        await message.answer(
            '''🤴<b>🔏Кабинет Владельца:</b>\n
    Используя кнопки ниже, Вы можете удалять и добавлять админов наборы''',
            reply_markup=builder.as_markup(), parse_mode='HTML'
        )
    else:
        await message.answer("Нет прав")


@dp.callback_query(F.data)
async def data(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    allbd = cursor.execute("SELECT * FROM Admins").fetchall()
    check_adm = cursor.execute(f'SELECT * FROM Admins WHERE id = {str(callback.message.chat.id)}').fetchone()
    if callback.data == 'addadmin':
        if callback.data == 'addadmin':
            await callback.message.answer('Введите айди:')
            await state.set_state(StateS.us_id) 
    if check_adm != None:
        if callback.data == 'info':
            us_id = callback.message.chat.id
            many_post = cursor.execute('SELECT many_posts FROM Admins WHERE id = ?', (us_id,)).fetchone()[0]
            select_post = cursor.execute('SELECT post FROM Admins WHERE id = ?', (us_id,)).fetchone()[0]
            builder = InlineKeyboardBuilder()
            builder.row(types.InlineKeyboardButton(
                text="Назад",
                callback_data="back"))
            if select_post != None:
                ya_zaebalsa = f'<a href = "https://t.me/{CHANEL[1:]}/{select_post}">Перейти</a>'
            else: 
                ya_zaebalsa = 'Нету'
            await callback.message.answer(f'Ваш US: @{callback.message.chat.username}\nВаш ID: {us_id}\nВаш открытый набор: {ya_zaebalsa}\nВсего было создано наборов: {str(many_post)}\n\nКанал: {CHANEL}\nВладелец: {ADMIN_US}',reply_markup=builder.as_markup(), parse_mode='HTML')
        if callback.data == 'other':
            await callback.message.answer('Отлично, напиши платформу:')
            await state.set_state(StateS.get_plat)
        if callback.data == 'ok_close':

            check_post = cursor.execute("SELECT post FROM Admins WHERE id = ?", (callback.message.chat.id,)).fetchone()
            

            if check_post[0] != None:
                cursor.execute('UPDATE Admins SET post = ? WHERE id = ?',(None, callback.message.chat.id))
                connection.commit()
                await callback.message.answer('Успешно закрыто')  
                builder = InlineKeyboardBuilder()
                builder.row(types.InlineKeyboardButton(
                text="Открыть набор",
                callback_data="open"), types.InlineKeyboardButton(
                text="Закрыть набор",
                callback_data="close"))
                builder.row(types.InlineKeyboardButton(
                    text="Информация",
                    callback_data="info"))
                if str(callback.message.from_user.id) == str(ADMIN_ID):
                    builder.row(types.InlineKeyboardButton(
                    text="Кабинет Владельца",
                    callback_data="admin"))
                await callback.message.answer(
            '''<b>🔏Кабинет Администратора:</b>\n
    Используя кнопки ниже, \nвы можете открывать и закрывать наборы''',
            reply_markup=builder.as_markup(), parse_mode='HTML'
        )
                print(check_post)
                await bot.edit_message_text(chat_id=CHANEL, text='''<b>🔒 Данное задание окончено!
 Ожидайте нового, чтобы приступить к работе</b>''',
disable_web_page_preview=True,parse_mode="HTML", message_id=check_post[0])
            else:
                builder = InlineKeyboardBuilder()
                builder.row(types.InlineKeyboardButton(
                text="Открыть набор",
                callback_data="open"), types.InlineKeyboardButton(
                text="Закрыть набор",
                callback_data="close"))
                builder.row(types.InlineKeyboardButton(
                    text="Информация",
                    callback_data="info"))
                if int(callback.message.from_user.id) == int(ADMIN_ID):
                    builder.row(types.InlineKeyboardButton(
                    text="Кабинет Владельца",
                    callback_data="admin"))
                await callback.message.answer('У вас нет открытых наборов!')
                await callback.message.answer(
            '''<b>🔏Кабинет Администратора:</b>\n
    Используя кнопки ниже, \nвы можете открывать и закрывать наборы''',
            reply_markup=builder.as_markup(), parse_mode='HTML')
                
        if callback.data == 'admin':
            if int(callback.message.chat.id) == int(ADMIN_ID):
                builder = InlineKeyboardBuilder()
                ids = cursor.execute('SELECT id, username FROM Admins').fetchall()
                if ids != []:
                    for i in ids:
                        builder.row(types.InlineKeyboardButton(
                        text=f'{str(i[0])} || {str(i[1])}',
                        callback_data=str(i[0])))
                builder.row(types.InlineKeyboardButton(
                text="Добавить админа",
                callback_data="addadmin"))
                builder.row(types.InlineKeyboardButton(
                text="Назад",
                callback_data="back"))
                
                await callback.message.answer(
                    '''<b>🔏Кабинет Владельца:</b>\n
        Используя кнопки ниже, Вы можете удалять и добавлять админов наборы''',
                    reply_markup=builder.as_markup(), parse_mode='HTML'
                )
            else:
                await callback.message.answer("Нет прав")

        if callback.data == 'back':
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await state.clear()
            await callback.message.answer('Ну ладненько... <3')
            builder = InlineKeyboardBuilder()
            builder.row(types.InlineKeyboardButton(
            text="Открыть набор",
            callback_data="open"), types.InlineKeyboardButton(
            text="Закрыть набор",
            callback_data="close"))
            builder.row(types.InlineKeyboardButton(
                    text="Информация",
                    callback_data="info"))
            if str(callback.message.from_user.id) == str(ADMIN_ID):
                    builder.row(types.InlineKeyboardButton(
                    text="Кабинет Владельца",
                    callback_data="admin"))
            await callback.message.answer(
            '''<b>🔏Кабинет Администратора:</b>\n
    Используя кнопки ниже, \nвы можете открывать и закрывать наборы''',
            reply_markup=builder.as_markup(), parse_mode='HTML'
        )
        if callback.data == 'close':
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
            text="Подтвердить",
            callback_data="ok_close"),types.InlineKeyboardButton(
            text="Назад",
            callback_data="back"))
            await callback.message.answer('Уверены что хотите закрыть набор?', reply_markup=builder.as_markup())
        if callback.data == 'no':
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await callback.message.answer('Ну ладненько... <3')
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
            text="Открыть набор",
            callback_data="open"),types.InlineKeyboardButton(
            text="Закрыть набор",
            callback_data="close"))
            if str(callback.message.from_user.id) == str(ADMIN_ID):
                    builder.row(types.InlineKeyboardButton(
                    text="Кабинет Владельца",
                    callback_data="admin"))
            builder.row(types.InlineKeyboardButton(
                    text="Информация",
                    callback_data="info"))
            await callback.message.answer(
            '''<b>🔏Кабинет Администратора:</b>\n
    Используя кнопки ниже, \nвы можете открывать и закрывать наборы''',
            reply_markup=builder.as_markup(), parse_mode='HTML'
        )
        if 'yes' in callback.data:
            us_id = callback.message.chat.id
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            many_post = cursor.execute('SELECT many_posts FROM Admins WHERE id = ?', (us_id,)).fetchone()[0]
            cursor.execute('UPDATE Admins SET many_posts = ? WHERE id = ?', (int(many_post)+1, us_id))
            connection.commit()
            post_builder = InlineKeyboardBuilder()
            post_builder.row(types.InlineKeyboardButton(text='Откликнуться', url=f'https://t.me/{callback.from_user.username}'))
            mes = await bot.send_message(CHANEL, text=txt, parse_mode='HTML', reply_markup=post_builder.as_markup(), disable_web_page_preview=True)
            mes_id = mes.message_id
            await bot.send_message(us_id,'Успешно открыт')
            cursor.execute('UPDATE Admins SET post = ? WHERE id = ?', (mes_id, us_id))
            connection.commit()
            builder = InlineKeyboardBuilder()
            builder.row(types.InlineKeyboardButton(
            text="Открыть набор",
            callback_data="open"), types.InlineKeyboardButton(
            text="Закрыть набор",
            callback_data="close"))
            builder.row(types.InlineKeyboardButton(
                    text="Информация",
                    callback_data="info"))
            if str(callback.message.chat.id) == str(ADMIN_ID):
                    builder.row(types.InlineKeyboardButton(
                    text="Кабинет Владельца",
                    callback_data="admin"))
            await callback.message.answer(
            '''<b>🔏Кабинет Администратора:</b>\n
    Используя кнопки ниже, \nвы можете открывать и закрывать наборы''',
            reply_markup=builder.as_markup(), parse_mode='HTML'
        )
        if callback.data == 'open':
            check_post = cursor.execute("SELECT post FROM Admins WHERE id = ?", (callback.message.chat.id,)).fetchone()
            if check_post[0] == None:
                open = InlineKeyboardBuilder()
                avito_btn = types.InlineKeyboardButton(
                        text="Авито",
                        callback_data="Авито")
                yandex_btn = types.InlineKeyboardButton(
                        text="Я. Карты",
                        callback_data="Яндекс Карты")
                google_btn = types.InlineKeyboardButton(
                        text="Google Maps",
                        callback_data="Google Maps")
                gis2_btn = types.InlineKeyboardButton(
                        text="2GIS",
                        callback_data="2GIS")
                other_platform = types.InlineKeyboardButton(
                        text="Другая платформа",
                        callback_data="other")
                open.row(avito_btn,yandex_btn)
                open.row(google_btn,gis2_btn)
                open.row(other_platform)
                await callback.message.answer('Отлично! Выбери платформу!', reply_markup=open.as_markup())
            else:
                await callback.message.answer('У вас уже есть открытый набор!')


        if 'del:' in callback.data:
            adm_id = str(callback.data).split(':')[1]
            cursor.execute("DELETE FROM Admins WHERE id = (?)", (adm_id,))
            connection.commit()
            await callback.message.answer("Успешно удалён")
        if str(callback.data).isdigit() == True:
            menu_admin = InlineKeyboardBuilder()
            menu_admin.row(types.InlineKeyboardButton(
                    text="Удалить",
                    callback_data=f"del:{callback.data}"))
            menu_admin.row(types.InlineKeyboardButton(
                text="Назад",
                callback_data="back"))
            
            await callback.message.answer(f'Управление админом #{callback.data}', reply_markup=menu_admin.as_markup())  
        else:
            if str(callback.data) in PLATFORMS:
                global platform
                platform = callback.data
                await callback.message.answer(f"Хорошо Ваша платформа: {callback.data}\n\nВведите оплату:")
                await state.set_state(StateS.get_price)


@dp.message(StateS.get_plat)
async def get_plat(message: types.Message, state: FSMContext):
    global platform
    platform = message.text
    await message.answer(f"Хорошо Ваша платформа: {message.text}\n\nВведите оплату:")
    await state.set_state(StateS.get_price)

@dp.message(StateS.us_id)
async def get_id(message: types.Message, state: FSMContext):
    global id_to_add
    id_to_add = message.text
    await message.answer('Введи юз')
    await state.set_state(StateS.get_us)

@dp.message(StateS.get_us)
async def get_us(message: types.Message, state: FSMContext):
    username = message.text
    cursor.execute('INSERT INTO Admins (id, post, username) VALUES (?, ?, ?)', (id_to_add, None, username))
    connection.commit()
    builder = InlineKeyboardBuilder()
    ids = cursor.execute('SELECT id, username FROM Admins').fetchall()
    if ids != []:
        for i in ids:
            builder.row(types.InlineKeyboardButton(
                text=f'{str(i[0])} || {str(i[1])}',
                callback_data=str(i[0])))
        builder.row(types.InlineKeyboardButton(
            text="Добавить админа",
            callback_data="addadmin"))
        builder.row(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back"))
                    
        await message.answer(
                        '''<b>🔏Кабинет Владельца:</b>\n
            Используя кнопки ниже, Вы можете удалять и добавлять админов наборы''',
                        reply_markup=builder.as_markup(), parse_mode='HTML'
                    )


@dp.message(StateS.get_price)
async def price(message: types.Message, state: FSMContext):
    global get_money
    get_money = message.text
    await message.answer(f'Платформа: {platform}\nОплата: {get_money}\n\nВведите комментарий:')
    await state.set_state(StateS.get_comment)

@dp.message(StateS.get_comment)
async def comment(message: types.Message, state: FSMContext):
    global txt
    txt = f'''• Платформа: {platform}
• Оплата: {get_money}
• Описание: {message.text}
————————
√ Писать: @{message.from_user.username}'''

    yes_no_btn = InlineKeyboardBuilder()
    yes_no_btn.row(types.InlineKeyboardButton(text='Да', callback_data=f'yes'),types.InlineKeyboardButton(text='Нет', callback_data=f'no'))
    await message.answer("Всё верно?\n\n"+txt, parse_mode='HTML', reply_markup=yes_no_btn.as_markup(), disable_web_page_preview=True)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

connection.close()