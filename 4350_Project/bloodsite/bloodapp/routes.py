import datetime
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from bloodapp.forms import CreateDonorForm, UpdateDonorForm, DonorForm, DonationForm, RequestResetForm, ResetPasswordForm
from bloodapp.forms import WithdrawForm, CreateEmployeeForm, LoginForm, UpdateEmployeeForm, BankForm
from bloodapp.models import Donor, Staff, Donation, Bank
from bloodapp import app, db, bcrypt, mail



@app.route('/createDonor', methods=["GET", "POST"])
@login_required
def createDonor():
    """This routes to the page where you create the donor
    Args (all taken in on valid submit of the CreateDonorForm):
       first_name (str): The first name of the donor
       last_name (str): the last name
       blood_type(str): Their blood type
       age (int): their age
       email (str): Their email address"""

    form = CreateDonorForm()
    if form.validate_on_submit():
        donor = Donor(first_name=form.first_name.data.lower(), last_name=form.last_name.data.lower(), email=form.email.data.lower(),
                    age=form.age.data, blood_type=form.blood_type.data)
        db.session.add(donor)
        db.session.commit()
        send_donor_email(donor)
        flash(f'Donor Added To Database', category='Success')
        return redirect(url_for('DonorPage', donor_id=donor.id))
    return render_template('new_donor.html', title="Register", form=form)

def send_donor_email(donor):
    """Sends new donors an email informing them of their ID
    Args:
        donor (obj): This is a donor from the DONOR table
    Returns:
        None"""
    msg = Message('New Donor ID', 
                   sender='NoReplyBloodBank@my.unt.edu', 
                   recipients=[donor.email])
    msg.body = f"""Thank you, {donor.first_name} for choosing to donate blood!
                   Your Donor ID is {donor.id}
                   We appreciate your blood!"""
    try:
        mail.send(msg)
    except Exception as e:
        print(e)

@app.route('/logout')
def logout():
    """Logs out user"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/UpdateDonor/<int:donor_id>', methods=["GET", "POST"])
@login_required
def UpdateDonor(donor_id):
    """"This routes to the page where you update the donor
    Args (all taken in on valid submit of the UpdateDonorForm):
       donor_id (int): the donors id, this loads their entry in the database
    The rest are optional:
       first_name (str): The first name of the donor
       last_name (str): the last name
       blood_type(str): Their blood type
       age (int): their age
       email (str): Their email address"""
    donor = Donor.query.get_or_404(donor_id)
    form = UpdateDonorForm()
    if form.validate_on_submit():
        donor.first_name=form.first_name.data.lower()
        donor.last_name=form.last_name.data.lower()
        donor.email=form.email.data.lower()
        donor.age=form.age.data
        donor.blood_type=form.blood_type.data
        db.session.commit()
        flash(f'Donor Updated', category='Success')
    elif request.method == 'GET':
        form.first_name.data=donor.first_name.capitalize()
        form.last_name.data=donor.last_name.capitalize()
        form.email.data=donor.email.capitalize()
        form.age.data=donor.age
        form.blood_type.choices=[donor.blood_type]
    return render_template('update_donor.html', title="Update Donor", form=form)


@app.route('/LoadDonor', methods=["GET", "POST"])
@login_required
def LoadDonor():
    """"This routes to the page where you load a donor
    Args (all taken in on valid submit of the DonorForm):
        donor_id (int): the id of the donor
        OR:
            first_name (str): The first name of the donor
            last_name (str): the last name
            email (str): Their email address"""
    form = DonorForm()
    donor = None
    if form.validate_on_submit():
        if form.donor_id.data:
            donor = Donor.query.filter_by(id=form.donor_id.data).first()
        elif form.first_name.data and form.email.data:
            donor = Donor.query.filter_by(first_name=form.first_name.data.lower(), last_name=form.last_name.data.lower(), email=form.email.data.lower()).first()
        if donor:
            return redirect(url_for('DonorPage', donor_id=donor.id))
        elif request.method == 'POST':
            flash(f'No Donor was detected')
    return render_template('load_donor.html', title="Load Donor", form=form)

def send_reset_email(staff):
    """Sends an employee a password reset token
    Args:
        staff (obj): This is a employee from the STAFF table
    Returns:
        None"""
    token = staff.get_reset_token()
    msg = Message('Password Reset Request', 
                   sender='NoReplyBloodBank@my.unt.edu', 
                   recipients=[staff.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request, then simply record this email and no changes will be made."""
    try:
        mail.send(msg)
    except Exception as e:
        print(e)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """An employee requests a password reset token"""
    if current_user.is_authenticated:
        return redirect('/home')
    form = RequestResetForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(email=form.email.data).first()
        send_reset_email(staff)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password',
                           form=form)
                          
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """This is where an employee can change their password using the token"""
    if current_user.is_authenticated:
        return redirect(url_for('LoadDonor'))
    staff = Staff.verify_reset_token(token)
    if staff is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        staff.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)                        
 

