from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_manager, login_user, current_user, login_required, logout_user, LoginManager
from dashboard.forms import RegForm, LoginForm
from flask_mongoengine import MongoEngine , Document
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['MONGODB_SETTINGS'] = {
'DB': 'flask_project',
 'host':"mongodb+srv://meetupadhyay59:Vp3kLDvUkFTnqpKA@cluster0.lfs0r8l.mongodb.net/"
}
db = MongoEngine(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'




class User(UserMixin, db.Document):
    meta = {'collection': 'login_data'}
    username = db.StringField(max_length = 10)
    email = db.StringField(max_length=30)
    password = db.StringField()


login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = bcrypt.generate_password_hash(form.password.data)
                hey = User(username = form.username.data, email = form.email.data,password =hashpass).save()
                login_user(hey)
                flash("Succsefully register ")
                return redirect(url_for('dashboard'))
            flash("select different username aur email id")
    return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(username=form.username.data).first()
            if check_user:
                if  bcrypt.check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    flash("You have Succesfully Login!!!")
                    return redirect(url_for('dashboard'))
            flash("Invalid Cred!")
    return render_template('login.html', form=form)



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    flash("Succesfully Logout")
    return redirect(url_for('login'))