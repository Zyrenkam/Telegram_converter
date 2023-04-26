import telebot
import os
import speech_recognition as sr
import soundfile
import gtts.lang

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
recognizer = sr.Recognizer()


def recognise(filename):
    with sr.AudioFile(filename) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='ru')
        return text


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Конвертация ГС в текст")
    btn2 = telebot.types.KeyboardButton("Конвертация текста в ГС")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот для конвертации аудио сообщений в текст".format(
                         message.from_user), reply_markup=markup)
    print('-----', message.from_user.username, message.from_user.first_name,  message.from_user.last_name)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Конвертация ГС в текст":
        bot.send_message(message.chat.id, text="Ты выбрал Конвертация ГС в текст")
        bot.send_message(message.chat.id, text="Отправь мне какое-нибудь голосовое")
        bot.send_message(message.chat.id, text="Ты тоже офигеваешь с таких людей, которым говоришь,"
                                               " чтобы они написали тебе, а вместо этого записывают"
                                               " длиннющие голосовые?")

    elif message.text == "Конвертация текста в ГС":
        bot.send_message(message.chat.id, text="Ты выбрал Конвертация текста в ГС")
        bot.send_message(message.chat.id, text="Отправь мне какой-нибудь тест и я его озвучу")
        bot.send_message(message.chat.id, text="Ты перешел на темную сторону. Ты отправляешь ГС"
                                               " вместо обычных сообщений, которые удобно читать в"
                                               " любой ситуации, чего не скажешь о голосовых...")
    else:
        msg = str(message.text)
        print(message.from_user.username, ": ", message.text)
        to_voice = gtts.gTTS(msg, lang='ru')
        to_voice.save("text_to_audio.wav")
        bot.send_audio(message.chat.id, audio=open('text_to_audio.wav', 'rb'))


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_name = "test.wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    data, samplerate = soundfile.read('test.wav')
    soundfile.write('newtest.wav', data, samplerate, subtype='PCM_16')

    result_text = recognise('newtest.wav')
    bot.reply_to(message, result_text)
    print(message.from_user.username, ": ", result_text)

    os.remove(file_name)


bot.polling(non_stop=True)
