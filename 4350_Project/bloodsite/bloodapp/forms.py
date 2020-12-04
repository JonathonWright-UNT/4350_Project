from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, Optional
from bloodapp.models import Donor, Staff, Bank


class EmployeeForm(FlaskForm):
    """This is the form where an employee can update their account
    Args:
        first_name (str): The first name of the staff
        last_name (str): the last name
        password (str): their password for their account
        email (str): Their email address
        role (str): Their job title
        location (str): The branch they work in"""

    banks = Bank.query.all()
    bank_names = [item.location for item in banks]

    first_name = StringField('First Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    password = PasswordField('Password',
                             validators=[InputRequired(), Length(min=5)])

    email = StringField('Email',
                             validators=[InputRequired(), Length(min=5, max=25)])

    role = StringField('Role',
                           validators=[Length(min=2, max=25)])

    location = SelectField('location', choices=bank_names, validators=[InputRequired()])

    submit = SubmitField('Create User')
               



class LoginForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(min=5)])
    email = StringField('Email',
                             validators=[InputRequired(), Length(min=5, max=25)])
    submit = SubmitField('Sign In')


class CreateDonorForm(FlaskForm):
    bloods = ['O-',	'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']

    blood_type = SelectField('blood_type', choices=bloods, validators=[InputRequired()])
    
    first_name = StringField('First Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    age = IntegerField('Age', validators=[InputRequired()])
    
    email = StringField('Email', validators=[InputRequired(), Email(check_deliverability=True)])

    submit = SubmitField('Create Donor')

    def validate_email(self, email):
        donor = Donor.query.filter_by(email=email.data).first()
        if donor:
            raise ValidationError('A donor with that email already exists')



class UpdateDonorForm(FlaskForm):
    """This form is for the employee to update the donor"""
    bloods = ['O-',	'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']

    blood_type = SelectField('blood_type', choices=bloods, validators=[InputRequired()])
    
    first_name = StringField('First Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    age = IntegerField('Age', validators=[InputRequired()])
    
    email = StringField('Email', validators=[InputRequired(Email(check_deliverability=True))])

    submit = SubmitField(f'Update Donor')

    def validate_email(self, email):
        """Validates that the email is unique"""
        donor = Donor.query.filter_by(email=email.data).first()
        if donor:
            if donor.email == self.email.data:
                return
            if donor.first_name == self.first_name.data and donor.last_name == self.last_name.data:
                return
            raise ValidationError('A donor with that email already exists')



class DonorForm(FlaskForm):
    """This is to load for the Donor:
    Args:
       first_name (str): The first name of the donor
       last_name (str): the last name
       last_blood_donation_date (date): the last time they donated blood
       last_plasma_donation_date (date): the last time they donated plasma
       blood_type(str): Their blood type
       age (int): their age
       email (str): Their email address """
    donor_id = IntegerField('Donor ID', validators=[Optional(strip_whitespace=True)])

    first_name = StringField('First Name',
                           validators=[])

    last_name = StringField('Last Name',
                           validators=[])

    email = StringField('Email', validators=[])

    submit = SubmitField('Load Donor')

    def validate_email(self, email):
        if self.donor_id.data:
            return
        elif not self.email.data:        
            raise ValidationError("Both names and email must be filled!")

    def validate_first_name(self, first_name):
        if self.donor_id.data:
            return
        elif not self.first_name.data:        
            raise ValidationError("Both names and email must be filled!")

    def validate_last_name(self, last_name):
        if self.donor_id.data:
            return
        elif not self.last_name.data:        
            raise ValidationError("Both names and email must be filled!")

class DonationForm(FlaskForm):
    """This allows for the selection of Donating plasma, blood, or updating the donor account"""
    donate_blood = SubmitField()
    donate_plasma = SubmitField()
    update_donor = SubmitField()
    

class WithdrawForm(FlaskForm):
    """This is the model for the Donor:
    Args:
       blood_type(str): Their blood type
       blood (bool): if the donation is blood
       plasma (bool): if the donation is plasma
       units (int): The amount of units requested"""
    bloods = ['O-',	'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']
    options = ['Blood', 'Plasma']
    blood_type = SelectField('Blood Type', choices=bloods, validators=[DataRequired()])
    blood_or_plasma = SelectField('Blood or Plasma', choices=options, validators=[DataRequired()])
    units = StringField('units', validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def validate_units(self, units):
        """This pulls in the units inputs as either a number or the word all"""
        try:
            if int(units.data):
                pass
        except Exception as e:
            if units.data.lower() != "all":
                raise ValidationError('Please enter the number of units you wish to have, or simply type "All"')
        

class CreateEmployeeForm(FlaskForm):
    """This is the form where an employee can create their account
    Args:
        first_name (str): The first name of the staff
        last_name (str): the last name
        password (str): their password for their account
        email (str): Their email address
        role (str): Their job title
        location (str): The branch they work in"""
    
    banks = Bank.query.all()
    bank_names = [item.location for item in banks]
    roles = ["Nurse", "Doctor", "Admin"]

    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5)])
                             
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), Length(min=5), EqualTo('password')])
    
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=25)])

    role = SelectField('Role', choices=roles, validators=[DataRequired()])

    location = SelectField('location', choices=bank_names, validators=[DataRequired()])

    submit = SubmitField('Create Employee')

    def validate_email(self, email):
        staff = Staff.query.filter_by(email=email.data).first()
        if staff:
            raise ValidationError('An employee with that email already exists')

class BankForm(FlaskForm):
    """This is the form to create a new bank
    Args:
        location (str): The location of the bank
        manager_id (int) (FK): This is the id of the manager of the bank"""
    location = StringField('Location Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    manager_id = IntegerField('Manager ID',
                           validators=[DataRequired()])
    
    submit = SubmitField('Create  Bank')

    def validate_location(self, location):
        """Here we validate that a branch does not already have that name"""
        bank = Bank.query.filter_by(location=location.data).first()
        if bank:
            raise ValidationError('A bank already exists at that location')

class RequestResetForm(FlaskForm):
    """This is the form to send an password reset request, it just takes an email address"""
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        """This verifies an account exists"""
        staff = Staff.query.filter_by(email=email.data).first()
        if staff is None:
            raise ValidationError('There is no account with that email. You must register first.')    

class ResetPasswordForm(FlaskForm):
    """This is the passwird reset form"""
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), Length(min=5), EqualTo('password')])
    submit = SubmitField('Reset Password')                    

class UpdateEmployeeForm(FlaskForm):
    """This is the form where an employee can update their account
    Args:
        first_name (str): The first name of the staff
        last_name (str): the last name
        password (str): their password for their account
        email (str): Their email address
        role (str): Their job title
        location (str): The branch they work in"""
    banks = Bank.query.all()
    bank_names = [item.location for item in banks]
    roles = ["Nurse", "Doctor", "Admin"]

    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    # password = StringField('Password')
    
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=25)])

    role = SelectField('Role', choices=roles,
                           validators=[Length(min=2, max=25)])

    location = SelectField('location', choices=bank_names, validators=[DataRequired()])

    submit = SubmitField('Update Employee')

    def validate_email(self, email):
        """This makes sure the email is unique"""
        staff = Staff.query.filter_by(email=email.data).first()
        if staff:
            if staff.email == current_user.email:
                return
            if staff.first_name == self.first_name.data and staff.last_name == self.last_name.data:
                return
        elif staff:
            raise ValidationError('A donor with that email already exists')

