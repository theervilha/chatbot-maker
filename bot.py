from settings import FLOWS
from telegram_token import TELEGRAM_TOKEN
from modules.BotObjects.BotBySets import BotBySets
from modules.Thinking.GoTo import GoTo

Bot = BotBySets(TELEGRAM_TOKEN, FLOWS, GoTo)
Bot.prepare()
Bot.run()