@app.route('/CreateBank', methods=["GET", "POST"])
@login_required
def CreateBank():
    """This page displays and creates new bank locations"""
    page_num = request.args.get('page', 1, type=int)
    form = BankForm()
    banks = Bank.query.paginate(per_page=5, page=page_num)
    table = {}
    for bank in banks.items:
        manager = Staff.query.filter_by(id=bank.manager_id).first()
        table.update({bank.location: {
            "id": bank.id,
            "location": bank.location,
            "manager": f"{manager.first_name.capitalize()} {manager.last_name.capitalize()}"
        }})
    if form.validate_on_submit():
        new_bank = Bank(location=form.location.data, manager_id=form.manager_id.data)
        db.session.add(new_bank)
        db.session.commit()
        flash(f'New Bank Created')
        return redirect(url_for('CreateBank'))
    return render_template('bank.html', title="Bank Page", form=form, table=table, banks=banks)

@app.route('/withdraw', methods=["GET", "POST"])
@login_required
def withdraw():
    """This page displays the current contents of all the banks and allows employees to make a withdraw"""
    form = WithdrawForm()
    units = None
    all_donations = {}
    donations = Donation.query.all()
    for item in donations:
        if item.location not in all_donations:
            all_donations.update({item.location: {}})
        if item.blood:
            entry = f"Blood Type {item.blood_type}"
            if entry not in all_donations[item.location]:
                all_donations[item.location].update({entry: {
                    "location": str(item.location),
                    "type": entry,
                    "count": 0}})
            all_donations[item.location][entry]["count"] += 1
        elif item.plasma:
            entry = f"Plasma Type {item.blood_type}"
            if entry not in all_donations[item.location]:
                all_donations[item.location].update({entry: {
                    "location": str(item.location),
                    "type": entry,
                    "count": 0}})
            all_donations[item.location][entry]["count"] += 1
    if form.validate_on_submit():
        shipped = 0
        if form.blood_or_plasma.data == 'Blood':
            units = Donation.query.filter_by(blood_type=form.blood_type.data, blood=True).all()
            if form.units.data.lower() == "all":
                for unit in units:
                    db.session.delete(unit)
                db.session.commit()
                shipped = "all"
            elif form.units.data.isnumeric():
                units_required = len(units)
                if int(form.units.data) < len(units):
                    units_required = len(units)
                for unit in units[:units_required]:
                    db.session.delete(unit)
                db.session.commit()
                shipped = units_required

        elif form.blood_or_plasma.data == 'Plasma':
            units = Donation.query.filter_by(blood_type=form.blood_type.data, plasma=True).all()
            if form.units.data.lower() == "all":
                for unit in units:
                    db.session.delete(unit)
                db.session.commit()
                shipped = "all"
            elif form.units.data.isnumeric():
                units_required = len(units)
                if int(form.units.data) < len(units):
                    units_required = len(units)
                for unit in units[:units_required]:
                    db.session.delete(unit)
                db.session.commit()
                shipped = units_required

        if len(units) > 0:
            flash(f'We have shipped {shipped} units', category='Success')
            return redirect(url_for('withdraw'))
        elif len(units) == 0:
            flash(f'We currently have no units of that type')
    return render_template('withdraw.html', title="withdraw", form=form, all_donations=all_donations)


