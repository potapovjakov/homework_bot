# Homework_bot
Телеграм бот, делающий запрос к API Яндекс.Домашки каждые 15 минут для оповещения о статусе домашнего задания. При изменении статуса отправляет уведомление с новым статусом.

## Стек технологий:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

## Как запустить проект:
- Клонируйте репозиторий:  
```git clone https://github.com/potapovjakov/homework_bot.git```
- Перейдите в директорию с проектом
- Создайте виртуальное окружение:  
```python -m venv venv```
- Активируйте виртуальное окружение:  
для linux: ```source venv/bin/activate```
- Установите зависимости:  
```pip install -r requirements.txt```
- Получите необходимые токены и Telegram ID 
- Создайте файл *.env*, в котором укажите переменную окружения *SECRET_KEY*, а так же укажите следующие значения:
- PRACTICUM_TOKEN = <Токен на Яндекс.Домашке>
- TELEGRAM_TOKEN = <Токен телеграм бота>
- TELEGRAM_CHAT_ID = <ID чата, в который будут приходить оповещения>


*** ***Выполнил [Потапов Яков](https://github.com/potapovjakov) при поддержке [Яндекс Практикума](https://practicum.yandex.ru/)***

