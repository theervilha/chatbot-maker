from modules.Bot import Bot

class BotBySets(Bot):
	def processTextAndReply(self):
		self.bot_responses = []

		# Here I'll try to recognize the user message, giving a context according it.
		self.context = self.recognize()
		print('cleaned_user_message:',self.cleaned_user_message)
		print('context found:',self.context)

		self.reply()
				
		self.storeData()
		#if int(self.datetime.hour) % 6 == 0:
		self.saveData()

	def recognize(self):
		recognized_sets_by_contains = self.set_recognizer.get_sets_by_contains(self.user_message)
		recognized_sets_by_equal = self.set_recognizer.get_sets_by_equal(self.user_message)
		recognized_sets_by_words_contains = self.set_recognizer.get_sets_by_words_contains(self.user_message)
		#print(recognized_sets_by_words_contains)

		recognized_entities_by_contains = self.entity_recognizer.get_entities_by_contains(self.user_message)
		recognized_entities_by_equal = self.entity_recognizer.get_entities_by_equal(self.user_message)
		recognized_entities_by_words_contains = self.entity_recognizer.get_entities_by_words_contains(self.user_message)
		print('entities word contains:',recognized_entities_by_words_contains)

		'''print('\n\n\n--- Recognized by sets ---')
		print('By Contains:',recognized_sets_by_contains)
		print('\nBy Equal:',recognized_sets_by_equal)
		print('\n\n\n--- Recognized by Entities ---')
		print('By Contains:',recognized_entities_by_contains)
		print('\nBy Equal:',recognized_entities_by_equal)'''

		# Here, self.context is like "last_context".
		# The result of this function will be the context recognized
		# So, I think we could generate all the possibilities of tracking user here
		
		#if self.context in ['tipos de planos', 'consultar_saldo']:
			# feedback
			# reclamação
			# falar com atendente;

		#if self.last_context == 'not_handled':
		

		"""if self.last_context in ['', 'greetings', 'not_handled']:
			if 'problem' in recognized_sets_by_contains and 'device' in recognized_entities_by_contains:
				self.metadata['intent'].append(recognized_sets_by_contains)
				self.metadata['entity'].append(recognized_entities_by_contains)
				return 'problem recognized and item recognized'
			elif 'problem' in recognized_sets_by_contains:
				self.metadata['intent'].append(recognized_sets_by_contains)
				return 'problem recognized and item not recognized'
			elif 'device' in recognized_entities_by_contains:
				self.metadata['entity'].append(recognized_entities_by_contains)
				return 'problem not recognized and item recognized'

			#if 'formas de pagamento' in recognized_sets_by_words_contains:
			#	return 'formas de pagamento'
			#
			#if 'sobre entrega' in recognized_sets_by_words_contains:
			#	return 'sobre entrega'
			if 'trocar' in recognized_sets_by_words_contains:
				return 'trocar'
			if 'pedido' in recognized_entities_by_words_contains:
				if 'reembolsar' in recognized_sets_by_words_contains:
					return 'reembolsar '
				if 'cancelar' in recognized_sets_by_words_contains:
					return 'cancelar pedido'
				else:
					return 'pedido?'
					
			if recognized_sets_by_words_contains:
				try:
					found_by_sets_words_contains = {context: values for context, values in recognized_sets_by_words_contains.items() if values}
					found_by_sets_words_contains = {context: values for context, values in found_by_sets_words_contains.items() if context not in ['sim', 'não']}
					print('vals:',[x for x in recognized_sets_by_words_contains.values()])
					found_by_sets_words_contains = list(found_by_sets_words_contains.keys())[0]
					print('Aleatoriament sets words contains:',found_by_sets_words_contains)
					return found_by_sets_words_contains
				except:
					print(found_by_sets_words_contains)
			if 'greetings' in recognized_sets_by_equal:
				return 'greetings'
			return 'not_handled'

		if 'greetings' in recognized_sets_by_equal:
			return 'greetings'"""
	
		
		if self.session_status == 'first_session':
			self.bot_responses.extend(self.GoTo.go_to['greetings']())
			return ''
			#self.quick_replies = self.go_to['saudacao']

	def reply(self):
		#self.bot_responses = self.flows[self.context]['bot_response']
		#self.bot_responses = self.put_variables_in_bot_responses_if_there()
		qt_bot_responses = len(self.bot_responses)
		for i, bot_response in enumerate(self.bot_responses):

			if i == qt_bot_responses - 1:
				quick_replies = self.flows[self.context]['quick_replies']
				if quick_replies:
					self.bot.send_message(self.chatId, bot_response, reply_markup=self.get_buttons_in_telegram_format(quick_replies))
				else:
					self.bot.send_message(self.chatId, bot_response)
			
			else:
				self.bot.send_message(self.chatId, bot_response)