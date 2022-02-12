import logging
import os
import time
from http import HTTPStatus
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

import requests
import telegram
from dotenv import load_dotenv

from exceptions import ApiDataIsEmpty, DataCheck, UrlNotAccess

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

formatter = Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler = RotatingFileHandler(
    filename='homework_bot.log',
    maxBytes=1048000,
    backupCount=1,
)
handler.setFormatter(formatter)
stream_handler = StreamHandler()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(stream_handler)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат"""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Отправлено сообщение: {message}')
    except Exception:
        logger.error(
            'Ошибка при отправке сообщения'
        )


def get_api_answer(current_timestamp):
    """Делает запрос к эндпоинту API-сервиса"""
    logger.info('Запрос отправлен')
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        api_answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception:
        raise UrlNotAccess(ENDPOINT)
    if api_answer.status_code != HTTPStatus.OK:
        raise UrlNotAccess(ENDPOINT)
    if api_answer:
        return api_answer.json()
    raise ApiDataIsEmpty(ENDPOINT)


def check_response(response):
    """Проверяет ответ API на корректность"""
    if not isinstance(response, dict):
        raise TypeError
    try:
        homework = response['homeworks']
    except KeyError:
        raise KeyError
    if not isinstance(homework, list):
        raise DataCheck()
    return homework


def parse_status(homework):
    """Извлекает из конкретной домашки ее статус"""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None and homework_status is None:
        raise DataCheck()
    try:
        verdict = HOMEWORK_STATUSES[homework_status]
    except KeyError:
        raise KeyError
    message = ('Изменился статус проверки работы '
               f'"{homework_name}". {verdict}')
    return message


def check_tokens():
    """Проверяет доступность переменных окружения"""
    if all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
        return True
    logger.critical('Отсутствуют переменные окружения')
    return False


def main():
    """Основная функция бота"""
    if not check_tokens():
        return
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    var_error = None
    while True:
        try:
            response = get_api_answer(current_timestamp)
            check_response_result = check_response(response)
            if check_response_result:
                parse_status_update = parse_status(check_response_result[0])
                send_message(bot, parse_status_update)
            current_timestamp = response.get('current_date', current_timestamp)
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.exception(message, exc_info=True)
            if str(error) != str(var_error):
                var_error = error
                send_message(bot, message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
