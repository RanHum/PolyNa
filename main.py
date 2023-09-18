from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import sqlite3
import re

conn = sqlite3.connect('mybazed.db')
cursor = conn.cursor()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton #ReplyKeyboardRemove


TOKEN = 'вставьте ваш токен'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
	print('Бот вышел в онлайн')


#команда старт и приветствие
@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
	await bot.send_message(message.from_user.id, 'Чтобы продолжить, нажмите на кнопку «NewМаршрут».', reply_markup=keyboard)


kb_client = KeyboardButton('NewМаршрут')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb_client)

#команда узнать маршрут и выбор кнопок аудитории и точки интереса
urlkb = InlineKeyboardMarkup(row_width=1) 
urlButton1 = InlineKeyboardButton(text='Маршрут до аудитории', callback_data='v1')
urlButton2 = InlineKeyboardButton(text='Маршрут до точки интереса', callback_data='v2')
urlButton3 = InlineKeyboardButton(text='Маршрут до кампуса', callback_data='v3')
urlkb.add(urlButton1, urlButton2, urlButton3)


@dp.message_handler(lambda message: message.text == 'NewМаршрут')
async def url_command(message : types.Message):
	await message.answer('Что Вы хотите узнать?', reply_markup=urlkb)



#АУДИТОРИИ
@dp.callback_query_handler(text='v1')
async def first_function(callback : types.CallbackQuery):
	global is_first_function_completed
	await callback.message.answer('Введите номер нужной аудитории в формате, который указан в Вашем расписании.\nНомер аудитории должен содержать буквенные символы, которые обозначают название кампуса, а также численные символы (4 цифры)\nПример ввода: АВ1407 \n"АВ"- обозначение кампуса на Автозаводской,\n"1" - корпус, "4" - этаж, "07" - аудитория.\n(На данный момент доступен первый корпус на ул.Автозаводская)')
	await callback.answer()
	is_first_function_completed = True

# функция для базы данных
@dp.message_handler()
async def second_function(message: types.Message):
	global is_first_function_completed
	if is_first_function_completed:
		room = message.text.strip().upper()#приводим текст к вернему регистру и убираем пробелы между символами


		query = "SELECT infa, fotka FROM Auditoriums WHERE room_number = ?"
		cursor.execute(query, (room,))
		row = cursor.fetchone()

		if re.match(r'^[а-яА-Я]{1,2}\d{4}$', room):
			if row is not None:
				infa, fotka = row
				await message.reply(f"{infa}")
				await bot.send_photo(chat_id=message.chat.id, photo=fotka)
			else:
				await message.reply(f"Информация о маршруте до аудитории {room} не найдена.")
		else:
			await message.answer('Номер аудитории был введён некорректно.\nПовоторите попытку.')


@dp.callback_query_handler(text='v2')
async def v2_call(callback : types.CallbackQuery):
	await callback.message.answer('По какому адресу Вы сейчас находитесь?', reply_markup=inkb)
	await callback.answer()


@dp.callback_query_handler(text='v3')
async def v3_call(callback : types.CallbackQuery):
	await callback.message.answer('Какой кампус Вам нужен?', reply_markup=inkam)
	await callback.answer()





#Маршрут до точки интереса 
inkb = InlineKeyboardMarkup(row_width=1)
kampus1 = InlineKeyboardButton(text='ул. Большая Семёновская, д. 38', callback_data='w1')
kampus2 = InlineKeyboardButton(text='ул. Автозаводская, д. 16', callback_data='w2')
kampus3 = InlineKeyboardButton(text='ул. Михалковская, д. 7', callback_data='w3')
kampus4 = InlineKeyboardButton(text='ул. Прянишкова, 2А', callback_data='w4')
kampus5 = InlineKeyboardButton(text='ул. Павла Корчагина, д. 22', callback_data='w5')
inkb.add(kampus1, kampus2, kampus3, kampus4, kampus5)

@dp.message_handler(commands='test')
async def test_command(message : types.Message):
	await message.answer('По какому адресу Вы сейчас находитесь?', reply_markup=inkb)

@dp.callback_query_handler(text='w1')
async def w1_call(callback : types.CallbackQuery):
	await callback.message.answer('Вы выбрали кампус на Большой Семёновской,\n "БС"-обозначение в Вашем расписании.')
	await callback.message.answer('Выберите, что вы хотите посетить:', reply_markup=tochka1)
	await callback.answer()

tochka1 = InlineKeyboardMarkup(row_width=1)
t1 = InlineKeyboardButton(text='Зона отдыха', callback_data='tok1')
t2 = InlineKeyboardButton(text='«Технопарк»', callback_data='tok2')
t3 = InlineKeyboardButton(text='Актовый зал', callback_data='tok3')
tochka1.add(t1, t2, t3)

