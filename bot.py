from settings import FLOWS, TELEGRAM_TOKEN
from modules.BotObjects.BotBySets import BotBySets

Bot = BotBySets(TELEGRAM_TOKEN, FLOWS)
Bot.prepare()
Bot.run()