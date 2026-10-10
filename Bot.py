import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
import datetime

# ========== یہاں اپنی معلومات ڈالیں ==========
TOKEN = "8936754443:AAHya67EmRo71dhEVK1QUz73F-qpShy8tmo"
ADSTERRA_SMARTLINK = "https://uplcm.com/4/11995331"
ADMIN_ID = 6850142516
# ==============================================

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users_data.json"

# ========== Settings (CPM ke hisaab se) ==========
POINT_VALUE = 0.001          # 1 point = $0.001 (yani 1000 points = $1)
MIN_WITHDRAW_DOLLARS = 1     # Minimum $1 withdrawal
MIN_REFERRALS = 10           # 10 referrals zaroori
# ==============================================

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
            "ads_today": 0,
            "lang": None,
            "referrals": 0,
            "wallet": None
        }
        save_data(data)
    return data[uid]

def update_user(user_id, updates):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"points": 0, "ads_watched": 0, "last_ad": None, "ads_today": 0, "lang": None, "referrals": 0, "wallet": None}
    data[uid].update(updates)
    save_data(data)

def add_points(user_id, points):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"points": 0, "ads_watched": 0, "last_ad": None, "ads_today": 0, "lang": None, "referrals": 0, "wallet": None}
    data[uid]["points"] += points
    data[uid]["ads_watched"] += 1
    save_data(data)

# ========== Languages ==========
TEXTS = {
    "en": {
        "welcome": "👋 Welcome!\n\nHere you can watch ads and earn points.\n\n📌 Tap the button below to watch ads.",
        "watch_ads": "📺 Watch Ads",
        "balance": "💰 My Balance",
        "referral": "🤝 Referral",
        "stats": "📊 My Stats",
        "language": "🌐 Language",
        "withdraw": "💸 Withdraw",
        "open_ad": "🔗 Open Ad",
        "ad_done_btn": "✅ I Watched the Ad",
        "ad_msg": "📺 Tap the button below to open the ad.\nAfter watching, tap 'I Watched the Ad'.",
        "ad_limit": "❌ Daily limit reached. Come back tomorrow.",
        "ad_earned": "✅ You earned 1 point!",
        "ad_earned_msg": "🎉 Great! You earned 1 point.",
        "balance_msg": "💰 Your Balance:\n\nPoints: {points}\nDollars: ${dollars}\nTotal Ads Watched: {ads}\nReferrals: {refs}",
        "referral_msg": "🤝 Your Referral Link:\n\n{link}\n\nYou will get 5 points for each referral.\nYour Referrals: {refs}",
        "stats_msg": "📊 Your Stats:\n\nPoints: {points}\nDollars: ${dollars}\nTotal Ads: {ads}\nToday's Ads: {today}\nReferrals: {refs}",
        "referral_earned": "🎉 You earned 5 points from a referral!",
        "choose_lang": "🌐 Choose your language:",
        "lang_set": "✅ Language set to English!",
        "withdraw_title": "💸 Withdraw",
        "withdraw_info": "💰 Your Balance: ${dollars}\n👥 Referrals: {refs}\n\n📋 Rules:\n• Minimum ${min_dollars} to withdraw\n• At least {min_refs} referrals required\n• 1000 points = $1",
        "withdraw_ready": "✅ You can withdraw! Send your wallet address (Binance/JazzCash/EasyPaisa) in a message.",
        "withdraw_not_ready": "❌ You cannot withdraw yet.\n\nNeed: ${min_dollars} and {min_refs} referrals\nYou have: ${dollars} and {refs} referrals",
        "withdraw_sent": "✅ Your withdrawal request has been sent to admin.\nWallet: {wallet}\nAmount: ${amount}\n\nYou will receive payment within 24-48 hours.",
        "wallet_prompt": "Please send your wallet address:"
    },
    "ur": {
        "welcome": "👋 خوش آمدید!\n\nیہاں آپ ایڈ دیکھ کر پوائنٹس کما سکتے ہیں۔\n\n📌 ایڈ دیکھنے کے لیے نیچے بٹن دبائیں۔",
        "watch_ads": "📺 ایڈ دیکھیں",
        "balance": "💰 میرا بیلنس",
        "referral": "🤝 ریفرل",
        "stats": "📊 میرے اعداد و شمار",
        "language": "🌐 زبان",
        "withdraw": "💸 رقم نکالیں",
        "open_ad": "🔗 ایڈ کھولیں",
        "ad_done_btn": "✅ میں نے ایڈ دیکھ لی",
        "ad_msg": "📺 نیچے بٹن سے ایڈ کھولیں۔\nایڈ دیکھنے کے بعد 'میں نے ایڈ دیکھ لی' دبائیں۔",
        "ad_limit": "❌ آج کی حد پوری ہو گئی۔ کل دوبارہ آئیں۔",
        "ad_earned": "✅ آپ کو 1 پوائنٹ ملا!",
        "ad_earned_msg": "🎉 شاباش! آپ کو 1 پوائنٹ ملا۔",
        "balance_msg": "💰 آپ کا بیلنس:\n\nپوائنٹس: {points}\nڈالر: ${dollars}\nکل ایڈ دیکھے: {ads}\nریفرل: {refs}",
        "referral_msg": "🤝 آپ کا ریفرل لنک:\n\n{link}\n\nہر ریفرل پر آپ کو 5 پوائنٹس ملیں گے۔\nآپ کے ریفرل: {refs}",
        "stats_msg": "📊 آپ کے اعداد و شمار:\n\nپوائنٹس: {points}\nڈالر: ${dollars}\nکل ایڈ: {ads}\nآج کے ایڈ: {today}\nریفرل: {refs}",
        "referral_earned": "🎉 آپ کو ایک ریفرل سے 5 پوائنٹس ملے!",
        "choose_lang": "🌐 اپنی زبان منتخب کریں:",
        "lang_set": "✅ زبان اردو میں سیٹ ہو گئی!",
        "withdraw_title": "💸 رقم نکالیں",
        "withdraw_info": "💰 آپ کا بیلنس: ${dollars}\n👥 ریفرل: {refs}\n\n📋 شرائط:\n• کم از کم ${min_dollars} رقم\n• کم از کم {min_refs} ریفرل\n• 1000 پوائنٹس = $1",
        "withdraw_ready": "✅ آپ رقم نکال سکتے ہیں! اپنا والٹ ایڈریس (Binance/JazzCash/EasyPaisa) بھیجیں۔",
        "withdraw_not_ready": "❌ ابھی رقم نہیں نکال سکتے۔\n\nضرورت: ${min_dollars} اور {min_refs} ریفرل\nآپ کے پاس: ${dollars} اور {refs} ریفرل",
        "withdraw_sent": "✅ آپ کی درخواست ایڈمن کو بھیج دی گئی ہے۔\nوالٹ: {wallet}\nرقم: ${amount}\n\n24-48 گھنٹوں میں ادائیگی ہو جائے گی۔",
        "wallet_prompt": "براہ کرم اپنا والٹ ایڈریس بھیجیں:"
    }
}

