import os
from flask import Flask, request
import mysql.connector
import telebot
from telebot import types

TOKEN = '5287178701:AAGqjOQohzho-G0wl48-zYNBCcRxW9JC_ic'
APP_URL = f'https://jenpuadminline.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

conn = mysql.connector.connect(host="194.39.67.215", user="jelastic-5256352", password="O60BFWSCBLbn4yJJiWJ3",
                               database='mydb', auth_plugin='mysql_native_password')
cursor = conn.cursor()


Fakultet1 = "Педагогика және психология институты"
Fakultet2 = "Қазақ тілі және әлем тілдері институты"
Fakultet3 = "Физика, математика және цифрлық \nтехнологиялар институты"
Fakultet4 = "Жаратылыстану институты"
Fakultet5 = "Әлеуметтік, гуманитарлық ғылымдар \nжәне өнер институты"
Fakultet6 = "Университет құрамындағы кәсіптік \nбілім беру колледжі"
Fakultet7 = "Магистратура және Докторантура"
homePage = "Бастапқы бетке оралу"

@bot.message_handler(commands=['start'])
def first(message):
    keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.add('Мәзір')
    send = bot.send_message(message.chat.id, 'Сәлеметсіз бе! \nБұл қабылдау комиссиясына кезекке қабылдау боты!\nМәзірді басып, өз факультетіңізді таңдаңыз!',reply_markup=keyboard)
    bot.register_next_step_handler(send,second)

def second(message):
    if message.text == 'Мәзір':
        keyboard = types.ReplyKeyboardMarkup(True,False)
        keyboard.add(Fakultet1)
        keyboard.add(Fakultet2)
        keyboard.add(Fakultet3)
        keyboard.add(Fakultet4)
        keyboard.add(Fakultet5)
        keyboard.add(Fakultet6)
        keyboard.add(Fakultet7)
        keyboard.add(homePage)
        send = bot.send_message(message.chat.id,'Таңдаңыз!', reply_markup=keyboard)
        bot.register_next_step_handler(send,third)
    else:
        bot.send_message(message.chat.id,'Төменде орналасқан \nмәзірдегі батырманы басыңыз')

@bot.message_handler(content_types=['text'])
def third(message):
    """===============================Fakultetter==================================================="""
    #=================================FAKULTET_1========================================================
    if message.text == Fakultet1:
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.add('Келесі')
        send = bot.send_message(message.chat.id,
                                'Келесі батырмасын басып, кезек қабылдаңыз!',
                                reply_markup=keyboard)
        bot.register_next_step_handler(send, secondPageFakultetF1)



    #===============================HOME_PAGE=============================================================
    elif message.text == homePage:
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.add('Мәзір')
        send = bot.send_message(message.chat.id,
                                'Сәлеметсіз бе! \nБұл қабылдау комиссиясына кезекке қабылдау боты!\nМәзірді басып, өз факультетіңізді таңдаңыз!',
                                reply_markup=keyboard)
        bot.register_next_step_handler(send, second)
    """=================================FINISH======================================================"""
    """===============================Fakultetter==================================================="""



def secondPageFakultetF1(message):

    if message.text == 'Келесі':
        cursor.execute('''SELECT COUNT(*) FROM db_f_1''')
        check_for_null = cursor.fetchall()
        print(check_for_null)
        if check_for_null[0][0] == 0:
            print("Table no contents")
            bot.send_message(message.chat.id, "Кезекте студент жоқ!")
            keyboard = types.ReplyKeyboardMarkup(True, False)
            keyboard.add('Келесі')
            send = bot.send_message(message.chat.id, '- - - - - - - - - - - - - - -', reply_markup=keyboard)
            bot.register_next_step_handler(send, secondPageFakultetF1)
        else:
            """=============================USER ID===================================="""
            cursor.execute("SELECT id FROM db_f_1 LIMIT 1")
            for get_user_id in cursor:
                print(get_user_id[0])
                bot.send_message(message.chat.id, "Кезек нөмірі:  " + str(get_user_id[0]))
            """==================USER_NAME CHECK FOR EXIST OR NONE======================="""
            cursor.execute("SELECT user_name FROM db_f_1 LIMIT 1")
            for check_name_null in cursor:
                print(check_name_null[0])
                if check_name_null[0] is None:
                    print("NULL")
                    bot.send_message(message.chat.id, "Есімі:  " + "Есімі жазылмаған")
                else:
                    bot.send_message(message.chat.id, "Есімі:  " + str(check_name_null[0]))
            """==================USER_SUR_NAME CHECK FOR EXIST OR NONE===================="""
            cursor.execute("SELECT user_surname FROM db_f_1 LIMIT 1")
            for check_sname_null in cursor:
                print(check_sname_null[0])
                if check_sname_null[0] is None:
                    print("NULL")
                    bot.send_message(message.chat.id, "Тегі:  " + "Тегі жазылмаған")
                else:
                    bot.send_message(message.chat.id, "Тегі:  " + str(check_sname_null[0]))
            """=========================================================================="""
            """==================USER_ID================================================="""


            """==============API-KEY======================================"""

            api_key = "5497810512:AAFI8DhRu4apgVAdyeID2ppPJSRQ7Oq0UhE"
            bots = telebot.TeleBot(api_key)

            bots.send_message(chat_id=get_user_id[0],
                                        text='Сіздің кезегіңіз келді! '
                                       '\n101-кабинетте күтеміз!'
                                       '\n5 минутта келмесеңіз,'
                                       '\nкезегіңіз жоғалады!')
            """==========================================================="""
            cursor.execute("DELETE FROM db_f_1 WHERE user_id='%s';" % get_user_id[0])
            conn.commit()



            keyboard = types.ReplyKeyboardMarkup(True, False)
            keyboard.add('Келесі')
            send = bot.send_message(message.chat.id, '- - - - - - - - - - - - - - -', reply_markup=keyboard)
            bot.register_next_step_handler(send, secondPageFakultetF1)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
