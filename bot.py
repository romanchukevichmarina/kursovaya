import telebot
from telebot import types
import table_controller

bot = telebot.TeleBot("6729812420:AAEOhJnCnd-kUUrfdQPHYA_UQDpHFpY0sNM")
message_list = []

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Остатки")
    btn2 = types.KeyboardButton("Отгрузки")
    btn3 = types.KeyboardButton("Поступления")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Добрый день, {0.first_name}! Что бы вы хотели узнать?".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Остатки"):
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Общий остаток в рублях")
        btn2 = types.KeyboardButton("Остаток определенного товара")
        btn3 = types.KeyboardButton("Остаток контроллеров")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="Выберите вариант", reply_markup=markup)
    elif(message.text == "Отгрузки"):
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        week = types.KeyboardButton("За неделю")
        month = types.KeyboardButton("За месяц")
        markup.add(week, month)
        bot.send_message(message.chat.id, text="За какой промежуток вывести отгрузки?", reply_markup=markup)
    elif(message.text == "Поступления"):
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        week = types.KeyboardButton("За неделю")
        month = types.KeyboardButton("За месяц")
        markup.add(week, month)
        bot.send_message(message.chat.id, text="За какой промежуток вывести поступления?", reply_markup=markup)
    elif(message.text == "За неделю"):
        message_list.append(message.text)
        print(message_list[-2])
        if message_list[-2] == "Поступления":
            delivery = table_controller.delivery(0)
            bot.send_message(message.chat.id, f'Поступления:\n{ delivery }')
        elif message_list[-2] == "Отгрузки":
            shipments = table_controller.shipments(0)
            bot.send_message(message.chat.id, f'Отгрузки:\n{ shipments }')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, text="Вернитесь в главное меню", reply_markup=markup)
    elif(message.text == "За месяц"):
        message_list.append(message.text)
        if message_list[-2] == "Поступления":
            delivery = table_controller.delivery(1)
            bot.send_message(message.chat.id, f'Поступления:\n{ delivery }')
        elif message_list[-2] == "Отгрузки":
            shipments = table_controller.shipments(1)
            bot.send_message(message.chat.id, f'Отгрузки:\n{ shipments }')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, text="Вернитесь в главное меню", reply_markup=markup)
    elif(message.text == "Общий остаток в рублях"):
        message_list.append(message.text)
        total_rest = table_controller.cash_rest()
        bot.send_message(message.chat.id, f'Остаток товара на складе { total_rest } рублей')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
    elif message.text == "Остаток определенного товара":
        message_list.append(message.text)
        bot.send_message(message.chat.id, text="Введите артикул товара")
    elif message.text == "Остаток контроллеров":
        message_list.append(message.text)
        cont_rest = table_controller.rest_of_controllers()
        bot.send_message(message.chat.id, f'Остаток контроллеров на складе:\n { cont_rest }')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
    elif (message.text == "Вернуться в главное меню"):
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Остатки")
        button2 = types.KeyboardButton("Отгрузки")
        button3 = types.KeyboardButton("Поступления")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        if message_list[-1] == "Остаток определенного товара":
            id = int(message.text)
            rest = table_controller.rest_of_good(id)
            bot.send_message(message.chat.id, f'{rest}')
        else:
            bot.send_message(message.chat.id, text="Такой команды нет")

bot.polling(none_stop=True)