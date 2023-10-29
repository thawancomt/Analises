from tinydb import TinyDB, Query
from flask import Flask, render_template, request, redirect
from flask_login import login_required, login_user, logout_user, LoginManager
from functions import *
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

    total = ''
    card = 0
    money = 0
    tabela = None
    store_name = None
    usage = None
    db = None
    data_to_chart = []

    if request.method == 'POST':
        date = request.form.get('date')
        store = request.form.get('stores')

        try:
            if date == '':
                total = 'voce nao selecionou data'

            elif store == '0':
                total = 'voce nao selecionou a loja'

            else:
                get_total = get_billing(int(store), date)
                get_production_info = get_production(int(store), date)
                get_usage_info = get_usage(int(store), date)

                total = f"{get_total['TOTAL']:.2f}"
                card = get_total['CARD']
                money = get_total['MONEY']
                store_name = define_store(int(store))

                db = get_usage_info

                usage = get_usage_info[0]['usage']

                tabela = get_production_info

                data_to_chart = create_data_to_chart_ball_usage(
                    int(store), date)

        except:

            total = 'Valor nao encontrado no banco de dados'

    return render_template('html/faturamento.html', billing=total, billing_card=card, billing_money=money,
                           tabela=tabela, store=store_name, usage=usage, db=db, store_list=store_list, labels2=data_to_chart)


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
    status = 'asd'

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