@dp.message_handler(commands='tochkamoi')
async def tochka_command(message: types.Message):
	await message.answer('Выберите, что Вы хотите посетить', reply_markup=tochka1)



@dp.callback_query_handler(text='w2')
async def w2_call(callback : types.CallbackQuery):
	await callback.message.answer('Вы выбрали кампус на Автозаводской,\n "АВ"-обозначение в Вашем расписании.')
	await callback.message.answer('Выберите, что Вы хотите посетить:', reply_markup=tochka2)
	await callback.answer()

tochka2 = InlineKeyboardMarkup(row_width=1)
t4 = InlineKeyboardButton(text='Зона отдыха', callback_data='tok4')
t5 = InlineKeyboardButton(text='Арт-политех', callback_data='tok5')
tochka2.add(t4, t5)

@dp.message_handler(commands='tochkamoi')
async def tochka_command(message : types.Message):
	await message.answer('Выберите, что Вы хотите посетить', reply_markup=tochka2)



@dp.callback_query_handler(text='w3')
async def w3_call(callback : types.CallbackQuery):
	await callback.message.answer('Вы выбрали кампус на Михалковской,\n "M"-обозначение в Вашем расписании.')
	await callback.message.answer('Выберите, что Вы хотите посетить:', reply_markup=tochka3)
	await callback.answer()

tochka3 = InlineKeyboardMarkup(row_width=1)
t6 = InlineKeyboardButton(text='Зона отдыха', callback_data='tok6')
tochka3.add(t6)

@dp.message_handler(commands='tochkamoi')
async def tochka_command(message : types.Message):
	await message.answer('Выберите, что Вы хотите посетить', reply_markup=tochka3)



@dp.callback_query_handler(text='w4')
async def w4_call(callback : types.CallbackQuery):
	await callback.message.answer('Вы выбрали кампус на Прянишкова,\n "ПР"-обозначение в Вашем расписании.')
	await callback.message.answer('Выберите, что Вы хотите посетить:', reply_markup=tochka4)
	await callback.answer()

tochka4 = InlineKeyboardMarkup(row_width=1)
t7 = InlineKeyboardButton(text='Зона отдыха', callback_data='tok7')
tochka4.add(t7)

@dp.message_handler(commands='tochkamoi')
async def tochka_command(message : types.Message):
	await message.answer('Выберите, что Вы хотите посетить', reply_markup=tochka4)



@dp.callback_query_handler(text='w5')
async def w5_call(callback : types.CallbackQuery):
	await callback.message.answer('Вы выбрали кампус на Павла Корчагина,\n "ПК"-обозначение в Вашем расписании.')
	await callback.message.answer('Выберите, что Вы хотите посетить:', reply_markup=tochka5)
	await callback.answer()

tochka5 = InlineKeyboardMarkup(row_width=1)
t8 = InlineKeyboardButton(text='Зона отдыха', callback_data='tok1')
t9 = InlineKeyboardButton(text='«Добро.Центр»', callback_data='tok2')
tochka5.add(t8, t9)

@dp.message_handler(commands='tochkamoi')
async def tochka_command(message : types.Message):
	await message.answer('Выберите, что Вы хотите посетить', reply_markup=tochka5)




#Маршрут до кампуса
inkam = InlineKeyboardMarkup(row_width=1)
kampus1 = InlineKeyboardButton(text='ул. Большая Семёновская, д. 38', url='https://yandex.ru/maps?rtext=55.824699%2C37.654953~55.781291%2C37.711518&rtt=mt')
kampus2 = InlineKeyboardButton(text='ул. Автозаводская, д. 16', url='https://yandex.ru/maps?rtext=55.781291%2C37.711518~55.70422%2C37.645196&rtt=mt')
kampus3 = InlineKeyboardButton(text='ул. Михалковская, д. 7', url='https://yandex.ru/maps?rtext=55.781291%2C37.711518~55.837459%2C37.533427&rtt=mt')
kampus4 = InlineKeyboardButton(text='ул. Прянишкова, 2А', url='https://yandex.ru/maps/-/CCUWz4eUGD')
kampus5 = InlineKeyboardButton(text='ул. Павла Корчагина, д. 22', url='https://yandex.ru/maps?rtext=55.781291%2C37.711518~55.819439%2C37.663351&rtt=mt')
inkam.add(kampus1, kampus2, kampus3, kampus4, kampus5)

@dp.message_handler(commands='test')
async def test_command(message : types.Message):
	await message.answer('По какому адресу Вы сейчас находитесь?', reply_markup=inkam)






#просто здравствуй просто как дела
# @dp.message_handler()
	# async def echo(message: types.Message):
	# text = message.text.lower() # приводим текст сообщения к нижнему регистру
    # await message.answer(text)




executor.start_polling(dp, skip_updates=True, on_startup=on_startup)