## Проект из модуля DVMN
[Чат-боты на Python](https://dvmn.org/modules/chat-bots)

#### Бот создан для оповещения о проверке заданий

Для работы требуется:
* python 3.6 и выше:
* установка зависимостей командой `pip install -r requirements.txt`
* создать файл .env в корне проекта и добавить переменные и значения: DVMN_TOKEN, BOT_TOKEN, TELEGRAM_USER_ID
в формате "ПЕРЕМЕННАЯ=значение"

Например:
```
  DVMN_TOKEN=1234
  BOT_TOKEN=qwe123
  TELEGRAM_USER_ID=0987
```

После этого можно запускать командой `python main.py`
или `python3 main.py`

### Выгрузка на Heroku
- Регистрируемся
- Добавляем новое приложение
- соединяем с репозиторием
- в разделе Settings -> Config Vars добавляем переменные окружения
- в разделе Resources активируем выполнение команды `bot python main.py`
