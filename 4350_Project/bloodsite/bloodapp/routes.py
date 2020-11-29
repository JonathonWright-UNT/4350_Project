import datetime
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from bloodapp.forms import CreateDonorForm, UpdateDonorForm, DonorForm, DonationForm, WithdrawForm, CreateEmployeeForm, LoginForm
from bloodapp.models import Donor, Staff, Donation, Bank
from bloodapp import app, db, bcrypt



@app.route('/', methods=["GET", "POST"])
@login_required
def createDonor():
    form = CreateDonorForm()
    if form.validate_on_submit():
        donor = Donor(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    age=form.age.data, blood_type=form.blood_type.data)
        db.session.add(donor)
        db.session.commit()
        flash(f'Donor Added To database,', category='Success')
    return render_template('new_donor.html', title="Register", form=form)


@app.route('/UpdateDonor/<int:donor_id>', methods=["GET", "POST"])
@login_required
def UpdateDonor(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    form = UpdateDonorForm()
    if form.validate_on_submit():
        donor.first_name=form.first_name.data
        donor.last_name=form.last_name.data
        donor.email=form.email.data
        donor.age=form.age.data
        donor.blood_type=form.blood_type.data
        db.session.commit()
        flash(f'Donor Updated', category='Success')
    elif request.method == 'GET':
        form.first_name.data=donor.first_name
        form.last_name.data=donor.last_name
        form.email.data=donor.email
        form.age.data=donor.age
        form.blood_type.data=donor.blood_type
    return render_template('update_donor.html', title="Update Donor", form=form)


@app.route('/LoadDonor', methods=["GET", "POST"])
@login_required
def LoadDonor():
    form = DonorForm()
    donor = None
    if form.validate_on_submit():
        if form.donor_id:
            donor = Donor.query.filter_by(id=form.donor_id.data).first()
    #     elif form.first_name and form.email:
    #         donor = Donor.query.filter_by(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data).first()
    if donor:
        return redirect(url_for('DonorPage', donor_id=donor.id))
    # elif request.method == 'POST':
        flash(f'No Donor was detected')
    return render_template('load_donor.html', title="Load Donor", form=form)

@app.route('/withdraw', methods=["GET", "POST"])
@login_required
def withdraw():
    form = WithdrawForm()
    units = None
    if form.validate_on_submit():
        if form.blood_or_plasma.data == 'Blood':
            units = Donation.query.filter_by(blood_type=form.blood_type.data, blood=True)
            if form.units.data.lower() == "all" or units.count < form.units.data:
                for unit in units:
                    db.session.delete(unit)
                db.session.commit()
            else:
                for unit in range(form.units.data):
                    db.session.delete(units[unit])
                db.session.commit()

        elif form.blood_or_plasma.data == 'Plasma':
            units = Donation.query.filter_by(blood_type=form.blood_type.data, plasma=True)
            if form.units.data.lower() == "all" or units.count < form.units.data:
                for unit in units:
                    db.session.delete(unit)
                db.session.commit()
            else:
                for unit in range(form.units.data):
                    db.session.delete(units[unit])
                db.session.commit()
        if units:
            if units.count() > 0:
                flash(f'We currently have {units.count()} units of that type')
            elif units.count() == 0:
                flash(f'We currently have no units of that type')
    return render_template('withdraw.html', title="withdraw", form=form)


@app.route('/DonorPage/<int:donor_id>', methods=["GET", "POST"])
@login_required
def DonorPage(donor_id):
    print(donor_id)
    donor = Donor.query.get_or_404(donor_id)
    form=DonationForm()
    if form.validate_on_submit():
        if form.donate_blood.data:
            if donor.last_blood_donation_date is None or (donor.last_blood_donation_date.timestamp() + 4838400)  < datetime.datetime.now().timestamp():
                donation = Donation(blood_type=donor.blood_type, blood=True, plasma=False, location=1)
                db.session.add(donor)
                donor.last_blood_donation_date = datetime.datetime.now()
                db.session.commit()
                flash(f'Blood Donated!', category='Success')
            else:
                last_donation = donor.last_blood_donation_date
                e = datetime.timedelta(weeks=8)
                eligable = last_donation + e
                flash(f'Donor not yet eligible to donate')
                flash(f'{Donor.first_name} will be eligable on {eligable}')
        elif form.donate_plasma.data:
            if donor.last_plasma_donation_date is None or (donor.last_plasma_donation_date.timestamp() + 2419200)  < datetime.datetime.now().timestamp():
                donation = Donation(blood_type=donor.blood_type, blood=False, plasma=True, location_id=0)
                db.session.add(donor)
                donor.last_plasma_donation_date = datetime.datetime.now()
                db.session.commit()
                flash(f'Plasma Donated!', category='Success')
            else:
                last_donation = donor.last_plasma_donation_date
                e = datetime.timedelta(weeks=4)
                eligable = last_donation + e
                flash(f'Donor not yet eligible to donate')
                flash(f'{Donor.first_name} will be eligable on {eligable}')
        elif form.update_donor:
            return redirect(url_for('UpdateDonor', donor_id=donor.id))
    return render_template('donor.html', title="Donor", form=form, donor=donor)

@app.route('/register', methods=["GET", "POST"])
def createEmployee():
    form = CreateEmployeeForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        staff = Staff(first_name=form.first_name.data, last_name=form.last_name.data, password=hashed_password, 
                    email=form.email.data, role=form.role.data, location=form.location.data)
        db.session.add(staff)
        db.session.commit()
        flash(f'Employee Added To Database', category='Success')
    return render_template('new_employee.html', title="Register", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(email=form.email.data).first()
        if staff and bcrypt.check_password_hash(staff.password, form.password.data):
            login_user(staff)
            next_page = request.args.get('next')
            flash(f'Login successful')
            return redirect(next_page) if next_page else redirect(url_for(''))
        else:
            flash(f'Login failed, please check email and password')
    return render_template('login.html', title="Login", form=form)
