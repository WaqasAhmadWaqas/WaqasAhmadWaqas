import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
import os
import json
import datetime

# ========== SETTINGS ==========
TOKEN = "8916537757:AAE2F9rLCY4ckiClcX-OQNFEFP1S3dUZ1mI"
ADSTERRA_SMARTLINK = "https://uplcm.com/4/11995331"
ADMIN_ID = 6850142516

POINT_VALUE = 0.0001
MIN_WITHDRAW_DOLLARS = 1
MIN_REFERRALS = 12
MB_RATE = 200
MIN_MB = 500
PREMIUM_PRICE = 50
PAID_CONTENT_PRICE = 100
PREMIUM_CHANNEL_ID = -1001234567890
# ==============================

bot = telebot.TeleBot(TOKEN)
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
            "points": 0, "ads_watched": 0, "last_ad": None, "ads_today": 0,
            "lang": None, "referrals": 0, "wallet": None, "phone": None,
            "premium": False, "channel_access": False
        }
        save_data(data)
    return data[uid]

def update_user(user_id, updates):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"points": 0, "ads_watched": 0, "last_ad": None, "ads_today": 0, "lang": None, "referrals": 0, "wallet": None, "phone": None, "premium": False, "channel_access": False}
    data[uid].update(updates)
    save_data(data)

def add_points(user_id, points):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"points": 0, "ads_watched": 0, "last_ad": None, "ads_today": 0, "lang": None, "referrals": 0, "wallet": None, "phone": None, "premium": False, "channel_access": False}
    data[uid]["points"] += points
    data[uid]["ads_watched"] += 1
    save_data(data)

