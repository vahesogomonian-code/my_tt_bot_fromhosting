import telebot
import os
import yt_dlp

# 1. Настройка получения токена
token = os.environ.get('BOT_TOKEN') 

if not token:
    # Путь для твоего телефона (Termux)
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
    
    # Проверка ссылки на TikTok или Instagram
    if "tiktok.com" in url or "instagram.com" in url:
        status_msg = bot.reply_to(message, "⏳ Видео обрабатывается...")
        
        video_name = f"video_{message.chat.id}.mp4"
        video_file = os.path.join(folder_path, video_name)
        
        # Настройки скачивания
        ydl_opts = {
            'outtmpl': video_file,
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            # Скачивание
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Отправка видео (слово "Же" убрано из подписи)
            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="Готово! Видео доставлено. 🦾")
            
        except Exception as e:
            bot.edit_message_text(f"❌ Ошибка: {str(e)[:100]}", message.chat.id, status_msg.message_id)
        
        finally:
            # Очистка: удаляем файл с сервера сразу после отправки
            if os.path.exists(video_file):
                os.remove(video_file)
                print(f"Файл {video_name} удален.")
            
            # Удаляем сообщение о загрузке
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except:
                pass

# Запуск бота
print("Бот запущен и готов к работе в облаке...")
bot.infinity_polling(skip_pending=T
                     rue)
