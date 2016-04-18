from __future__ import unicode_literals
import telegram
from telegram.ext import Updater
import logging
import time
import os

PORT = int(os.getenv('PORT', 8000))
os.chdir('static')


token = '184561786:AAGT5NJjxPSqTm3P4b30_hmGLhnTzgZV34s'

# credinitials= {
# 	"password": "hCaXunqOtwvo",
# 	"username": "2eedabf3-b0e6-4a88-ba42-8fcbe1351584"
# }

credinitials= {
    "password": "vgorRfqqtlAw",
    "username": "13cb4351-e251-4094-a586-fe9a82c71770",
}

# dialog_id = 'a75e74fe-c244-4698-8949-7105ce2c6fd3'

# dialog_id = 'db80c0b7-b5a1-4a73-848e-e30f379101ef'
dialog_id = '94f94a25-4e49-43d3-afa6-396261ac3fa4'

def start(bot, update):
	print 'start called!'
	try:
		bot.watson_info = dict()
		bot.credinitials = credinitials
		bot.watson_info['dialog_id'] = dialog_id
		bot.dialog = DialogV1(username=credinitials['username'], password = credinitials['password'])
		response = bot.dialog.conversation(dialog_id)
		print 'got a resp from start'
	
		bot.watson_info['conversation_id'] = response['conversation_id']
		bot.watson_info['client_id'] = response['client_id']
		
		bot.sendMessage(chat_id=update.message.chat_id, text='\n'.join(response['response']))
		print 'sent a message!'
	except e:
		print 'start'
		print e 

def echo(bot, update):
	print 'echoing!'
	try:
		response = bot.dialog.conversation(bot.watson_info['dialog_id'],update.message.text,bot.watson_info['client_id'],
						bot.watson_info['conversation_id'])
		bot.sendMessage(update.message.chat_id, text ='\n'.join(response['response']))
		print 'message sent!'
	except e:
		print 'echo'
		print e

if __name__ == '__main__':
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
	# httpd = Server(("", PORT), Handler)
	# try:
	#   print("Start serving at port %i" % PORT)
	#   httpd.serve_forever()
	# except KeyboardInterrupt:
	#   pass
	#httpd.server_close()
