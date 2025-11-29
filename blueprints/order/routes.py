import os
from flask import Blueprint

from configs.access import group_permission_decorator, group_validation_decorator
from sql_provider import SQLProvider
from flask import render_template, request
from dbcon import get_db_config, work_with_db

order_app = Blueprint('select', __name__, template_folder='templates')
db_config = get_db_config()
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@order_app.route('/')
@group_validation_decorator
def order_index():
    return render_template('index_for_orders.html')


@order_app.route('/sql_task1', methods=['GET', 'POST'])
@group_permission_decorator
def sql1():
    if request.method == 'GET':
        return render_template('user_input_tsk1.html')
    flight_num = request.form.get('flight_num')
    year_sell = request.form.get('year_sell')
    sql = provider.get('check_select.sql', flight_num=flight_num)
    check = work_with_db(config=db_config, sql=sql)
    if check:
        sql = provider.get('task_1.sql', flight_num=flight_num, year_sell=year_sell)
        result = work_with_db(config=db_config, sql=sql)
        return render_template('result_for_1.html', result=result, str=f"Для заданного рейса не было куплено билетов в {year_sell} год", str_info=f"Для рейса {flight_num} в {year_sell} год")
    else:
        return render_template('result_for_1.html', result=None, str=f"Рейс с номером {flight_num} не найден")


@order_app.route('/sql_task2', methods=['GET', 'POST'])
@group_permission_decorator
def sql2():
    if request.method == 'GET':
        return render_template('user_input_tsk2.html')
    from_date = request.form.get('from_date', None)
    to_date = request.form.get('to_date', None)
    sql = provider.get('task_2.sql', from_date=from_date, to_date=to_date)
    result = work_with_db(config=db_config, sql=sql)
    return render_template('result_for_2.html', result=result, str=f"В период с {from_date} по {to_date} не было отправлено или запланировано рейсов.", str_info=f"в период с {from_date} по {to_date}")
