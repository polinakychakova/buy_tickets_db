from flask import Blueprint, session, render_template, request
from sql_provider import SQLProvider
from flask import render_template, request
from dbcon import get_db_config, work_with_db
from configs.access import group_permission_decorator

authen_app = Blueprint('auth', __name__, template_folder='templates')
db_config = get_db_config()
provider = SQLProvider("blueprints/scen_auth/sql/")


@authen_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', None)
        password = request.form.get('password', None)

        sql = provider.get('identify_group.sql', login=login, password=password)
        result = work_with_db(db_config, sql)
        if len(result) != 0:
            result = result[0]
            user_group = result['role']
            if user_group is not None:
                session['role'] = user_group
                return render_template('response.html', text='Авторизация прошла успешно')
            else:
                return render_template('response.html', text='Неправильный логин или пароль.')
        else:
            return render_template('response.html', text='Неправильный логин или пароль. ')
