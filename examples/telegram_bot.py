"""
This is a basic telegram bot that can send your Finalynx portfolio as an image message.

Setup steps:
    1. Watch the beginner tutorial and follow the steps to create your own bot:
        > https://www.youtube.com/watch?v=vZtm1wuA2yc

    2. Install the python package that implements a python bot handler:
        > pip install python-telegram-bot

    3. Set the constant variables:
        > TOKEN is the Telegram bot token given when you created your bot with @FatherBot
        > BOT_USERNAME is the bot username you chose when you created your bot
        > CONFIG_PATH is either a relative path from this file location to your config,
          or an absolute path to your python config.

    4. Search for your own bot username on Telegram and start a conversation

    5. Run the /portfolio command and get your up-to-date portfolio as an image!

NOTE: If you cloned this repo (you're probably a contributor), don't set your own private
information in this file as you might accidentally commit your changes to GitHub. Instead,
create your own copy of this file somewhere outside this repo and set your constants there.
"""
# type: ignore
import os
from typing import Final

from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import MessageHandler


# SET YOUR OWN INFORMATION HERE
API_TOKEN: Final = "YOUR_BOT_API_KEY"
BOT_USERNAME: Final = "@MyFinalynxBot"
CONFIG_PATH: Final = "demo.py"


# Lets us use the /start command
async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello there! Use the /portfolio command to generate a fresh image of your Finalynx portfolio 👀"
    )


# Lets us use the /help command
async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /portfolio to display your portfolio")


# Lets us use the /portfolio command
async def command_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Generating your portfolio...")
    full_path = os.path.join(os.path.dirname(__file__), CONFIG_PATH)
    os.system(f"python3 {full_path} --no-export -c")
    await update.message.reply_photo("portfolio.png")


def handle_response(text: str) -> str:
    """To be improved one day, feature requests welcome :)"""
    processed: str = text.lower()
    if "hello" in processed:
        return "Hey there!"
    if "how are you" in processed:
        return "I'm good!"
    return "I don't understand"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type} chat said: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == "group":
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print("Bot reponse:", response)
    await update.message.reply_text(response)


# Log errors
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print(f"Starting up bot {BOT_USERNAME}...")
    app = Application.builder().token(API_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", command_start))
    app.add_handler(CommandHandler("help", command_help))
    app.add_handler(CommandHandler("portfolio", command_portfolio))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(handle_error)

    # Run the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
