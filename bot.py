#!/bin/python3

from telegram import InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ, mkdir
from lxml.html import fromstring
from json import load
from cloudscraper import create_scraper
# from urllib.parse import quote

###        								###
###        								###
###        								###
#print("arregral la linea 32, esta feisima")
###        								###
###    									###
###    									###

BOT_TOKEN = environ.get("BOT_TOKEN")
DEBUG_ID = environ.get("DEBUG_ID")


CONFIG = load(open("./config.json"))
WEB_HEADERS = CONFIG["WEB_HEADERS"]
WEB_BROWSER = CONFIG["WEB_BROWSER"]
URL_NARTAG = CONFIG["URL_NARTAG"]

scraper = create_scraper(browser=WEB_BROWSER)

def printt(*values):
	rep = ""
	if len(values) == 1:
		rep += values[0]
	else:
		for c in values:
			rep += f"{c}\n"
	bot.send_message(chat_id=DEBUG_ID, text=rep)




def command_start(update, context):
	chatId = update["message"]["chat"]["id"]
	print("/start")
	print(update)
	bot.send_message(chat_id=chatId, text="Still under creation...")

if __name__ == '__main__':
	updater = Updater(BOT_TOKEN)
	dispatcher = updater.dispatcher
	bot = updater.bot

	dispatcher.add_handler(CommandHandler(command="start", callback=command_start))

	bot.send_message(chat_id=DEBUG_ID, text="Polling!!!")
	print("Polling!!!")
	updater.start_polling(drop_pending_updates=True)