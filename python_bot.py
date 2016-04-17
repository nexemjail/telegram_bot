from __future__ import unicode_literals
import telegram
from telegram.ext import Updater
import logging
import time


token = '184561786:AAGT5NJjxPSqTm3P4b30_hmGLhnTzgZV34s'

credinitials= {
	"password": "hCaXunqOtwvo",
	"username": "2eedabf3-b0e6-4a88-ba42-8fcbe1351584"
}
dialog_id = 'a75e74fe-c244-4698-8949-7105ce2c6fd3'

	
def start(bot, update):
	bot.watson_info = dict()
	bot.credinitials = credinitials
	bot.watson_info['dialog_id'] = dialog_id
	bot.dialog = DialogV1(username=bot.credinitials['username'], password = bot.credinitials['password'])
	response = bot.dialog.conversation(bot.watson_info['dialog_id'])
	print 'got a resp from start'
	
	bot.watson_info['conversation_id'] = response['conversation_id']
	bot.watson_info['client_id'] = response['client_id']
	
	bot.sendMessage(chat_id=update.message.chat_id, text='\n'.join(response['response']))
	print 'sent a message!'

def echo(bot, update):
	print 'echoing!'
	response = bot.dialog.conversation(bot.watson_info['dialog_id'],update.message.text,bot.watson_info['client_id'],
					bot.watson_info['conversation_id'])
	bot.sendMessage(update.message.chat_id, text ='\n'.join(response['response']))


if __name__ == '__main__':
	import logging
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	bot = telegram.Bot(token=token)
	updater = Updater(token=token)
	# updater.dispatcher.telegram_command_handlers.pop('start')
	updater.dispatcher.addTelegramCommandHandler('start', start)
	# updater.dispatcher.telegram_message_handlers.pop()
	updater.dispatcher.addTelegramMessageHandler(echo)
	updater.start_polling()
	print 'polled!'