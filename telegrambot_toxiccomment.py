import pandas as pd
import telebot
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
import joblib


model_path = "C:/Users/mrsau/OneDrive/Desktop/minorproject/toxic_detection_model.joblib"
model, vectorizer = joblib.load(model_path)


BOT_TOKEN = "7854201105:AAGK2fQaDWsl_UzBYEg0otwHPOAZ7w30Urw" 


user_warnings = defaultdict(int)


bot = telebot.TeleBot(BOT_TOKEN)


def is_toxic(message_text):
    cleaned_message = message_text.lower()  
    message_vectorized = vectorizer.transform([cleaned_message])
    prediction = model.predict(message_vectorized)
    return prediction[0] == 1  


def warn_and_block_user(message):
    user_id = message.from_user.id
    user_warnings[user_id] += 1 
    
    if user_warnings[user_id] >= 3:
       
        bot.reply_to(message, "You have been banned due to multiple violations of the rules.")
        bot.kick_chat_member(message.chat.id, user_id)
        
        del user_warnings[user_id]
    else:
        
        bot.reply_to(message, f"Warning {user_warnings[user_id]}: Your message contains inappropriate language. Please be respectful!")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.type in ['group', 'supergroup']:
        if is_toxic(message.text):
            warn_and_block_user(message)
        else:
            
            bot.reply_to(message, message.text)
    elif message.chat.type == 'private':
        if is_toxic(message.text):
            warn_and_block_user(message)
        else:
            bot.reply_to(message, message.text)
           

print("Bot is running and listening for messages...")


bot.infinity_polling()