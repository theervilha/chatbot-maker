from datetime import datetime
import os
import pandas as pd
from abc import ABC
import telebot

from modules.extractors.Entities import Entities
from modules.extractors.Sets import Sets

class Bot(ABC):
	def __init__(self, TELEGRAM_TOKEN, flows):
		self.bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode='HTML')
		self.data = pd.DataFrame()
		self.flows = flows

	def prepare(self):
		self.sets = Sets().get()
		print(self.sets)
		self.entities = Entities().get()
		print(self.entities)
		#print(self.SetRecognizer.sets)


	def run(self):
		@self.bot.message_handler(func=lambda m: True)
		def processTextAndReply(message):
			self.message = message
			self.getUserHistory()
			self.getUserSession()
			self.processTextAndReply()


		@self.bot.message_handler(content_types=[
			"audio", "document", "photo", "sticker", "video", "video_note", "voice",
			"location", "contact", "new_chat_members", "left_chat_member", "new_chat_title",
			"new_chat_photo", "delete_chat_photo", "group_chat_created", "supergroup_chat_created",
			"channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id", "pinned_message"
		])
		def isNotText(message):
			self.bot.reply_to(message, "Poxa... eu só consigo entender quando você digita algo")

		self.bot.polling()

	def processTextAndReply(self):
		self.getData()

		self.bot_responses = ["Hey! I'm a simple bot"]
		[self.bot.send_message(self.chatId, bot_response) for bot_response in self.bot_responses]

		self.storeData()
		#if self.datetime.hour % 6 == 0:
		self.saveData()

	def getData(self):
		self.userMessage = self.message.text
		self.chatId = self.message.chat.id
		self.datetime = datetime.now()
		self.context = ''

	def storeData(self):
		self.data = self.data.append({
			'chat_id': self.chatId,
			'user_message': self.userMessage,
			'bot_response': self.bot_responses,
			'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
			'context': self.context,
		}, ignore_index=True)

	def saveData(self, path='reports'):
		if not os.path.exists(path):
			os.makedirs(path)

		date = datetime.now().strftime("%Y-%m-%d")
		self.data.to_csv(f'{path}/report - {date}.csv', index=False, encoding='utf-8')

	def getUserHistory(self):
		try:
			self.userHistory = self.data.loc[self.data['chat_id'] == self.chatId]
		except KeyError:
			self.userHistory = pd.DataFrame()

	def getUserSession(self):
		if len(self.userHistory) == 0:
			self.userSession = 'firstSession'
		else:
			self.userSession = 'anotherSession'