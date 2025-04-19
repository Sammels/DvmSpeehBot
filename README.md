# Телеграмм бот для работы с речью.

Данный телеграмм бот создается для помощи службе поддержи ВЫМЫШЛЕННОГО агенства "Игра глаголов"


## Установка

### Установка Python
Для работы, понадобится Python до версии `3.12.*`. Скачать его можно с [официального сайта (версия 3.12.8)](https://www.python.org/downloads/release/python-3128/).

1. Зарегестрировать нового бота у `@BotFather`, и получить токен.
2. Создать и перейти в  рабочую дерикторию
```bash
mkdir path/to/project/
cd /path/to/project/
```
3. Создать виртуальное окружение
```bash
python3 -m venv .env
```
4. Активировать это окружение
```bash
source .env/bin/activate
```
5. Склонировать резозиторий и перейти в директорию проекта
```bash
git clone https://github.com/Sammels/DvmSpeehBot.git
cd DvmSpeehBot
```
6. Установить необходимые библиотеки для запуска бота.
```bash
pip3 install -r requirements.txt
```
7. Создать файл окружения, для сокрытия Токена
```bash
touch .env
```
внести туда токены
```
TG_BOT_LOGGER_TOKEN=Токен, для доступа к ТГ бот-Логгеру.
TG_CHAT_ID= ID чата, куда ТГ бот-Логгер будет сыпать сообщения об ошибках.
TELEGRAM_TOKEN=Токен полученный из п.1
VK_GROUP_TOKEN=Персональный токен для доступа к группе вк, которая будет отвечать на вопросы пользователей.
GOOGLE_APPLICATION_CREDENTIALS=Путь к JSONфайлу полученнопу по инструкции "Установка Diagflow т Google"
PROJECT_ID=Название проекта в DiagFlow google
LANGUAGE_CODE=ru-RU
```

### Установка Dialogflow от Google

1. Cоздайте проект в Google Cloud, используя [документацию](https://cloud.google.com/dialogflow/es/docs/quick/setup). 
2. Cоздайте диалогового агента, который будет выполнять основную работу по общению с пользователем, используя [документацию](https://cloud.google.com/dialogflow/es/docs/quick/build-agent). 
3. Для обращения к сервису через API понадобится JSON-ключ, необходимый для авторизаци. Подробнее [здесь](https://cloud.google.com/docs/authentication/api-keys).




### Как работают боты.

`Написать как запускаеься тг и вк бот.`


Примеры работы ботов:

![vk_bot](./demo_vk_bot.gif)

Ссылка на vk-бота [здесь](https://vk.com/club229354790).

![tg_bot](./demo_tg_bot.gif)

Ссылка на telegram-бота [здесь](https://t.me/SammelsDevmanSpeechbot).