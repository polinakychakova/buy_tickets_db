import json

from flask import Flask, render_template, session  # , request, redirect
# from dbcon import get_db_config, work_with_db
from blueprints.basket.routes import basket_app
from blueprints.order.routes import order_app
from blueprints.scen_auth.routes import authen_app


app = Flask(__name__)

app.register_blueprint(order_app, url_prefix='/select')
app.register_blueprint(authen_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix='/basket')

app.config['SECRET_KEY'] = 'super secret key'
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/end')
def end():
    for key in list(session.keys()):
        session.pop(key)
    return render_template('end.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
