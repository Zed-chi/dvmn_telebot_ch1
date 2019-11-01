### Project from module
https://dvmn.org/modules/chat-bots

Telebot will notify you when 
your mentor will check your work on the dvmn website

You need to install dependancies:
```bash
pip install -r requirements.txt
```
Also you need to create .env file in root of the directory
and write values of env variables: DVMN_TOKEN, BOT_TOKEN, TELEGRAM_USER_ID
in format "VAR=value"
for example:
```
  DVMN_TOKEN=1234
  BOT_TOKEN=qwe123
  TELEGRAM_USER_ID=0987
```

And after you can execute `python main.py`
