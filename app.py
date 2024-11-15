!pip install pyTelegramBotAPI
import sqlite3
import telebot
import datetime
import logging
import threading

# Configure logging to capture errors
logging.basicConfig(level=logging.ERROR, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Replace 'YOUR_TOKEN' with your actual bot token
bot = telebot.TeleBot('7088516662:AAGjbT9agaVOYdEoO4o7EUDsVXp4Px-xZCY')

def get_schedule(formatted_date):
    try:
        conn = sqlite3.connect('schedule.db')
        cursor = conn.cursor()
        a = cursor.execute('''SELECT * FROM timetable WHERE day = ?''', (formatted_date,)).fetchall()
        conn.close()
        return a
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return []  # Return empty list on error
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет!  Используй /schedule чтобы посмотреть расписание.")
    #Start the reminder thread only once.  This is a simplification.  A more robust solution might involve checking if the thread is already running.
    thread = threading.Thread(target=reminder_thread, args=(message.chat.id,))
    thread.start()


@bot.message_handler(commands=['schedule'])
def schedule_command(message):
    today = datetime.date.today()
    formatted_date = today.strftime("%d.%m.%Y")
    lectures = get_schedule(formatted_date)
    if lectures:
        response = "Сегодня лекции:\n"
        for lecture in lectures:
            #Format the output nicely to show all columns
            response += f" время: {lecture[1]},  предмет: {lecture[2]},  аудитория: {lecture[3]},  вид занятия: {lecture[4]},  \n преподователь: {lecture[5]} \n"
    else:
        response = "Сегодня лекций нет."
    bot.reply_to(message, response)


def reminder_thread(chat_id):
    # Implement your reminder logic here.  This is a placeholder.
    #  This function should send reminders at appropriate times.
    #  Remember to handle exceptions and logging appropriately.
    try:
        while True:
            # Add your reminder logic here
            # For example, check the schedule for the next day, and send a notification
            print("Reminder thread running...")
            time.sleep(60*60)  # Check every hour. Adjust as needed.
    except Exception as e:
        logging.error(f"Error in reminder thread: {e}")

import time

bot.polling(none_stop=True)
