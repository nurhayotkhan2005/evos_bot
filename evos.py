from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application,MessageHandler,CommandHandler,CallbackQueryHandler,filters,ContextTypes
TOKEN = '8960031038:AAHvZ9kRcWgJxRlDtF6iySotdnf4Td_bHEk'

user_language = {}
user_card = {}
waiting_for_fedback = {}
waiting_for_address = {}

TEXT = {
    "start" : {
        "uz": "Quyidagilardan birini tanlang:",
        "ru": "Выберите одно из следующего:",
        "en": "Please select one of the following:"
    },
      "feedback_received": {
        "uz": "✅ Qabul qilindi, rahmat! 😊",
        "ru": "✅ Получено, спасибо! 😊",
        "en": "✅ Received, thank you! 😊"
    },
    "feedback" :{
        "uz": "Fikringizni yozib qoldiring:",
        "ru": "Оставьте свой отзыв:",
        "en": "Leave your feedback:"
    },
    "adress": {
        "uz" : "Iltimos, yetkazib berish manzilingizni matn ko'rinishida kiriting:",
        "ru" : "Пожалуйста, введите адрес доставки в виде текста:",
        "en" : "Please enter your delivery address as text:"
    },
    "address_saved": {
        "uz": "✅ Manzilingiz saqlandi: {}",
        "ru": "✅ Ваш адрес сохранен: {}",
        "en": "✅ Your address has been saved: {}"
    },
       "settings_language": {
        "uz": "Tilni tanlang:",
        "ru": "Выберите язык:",
        "en": "Choose a language:"
    },


     "order_confirmed": {
        "uz": "🎉 Buyurtmangiz qabul qilindi! Tez orada yetkazib beriladi. 🚀",
        "ru": "🎉 Ваш заказ принят! Скоро он будет доставлен. 🚀",
        "en": "🎉 Your order has been accepted! It will be delivered soon. 🚀"
    },
    "order_empty": {
        "uz": "🛒 Savatchangiz bo'sh!",
        "ru": "🛒 Ваша корзина пуста!",
        "en": "🛒 Your cart is empty!"
    }
}

MENU_BUTTONS = {
    "uz": ["🍴 Menyu", "🛍 Mening buyurtmalarim", "📍 Manzilni sozlash", "✍️ Fikir bildirish", "⚙️ Sozlamalar","tasdiqlash"],
    "ru": ["🍴 Меню", "🛍 Мои заказы", "📍 Настроить адрес", "✍️ Оставить отзыв", "⚙️ Настройки",'Подтвердить'],
    "en": ["🍴 Menu", "🛍 My Orders", "📍 Set Address", "✍️ Feedback", "⚙️ Settings",'confirm']
}

LANG_BUTTONS = {
    "uz": [("🇺🇿 O'zbekcha", "lang_uz"), ("🇷🇺 Русский", "lang_ru"), ("🇬🇧 English", "lang_en")],
    "ru": [("🇺🇿 Узбекский", "lang_uz"), ("🇷🇺 Русский", "lang_ru"), ("🇬🇧 Английский", "lang_en")],
    "en": [("🇺🇿 Uzbek", "lang_uz"), ("🇷🇺 Russian", "lang_ru"), ("🇬🇧 English", "lang_en")]
}

Menyu_buttons = {
    "uz" : [
        {"Lavash 🌯": 20000},
        {"Hot-dog 🌭":13000},
        {"Sandwich 🥪": 16000},
        {"Burger 🍔": 18000},
        {"Pepsi 0.5": 10000},
        {"Cola 0.5": 10000}
    ],
"ru": [
     {"Лаваш 🌯": 20000},
     {"Хот-дог 🌭":13000},
     {"Сэндвич 🥪": 16000},
     {"Бургер 🍔": 18000},
     {"Pepsi 0.5": 10000},
     {"Cola 0.5": 10000}
    ],
"en": [
     {"Lavash 🌯": 20000},
     {"Hot-dog 🌭":13000},
     {"Sandwich 🥪": 16000},
     {"Burger 🍔": 18000},
     {"Pepsi 0.5": 10000},
     {"Cola 0.5": 10000}
    ]
}
back = {"uz":"Menyuga qaytish","ru":"к меню","en":"back-to main"}

def start_button(chat_id):
    lang = user_language.get(chat_id,"uz")
    buttons = MENU_BUTTONS[lang]
    keyboard = [
        [KeyboardButton(text=buttons[0])],
        [KeyboardButton(text=buttons[1]),KeyboardButton(text=buttons[2])],
        [KeyboardButton(text=buttons[3]),KeyboardButton(text=buttons[4])],
        [KeyboardButton(text=buttons[5])]
    ]
    return ReplyKeyboardMarkup(keyboard,resize_keyboard=True)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_language.get(chat_id,"uz")
    reply_text1 =  TEXT["start"][lang]
    await update.message.reply_text(reply_text1,reply_markup=start_button(chat_id))

