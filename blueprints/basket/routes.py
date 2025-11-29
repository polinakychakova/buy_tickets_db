import os
from datetime import date

from flask import Blueprint, redirect, render_template, request, session, current_app, url_for

# from blueprints.basket.NOTNEEDutils import add_to_basket, clear_basket
from configs.access import group_permission_decorator
from sql_provider import SQLProvider
from dbcon import get_db_config, work_with_db, make_update

basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
db_config = get_db_config()


@basket_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def list_order_handler():
    # db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('list_departs.sql')
        items = work_with_db(db_config, sql)
        return render_template('basket_list.html', items=items)
    else:
        idDeparture = request.form['idDeparture']
        session['idDeparture'] = idDeparture
        sql = provider.get('order_item.sql', idDeparture=idDeparture)
        item = work_with_db(db_config, sql)
        return render_template('input_ticket.html', item=item)


@basket_app.route('/insert_info', methods=['GET', 'POST'])
@group_permission_decorator
def insert_ticket():
    if request.method == 'GET':
        idDeparture = session.get('idDeparture')
        sql = provider.get('order_item.sql', idDeparture=idDeparture)
        item = work_with_db(db_config, sql)
        # print(item)
        return render_template('input_ticket.html', idDeparture=idDeparture)
    else:
        Passenger_LastName = request.form.get('Passenger_LastName')
        Pasport = request.form.get('Pasport')
        Passenger_FirstName = request.form.get('Passenger_FirstName')
        idcashier = request.form.get('idcashier')
        idDeparture = session.get(('idDeparture'))
        sql = provider.get('insert_ticket.sql',  DATE_sell=date.today(), Passenger_LastName=Passenger_LastName, Passenger_FirstName=Passenger_FirstName, Pasport=Pasport, idcashier=idcashier, idDeparture=idDeparture)
        # print(sql)
        result = work_with_db(db_config, sql)
        # print(result)
        sql = provider.get('list_departs.sql')
        result = work_with_db(db_config, sql)
        return render_template('basket_list.html', result=result)


@basket_app.route('/clear')
@group_permission_decorator
def clear_basket_handler():
    sql = provider.get('list_departs.sql')
    result = work_with_db(db_config, sql)
    return render_template('basket_list.html', result=result)


#     <!-- CSS only -->
# <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
# <!-- JavaScript Bundle with Popper -->
# <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>