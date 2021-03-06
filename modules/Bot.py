from datetime import datetime
import os
import pandas as pd

import itertools
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
	def __init__(self, TELEGRAM_TOKEN, flows, GoTo, restart_bot_when_new_session = True):
		self.bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode='HTML')
		self.data = pd.DataFrame()
		self.flows = flows
		self.variables = {}
		self.restart_bot_when_new_session = restart_bot_when_new_session
		self.GoTo = GoTo(self)

	def prepare(self):
		self.sets = Sets().get()
		self.entities = Entities().get()
		self.set_recognizer = SetRecognizer(self.sets)
		self.entity_recognizer = EntityRecognizer(self.entities)

		self.metadata = {
			'intent': [],
			'entity': [],
		}

	def run(self):
		@self.bot.message_handler(func=lambda m: True)
		def processTextAndReply(message):
			self.message = message
			self.getData()
			self.get_user_history()
			self.get_user_session()
			if self.session_status == 'new session' and self.restart_bot_when_new_session:
				self.last_context = ''

			self.cleaned_user_message = self.clean_text(self.user_message)

			self.processTextAndReply()
		
		@self.bot.message_handler(content_types=[
			"audio", "document", "photo", "sticker", "video", "video_note", "voice",
			"location", "contact", "new_chat_members", "left_chat_member", "new_chat_title",
			"new_chat_photo", "delete_chat_photo", "group_chat_created", "supergroup_chat_created",
			"channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id", "pinned_message"
		])
		def isNotText(message):
			self.bot.reply_to(message, "Poxa... eu só consigo entender quando você digita algo em formato de texto")

		self.bot.polling()

	def getData(self):
		self.user_message = self.message.text
		self.chatId = self.message.chat.id
		self.datetime_user_message = datetime.now()
		self.last_context = ''

	def processTextAndReply(self):
		self.bot_responses = ["Hey! I'm a simple bot"]
		[self.bot.send_message(self.chatId, bot_response) for bot_response in self.bot_responses]

		self.storeData()
		#if self.datetime.hour % 6 == 0:
		self.saveData()

	def get_user_history(self):
		try:
			self.userHistory = self.data.loc[self.data['chat_id'] == self.chatId]
		except KeyError:
			self.userHistory = pd.DataFrame()

	def get_user_session(self):
		if self.userHistory.empty:
			self.session_id = 1
			self.session_status = 'first_session'
			self.seconds_ellapsed_from_last_msg = 0
		else:
			self.update_session_id_if_so(limit_interval_msgs=15)
	
	def update_session_id_if_so(self, limit_interval_msgs=15):
		self.seconds_ellapsed_from_last_msg = (self.datetime_user_message - self.userHistory['datetime_user_message'].iloc[-1])
		self.seconds_ellapsed_from_last_msg = self.seconds_ellapsed_from_last_msg.seconds
		if self.seconds_ellapsed_from_last_msg > limit_interval_msgs*60 : # 900 seconds = 15 minutes
			self.session_id += 1
			self.session_status = 'new_session'

	def restart_bot_if_new_session(self):
		pass
		


	def clean_text(self, text):
		text = self.user_message.lower()
		text = re.sub(' +', ' ', text)
		text = remove_accents(text)
		text = text.strip()
		text = text.translate(str.maketrans('', '', string.punctuation)) # remove punctuations
		#text = self.remove_repeated_chars(text)
		return text
		
	def remove_repeated_chars(self, text):
		return ''.join(c[0] for c in itertools.groupby(text))

	def storeData(self):
		self.data = self.data.append({
			'chat_id': self.chatId,
			'session_id': self.session_id,
			'user_message': self.user_message,
			'response': self.bot_responses,
			#'metadata': self.metadata,
			'context': self.context,
			'datetime_user_message': self.datetime_user_message,#.strftime("%Y-%m-%d %H:%M:%S"),
			'datetime_response': datetime.now(),
			'seconds_ellapsed_from_last_msg': self.seconds_ellapsed_from_last_msg,
			'telegram_message_data': self.message,
		}, ignore_index=True)

	def saveData(self, path='reports'):
		if not os.path.exists(path):
			os.makedirs(path)

		date = datetime.now().strftime("%Y-%m-%d")
		self.data.to_csv(f'{path}/report - {date}.csv', index=False, encoding='utf-8')


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