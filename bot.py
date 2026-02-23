import telebot
import json
import time
from telebot.types import ReplyKeyboardMarkup

TOKEN = "8534248097:AAHwqpJMYRcjsBkd-7oODAlHygbXO40tmrs"
CHANNEL_ID = -1003856984651
CHANNEL_LINK = "https://t.me/DalyEarningOfficial"
ADMIN_ID = 8033702577

JOIN_REWARD = 5
REF_REWARD = 2
MIN_WITHDRAW = 10

bot = telebot.TeleBot(TOKEN)

DB_FILE = "database.json"

# Load database
def load_db():
    try:
        with open(DB_FILE,"r") as f:
            return json.load(f)
    except:
        return {}

# Save database
def save_db(data):
    with open(DB_FILE,"w") as f:
        json.dump(data,f)

# Menu
def menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("💰 Earn Money","👥 Refer & Earn")
    m.row("📊 Dashboard","💳 Withdraw")
    m.row("📢 Join Channel")
    return m

# Start command
@bot.message_handler(commands=['start'])
def start(message):

    db = load_db()

    uid = str(message.from_user.id)

    args = message.text.split()

    ref = None

    if len(args)>1:
        ref = args[1]

    if uid not in db:

        db[uid] = {
            "balance":0,
            "upi":"",
            "ref":ref,
            "refs":0,
            "join_time":0
        }

        if ref and ref in db:
            db[ref]["balance"] += REF_REWARD
            db[ref]["refs"] += 1

        save_db(db)

    bot.send_message(
        message.chat.id,
        "💰 Welcome to Daly Earning Bot",
        reply_markup=menu()
    )

# Join channel button
@bot.message_handler(func=lambda m:m.text=="📢 Join Channel")
def join_channel(message):

    bot.send_message(
        message.chat.id,
        CHANNEL_LINK
    )

# Earn money
@bot.message_handler(func=lambda m:m.text=="💰 Earn Money")
def earn(message):

    db = load_db()

    uid = str(message.from_user.id)

    try:

        member = bot.get_chat_member(CHANNEL_ID,message.from_user.id)

        if member.status in ["member","administrator","creator"]:

            if db[uid]["join_time"] == 0:

                db[uid]["join_time"] = time.time()

                db[uid]["balance"] += JOIN_REWARD

                save_db(db)

                bot.send_message(
                    message.chat.id,
                    f"✅ ₹{JOIN_REWARD} added to wallet"
                )

            else:

                bot.send_message(
                    message.chat.id,
                    "Already completed"
                )

        else:

            bot.send_message(
                message.chat.id,
                "❌ Join channel first"
            )

    except:

        bot.send_message(
            message.chat.id,
            "❌ Join channel first"
        )

# Dashboard
@bot.message_handler(func=lambda m:m.text=="📊 Dashboard")
def dashboard(message):

    db = load_db()

    uid = str(message.from_user.id)

    data = db[uid]

    bot.send_message(
        message.chat.id,
        f"""
💰 Balance: ₹{data['balance']}

👥 Referrals: {data['refs']}
"""
    )

# Refer system
@bot.message_handler(func=lambda m:m.text=="👥 Refer & Earn")
def refer(message):

    link = f"https://t.me/{bot.get_me().username}?start={message.from_user.id}"

    bot.send_message(
        message.chat.id,
        f"Refer and earn ₹2 per user\n\n{link}"
    )

# Withdraw
@bot.message_handler(func=lambda m:m.text=="💳 Withdraw")
def withdraw(message):

    db = load_db()

    uid = str(message.from_user.id)

    balance = db[uid]["balance"]

    if balance < MIN_WITHDRAW:

        bot.send_message(
            message.chat.id,
            "Minimum withdraw ₹10"
        )

        return

    bot.send_message(
        ADMIN_ID,
        f"Withdraw request\nUser: {uid}\nAmount: ₹{balance}"
    )

    bot.send_message(
        message.chat.id,
        "Withdraw request sent"
    )

print("Bot running...")
bot.infinity_polling()