def get_lang(user_id):
    user = get_user(user_id)
    return user.get("lang") or "en"

def t(user_id, key):
    lang = get_lang(user_id)
    return TEXTS[lang][key]

def points_to_dollars(points):
    return round(points * POINT_VALUE, 4)

def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(t(user_id, "watch_ads"), callback_data="watch_ad"),
        InlineKeyboardButton(t(user_id, "balance"), callback_data="balance"),
        InlineKeyboardButton(t(user_id, "referral"), callback_data="referral"),
        InlineKeyboardButton(t(user_id, "stats"), callback_data="stats"),
        InlineKeyboardButton(t(user_id, "withdraw"), callback_data="withdraw"),
        InlineKeyboardButton(t(user_id, "language"), callback_data="language")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    args = message.text.split()
    referred_by = args[1] if len(args) > 1 else None
    
    get_user(user_id)
    
    if referred_by and referred_by != str(user_id):
        add_points(referred_by, 5)
        data = load_data()
        ref_uid = str(referred_by)
        if ref_uid in data:
            data[ref_uid]["referrals"] = data[ref_uid].get("referrals", 0) + 1
            save_data(data)
        try:
            bot.send_message(int(referred_by), t(int(referred_by), "referral_earned"))
        except:
            pass
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"),
        InlineKeyboardButton("اردو 🇵🇰", callback_data="set_lang_ur")
    )
    
    bot.send_message(user_id, t(user_id, "choose_lang"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_lang_"))
def set_lang(call):
    user_id = call.message.chat.id
    lang = call.data.split("_")[2]
    update_user(user_id, {"lang": lang})
    bot.answer_callback_query(call.id, t(user_id, "lang_set"))
    bot.edit_message_text(
        t(user_id, "welcome"),
        user_id,
        call.message.message_id,
        reply_markup=main_menu(user_id)
    )

@bot.callback_query_handler(func=lambda call: call.data == "language")
def language(call):
    user_id = call.message.chat.id
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"),
        InlineKeyboardButton("اردو 🇵🇰", callback_data="set_lang_ur")
    )
    bot.edit_message_text(
        t(user_id, "choose_lang"),
        user_id,
        call.message.message_id,
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "watch_ad")
def watch_ad(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    
    today = str(datetime.date.today())
    if user.get("last_ad") != today:
        update_user(user_id, {"ads_today": 0, "last_ad": today})
        user = get_user(user_id)
    
    if user["ads_today"] >= 30:
        bot.answer_callback_query(call.id, t(user_id, "ad_limit"), show_alert=True)
        return
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, "open_ad"), url=ADSTERRA_SMARTLINK))
    markup.add(InlineKeyboardButton(t(user_id, "ad_done_btn"), callback_data="ad_done"))
    
    bot.send_message(user_id, t(user_id, "ad_msg"), reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "ad_done")
