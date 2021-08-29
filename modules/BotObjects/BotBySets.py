from modules.Bot import Bot

class BotBySets(Bot):
	def processTextAndReply(self):
		self.getData()

		# Here I'll try to recognize the user message, giving a context according it.
		self.context = ''

		# Here the bot will respond the user according his context.
		self.bot_responses = self.flows[self.context]['bot_response']
		[self.bot.send_message(self.chatId, bot_response) for bot_response in self.bot_responses]

		# Storing data
		self.storeData()
		#if int(self.datetime.hour) % 6 == 0:
		self.saveData()

	def recognize(self):
		...