from dotenv import dotenv_values

from settings import FLOWS
from modules.BotObjects.BotBySets import BotBySets
from modules.Thinking.GoTo import GoTo

TELEGRAM_TOKEN = dotenv_values(".env").get('TELEGRAM_TOKEN')
Bot = BotBySets(TELEGRAM_TOKEN, FLOWS, GoTo)
Bot.prepare()
Bot.run()