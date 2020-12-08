import telebot
from telebot.types import *
from Crypto_Converter import convert_to

user_dict = {}
bot = telebot.TeleBot(<TOKEN>) #Telegram Bot API


@bot.message_handler(commands=['start'])
def start(message):
    msg = "hello %s i'm cambot\ni will help you understand crypto currency and all things related\n\nfirst things first start by  pressing the help button to understand how I work"%(message.from_user.username)
    keyboard = ReplyKeyboardMarkup(True)
    keyboard.row("Airdrops","Convert")
    keyboard.row("News","FAQ")
    keyboard.row(KeyboardButton("/help"))
    bot.reply_to(message,msg,reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Contact developer",url="telegram.me/nacbotics"))
    help = """(1) Use the AIRDROPS button to check for available Airdrops
    (2) Use the CONVERT button to convert between two cryptocurrencies
    (3) Use the FAQ button to get answers to most common Crypto questions
    (4) Use the NEWS button to get list of websites that show market analysis for some cryptocurrencies"""
    bot.reply_to(message,help,reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == "Convert":
        msg = bot.send_message(message.chat.id,"Select the Crypto/fiat you are converting from", reply_markup=converting_keys())
        bot.register_next_step_handler(msg,get_next_crypto)

    elif message.text == "Airdrops":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Click to see available Airdrops",url="https://airdrops.io/"))
        bot.reply_to(message,"Don't worry we got you covered on legit Airdrops", reply_markup=markup)
    
    elif message.text == "News":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("CoinDesk",url="https://www.coindesk.com/"))
        markup.add(InlineKeyboardButton("CoinTelegraph",url="https://cointelegraph.com/"))
        markup.add(InlineKeyboardButton("Bitcoinist",url="https://bitcoinist.com/"))
        markup.add(InlineKeyboardButton("TodayonChain",url="https://www.todayonchain.com/"))
        bot.reply_to(message,"Here are some interesting websites recommended by My Developer", reply_markup=markup)
    
    elif message.text == "FAQ":
        bot.send_message(message,f"{message.text} is coming very soon")



def converting_keys():
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=False)
    keyboard.row("Bitcoin","Litecoin")
    keyboard.row("USD","Naira")
    keyboard.row("Ripple","Etherium")
    keyboard.row("Tron")
    return(keyboard)

def get_next_crypto(message):
    """ gets the second cryptocurrency to convert to after getting the first one"""
    try:
        C1 = message.text
        user_dict["Crypto1"] = C1
        msg = bot.reply_to(message,"select the Crypto/fiat you are converting to",reply_markup=converting_keys())
        bot.register_next_step_handler(msg,get_crypto_amount)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')

def get_crypto_amount(message):
    """ get_crypto_amount(message) queries for tye cryptocurrency amount to convert from """
    try:
        C1 = message.text
        user_dict["Crypto2"] = C1
        msg = bot.reply_to(message,"Enter the amount you are converting",reply_markup=converting_keys())
        bot.register_next_step_handler(msg, process_results)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')

def process_results(message):
    """ process_results(message) starts the Crypto/fiat conversion process"""
    try:
        amnt = message.text
        user_dict["Amount"] = amnt
        if not amnt.isdigit():
            msg = bot.reply_to(message, "The amount should be a number not text, just a number")
            bot.register_next_step_handler(msg, process_results)
            return
        else:
            print(user_dict)
            result = convert_to(user_dict["Crypto1"],user_dict["Crypto2"],user_dict["Amount"])
            bot.send_message(message.chat.id, result)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')


# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

#start the pulling process
bot.polling()



