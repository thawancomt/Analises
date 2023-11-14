from tinydb import TinyDB, Query
from flask import Flask, render_template, request, redirect, flash
from functions import StoreAnalysis, store_dict
from managers.sessions import Session
from managers.users_manager import Users, usersdb
from managers.production import Production, DbConnection
from datetime import date as dt


from datetime import datetime

app = Flask(__name__)
app.secret_key = 'thawan'

db = TinyDB('managers/databases/dados.json', indent=4)


def get_user_data():
    return Session(request.remote_addr).get_session()


@app.route('/')
def index():
    return redirect('/homepage')


@app.route('/homepage')
def home():

    connected_user = Users(username=get_user_data()['username'])
    if not Session(request.remote_addr).get_session()['loged']:
        return redirect('/login')

    return render_template('html/homepage.html',
                           current_user=get_user_data()['username'],
                           isadmin=get_user_data()['admin'],
                           store=store_dict[int(connected_user.store)],
                           last_login=connected_user.last_login)


# @app.route('/homepage/faturamento')
# def show_billing():
#     return render_template('/html/faturamento.html')


@app.route('/faturamento', methods=['GET', 'POST'])
def billing():

    if Session(request.remote_addr).get_session()['admin']:
        pass

    else:
        return redirect('/login')

    billing: list = None

    items_production: list = None

    items_usage:  list = None

    store_name = None

    data_to_chart = []

    if request.method == 'POST':

        date = request.form.get('date')
        store = int(request.form.get('stores'))

        try:
            # change the name to object_store
            analisy = StoreAnalysis(store, date)

            store_name = analisy.define_store()

            billing = analisy.get_billing()

            items_production = analisy.get_production()

            items_usage = analisy.get_usage()

            data_to_chart = analisy.create_data_to_ball_usage_chart(-7)

        except:

            total = 'Valor nao encontrado no banco de dados'

    return {'store_name': store_name,
            'items_production': items_production,
            'items_usage': items_usage,
            'billing': billing,
            'data_to_chart': data_to_chart}


@app.route('/login',  methods=['GET', 'POST'])
def login():
    connected_user = Session(request.remote_addr)

    status = ''

    if request.method == 'POST':

        email = request.form.get('email')
        pwd = request.form.get('password')

        object_user = Users(email=email, password=pwd)
        object_user.login()

        status = object_user.status
        is_admin = object_user.admin

        if status == 'loged':
            connected_user.username = object_user.username
            connected_user.admin = is_admin
            connected_user.loged = True

            connected_user.create_session()

            return redirect('homepage')
        else:
            flash(f'{object_user.status}')

    return render_template('html/login.html',
                           current_user=connected_user.get_session()['username'])


def check_loged():
    if not Session(request.remote_addr).get_session()['loged']:
        return redirect('/login')


@app.route('/logoff')
def log_off():
    Session(request.remote_addr).logoff()
    return redirect('/homepage')


@app.route('/register', methods=['GET', 'POST'])
def register():

    username = ''
    status = ''
    password = ''

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        store_id = request.form.get('store')

        # Check if the new user is admin, checking if "isAdmin" is in request form
        if 'isAdmin' in request.form:
            admin = True
        else:
            admin = False

        # the next objetive is make register be a login required function
        object_register = Users(username=username, email=email,
                                password=password, admin=admin,
                                store=store_id)

        object_register.create_user()

        status = object_register.status
    check_loged()
    return render_template('html/register.html',
                           status=status,
                           password=password,
                           store_dict=store_dict)


@app.route('/users')
def users():
    user_list = usersdb.search(Query().email != None)

    connected_user = Session(request.remote_addr)

    return render_template('/html/users.html',
                           users=user_list,
                           current_user=get_user_data()['username'])


@app.route('/users/<username>', methods=['GET', 'POST'])
def user(username):
    new_username = username

    if request.method == 'POST':
        if Session(request.remote_addr).get_session()['admin']:

            new_username = request.form.get('username')

            new_email = request.form.get('email')

            new_password = request.form.get('password')
            password_confirmation = request.form.get('password_confirmation')

            new_store = request.form.get('store')

            User = Users(username=username)
            User.store = new_store

            if not new_username == '':
                User.username = new_username
            elif not new_email == '':
                User.email = new_email
            elif not new_store == '':
                User.store = new_store

            if new_password == '' and password_confirmation == '':
                User.password = Users().check_user_exists(
                    username=username)[0]['password']
            else:
                User.password = password_confirmation

            if new_password == password_confirmation:
                User.edit_user_info(username)

        else:
            return 'Apenas admins podem editar'

    return render_template('/html/user_profile.html',
                           username=username,
                           old_info=Users(username=username),
                           store_dict=store_dict
                           )


@app.route('/production', methods=['GET', 'POST'])
def enter_production():

    conection = DbConnection('teste.json')

    conection.store = int(Users(username=get_user_data()['username']).store)

    date = 0

    production = Production()

    if request.method == 'POST':

        big_ball = request.form.get('big_balls')
        small_ball = request.form.get('small_balls')
        garlic_bread = request.form.get('garlic_bread')
        date = request.form.get('date')
        store = request.form.get('store')
        conection.store = int(store)

        production = Production()

        production.big_balls = int(big_ball)
        production.small_balls = int(small_ball)
        production.garlic_bread = int(garlic_bread)
        production.date = date
        conection.data = production.get_data()
        conection.insert()

    return redirect(f'/production/{conection.store}/{dt.today()}')


@app.route('/production/<store>/<date>', methods=['GET', 'POST'])
def production_view(date, store):
    is_admin = get_user_data()['admin']

    if get_user_data()['username'] != None:

        connection = DbConnection('teste.json')
        connection.store = store
        data = connection.get_data(date=date)[0]

        user_store = Users(username=get_user_data()['username']).store

        return render_template('/html/production.html',
                               store_dict=store_dict,
                               articles=Production().articles,
                               produced=data,
                               user_store=user_store,
                               store=store,
                               current_user=get_user_data()['username'],
                               is_admin=is_admin)
    else:
        return redirect('/homepage')


app.run(debug=True, host='0.0.0.0', port=5000)
