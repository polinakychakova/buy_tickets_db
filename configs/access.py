from functools import wraps
from flask import session, request, current_app, render_template


def group_validation():
    group_name = session.get('role', '')
    if group_name:
        return True
    return False


def group_validation_decorator(f):
    def wrapper(*args, **kwargs):
        if group_validation():
            return f(*args, **kwargs)  # здесь функция запускается и работает, т.е. возвр. результат функции
        return render_template('response.html', text='Доступ к странице запрещен.')

    return wrapper  # здесь функция не запускается, а просто возвр ссылка на функцию


def group_permission_validation() -> bool:
    access_config = current_app.config['ACCESS_CONFIG']
    group = session.get('role', 'unauthorized')
    order = {
        1: '',
        2: request.endpoint
    }
    target_app = order[len(request.endpoint.split('.'))]
    # print(target_app)
    if group in access_config and target_app in access_config[group]:
        return True
    return False


def group_permission_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return f(*args, **kwargs)
        return render_template('response.html', text='Доступ к странице запрещен.')

    return wrapper
