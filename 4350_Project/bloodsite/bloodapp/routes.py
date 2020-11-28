from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from bloodapp.forms import CreateDonorForm, CreateEmployeeForm, LoginForm
from bloodapp.models import Donor, Staff
from bloodapp import app, db, bcrypt


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



@app.route('/', methods=["GET", "POST"])
def createDonor():
    form = CreateDonorForm()
    if form.validate_on_submit():
        donor = Donor(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    age=form.age.data, blood_type=form.blood_type.data)
        db.session.add(donor)
        db.session.commit()
        flash(f'Donor Added To database,', category='Success')
    return render_template('new_donor.html', title="Register", form=form)

@app.route('/register', methods=["GET", "POST"])
def createEmployee():
    form = CreateEmployeeForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        staff = Staff(first_name=form.first_name.data, last_name=form.last_name.data, password=hashed_password, 
                    email=form.email.data, role=form.role.data, location_id=form.location_id.data)
        db.session.add(staff)
        db.session.commit()
        flash(f'Employee Added To Database', category='Success')
    return render_template('new_employee.html', title="Register", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(email=form.email.data.lower()).first()
        if staff and bcrypt.check_password_hash(staff.password, form.password.data):
            login_user(staff, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Login failed, please check email and password')
    return render_template('login.html', title="Login", form=form)
