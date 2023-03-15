#!/bin/python3

# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import pandas as pd
import datetime
from telegram import __version__ as TG_VER

def getTime():
    current_time = datetime.datetime.now()
    today = datetime.date.today()

    return current_time.strftime("%H:%M:%S"), today.strftime("%A")

time_hour, time_day = getTime()

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

def loadData():
    return pd.read_csv('orari1.csv'), pd.read_csv('orari2.csv'), pd.read_csv('orari3.csv')

def uni_city():
    tmpList = []
    for index, row in ing_city.iterrows():
        if row['ora'] >= time_hour:
            if ing_city.loc[index]['flag'] == 1:
                tmpList.append(["Fermata Ingegneria", ing_city.loc[index]['ora'], "Barrata"])
            else:
                tmpList.append(["Fermata Ingegneria", ing_city.loc[index]['ora'], ""])
            break
    
    for index, row in mensa_city.iterrows():
        if row['ora'] >= time_hour:
            if mensa_city.loc[index]['flag'] == 1:
                tmpList.append(["Fermata Mensa", mensa_city.loc[index]['ora'], "Barrata"])
            else:
                tmpList.append(["Fermata Mensa", mensa_city.loc[index]['ora'], ""])
            break
    
    return tmpList

def city_uni():
    tmpList = []
    for index, row in city_ing.iterrows():
        if row['ora'] >= time_hour:
            if city_ing.loc[index]['flag'] == 1:
                tmpList.append(["Fermata City Terminal", city_ing.loc[index]['ora'], "Barrata"])
            else:
                tmpList.append(["Fermata City Terminal", city_ing.loc[index]['ora'], ""])
            break
    
    return tmpList

def writeMessage(choice):
    listaOrari = []
    result = ""
    if choice == 0:
        listaOrari = uni_city()
    else:
        listaOrari = city_uni()

    for item in listaOrari:
        row = f"{item[0]}: {item[1]}\n"
        result = result + row
    
    return result

city_ing, ing_city, mensa_city = loadData()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html("Ciao! Il Bot è attivo")

async def uni_city_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    time_hour, time_day = getTime()
    user = update.effective_user
    testo = writeMessage(0)

    await update.message.reply_html(testo)

async def city_uni_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    time_hour, time_day = getTime()
    user = update.effective_user
    testo = writeMessage(1)

    await update.message.reply_html(testo)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop the bot"""
    await update.message.reply_text("Stopping the bot...")
    context.application.stop()


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5845843026:AAF-dFgvKTanXqGpcCaWuSxDtnhUSVuD0oY").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("uni_city",uni_city_handler))
    application.add_handler(CommandHandler("city_uni", city_uni_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()