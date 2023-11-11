from tinydb import TinyDB, Query
from flask import Flask, render_template, request, redirect, flash
from functions import StoreAnalysis, store_dict
from managers.sessions import Session
from managers.users_manager import Users, usersdb
from managers.production import Production, DbConnection


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
    return render_template('html/homepage.html',
                           current_user=get_user_data()['username'])


@app.route('/faturamento', methods=['GET', 'POST'])
def show_billing():

    if Session(request.remote_addr).get_session()['admin']:
        pass

    else:
        return redirect('/login')

    billing: list = None
    """
        Receive a list of amount of billing
            {   
                0 : money
                1 : card
                2 : total
            }
    """

    items_production: list = None
    """
        Receive a list of products amounts
            {
                0 : garlic bread
                1 : small_ball
                2 : big_ball
            }
    """

    items_usage:  list = None
    """
        Receive a list of amount of usaged items
        {
            0: garlic bread
            1: small_ball
            2: big_ball
            3: chessse
        }
    """

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

    return render_template('html/faturamento.html',
                           store=store_name,
                           billing=billing,
                           production=items_production,
                           usage_balls=items_usage,
                           usage_chart=data_to_chart,
                           store_dict=store_dict)


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

    return render_template('html/homepage.html',
                           current_user=connected_user.get_session()['username'])


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

            User.password = new_password
            User.store = new_store

            if not new_username == '':
                User.username = new_username
            elif not new_email == '':
                User.email = new_email
            elif not new_store == '':
                User.store = new_store
            elif new_password == '' and password_confirmation == '':
                User.password = Users.check_user_exists(
                    username=username)[0]['password']

            if str(new_password) == str(password_confirmation):

                User.edit_user_info(username)
            else:
                return f'{new_password} -  {password_confirmation}'

            return redirect(f'/users/{User.username}')
        else:
            return 'Apenas admins podem editar'

    return render_template('/html/user_profile.html',
                           username=username,
                           old_info=Users(username=username),
                           store_dict=store_dict
                           )


@app.route('/production', methods=['GET', 'POST'])
def production():
    if Session(request.remote_addr).get_session()['admin']:
        if request.method == 'POST':

            big_ball = request.form.get('big_ball')
            small_ball = request.form.get('small_ball')
            garlic_bread = request.form.get('garlic_bread')

            production = Production()

            production.big_balls = int(big_ball)
            production.small_balls = int(small_ball)
            production.garlic_bread = int(garlic_bread)

            conection = DbConnection('teste.json')
            conection.data = production.get_data()
            conection.store = Users(username=get_user_data()['username']).store
            conection.insert()
    else:
        return 'not permissive'

    return render_template('/html/production.html', store_dict=store_dict,
                           current_user=get_user_data()['username'],
                           store=Users(username=get_user_data()['username']).store)


app.run(debug=True, host='0.0.0.0', port=5000)
