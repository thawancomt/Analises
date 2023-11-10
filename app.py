from tinydb import TinyDB, Query
from flask import Flask, render_template, request, redirect, flash
from functions import StoreAnalysis, store_dict
from users_manager import Users, usersdb
from sessions import Session

from datetime import datetime

app = Flask(__name__)
app.secret_key = 'thawan'

db = TinyDB('databases/dados.json', indent=4)


@app.route('/')
def index():
    return redirect('/homepage')


@app.route('/homepage')
def home():
    conected_user = Session(request.remote_addr)
    return render_template('html/homepage.html', current_user=Session(request.remote_addr).get_session())


@app.route('/faturamento', methods=['GET', 'POST'])
def show_billing():

    if conect_user() != 'Guest' and conect_user()['admin']:
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
    conected_user = Session(request.remote_addr)

    status = ''

    if request.method == 'POST':

        email = request.form.get('email')
        pwd = request.form.get('password')

        object_user = Users(email=email, password=pwd)
        object_user.login()

        status = object_user.status
        is_admin = object_user.admin

        if object_user.status == 'loged':
            conected_user.username, conected_user.admin, conected_user.loged = object_user.username, is_admin, status
            conected_user.create_session()

            return redirect('homepage')
        else:
            flash(f'{object_user.status}')

    return render_template('html/homepage.html', current_user=Session(request.remote_addr).get_session())


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

        # Check if the new user is admin, checking if "isAdmin" is in request form
        if 'isAdmin' in request.form:
            admin = True
        else:
            admin = False

        # the next objetive is make register be a login required function
        object_register = Users(username=username, email=email,
                                password=password, admin=admin)

        object_register.create_user()

        status = object_register.status

        return render_template('html/register.html',
                               status=status,
                               password=password)

    return render_template('html/register.html',
                           status=status,
                           password=password)


@app.route('/users')
def users():
    user_list = usersdb.search(Query().email != '')
    return render_template('/html/users.html', users=user_list, current_user=conect_user()['username'])


@app.route('/users/<username>', methods=['GET', 'POST'])
def user(username):
    new_username = username
    if request.method == 'POST':
        if session['admin']:
            new_username = request.form.get('username')
            new_email = request.form.get('email')
            new_password = request.form.get('password')
            password_confirmation = request.form.get('password_confirmation')

            User = Users(username=username)

            User.username = new_username
            User.email = new_email
            User.password = new_password

            if str(new_password) == str(password_confirmation):

                User.edit_user_info(username)
            else:
                return f'{new_password} -  {password_confirmation}'

            return redirect(f'/users/{User.username}')
        else:
            return 'Apenas admins podem editar'

    return render_template('/html/user_profile.html', username=new_username,
                           old_user_info=Users(username=username))


app.run(debug=True, host='0.0.0.0', port=5000)
