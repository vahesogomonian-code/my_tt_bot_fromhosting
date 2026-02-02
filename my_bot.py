import telebot
import os
import yt_dlp

# Твой токен вписан напрямую, теперь файл bot_token не нужен
token = "7316617770:AAFPKR0ZEp-24AEeEYrAmXg4d6tcNoeCmCY"

# Настройка папки для видео (подходит для Termux)
if os.path.exists("/storage/emulated/0/"):
    folder_path = "/storage/emulated/0/папка работ/для скачки видео/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
else:
    folder_path = "./"

bot = telebot.TeleBot(token)

# 1. ОБРАБОТКА КОМАНДЫ /START (Будет реагировать первым)
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Добрый день! 🦾\n"
        "Я готов к работе. Просто пришли мне ссылку на видео из TikTok или Instagram, и я его скачаю."
    )

# 2. ОБРАБОТКА ССЫЛОК
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()

    if "tiktok.com" in url or "instagram.com" in url:
        status_msg = bot.reply_to(message, "⏳ Видео обрабатывается...")
        video_name = f"video_{message.chat.id}.mp4"
        video_file = os.path.join(folder_path, video_name)

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
                bot.send_video(message.chat.id, video, caption="Готово! Видео скачано. 🦾")

        except Exception as e:
            # Ошибка исправлена: убрана лишняя скобка
            bot.edit_message_text(f"Ошибка: {str(e)[:50]}", message.chat.id, status_msg.message_id)

        finally:
            if os.path.exists(video_file):
                os.remove(video_file)
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except:
                pass
    else:
        bot.reply_to(message, "Я понимаю только ссылки на TikTok или Instagram! 😉")

# 3. ЗАПУСК БОТА (Исправлено: одна строка без разрывов)
print("Бот успешно запущен!")
bot.infinity_polling(skip_pe
                     nding=True)
