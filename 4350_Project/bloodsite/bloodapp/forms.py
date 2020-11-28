from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bloodapp.models import Donor, Staff


class EmployeeForm(FlaskForm):

    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5)])

    email = StringField('Email',
                             validators=[DataRequired(), Length(min=5, max=25)])

    role = StringField('Role',
                           validators=[Length(min=2, max=25)])
    location_id = StringField('Location ID',
                           validators=[Length(min=2, max=25)])
    submit = SubmitField('Create User')
               



class LoginForm(FlaskForm):
    pin = StringField('Employee ID Number',
                           validators=[Length(min=2, max=25)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5)])

    submit = SubmitField('Sign In')


class CreateDonorForm(FlaskForm):
    bloods = ['O−',	'O+', 'A−', 'A+', 'B−', 'B+', 'AB−', 'AB+']

    blood_type = SelectField('blood_type', choices=bloods, validators=[DataRequired()])
    
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    password = StringField('Password',
                           validators=[DataRequired(), Length(min=2, max=20)])

    age = IntegerField('Age', validators=[DataRequired()])
    
    email = StringField('Email', validators=[DataRequired()])

    submit = SubmitField('Create Donor')

    def validate_email(self, email):
        donor = Donor.query.filter_by(email=email.data).first()
        if donor:
            raise ValidationError('A donor with that email already exists')



class DonorForm(FlaskForm):
    donor_id = StringField('Donor ID', validators=[DataRequired()])

    submit = SubmitField('Load Donor')

class DonationForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    condition = StringField('Condition', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    submit = SubmitField('Post Book')
    

class WithdrawForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class CreateEmployeeForm(FlaskForm):
    
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    password = StringField('Password',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', validators=[DataRequired()])

    role = StringField('Role',
                           validators=[Length(min=2, max=25)])

    location_id = StringField('Location ID',
                           validators=[Length(min=2, max=25)])

    submit = SubmitField('Create Employee')

    def validate_email(self, email):
        staff = Staff.query.filter_by(email=email.data).first()
        if staff:
            raise ValidationError('An employee with that email already exists')