from datetime import datetime
import os
import pandas as pd

import re, string, regex
from unidecode import unidecode as remove_accents

from abc import ABC
import telebot
from telebot import types


from modules.extractors.Entities import Entities
from modules.extractors.Sets import Sets
from modules.recognize.SetRecognizer import SetRecognizer
from modules.recognize.EntityRecognizer import EntityRecognizer

class Bot(ABC):
	def __init__(self, TELEGRAM_TOKEN, flows):
		self.bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode='HTML')
		self.data = pd.DataFrame()
		self.flows = flows

	def prepare(self):
		self.sets = Sets().get()
		self.entities = Entities().get()
		print('--- Extracted Sets ---')
		print(self.sets)
		print('--- Extracted Entities ---')
		print(self.entities)
		self.set_recognizer = SetRecognizer(self.sets)
		self.entity_recognizer = EntityRecognizer(self.entities)


		self.metadata = {
			'intent': [],
			'entity': [],
		}


	def run(self):
		@self.bot.message_handler(commands=['send'])
		def send_to_all_chats(message):
			# This method is to exemplify how to send a message to all chat ids
			# It's also possible to send photo, audio, etc... 
			self.message = message
			self.getData()

			to_send = self.user_message.split('/send ')[1:]
			if not to_send:
				self.bot.send_message(self.chatId, 'Me diga o que devo enviar para os usuários. Ex: /send Opa rapá. Joia?')
			else:
				data = return_all_reports_in_one()
				all_chat_ids = data['chat_id'].unique()
				for chat_id in all_chat_ids:
					try:
						self.bot.send_message(chat_id, to_send)
					except:
						print('não enviou mensagem para o chat:',chat_id)

		def return_all_reports_in_one():
			filenames = list(os.walk('reports'))[0][2]
			df = pd.DataFrame()
			for file in filenames:
				df = df.append(pd.read_csv(f'reports/{file}'))
			return df

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
		self.clear_user_message()

		self.bot_responses = ["Hey! I'm a simple bot"]
		[self.bot.send_message(self.chatId, bot_response) for bot_response in self.bot_responses]

		self.storeData()
		#if self.datetime.hour % 6 == 0:
		self.saveData()

	def getData(self):
		self.user_message = self.message.text
		self.chatId = self.message.chat.id
		self.datetime = datetime.now()
		self.context = ''

	def clear_user_message(self):
		#self.original_text = self.user_message
		self.user_message = self.user_message.lower()
		self.user_message = re.sub(' +', ' ', self.user_message)
		self.user_message = remove_accents(self.user_message)
		self.user_message = self.user_message.strip()
		self.user_message = self.user_message.translate(str.maketrans('', '', string.punctuation))
		
	def storeData(self):
		self.data = self.data.append({
			'chat_id': self.chatId,
			'session': self.session,
			'user_message': self.user_message,
			'bot_response': self.bot_responses,
			'metadata': self.metadata,
			'context': self.context,
			'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
			'telegram_message_data': self.message,
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
		try:
			self.session = len(self.userHistory['sessions'].unique())
		except KeyError:
			self.session = 0

	def put_variables_in_bot_responses_if_there(self):
		for j, self.bot_response in enumerate(self.bot_responses):
			r = regex.compile(r'\{((?:[^{}]|(?R))+)\}')
			variation = 0
			self.counter = {'intent': 0, 'entity': 0}
			for m in r.finditer(self.bot_response):
				captured = m.captures()[0][1:-1] # ['{intent}'] --> 'intent'
				to_replace = self.get_variable_to_replace(captured)
				self.counter[captured] += 1

				start_index, end_index = m.start()+variation, m.end()+variation
				self.bot_responses[j] = self.bot_responses[j][:start_index] + to_replace + self.bot_responses[j][m.end():]

				variation += (m.end() - m.start()) - (len(captured) + 3) 

		return self.bot_responses

	def get_variable_to_replace(self, captured):
		try:
			last_index = -1-self.counter[captured]
			print('captured:',captured)
			if captured == 'entity':
				entity = list(self.metadata[captured][last_index].values()) # device
				print('entity:',entity)
				return list(entity[0].keys())[0] # computer
			elif captured == 'intent':
				return list(self.metadata[captured][last_index].keys())[0]
			raise Exception(f"For some reason, the bot can't to find the metadata. Check out the name in the brackets in the bot message: '{self.bot_response}'; and the metadata.\nMetadata:",self.metadata)
		except Exception as e:
			raise Exception(f"For some reason,{e}... the bot can't to find the metadata. Check out the name in the brackets in the bot message: '{self.bot_response}'; and the metadata.\nMetadata:",self.metadata)

	def get_buttons_in_telegram_format(self, buttons):
		markup = types.ReplyKeyboardMarkup(row_width=2)
		[markup.add(types.KeyboardButton(button)) for button in buttons]
		return markup