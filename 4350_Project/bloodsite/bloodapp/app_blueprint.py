from flask import render_template, url_for, flash, redirect
from bloodapp import app, db, Bcrypt
from bloodapp.forms import RegistrationForm, LoginForm


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018',
        'image': 'https://pictures.abebooks.com/isbn/9781259872976-us-300.jpg'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018',
        'image': 'https://pictures.abebooks.com/isbn/9781259872976-us-300.jpg'
    }
]

@app_blueprint.route('/')
def index():
    return render_template('home.html', posts=posts)


@app_blueprint.route('/about')
def about():
    return render_template('about.html')


@app_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', category='Success')
        return redirect(url_for('app_blueprint.index'))
    return render_template('register.html', title="Register", form=form)

@app_blueprint.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)