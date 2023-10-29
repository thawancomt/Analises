from tinydb import TinyDB, Query
from flask import Flask, render_template, request, redirect
from flask_login import login_required, login_user, logout_user, LoginManager
from functions import *
from teste import users

app = Flask(__name__)

db = TinyDB('databases/dados.json')

usersdb = TinyDB('databases/users.json', indent=4)

loged = False

session = {}


@app.route('/')
def home():
    return render_template('html/homepage.html')


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
    before_and_after = None

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

                before_and_after = increment_date(int(store), date)

                tabela = get_production_info

        except:

            total = 'Valor nao encontrado no banco de dados'

    return render_template('html/faturamento.html', billing=total, billing_card=card, billing_money=money,
                           tabela=tabela, store=store_name, usage=usage, db=db, store_list=store_list,
                           usage_ballbna=before_and_after)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    from teste import users

    global loged
    status = 'Log In'

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
            pass

    return render_template('html/login.html', status=status)
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        # Instacia o usuario e chama a funcao criar user da classe users
        object_user = users(email, password)
        object_user.create_user(usersdb, email, password)

    return render_template('html/register.html')


app.run(debug=True, host='0.0.0.0', port=5000)
