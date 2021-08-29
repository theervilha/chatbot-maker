from modules.Bot import Bot

class BotBySets(Bot):
	def processTextAndReply(self):
		self.getData()

		self.context = ''
		self.bot_responses = self.flows[self.context]['bot_response']
		[self.bot.send_message(self.chatId, bot_response) for bot_response in self.bot_responses]

		self.storeData()
		#if int(self.datetime.hour) % 6 == 0:
		self.saveData()

	def recognize(self):
		...