#!/usr/bin/env python3
"""Telegram бот Го — только Mini App."""

import os, json

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, MenuButtonDefault
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "")


def wa(sz=9):
    return WebAppInfo(url=f"{WEBAPP_URL}?start={sz}")


async def start(update, _):
    await update.get_bot().set_chat_menu_button(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonDefault(),
    )
    await update.message.reply_text(
        "Нажми кнопку ниже ⬇️",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🎮 Играть", web_app=wa(9)),
        ]]),
    )


async def newgame(update, _):
    await update.get_bot().set_chat_menu_button(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonDefault(),
    )
    await update.message.reply_text(
        "Нажми кнопку ниже ⬇️",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🎮 Играть", web_app=wa(9)),
        ]]),
    )


async def cb_webapp(update, _):
    data = json.loads(update.message.web_app_data.data)
    sc = data.get("score", {})
    w = data.get("winner", "?")
    mv = data.get("moves", 0)
    await update.message.reply_text(
        f"🏁 <b>Игра завершена!</b>\n"
        f"⚫ Чёрные: {sc.get('black', 0)} | ⚪ Белые: {sc.get('white', 0)}\n"
        f"Ходов: {mv} | Победитель: {w}\n\n"
        f"/newgame — сыграть ещё",
        parse_mode=ParseMode.HTML,
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newgame", newgame))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, cb_webapp))
    print("🤖 Go Bot запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
