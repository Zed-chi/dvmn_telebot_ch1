import requests
import os
import telegram
import logging
from dotenv import load_dotenv


REVIEWS_URL = "https://dvmn.org/api/user_reviews/"
POOL_API_URL = "https://dvmn.org/api/long_polling/"


def update_time(json_data):
    if "last_attempt_timestamp" in json_data:
        return json_data["last_attempt_timestamp"]
    elif "timestamp_to_request" in json_data:
        return json_data["timestamp_to_request"]
    else:
        return None


class BotLogHandler(logging.Handler):
    def __init__(self, bot_token, telegram_user_id):
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = telegram_user_id
        logging.Handler.__init__(self)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    load_dotenv()
    dvmn_token = os.getenv("DVMN_TOKEN")
    bot_token = os.getenv("BOT_TOKEN")
    my_id = os.getenv("TELEGRAM_USER_ID")

    logger = logging.getLogger("BotLogger")
    logger.setLevel(logging.INFO)
    handler = BotLogHandler(bot_token, my_id)
    logger.addHandler(handler)

    timestamp = None
    headers = {"Authorization": f"Token {dvmn_token}"}
    logger.info("Начало цикла ожидания.")
    while True:
        try:
            logger.debug("шлю запрос ->")
            payload = {"timestamp": timestamp} if timestamp else {}
            response = requests.get(
                POOL_API_URL, headers=headers, params=payload
            )
            response.raise_for_status()
            json_data = response.json()
            timestamp = update_time(json_data)
            if json_data["status"] != "found":
                logger.debug(
                    "Got response, but status - {}".format(json_data["status"])
                )
                continue
            checked_exercises = [
                {
                    "title": attempt["lesson_title"],
                    "result": "Но у преподавателя есть замечания."
                    if attempt["is_negative"]
                    else "Все хорошо, можете продолжать.",
                }
                for attempt in json_data["new_attempts"]
            ]
            for exercise in checked_exercises:
                message = "Работа '{}' проверена, {}".format(
                    exercise["title"], exercise["result"]
                )
                logger.info(message)
        except requests.exceptions.ReadTimeout as e:
            logger.error(e)
        except requests.exceptions.ConnectionError as e:
            logger.error(e)
        except requests.exceptions.HTTPError as e:
            logger.error(e)
