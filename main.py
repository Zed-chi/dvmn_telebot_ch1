import requests
import os
import telegram
from dotenv import load_dotenv


REVIEWS_URL = "https://dvmn.org/api/user_reviews/"
POOL_API_URL = "https://dvmn.org/api/long_polling/"


def main():
    load_dotenv()
    dvmn_token = os.getenv("dvmn_token")
    bot_token = os.getenv("bot_token")
    my_id = os.getenv("id")
    headers = {"Authorization": f"Token {dvmn_token}"}
    timestamp = None
    while True:
        try:
            if timestamp:
                payload = {"timestamp": timestamp}
                response = requests.get(
                    POOL_API_URL, headers=headers, params=payload
                ).json()
            else:
                response = requests.get(POOL_API_URL, headers=headers).json()
                if "last_attempt_timestamp" in response:
                    timestamp = response["last_attempt_timestamp"]
                elif "timestamp_to_request" in response:
                    timestamp = response["timestamp_to_request"]

            if response["status"] == "found":
                for attempt in response["new_attempts"]:
                    title = attempt["lesson_title"]
                    if attempt["is_negative"]:
                        result = "Но у преподавателя есть замечания."
                    else:
                        result = "Все хорошо, можете продолжать."
                message = f"Работа {title} проверена, \n{result}"
                bot = telegram.Bot(token=bot_token)
                bot.send_message(chat_id=my_id, text=message)
            else:
                print(response["status"])
        except requests.exceptions.ReadTimeout as e:
            print(e)
        except requests.exceptions.ConnectionError as e:
            print(e)


if __name__ == "__main__":
    main()
