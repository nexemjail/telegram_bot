
# coding: utf-8

# In[1]:

import telegram
from telegram.ext import Updater
from __future__ import unicode_literals
import pycurl


# In[2]:

credinitials= {
    "password": "hCaXunqOtwvo",
    "username": "2eedabf3-b0e6-4a88-ba42-8fcbe1351584"
}


# In[3]:

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# In[4]:

token = '184561786:AAGT5NJjxPSqTm3P4b30_hmGLhnTzgZV34s'


# In[5]:

bot = telegram.Bot(token=token)


# In[6]:

updater = Updater(token=token)


# In[7]:

print bot.getMe()


# In[8]:

import json
from watson_developer_cloud import DialogV1


# In[15]:

dialog = DialogV1(username=credinitials['username'],
                    password=credinitials['password'])


# In[16]:

print dialog.get_dialogs()


# In[17]:

dialog_id = '3f8b55f2-6732-4448-a013-79b4342b10a2'
dialog_id = 'a75e74fe-c244-4698-8949-7105ce2c6fd3'
#response =  dialog.conversation(dialog_id)


# In[28]:

# print response

# conversation_id = response['conversation_id']
# client_id = response['client_id']
# message = response['response']
# print '\n'.join(message)


# In[18]:

def start(bot, update):
    bot.watson_info = dict()
    bot.credinitials = credinitials
    bot.watson_info['dialog_id'] = dialog_id
    bot.dialog = DialogV1(username=bot.credinitials['username'], password = bot.credinitials['password'])
    response = bot.dialog.conversation(bot.watson_info['dialog_id'])
    
    bot.watson_info['conversation_id'] = response['conversation_id']
    bot.watson_info['client_id'] = response['client_id']
    
    bot.sendMessage(chat_id=update.message.chat_id, text='\n'.join(response['response']))

updater.dispatcher.telegram_command_handlers.pop('start')
updater.dispatcher.addTelegramCommandHandler('start', start)


# In[19]:

def echo(bot, update):
    response = bot.dialog.conversation(bot.watson_info['dialog_id'],update.message.text,bot.watson_info['client_id'],
                    bot.watson_info['conversation_id'])
    bot.sendMessage(update.message.chat_id, text ='\n'.join(response['response']))

#updater.dispatcher.stop()
updater.dispatcher.telegram_message_handlers.pop()
updater.dispatcher.addTelegramMessageHandler(echo)


# In[21]:

updater.start_polling()
#updater.stop()


# In[20]:




# In[29]:

user_input = 'Hi!'


# In[30]:

other_response = dialog.conversation(dialog_id,user_input,client_id,
                    conversation_id)
print other_response

