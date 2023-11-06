from tinydb import TinyDB, Query
from flask import Flask, render_template, request, redirect
from functions import StoreAnalysis, store_dict
from users_manager import Users

app = Flask(__name__)

db = TinyDB('databases/dados.json', indent=4)

usersdb = TinyDB('databases/users.json', indent=4)


loged = False

current_user = ''


@app.route('/homepage')
def home():
    username = ''
    return render_template('html/homepage.html',
                           current_user=current_user)


@app.route('/faturamento', methods=['GET', 'POST'])
def show_billing():

    if loged:
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

    items_usage = list = None
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
    global current_user
    global loged
    status = ''

    if request.method == 'POST':

        email = request.form.get('email')
        pwd = request.form.get('password')

        if usersdb.search(
            (Query().email == email) &
            (Query().password == pwd)
        ):
            loged = True
            current_user = usersdb.search(Query().email == email)[
                0]['username']
            return redirect('faturamento')

        else:
            return redirect('users')

    return render_template('html/login.html', status=status)


@app.route('/register', methods=['GET', 'POST'])
def register():
    status = ''
    password = ''

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if 'isAdmin' in request.form:
            admin = True
        else:
            admin = False

        # Instacia o usuario e chama a funcao criar user da classe users
        object_user = Users(username=username, email=email,
                            password=password, admin=admin)
        object_user.create_user(usersdb, username, email, password)

        status = object_user.status

        return render_template('html/register.html',
                               status=status,
                               password=password)

    return render_template('html/register.html',
                           status=status,
                           password=password)


@app.route('/users')
def users():
    user_list = usersdb.search(Query().email != '')
    return render_template('/html/users.html', users=user_list, current_user=current_user)


@app.route('/users/<username>')
def user(username):
    username = 'Eu mesmo'
    return username


app.run(debug=True, host='0.0.0.0', port=5000)