def sanash():
     keyboard = [
          [
               InlineKeyboardButton(text="1",callback_data="sana_1"),
               InlineKeyboardButton(text="2",callback_data="sana_2"),
               InlineKeyboardButton(text="3",callback_data="sana_3"),
               InlineKeyboardButton(text="4",callback_data="sana_4"),
               InlineKeyboardButton(text="5",callback_data="sana_5")
               
           ]
     ]
     return InlineKeyboardMarkup(keyboard)

def lang_button(chat_id):
    lang = user_language.get(chat_id,"uz")
    keyboard = []

    for text,data in LANG_BUTTONS[lang]:
        keyboard.append([InlineKeyboardButton(text=text,callback_data=data)])
    return InlineKeyboardMarkup(keyboard)

def menu_buttons(chat_id):
    lang = user_language.get(chat_id,"uz")
    buttons = Menyu_buttons[lang]
    back_button = back[lang]
    keyboard = []
    for taomlar in range(0,len(buttons),2):
        juftlik = buttons[taomlar:taomlar+2]
        qator = []
        for taom in juftlik:
            qator.append(KeyboardButton(text=list(taom.keys())[0]))
        keyboard.append(qator)
    keyboard.append([KeyboardButton(text=back_button)])   

    return ReplyKeyboardMarkup(keyboard,resize_keyboard=True)

