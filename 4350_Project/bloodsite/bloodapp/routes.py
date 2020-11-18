from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from bloodapp.forms import CreateDonorForm
from bloodapp.models import Donor
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
