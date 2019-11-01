import requests
import os
import telegram
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


if __name__ == "__main__":
    load_dotenv()
    dvmn_token = os.getenv("DVMN_TOKEN")
    bot_token = os.getenv("BOT_TOKEN")
    bot = telegram.Bot(token=bot_token)
    my_id = os.getenv("TELEGRAM_USER_ID")
    timestamp = None
    headers = {"Authorization": f"Token {dvmn_token}"}

    while True:
        try:
            print("sending req->")
            payload = {"timestamp": timestamp} if timestamp else {}
            response = requests.get(
                POOL_API_URL, headers=headers, params=payload
            )
            response.raise_for_status()
            json_data = response.json()
            timestamp = update_time(json_data)
            if json_data["status"] != "found":
                print(
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
                bot.send_message(chat_id=my_id, text=message)
        except requests.exceptions.ReadTimeout as e:
            print(e)
        except requests.exceptions.ConnectionError as e:
            print(e)
        except requests.exceptions.HTTPError as e:
            print(e)
