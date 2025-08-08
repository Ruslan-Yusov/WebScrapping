import datetime
from functools import wraps


def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(f'Дата и время вызова функции {datetime.datetime.now()} '
                               f'Имя функции {old_function.__name__} '
                               f'Аргументы функции ({args}, {kwargs}) '
                               f'Возвращаемое значение {old_function(*args, **kwargs)}\n')
                return old_function(*args, **kwargs)
        return new_function
    return __logger