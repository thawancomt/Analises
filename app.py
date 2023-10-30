from tinydb import TinyDB, Query
from flask import Flask, render_template, request, redirect
from flask_login import login_required, login_user, logout_user, LoginManager
from functions import StoreAnalysis, store_dict
from users_manager import users

app = Flask(__name__)

db = TinyDB('databases/dados.json', indent=4)

usersdb = TinyDB('databases/users.json', indent=4)


loged = False


@app.route('/')
def home():
    return redirect('login')


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

    items_usage = list
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
            print(date, store)

            analisy = StoreAnalysis(store, date)

            store_name = analisy.define_store()

            billing = analisy.get_billing()

            items_production = analisy.get_production()

            items_usage = analisy.get_usage()

            print(billing)

            data_to_chart = analisy.create_data_to_ball_usage_chart(-12)

        except:

            total = 'Valor nao encontrado no banco de dados'

    return render_template('html/faturamento.html', store=store_name, billing=billing, production=items_production, usage_balls=items_usage,
                           usage_chart=data_to_chart, store_dict=store_dict)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    from users_manager import users

    global loged
    status = ''

    def check_login(email, password):
        if usersdb.search((Query().email == email) &
                          (Query().password == password)):
            return True

        elif usersdb.search(Query().email == email)[0]['password'] != password:
            return False

        else:
            return 'user not found'

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        ip = request.remote_addr

        try:

            result = check_login(email, password)

            if result:

                loged = True
                ip = request.remote_addr
                print('Your IP is', ip)
                return redirect('faturamento')

            elif not result:
                status = 'The Password is invalid'

            elif result == 'user not found':
                status = 'User Not Found'

        except:
            status = 'User not found'

    return render_template('html/login.html', status=status)


@app.route('/register', methods=['GET', 'POST'])
def register():
    status = ''

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        # Instacia o usuario e chama a funcao criar user da classe users
        object_user = users(email, password)
        object_user.create_user(usersdb, email, password)

        status = object_user.status

        return render_template('html/register.html', status=status)

    return render_template('html/register.html', status=status)


app.run(debug=True, host='0.0.0.0', port=5000)
