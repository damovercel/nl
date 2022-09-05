#!/bin/python3

from telegram import InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ, mkdir
from lxml.html import fromstring
from time import sleep
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
NLS = load(open("./nls.json"))
WEB_HEADERS = CONFIG["WEB_HEADERS"]
WEB_BROWSER = CONFIG["WEB_BROWSER"]
URL_NARTAG = CONFIG["URL_NARTAG"]

scraper = create_scraper(browser=WEB_BROWSER)

def printt(*values):
	rep = ""
	if len(values) == 1:
		rep += str(values[0])
	else:
		for c in values:
			rep += f"{c}\n"
	bot.send_message(chat_id=DEBUG_ID, text=rep)




def command_start(update, context):
	chatId = update["message"]["chat"]["id"]
	print("/start")
	print(NLS.keys())
	#print(update)
	bot.send_message(chat_id=chatId, text="Still under construction...")

def command_demo(update, context):
	chatId = update["message"]["chat"]["id"]
	print("/demo")
	#print(NLS.keys())
	#print(update)
	bot.send_message(chat_id=chatId, text="Working")
	raw_page = scraper.get(url=f'{URL_NARTAG}/el-principio-despues-del-fin-novela')
	printt(raw_page.status_code)
	print(raw_page.status_code)

	raw_tree = fromstring(html=raw_page.content)
	di_list = []
	ord_list = []
	for element in raw_tree.xpath('//*[@class="main version-chap no-volumn"]')[0]:
		sleep(1)
		print(element)
		printt(element)
		if element.tag == "li":
			if element.attrib["class"] == "wp-manga-chapter    ":
				di_list.append([element[0].text, element[0].attrib["href"]])
				printt(element[0].text, element[0].attrib["href"])
	ord_list = di_list[::-1]
	from ebooklib import epub

	bu = epub.EpubBook()
	bu.set_title("la vida despues de la muerte")
	cover = scraper.get(url="https://nartag.com/wp-content/uploads/2021/02/Portada-1-683x1024.jpg", stream=True)
	bu.set_cover("Cover.jpg", content=cover.content)
	bu.set_language("es")
	bu.add_author("d")
	caps = []
	inde = []
	for index, capitle in enumerate(ord_list):
		print(capitle)
		printt(capitle)
		raw_cap = scraper.get(url=capitle[1])
		raw_cap_tree = fromstring(html=raw_cap.content)
		exec(f'cap_{index} = epub.EpubHtml(title=capitle[0], file_name=f"{capitle[0]}.xhtml")')
		inde.append(epub.Link(f"{capitle[0]}.xhtml", capitle[0], "arbol"))
		caps.append(f"cap_{index}")
		cap_text = raw_cap_tree.xpath('//*[@class="text-left"]')[0].text_content()
		exec(f'cap_{index}.content = {cap_text}')

		bu.add_item(f"cap_{index}")

	bu.add_item(epub.EpubNcx())
	bu.add_item(epub.EpubNav())
	bu.toc = tuple(inde)
	print(tuple(inde))
	print(["cover"] + caps)
	#bu.toc = (epub.Link("chap_195.xhtml", "chap_195", "arbol"),)
	style = 'BODY {color: white;}'
	nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
	bu.add_item(nav_css)

	bu.spine = ["cover"] + caps

	epub.write_epub("vida.epub", bu)
	bot.send_document(chat_id=chatId, document=open(file="./vida.epub", mode="rb"))


	#raw_page = scraper.get(url=)

if __name__ == '__main__':
	updater = Updater(BOT_TOKEN)
	dispatcher = updater.dispatcher
	bot = updater.bot

	dispatcher.add_handler(CommandHandler(command="start", callback=command_start))
	dispatcher.add_handler(CommandHandler(command="demo", callback=command_demo))

	bot.send_message(chat_id=DEBUG_ID, text="Polling!!!")
	print("Polling!!!")
	updater.start_polling(drop_pending_updates=True)