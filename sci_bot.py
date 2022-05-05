from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from scholar import ScholarQuerier, SearchScholarQuery
import logging


updater = Updater("5311000608:AAEAdjWcm3Mrfttg2qd1ZIGlQirFRBvr7Q0",
                  use_context=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)  

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello dear user! Welcome to the Bot. Please write\
        /help to see the commands available.")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
    /search () - To get the Sci-Hub paper you want  
    /sugestions - To get gmail URL to contact-me :) 
    """)

def search(update: Update, context: CallbackContext, args):
    search_command = ' '.join(args)

    update.message.reply_text("You searched for: " + search_command)

    querier = ScholarQuerier()
    query = SearchScholarQuery()
    query.set_words(args)
    querier.send_query(query)
    
    articles = querier.articles
    
    message = ""

    update.message.reply_text("Number of results: " + str(len(articles)))

    index = 0
    for article in articles:
        update.message.reply_text(str(index+1)+". " + article.attrs['title'][0])

def gmail_url(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Any suggestions can be sent to me through\
        rubenesteche@hotmail.com")
  
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
  
  
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
  
  
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('search', search, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('sugestions', gmail_url))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
  
updater.start_polling()