def ad_done(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    
    if user["ads_today"] >= 30:
        bot.answer_callback_query(call.id, t(user_id, "ad_limit"), show_alert=True)
        return
    
    add_points(user_id, 1)
    update_user(user_id, {"ads_today": user["ads_today"] + 1})
    
    bot.answer_callback_query(call.id, t(user_id, "ad_earned"), show_alert=True)
    bot.send_message(user_id, t(user_id, "ad_earned_msg"), reply_markup=main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "balance")
def balance(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    dollars = points_to_dollars(user['points'])
    bot.send_message(
        user_id,
        t(user_id, "balance_msg").format(
            points=user['points'],
            dollars=dollars,
            ads=user['ads_watched'],
            refs=user.get('referrals', 0)
        ),
        reply_markup=main_menu(user_id)
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "referral")
def referral(call):
    user_id = call.message.chat.id
    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={user_id}"
    user = get_user(user_id)
    bot.send_message(
        user_id,
        t(user_id, "referral_msg").format(link=link, refs=user.get('referrals', 0)),
        reply_markup=main_menu(user_id)
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "stats")
def stats(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    dollars = points_to_dollars(user['points'])
    bot.send_message(
        user_id,
        t(user_id, "stats_msg").format(
            points=user['points'],
            dollars=dollars,
            ads=user['ads_watched'],
            today=user['ads_today'],
            refs=user.get('referrals', 0)
        ),
        reply_markup=main_menu(user_id)
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def withdraw(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    dollars = points_to_dollars(user['points'])
    refs = user.get('referrals', 0)
    
    if dollars >= MIN_WITHDRAW_DOLLARS and refs >= MIN_REFERRALS:
        bot.send_message(user_id, t(user_id, "withdraw_ready"))
        bot.register_next_step_handler_by_chat_id(user_id, process_wallet)
    else:
        bot.send_message(
            user_id,
            t(user_id, "withdraw_not_ready").format(
                min_dollars=MIN_WITHDRAW_DOLLARS,
                min_refs=MIN_REFERRALS,
                dollars=dollars,
                refs=refs
            ),
            reply_markup=main_menu(user_id)
        )
    bot.answer_callback_query(call.id)

def process_wallet(message):
    user_id = message.chat.id
    wallet = message.text.strip()
    user = get_user(user_id)
    dollars = points_to_dollars(user['points'])
    
    update_user(user_id, {"wallet": wallet})
    
    bot.send_message(
        user_id,
        t(user_id, "withdraw_sent").format(wallet=wallet, amount=dollars),
        reply_markup=main_menu(user_id)
    )
    
    try:
        bot.send_message(
            ADMIN_ID,
            f"💸 New Withdraw Request\n\n"
            f"User ID: {user_id}\n"
            f"Points: {user['points']}\n"
            f"Amount: ${dollars}\n"
            f"Referrals: {user.get('referrals', 0)}\n"
            f"Wallet: {wallet}"
        )
    except:
        pass

print("Bot is running...")
bot.infinity_polling()
