import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
import random
import datetime
import requests

# ========== یہاں اپنی معلومات ڈالیں ==========
TOKEN = "YAHAN_APNA_TELEGRAM_TOKEN_DALEIN"
ADSTERRA_SMARTLINK = "YAHAN_APNA_ADSTERRA_SMARTLINK_DALEIN"
ADMIN_ID = 6277866627  # یہاں اپنی Telegram ID ڈالیں
# ==============================================

bot = telebot.TeleBot(TOKEN)

# ڈیٹا فائل (پوائنٹس محفوظ کرنے کے لیے)
DATA_FILE = "users_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {
            "points": 0,
            "ads_watched": 0,
            "last_ad": None,
            "ads_today": 0
        }
        save_data(data)
    return data[uid]

def update_user(user_id, updates):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"points": 0, "ads_watched": 0, "last_ad": None, "ads_today": 0}
    data[uid].update(updates)
    save_data(data)

def add_points(user_id, points):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"points": 0, "ads_watched": 0, "last_ad": None, "ads_today": 0}
    data[uid]["points"] += points
    data[uid]["ads_watched"] += 1
    save_data(data)

# ========== مینو ==========
def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📺 ایڈ دیکھیں", callback_data="watch_ad"),
        InlineKeyboardButton("💰 میرا بیلنس", callback_data="balance"),
        InlineKeyboardButton("🤝 ریفرل", callback_data="referral"),
        InlineKeyboardButton("📊 میرے اعداد و شمار", callback_data="stats")
    )
    return markup

# ========== /start کمانڈ ==========
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    args = message.text.split()
    referred_by = args[1] if len(args) > 1 else None
    
    get_user(user_id)  # یوزر رجسٹر کریں
    
    # ریفرل پوائنٹس
    if referred_by and referred_by != str(user_id):
        add_points(referred_by, 5)
        try:
            bot.send_message(int(referred_by), "🎉 آپ کو ایک ریفرل سے 5 پوائنٹس ملے!")
        except:
            pass
    
    bot.send_message(
        user_id,
        "👋 خوش آمدید!\n\nیہاں آپ ایڈ دیکھ کر پوائنٹس کما سکتے ہیں۔\n\n"
        "📌 ایڈ دیکھنے کے لیے نیچے بٹن دبائیں۔",
        reply_markup=main_menu(user_id)
    )

# ========== ایڈ دیکھنے کا بٹن ==========
@bot.callback_query_handler(func=lambda call: call.data == "watch_ad")
def watch_ad(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    
    today = str(datetime.date.today())
    if user.get("last_ad") != today:
        update_user(user_id, {"ads_today": 0, "last_ad": today})
        user = get_user(user_id)
    
    if user["ads_today"] >= 30:
        bot.answer_callback_query(call.id, "❌ آج کی حد پوری ہو گئی۔ کل دوبارہ آئیں۔", show_alert=True)
        return
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔗 ایڈ کھولیں", url=ADSTERRA_SMARTLINK))
    markup.add(InlineKeyboardButton("✅ میں نے ایڈ دیکھ لی", callback_data="ad_done"))
    
    bot.send_message(
        user_id,
        "📺 نیچے بٹن سے ایڈ کھولیں۔\nایڈ دیکھنے کے بعد 'میں نے ایڈ دیکھ لی' دبائیں۔",
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

# ========== ایڈ مکمل ہونے کا بٹن ==========
@bot.callback_query_handler(func=lambda call: call.data == "ad_done")
def ad_done(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    
    if user["ads_today"] >= 30:
        bot.answer_callback_query(call.id, "❌ آج کی حد پوری ہو گئی۔", show_alert=True)
        return
    
    add_points(user_id, 1)
    update_user(user_id, {"ads_today": user["ads_today"] + 1})
    
    bot.answer_callback_query(call.id, "✅ آپ کو 1 پوائنٹ ملا!", show_alert=True)
    bot.send_message(user_id, "🎉 شاباش! آپ کو 1 پوائنٹ ملا۔", reply_markup=main_menu(user_id))

# ========== بیلنس ==========
@bot.callback_query_handler(func=lambda call: call.data == "balance")
def balance(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    bot.send_message(
        user_id,
        f"💰 آپ کا بیلنس:\n\n"
        f"پوائنٹس: {user['points']}\n"
        f"کل ایڈ دیکھے: {user['ads_watched']}",
        reply_markup=main_menu(user_id)
    )
    bot.answer_callback_query(call.id)

# ========== ریفرل ==========
@bot.callback_query_handler(func=lambda call: call.data == "referral")
def referral(call):
    user_id = call.message.chat.id
    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={user_id}"
    bot.send_message(
        user_id,
        f"🤝 آپ کا ریفرل لنک:\n\n{link}\n\n"
        f"ہر ریفرل پر آپ کو 5 پوائنٹس ملیں گے۔",
        reply_markup=main_menu(user_id)
    )
    bot.answer_callback_query(call.id)

# ========== اعداد و شمار ==========
@bot.callback_query_handler(func=lambda call: call.data == "stats")
def stats(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    bot.send_message(
        user_id,
        f"📊 آپ کے اعداد و شمار:\n\n"
        f"پوائنٹس: {user['points']}\n"
        f"کل ایڈ: {user['ads_watched']}\n"
        f"آج کے ایڈ: {user['ads_today']}",
        reply_markup=main_menu(user_id)
    )
    bot.answer_callback_query(call.id)

# ========== بوٹ چلائیں ==========
print("بوٹ چل رہا ہے...")
bot.infinity_polling()