@app.route('/DonorPage/<int:donor_id>', methods=["GET", "POST"])
@login_required
def DonorPage(donor_id):
    """This is the page that LoadDonor leads to, where the
    Donor can choose to donate or the donor can be updated
    Args:
        donor_id (int): this is the donors id"""
    donor = Donor.query.get_or_404(donor_id)
    form=DonationForm()
    if form.validate_on_submit():
        if form.donate_blood.data:
            if donor.last_blood_donation_date is None or (donor.last_blood_donation_date.timestamp() + 4838400)  < datetime.datetime.now().timestamp():
                donation = Donation(blood_type=donor.blood_type, blood=True, plasma=False, location=current_user.location)
                db.session.add(donation)
                donor.last_blood_donation_date = datetime.datetime.now()
                db.session.add(donor)
                db.session.commit()
                flash(f'Blood Donated!', category='Success')
            else:
                last_donation = donor.last_blood_donation_date
                e = datetime.timedelta(weeks=8)
                eligible = last_donation + e
                flash(f'Donor not yet eligible to donate')
                flash(f'{donor.first_name} will be eligible on {eligible}')
        elif form.donate_plasma.data:
            if donor.last_plasma_donation_date is None or (donor.last_plasma_donation_date.timestamp() + 2419200)  < datetime.datetime.now().timestamp():
                donation = Donation(blood_type=donor.blood_type, blood=False, plasma=True, location=current_user.location)
                db.session.add(donation)
                donor.last_plasma_donation_date = datetime.datetime.now()
                db.session.add(donor)
                db.session.commit()
                flash(f'Plasma Donated!', category='Success')
            else:
                last_donation = donor.last_plasma_donation_date
                e = datetime.timedelta(weeks=4)
                eligible = last_donation + e
                flash(f'Donor not yet eligible to donate')
                flash(f'{donor.first_name} will be eligible on {eligible}')
        elif form.update_donor:
            return redirect(url_for('UpdateDonor', donor_id=donor.id))
    return render_template('donor.html', title="Donor", form=form, donor=donor)

@app.route('/register', methods=["GET", "POST"])
def createEmployee():
    """This is the page where the employee can register"""
    form = CreateEmployeeForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        staff = Staff(first_name=form.first_name.data, last_name=form.last_name.data, password=hashed_password, 
                    email=form.email.data, role=form.role.data, location=form.location.data)
        db.session.add(staff)
        db.session.commit()
        flash(f'Employee Added To Database', category='Success')
        return redirect(url_for('login'))
    return render_template('new_employee.html', title="Register", form=form)

@app.route('/account', methods=["GET", "POST"])
@login_required
def UpdateEmployee():
    """This allows the logged in user to update their account"""
    staff = current_user
    form = UpdateEmployeeForm()
    if form.validate_on_submit():
        staff.first_name=form.first_name.data.lower()
        staff.last_name=form.last_name.data.lower()
        staff.email=form.email.data
        staff.location=form.location.data
        db.session.commit()
        flash(f'Employee Updated', category='Success')
    elif request.method == 'GET':
        form.first_name.data=staff.first_name.capitalize()
        form.last_name.data=staff.last_name.capitalize()
        form.email.data=staff.email
        form.role.choices=[staff.role]
        form.location.data=staff.location
    return render_template('update_employee.html', title="Update Employee", form=form)

@app.route('/')
@app.route('/home')
def home():
    """Home page"""
    return render_template('home.html', title="Home")

@app.route('/login', methods=["GET", "POST"])
def login():
    """This takes in the email and password of an employee and logs them in"""
    if current_user.is_authenticated:
        return redirect(url_for('LoadDonor'))
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(email=form.email.data).first()
        if staff and bcrypt.check_password_hash(staff.password, form.password.data):
            login_user(staff)
            next_page = request.args.get('next')
            flash(f'Login successful')
            return redirect(next_page) if next_page else redirect(url_for('createDonor'))
        else:
            flash(f'Login failed, please check email and password')
    return render_template('login.html', title="Login", form=form)

