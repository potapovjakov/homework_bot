class DataCheck(Exception):
    """Проверка доступности ключей в запросе."""
    def __init__(self):
        self.message = 'Полученные данные не соответствуют ожидаемым'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
