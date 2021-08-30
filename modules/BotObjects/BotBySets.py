from modules.Bot import Bot

class BotBySets(Bot):
	def processTextAndReply(self):
		self.getData()
		self.clear_user_message()

		# Here I'll try to recognize the user message, giving a context according it.
		self.context = self.recognize()
		print('context found:',self.context)

		# Here the bot will respond the user according his context.
		self.bot_responses = self.flows[self.context]['bot_response']
		[self.bot.send_message(self.chatId, bot_response) for bot_response in self.bot_responses]

		# Storing data
		self.storeData()
		#if int(self.datetime.hour) % 6 == 0:
		self.saveData()

	def recognize(self):
		recognized_sets_by_contains = self.set_recognizer.get_sets_by_contains(self.user_message)
		recognized_sets_by_equal = self.set_recognizer.get_sets_by_equal(self.user_message)
		recognized_entities_by_contains = self.entity_recognizer.get_entities_by_contains(self.user_message)
		recognized_entities_by_equal = self.entity_recognizer.get_entities_by_equal(self.user_message)
		
		print('\n\n\n--- Recognized by sets ---')
		print('By Contains:',recognized_sets_by_contains)
		print('\nBy Equal:',recognized_sets_by_equal)
		print('\n\n\n--- Recognized by Entities ---')
		print('By Contains:',recognized_entities_by_contains)
		print('\nBy Equal:',recognized_entities_by_equal)

		if self.context in ['', 'greetings', 'not_handled']:
			if 'problem' in recognized_sets_by_contains and 'device' in recognized_entities_by_contains:
				return 'problem recognized and item recognized'
			elif 'problem' in recognized_sets_by_contains:
				return 'problem recognized and item not recognized'
			elif 'device' in recognized_entities_by_contains:
				return 'problem not recognized and item recognized'

			if 'greetings' in recognized_sets_by_equal:
				return 'greetings'
			return 'not_handled'

		if 'greetings' in recognized_sets_by_equal:
			return 'greetings'
		return 'not_handled'