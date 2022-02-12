class DataCheck(Exception):
    """Проверка доступности ключей в запросе."""
    def __init__(self):
        self.message = 'Полученные данные не соответствуют ожидаемым'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class UrlNotAccess(Exception):
    """Проверка доступности эндпоинта"""
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.message = f'Ошибка подключения к {endpoint}'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class ApiDataIsEmpty(Exception):
    """Проверка данных API"""
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.message = f'Из {endpoint} получены некорректные данные'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