TEXTS = {
    "en": {
        "welcome": "👋 Welcome!\n\nWatch ads, earn points, get MB or USDT!",
        "watch_ads": "📺 Watch Ads", "balance": "💰 My Balance",
        "referral": "🤝 Referral", "stats": "📊 My Stats",
        "language": "🌐 Language", "withdraw_mb": "📱 Get MB",
        "withdraw_usdt": "💸 Get USDT", "premium": "⭐ Premium",
        "paid_content": "📚 Paid Content", "digital_goods": "🛒 Digital Goods",
        "affiliate": "📈 Affiliate", "open_ad": "🔗 Open Ad",
        "ad_done_btn": "✅ I Watched the Ad",
        "ad_msg": "📺 Tap below to open ad.\nAfter watching, tap 'I Watched the Ad'.",
        "ad_limit": "❌ Daily limit reached.", "ad_earned": "✅ You earned 1 point!",
        "ad_earned_msg": "🎉 You earned 1 point.",
        "balance_msg": "💰 Balance:\n\nPoints: {points}\nDollars: ${dollars}\nMB: {mb} MB\nReferrals: {refs}\nPremium: {premium}",
        "referral_msg": "🤝 Your Referral Link:\n\n{link}\n\n5 points per referral.\nReferrals: {refs}",
        "stats_msg": "📊 Stats:\n\nPoints: {points}\nDollars: ${dollars}\nTotal Ads: {ads}\nToday: {today}\nReferrals: {refs}",
        "referral_earned": "🎉 You earned 5 points from referral!",
        "choose_lang": "🌐 Choose language:", "lang_set": "✅ Language set!",
        "mb_info": "📱 MB Withdrawal\n\nYour MB: {mb} MB\nMinimum: {min_mb} MB\n\nSend your phone number.",
        "mb_not_ready": "❌ Need {min_mb} MB. You have {mb} MB.",
        "mb_sent": "✅ MB request sent!\nPhone: {phone}\nMB: {mb}",
        "usdt_info": "💸 USDT Withdrawal\n\nBalance: ${dollars}\nMinimum: ${min_dollars}\nReferrals: {refs}/{min_refs}\n\nSend wallet address.",
        "usdt_not_ready": "❌ Need ${min_dollars} and {min_refs} referrals.",
        "usdt_sent": "✅ USDT request sent!\nWallet: {wallet}\nAmount: ${amount}",
        "premium_info": "⭐ Premium\n\nPrice: {price} Stars\n✅ Unlimited ads\n✅ 2x points",
        "premium_buy": "⭐ Buy Premium ({price} Stars)",
        "premium_success": "✅ Premium activated!",
        "premium_already": "✅ You are already Premium!",
        "paid_content_info": "📚 Paid Content\n\nBuy access to private channel for {price} Stars.",
        "paid_content_buy": "📚 Buy Access ({price} Stars)",
        "paid_content_success": "✅ Access granted! Join: {link}",
        "paid_content_already": "✅ You already have access!",
        "digital_goods_info": "🛒 Digital Goods\n\nUC, Diamonds, Gift Cards available.\nContact admin for purchase.",
        "affiliate_info": "📈 Affiliate Marketing\n\nEarn commission by promoting products.\nContact admin for details.",
        "back_menu": "⬅ Back to Menu"
    },
    "ur": {
        "welcome": "👋 خوش آمدید!\n\nایڈ دیکھیں، پوائنٹس کمائیں، MB یا USDT حاصل کریں!",
        "watch_ads": "📺 ایڈ دیکھیں", "balance": "💰 میرا بیلنس",
        "referral": "🤝 ریفرل", "stats": "📊 میرے اعداد و شمار",
        "language": "🌐 زبان", "withdraw_mb": "📱 MB لیں",
        "withdraw_usdt": "💸 USDT لیں", "premium": "⭐ پریمیم",
        "paid_content": "📚 پیڈ کنٹینٹ", "digital_goods": "🛒 ڈیجیٹل گڈز",
        "affiliate": "📈 ایفیلیئٹ", "open_ad": "🔗 ایڈ کھولیں",
        "ad_done_btn": "✅ میں نے ایڈ دیکھ لی",
        "ad_msg": "📺 نیچے بٹن سے ایڈ کھولیں۔\nایڈ دیکھنے کے بعد 'میں نے ایڈ دیکھ لی' دبائیں۔",
        "ad_limit": "❌ آج کی حد پوری ہو گئی۔", "ad_earned": "✅ آپ کو 1 پوائنٹ ملا!",
        "ad_earned_msg": "🎉 آپ کو 1 پوائنٹ ملا۔",
        "balance_msg": "💰 بیلنس:\n\nپوائنٹس: {points}\nڈالر: ${dollars}\nMB: {mb} MB\nریفرل: {refs}\nپریمیم: {premium}",
        "referral_msg": "🤝 آپ کا ریفرل لنک:\n\n{link}\n\nہر ریفرل پر 5 پوائنٹس۔\nریفرل: {refs}",
        "stats_msg": "📊 اعداد و شمار:\n\nپوائنٹس: {points}\nڈالر: ${dollars}\nکل ایڈ: {ads}\nآج: {today}\nریفرل: {refs}",
        "referral_earned": "🎉 آپ کو ریفرل سے 5 پوائنٹس ملے!",
        "choose_lang": "🌐 زبان منتخب کریں:", "lang_set": "✅ زبان سیٹ ہو گئی!",
        "mb_info": "📱 MB نکالیں\n\nآپ کے MB: {mb} MB\nکم از کم: {min_mb} MB\n\nاپنا فون نمبر بھیجیں۔",
        "mb_not_ready": "❌ کم از کم {min_mb} MB چاہیے۔ آپ کے پاس {mb} MB ہیں۔",
        "mb_sent": "✅ MB درخواست بھیج دی گئی!\nفون: {phone}\nMB: {mb}",
        "usdt_info": "💸 USDT نکالیں\n\nبیلنس: ${dollars}\nکم از کم: ${min_dollars}\nریفرل: {refs}/{min_refs}\n\nوالٹ ایڈریس بھیجیں۔",
        "usdt_not_ready": "❌ ${min_dollars} اور {min_refs} ریفرل چاہیے۔",
        "usdt_sent": "✅ USDT درخواست بھیج دی گئی!\nوالٹ: {wallet}\nرقم: ${amount}",
        "premium_info": "⭐ پریمیم\n\nقیمت: {price} اسٹارز\n✅ لامحدود ایڈ\n✅ 2 گنا پوائنٹس",
        "premium_buy": "⭐ پریمیم خریدیں ({price} اسٹارز)",
        "premium_success": "✅ پریمیم فعال!",
        "premium_already": "✅ آپ پہلے سے پریمیم ہیں!",
        "paid_content_info": "📚 پیڈ کنٹینٹ\n\nپرائیویٹ چینل کا access {price} اسٹارز میں خریدیں۔",
        "paid_content_buy": "📚 Access خریدیں ({price} اسٹارز)",
        "paid_content_success": "✅ Access مل گیا! جوائن کریں: {link}",
        "paid_content_already": "✅ آپ کے پاس پہلے سے access ہے!",
        "digital_goods_info": "🛒 ڈیجیٹل گڈز\n\nUC، ڈائمنڈز، گفٹ کارڈز دستیاب ہیں۔\nخریداری کے لیے ایڈمن سے رابطہ کریں۔",
        "affiliate_info": "📈 ایفیلیئٹ مارکیٹنگ\n\nپروڈکٹس کی تشہیر کر کے کمیشن کمائیں۔\nتفصیل کے لیے ایڈمن سے رابطہ کریں۔",
        "back_menu": "⬅ مینو پر واپس"
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

def points_to_mb(points):
    return int(points * (MB_RATE / 100))

def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(t(user_id, "watch_ads"), callback_data="watch_ad"),
        InlineKeyboardButton(t(user_id, "balance"), callback_data="balance"),
        InlineKeyboardButton(t(user_id, "referral"), callback_data="referral"),
        InlineKeyboardButton(t(user_id, "stats"), callback_data="stats"),
        InlineKeyboardButton(t(user_id, "withdraw_mb"), callback_data="withdraw_mb"),
        InlineKeyboardButton(t(user_id, "withdraw_usdt"), callback_data="withdraw_usdt"),
        InlineKeyboardButton(t(user_id, "premium"), callback_data="premium"),
        InlineKeyboardButton(t(user_id, "paid_content"), callback_data="paid_content"),
        InlineKeyboardButton(t(user_id, "digital_goods"), callback_data="digital_goods"),
        InlineKeyboardButton(t(user_id, "affiliate"), callback_data="affiliate"),
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
    bot.edit_message_text(t(user_id, "welcome"), user_id, call.message.message_id, reply_markup=main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "language")
def language(call):
    user_id = call.message.chat.id
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"),
        InlineKeyboardButton("اردو 🇵🇰", callback_data="set_lang_ur")
    )
    bot.edit_message_text(t(user_id, "choose_lang"), user_id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "watch_ad")
def watch_ad(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    today = str(datetime.date.today())
    if user.get("last_ad") != today:
        update_user(user_id, {"ads_today": 0, "last_ad": today})
        user = get_user(user_id)
    daily_limit = 100 if user.get("premium") else 30
    if user["ads_today"] >= daily_limit:
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
    daily_limit = 100 if user.get("premium") else 30
    if user["ads_today"] >= daily_limit:
        bot.answer_callback_query(call.id, t(user_id, "ad_limit"), show_alert=True)
        return
    points = 2 if user.get("premium") else 1
    add_points(user_id, points)
    update_user(user_id, {"ads_today": user["ads_today"] + 1})
    bot.answer_callback_query(call.id, t(user_id, "ad_earned"), show_alert=True)
    bot.send_message(user_id, t(user_id, "ad_earned_msg"), reply_markup=main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "balance")
def balance(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    dollars = points_to_dollars(user['points'])
    mb = points_to_mb(user['points'])
    premium = "✅" if user.get("premium") else "❌"
    bot.send_message(user_id, t(user_id, "balance_msg").format(points=user['points'], dollars=dollars, mb=mb, refs=user.get('referrals', 0), premium=premium), reply_markup=main_menu(user_id))
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "referral")
def referral(call):
    user_id = call.message.chat.id
    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={user_id}"
    user = get_user(user_id)
    bot.send_message(user_id, t(user_id, "referral_msg").format(link=link, refs=user.get('referrals', 0)), reply_markup=main_menu(user_id))
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "stats")
def stats(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    dollars = points_to_dollars(user['points'])
    bot.send_message(user_id, t(user_id, "stats_msg").format(points=user['points'], dollars=dollars, ads=user['ads_watched'], today=user['ads_today'], refs=user.get('referrals', 0)), reply_markup=main_menu(user_id))
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "withdraw_mb")
def withdraw_mb(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    mb = points_to_mb(user['points'])
    if mb >= MIN_MB:
        bot.send_message(user_id, t(user_id, "mb_info").format(mb=mb, min_mb=MIN_MB))
        bot.register_next_step_handler_by_chat_id(user_id, process_mb_phone)
    else:
        bot.send_message(user_id, t(user_id, "mb_not_ready").format(mb=mb, min_mb=MIN_MB), reply_markup=main_menu(user_id))
    bot.answer_callback_query(call.id)

def process_mb_phone(message):
    user_id = message.chat.id
    phone = message.text.strip()
    user = get_user(user_id)
    mb = points_to_mb(user['points'])
    update_user(user_id, {"phone": phone})
    bot.send_message(user_id, t(user_id, "mb_sent").format(phone=phone, mb=mb), reply_markup=main_menu(user_id))
    try:
        bot.send_message(ADMIN_ID, f"📱 MB Request\n\nUser: {user_id}\nPhone: {phone}\nMB: {mb}")
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == "withdraw_usdt")
def withdraw_usdt(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    dollars = points_to_dollars(user['points'])
    refs = user.get('referrals', 0)
    if dollars >= MIN_WITHDRAW_DOLLARS and refs >= MIN_REFERRALS:
        bot.send_message(user_id, t(user_id, "usdt_info").format(dollars=dollars, min_dollars=MIN_WITHDRAW_DOLLARS, refs=refs, min_refs=MIN_REFERRALS))
        bot.register_next_step_handler_by_chat_id(user_id, process_usdt_wallet)
    else:
        bot.send_message(user_id, t(user_id, "usdt_not_ready").format(min_dollars=MIN_WITHDRAW_DOLLARS, min_refs=MIN_REFERRALS, dollars=dollars, refs=refs), reply_markup=main_menu(user_id))
    bot.answer_callback_query(call.id)

def process_usdt_wallet(message):
    user_id = message.chat.id
    wallet = message.text.strip()
    user = get_user(user_id)
    dollars = points_to_dollars(user['points'])
    update_user(user_id, {"wallet": wallet})
    bot.send_message(user_id, t(user_id, "usdt_sent").format(wallet=wallet, amount=dollars), reply_markup=main_menu(user_id))
    try:
        bot.send_message(ADMIN_ID, f"💸 USDT Request\n\nUser: {user_id}\nWallet: {wallet}\nAmount: ${dollars}\nReferrals: {user.get('referrals', 0)}")
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == "premium")
def premium(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    if user.get("premium"):
        bot.answer_callback_query(call.id, t(user_id, "premium_already"), show_alert=True)
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, "premium_buy").format(price=PREMIUM_PRICE), callback_data="buy_premium"))
    markup.add(InlineKeyboardButton(t(user_id, "back_menu"), callback_data="back_menu"))
    bot.edit_message_text(t(user_id, "premium_info").format(price=PREMIUM_PRICE), user_id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "buy_premium")
