# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Translator-Bot/blob/main/LICENSE

import os
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator

FayasNoushad = Client(
    "Translator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """
Hello {}, Saya adalah bot google penerjemah.

▪ **Managed by:** [Ebnu](https://t.me/ebnudoang)
▪ **Cara penggunaan:** [lihat disini](https://telegra.ph/file/129d5beabc0005f3eda7d.mp4)
▪ **Daftar kode bahasa:** [lihat disini](https://telegra.ph/-08-14-3100)
"""
HELP_TEXT = """
- Cukup kirim kata kata dengan kode bahasa

Contoh :- `Hallo selamat pagi | en (kode bahasa)`

Made by [Ebnu](https://t.me/ebnudoang)
"""
ABOUT_TEXT = """
- **Bot :** `Translator Bot`
- **Creator :** [Ebnu](https://t.me/ebnudoang)
- **Channel :** [Klik disini](https://t.me/Katakatauntukmu)
- **Instagram :** [Klik disini](https://www.instagram.com/ebnu_am/)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://t.me/katakatauntukmu'),
        InlineKeyboardButton('Feedback', url='https://t.me/ebnudoang')
        ],[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
CLOSE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
TRANSLATE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://t.me/katakatauntukmu')
        ]]
    )
DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "en")

@FayasNoushad.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()
    

@FayasNoushad.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@FayasNoushad.on_message((filters.private | filters.group | ~filters.channel) & filters.text)
async def translate(bot, update):
    if update.chat.type == "private":
        if " | " in update.text:
            text, language = update.text.split(" | ", 1)
        else:
            text = update.text
            language = DEFAULT_LANGUAGE
    else:
        text = update.reply_to_message.text
        if " " in update.text:
            command, language = update.text.split(" | ", 1)
        else:
            language = DEFAULT_LANGUAGE
    translator = Translator()
    await update.reply_chat_action("typing")
    message = await update.reply_text("`Translating...`")
    try:
        translate = translator.translate(text, dest=language)
        translate_text = f"**Translated to {language}**"
        translate_text += f"\n\n{translate.text}"
        translate_text += "\n\nMade by @ebnudoang"
        if len(translate_text) < 4096:
            await message.edit_text(
                text=translate_text,
                disable_web_page_preview=True,
                reply_markup=TRANSLATE_BUTTON
            )
        else:
            with BytesIO(str.encode(str(translate_text))) as translate_file:
                translate_file.name = language + ".txt"
                await update.reply_document(
                    document=translate_file,
                    caption="Made by @ebnudoang",
                    reply_markup=TRANSLATE_BUTTON
                )
                await message.delete()
    except Exception as error:
        print(error)
        await message.edit_text("Something wrong. Contact @ebnudoang.")
        return

FayasNoushad.run()
