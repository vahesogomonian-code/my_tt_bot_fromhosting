import telebot
import os
import yt_dlp

# Настройка путей
token = os.environ.get('BOT_TOKEN')
if not token:
    # Путь для твоего телефона
    folder_path = "/storage/emulated/0/папка работ/для скачки видео/"
    path_to_token = folder_path + "bot_tokrn"
    with open(path_to_token, 'r') as f:
        token = f.read().strip()
else:
    # Путь для хостинга (Choreo)
    folder_path = "./" 

bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if "tiktok.com" in url or "instagram.com" in url:
        status_msg = bot.reply_to(message, "⏳ Видео обрабатывается...")
        
        video_name = f"video_{message.chat.id}.mp4"
        video_file = os.path.join(folder_path, video_name)
        
        ydl_opts = {'outtmpl': video_file, 'format': 'best', 'quiet': True}
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open(video_file, 'rb') as video:
                # Убрал "Же" из текста отправки
                bot.send_video(message.chat.id, video, caption="Готово! Видео доставлено. 🦾")
            
        except Exception as e:
            bot.edit_message_text(f"❌ Ошибка: {str(e)[:50]}", message.chat.id, status_msg.message_id)
        
        finally:
            if os.path.exists(video_file):
                os.remove(video_file)
                print(f"Файл {video_name} удален.")
            
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except:
                pass

# Добавил skip_pending=True, чтобы не было конфликтов при перезапуске
print("Бот запущен и готов к работе...")
bot.infinity_polling(skip_pending=True)

