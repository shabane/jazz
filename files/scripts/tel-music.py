import telebot
import os

# Get the bot token from the environment variable
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_FOLDER = "./raw" # musics that not converted yet.

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@bot.message_handler(content_types=['document', 'video', 'audio', 'voice'])
def handle_files(message):
    try:
        file_info = None
        file_name = None

        if message.document:
            file_info = bot.get_file(message.document.file_id)
            file_name = message.document.file_name
        elif message.video:
            file_info = bot.get_file(message.video.file_id)
            file_name = message.video.file_name
        elif message.audio:
            file_info = bot.get_file(message.audio.file_id)
            file_name = message.audio.file_name
        elif message.voice:
            file_info = bot.get_file(message.voice.file_id)
            file_name = f"voice_{message.voice.file_id}.ogg"

        if file_info and file_name:
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, f"File '{file_name}' downloaded successfully!")
        else:
            bot.reply_to(message, "Failed to download the file.")

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me a file, and I'll download it!")

print("Bot started. Listening for files...")
bot.polling()