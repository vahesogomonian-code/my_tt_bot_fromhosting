import telebot
import os
import yt_dlp

# 1. Получение токена
token = os.environ.get('BOT_TOKEN')

if not token:
    # Termux
    folder_path = "/storage/emulated/0/папка работ/для скачки видео/"
    path_to_token = folder_path + "bot_token"
    with open(path_to_token, 'r') as f:
        token = f.read().strip()
else:
    # Хостинг
    folder_path = "./"

bot = telebot.TeleBot(token)

# ===== /start =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добрый день.\n"
        "Я бот, который помогает скачивать видео из TikTok и Instagram.\n\n"
        "Просто пришлите ссылку на видео — я отправлю файл."
    )

# ===== Обработка сообщений =====
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()

    if "tiktok.com" not in url and "instagram.com" not in url:
        bot.reply_to(
            message,
            "Пришлите ссылку на видео из TikTok или Instagram."
        )
        return

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
            bot.send_video(
                message.chat.id,
                video,
                caption="Готово. Видео скачано."
            )

    except Exception as e:
        bot.edit_message_text(
            f"Ошибка загрузки: {str(e)[:100]}",
            message.chat.id,
            status_msg.message_id
        )

    finally:
        if os.path.exists(video_file):
            os.remove(video_file)

        try:
            bot.delete_message(message.chat.id, status_msg.message_id)
        except:
            pass

# ===== Запуск =====
print("Бот запущен.")
bot.infinity_polling(skip_pending=True)