def buy_premium(call):
    user_id = call.message.chat.id
    try:
        bot.send_invoice(chat_id=user_id, title="Premium Subscription", description="Unlimited ads + 2x points", invoice_payload="premium_purchase", provider_token="", currency="XTR", prices=[LabeledPrice(label="Premium", amount=PREMIUM_PRICE)])
    except Exception as e:
        bot.answer_callback_query(call.id, f"Error: {e}", show_alert=True)

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    user_id = message.chat.id
    update_user(user_id, {"premium": True})
    bot.send_message(user_id, t(user_id, "premium_success"), reply_markup=main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "paid_content")
def paid_content(call):
    user_id = call.message.chat.id
    user = get_user(user_id)
    if user.get("channel_access"):
        bot.answer_callback_query(call.id, t(user_id, "paid_content_already"), show_alert=True)
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, "paid_content_buy").format(price=PAID_CONTENT_PRICE), callback_data="buy_paid_content"))
    markup.add(InlineKeyboardButton(t(user_id, "back_menu"), callback_data="back_menu"))
    bot.edit_message_text(t(user_id, "paid_content_info").format(price=PAID_CONTENT_PRICE), user_id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "buy_paid_content")
def buy_paid_content(call):
    user_id = call.message.chat.id
    try:
        bot.send_invoice(chat_id=user_id, title="Paid Content Access", description="Private channel access", invoice_payload="paid_content_purchase", provider_token="", currency="XTR", prices=[LabeledPrice(label="Access", amount=PAID_CONTENT_PRICE)])
    except Exception as e:
        bot.answer_callback_query(call.id, f"Error: {e}", show_alert=True)

@bot.message_handler(content_types=['successful_payment'])
def successful_payment_paid(message):
    user_id = message.chat.id
    update_user(user_id, {"channel_access": True})
    try:
        link = bot.create_chat_invite_link(PREMIUM_CHANNEL_ID, member_limit=1)
        bot.send_message(user_id, t(user_id, "paid_content_success").format(link=link.invite_link), reply_markup=main_menu(user_id))
    except:
        bot.send_message(user_id, "✅ Access granted! Contact admin for channel link.", reply_markup=main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "digital_goods")
def digital_goods(call):
    user_id = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, "back_menu"), callback_data="back_menu"))
    bot.edit_message_text(t(user_id, "digital_goods_info"), user_id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "affiliate")
def affiliate(call):
    user_id = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, "back_menu"), callback_data="back_menu"))
    bot.edit_message_text(t(user_id, "affiliate_info"), user_id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_menu")
def back_menu(call):
    user_id = call.message.chat.id
    bot.edit_message_text(t(user_id, "welcome"), user_id, call.message.message_id, reply_markup=main_menu(user_id))
    bot.answer_callback_query(call.id)

print("Bot is running...")
bot.infinity_polling()
