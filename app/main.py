from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from database import Config


app = Flask(__name__, static_folder='static', template_folder='templates')
login_manager = LoginManager(app)
app.config.from_object(Config)
db = SQLAlchemy()
migrate = Migrate(app, db)
admin = Admin(app, name='My Admin Panel', template_mode='bootstrap4')
from models import User


@app.route("/")
def index():
    messag = 'Welcome'
    return render_template('base.html', hw=messag)


@app.route("/register", methods=['GET', 'POST'] )
def register():
    form3 = LoginForm()
    if request.method == 'POST':
        if form3.validate_on_submit():
            name = form3.username.data
            data = User(name=form3.username.data, password=form3.password.data, is_active=False)
            db.session.add(data)
            db.session.commit()
            flash('ПОЛЬЗОВАТЕЛЬ ' + name + ' ЗАРЕГИСТРИРОВАН')
            return redirect(url_for('index'))
    return render_template('register.html', form2=form3)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        print('*' * 20)
        print(user)
        if user is None or not user.check_password(form.pasword.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('base'))
    return render_template('login_enter.html', form=form)


@app.route('/')
def logout():
    logout_user()
    render_template('base.html')
    #return redirect(url_for('base'))


def seed_db():
    with app.app_context():
        db.create_all()
        have_user = User.query.first()
        print(have_user)
        if not have_user:
             from seed import seeds
             seeds()



if __name__ == '__main__':
    seed_db()
    app.run(port=5001, debug=True)
