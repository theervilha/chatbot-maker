from settings import FLOWS
from telegram_token import TELEGRAM_TOKEN
from modules.BotObjects.BotBySets import BotBySets

Bot = BotBySets(TELEGRAM_TOKEN, FLOWS)
Bot.prepare()
Bot.run()