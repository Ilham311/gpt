import requests
import telebot 

TELEGRAM_BOT_TOKEN = "5219568853:AAFvJZ7SmP24wrVfNranLFebbTNQjY7v1gY"
BOT_USERNAME = "@Soranosbot"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

user_conversations = {}

def ask_gpt_bot(question):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        "x-goog-api-key": "AIzaSyDTsv7eS31kT3LsvoiuYNe_Le0DGpubJaM",
        "x-goog-api-client": "genai-android/0.9.0",
        "accept": "application/json",
        "accept-charset": "UTF-8",
        "user-agent": "Ktor client",
        "content-type": "application/json",
        "accept-encoding": "gzip"
    }
    data = {
        "model": "models/gemini-1.5-flash",
        "contents": [
            {"role": "user", "parts": [{"text": question}]}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    answer_text = response_json['candidates'][0]['content']['parts'][0]['text']
    return answer_text

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya adalah bot berbasis GPT. Tag saya untuk meminta bantuan!")
    user_id = message.from_user.id
    user_conversations[user_id] = []

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_message = message.text
    if BOT_USERNAME in user_message:
        question = user_message.replace(BOT_USERNAME, "").strip()
        if question:
            bot_reply = ask_gpt_bot(question)
            if user_id in user_conversations:
                user_conversations[user_id].append({
                    'question': question,
                    'answer': bot_reply
                })
            else:
                user_conversations[user_id] = [{
                    'question': question,
                    'answer': bot_reply
                }]
            bot.reply_to(message, bot_reply)
        else:
            bot.reply_to(message, "Tolong berikan saya pertanyaan setelah mention.")
    else:
        pass

bot.polling()
