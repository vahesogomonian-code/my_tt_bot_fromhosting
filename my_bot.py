import telebot
import os
import yt_dlp

# 1. ПОЛУЧАЕМ ТОКЕН
# Сначала проверяем Secrets на хостинге, если там пусто — берем этот
token = os.getenv("BOT_TOKEN") 
if not token:
    token = "7316617770:AAFPKR0ZEp-24AEeEYrAmXg4d6tcNoeCmCY"

# 2. НАСТРОЙКА ПАПОК
folder_path = "./downloads/"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

bot = telebot.TeleBot(token)

# ОБРАБОТКА /START
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id, 
        "Бот запущен и готов к работе! 🦾\nПришли мне ссылку на TikTok или Instagram."
    )

# ОБРАБОТКА ССЫЛОК
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    
    if "tiktok.com" in url or "instagram.com" in url:
        status_msg = bot.reply_to(message, "⏳ Видео обрабатывается...")
        video_file = os.path.join(folder_path, f"video_{message.chat.id}.mp4")
        
        ydl_opts = {
            'outtmpl': video_file,
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="Готово! 🦾")
                
        except Exception as e:
            bot.edit_message_text(f"Ошибка: {str(e)[:50]}", message.chat.id, status_msg.message_id)
            
        finally:
            if os.path.exists(video_file):
                os.remove(video_file)
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except:
                pass
    else:
        bot.reply_to(message, "Я жду ссылку на TikTok или Instagram! 😉")

# 3. ЗАПУСК
print("Бот успешно запущен!")
bot.infinity_polling(skip_pending=
    True)