async def lang_control(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    lang = user_language.get(chat_id,"uz")
    data = query.data

    if data.startswith("lang_"):
        yangi_til = data[5:]
        user_language[chat_id] = yangi_til
        if yangi_til == "uz":
            til = "O'zbek tili tanlandi!"
        elif yangi_til == "ru":
            til = "Выбран русский язык!"
        elif yangi_til == "en":
            til = "English language selected!"
        await query.edit_message_text(text=til)

        await context.bot.send_message(
          chat_id=chat_id,
          text=TEXT["start"][yangi_til],
          reply_markup=start_button(chat_id)
          )
    elif data.startswith("sana_"):
        miqdor = int(data[5:])

        caption = query.message.caption
        if not caption:
            return
        taom_line = caption.split("\n")[0]  
        taom_nomi = taom_line.replace("Taom: ", "").split(" narxi:")[0].strip()
          
        if chat_id not in user_card:
            user_card[chat_id] = {}
        user_card[chat_id][taom_nomi] = miqdor

        if lang == "uz":
               m_text = f"✅ {taom_nomi} x {miqdor} savatchaga qo'shildi!"
        elif lang == "ru":
               m_text = f"✅ {taom_nomi} x {miqdor} добавлено в корзину!"
        elif lang == "en":
               m_text = f"✅ {taom_nomi} x {miqdor} added to cart!"
          
        await context.bot.send_message(
               chat_id=chat_id,
               text=m_text

          )
    elif data == "confirm_order":

          if chat_id in user_card and user_card[chat_id]:
               user_card[chat_id] = {}

               await query.edit_message_text(
                    text=TEXT["order_confirmed"][lang]
               )

               await context.bot.send_message(
                    chat_id=chat_id,
                    text=TEXT["start"][lang],
                    reply_markup=menu_buttons(chat_id)
        )

          else:
               await query.edit_message_text(
                    text=TEXT["order_empty"][lang]
               )

        
    

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    chat_id = update.effective_chat.id
    lang = user_language.get(chat_id,"uz")

    if matn == MENU_BUTTONS[lang][0]:
        await update.message.reply_text(TEXT["start"][lang],
                                        reply_markup=menu_buttons(chat_id))
    elif waiting_for_address.get(chat_id):
        waiting_for_address[chat_id] = False
        await update.message.reply_text(TEXT["address_saved"][lang].format(matn),
                                        reply_markup=start_button(chat_id))
    elif matn == MENU_BUTTONS[lang][1]:
        cart = user_card.get(chat_id,{})
        if not cart:
            await update.message.reply_text(text=TEXT["order_empty"][lang])
            return
        if lang == "uz":
            savatcha_matni = "**Sizning savatchangiz:**\n\n"
        elif lang == "ru":
            savatcha_matni = "**Ваша корзина:**\n\n"
        elif lang == "en":
            savatcha_matni = "**Your card:**\n\n"
        narxlar_dict = {}
        for l in ["uz", "ru", "en"]:
            for t_dict in Menyu_buttons[l]:
                    t_nomi = list(t_dict.keys())[0]
                    t_narxi = list(t_dict.values())[0]
                    narxlar_dict[t_nomi] = t_narxi

          # Savat ichidagi narsalarni bittalab aylanamiz

        umumiy_narx = 0
        for taom, miqdor in cart.items():
               narx = narxlar_dict.get(taom, 0) # o'sha taomning narxini topamiz
               jami_taom_narxi = narx * miqdor  # nechta olgan bo'lsa ko'paytiramiz
               umumiy_narx += jami_taom_narxi   # umumiy hisobga qo'shamiz
               
               savatcha_matni += f"🔹 {taom} \n   {miqdor} dona x {narx:,} = {jami_taom_narxi:,} UZS\n\n"
        if lang == "uz":
               savatcha_matni += f"🏁 **Umumiy summa: {umumiy_narx:,} UZS**"
        elif lang == "ru":
               savatcha_matni += f"🏁 **Итоговая сумма: {umumiy_narx:,} UZS**"
        else:
               savatcha_matni += f"🏁 **Total amount: {umumiy_narx:,} UZS**"
        await update.message.reply_text(text=savatcha_matni, parse_mode="Markdown")
        return
  
    elif matn == MENU_BUTTONS[lang][2]:
        waiting_for_address[chat_id] = True
        await update.message.reply_text(
            text=TEXT["adress"][lang]
        )
        
        
    elif waiting_for_fedback.get(chat_id):
        waiting_for_fedback[chat_id] = False
        await update.message.reply_text(TEXT["feedback_received"][lang],
                                        reply_markup=start_button(chat_id))
    elif matn == MENU_BUTTONS[lang][3]:
        waiting_for_fedback[chat_id] = True
        await update.message.reply_text(text = TEXT["feedback"][lang])
    elif matn == MENU_BUTTONS[lang][4]:
        await update.message.reply_text(
            TEXT['settings_language'][lang],
            reply_markup=lang_button(chat_id)
        )

    elif matn == MENU_BUTTONS[lang][5]:
        await update.message.reply_text(
            text=TEXT["order_confirmed"][lang],
            reply_markup=start_button(chat_id)
        )
        user_card.pop(chat_id, None)

    elif matn == "Menyuga qaytish" or matn == "back-to main" or matn == "к меню":
        await update.message.reply_text(TEXT["start"][lang],
                                        reply_markup=start_button(chat_id))
    
    elif matn in Menyu_buttons[lang][0]:
        nom = matn
        narx = Menyu_buttons[lang][0][matn]
        await update.message.reply_photo(photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlaIQrcbBdWXoZCJhgFMFOQ6wcqAOKzKKP89gLPe-X0AwtIpBn37gXosru&s=10',
                                         caption=f"{nom.capitalize()} \nnarxi: {narx} so'm",
                                             reply_markup=sanash())
    elif matn in Menyu_buttons[lang][1]:
        nom = matn
        narx = Menyu_buttons[lang][1][matn]
        await update.message.reply_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbzxy1qoS0ptyyesmaV--b0kNU3igq0YMURjjfxw09Nr_HEU8J5fZxZk-9&s=10",
                                         caption=f"{nom.capitalize()}\nNarxi: {narx} so'm",
                                         reply_markup=sanash())
    elif matn in Menyu_buttons[lang][2]:
        nom = matn
        narx = Menyu_buttons[lang][2][matn]
        await update.message.reply_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQHl5eb9sedGteCN7PZxWptTDDzBHHAhLy5ToEDTk3uw&s=10",
                                        caption=f"{nom.capitalize()}\nNarxi: {narx} so'm",reply_markup=sanash())
    elif matn in Menyu_buttons[lang][3]:
        nom = matn
        narx = Menyu_buttons[lang][3][matn]
        await update.message.reply_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRt7TrTfsv-LJkPOEDnSFJ2spNbv363VF632kEkjN0Mjfvtbz5KmAnrEHjT&s=10",
                                         caption=f"{nom.capitalize()}\nNarxi: {narx} so'm",
                                         reply_markup=sanash())
    elif matn in Menyu_buttons[lang][4]:
        nom = matn
        narx = Menyu_buttons[lang][4][matn]
        await update.message.reply_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDcTQdScclWp1lgPOuDJwG_OdaTQPmNuX4zOSKZLZV8o1BoemDPiJsUbw&s=10",
                                         caption=f"{nom.capitalize()}\nNarxi: {narx} so'm",
                                         reply_markup=sanash())
    elif matn in Menyu_buttons[lang][5]:
        nom = matn
        narx = Menyu_buttons[lang][5][matn]
        await update.message.reply_photo(photo="https://dostavo4ka.uz/upload-file/2021/07/01/6220/750x750-714ef3dc-6439-4bb3-9885-d9334ea52fd9.jpg",
                                         caption=f"{nom.capitalize()}\nNarxi: {narx} so'm",
                                         reply_markup=sanash())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))
    app.add_handler(CallbackQueryHandler(lang_control))
    print("Bot ishga tushdi..")
    app.run_polling()

if __name__ == "__main__":
    main()