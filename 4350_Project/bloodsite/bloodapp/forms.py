from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, Optional
from bloodapp.models import Donor, Staff, Bank


class EmployeeForm(FlaskForm):

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
    bloods = ['O−',	'O+', 'A−', 'A+', 'B−', 'B+', 'AB−', 'AB+']

    blood_type = SelectField('blood_type', choices=bloods, validators=[InputRequired()])
    
    first_name = StringField('First Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    age = IntegerField('Age', validators=[InputRequired()])
    
    email = StringField('Email', validators=[InputRequired()])

    submit = SubmitField('Create Donor')

    def validate_email(self, email):
        donor = Donor.query.filter_by(email=email.data).first()
        if donor:
            raise ValidationError('A donor with that email already exists')



class UpdateDonorForm(FlaskForm):
    bloods = ['O−',	'O+', 'A−', 'A+', 'B−', 'B+', 'AB−', 'AB+']

    blood_type = SelectField('blood_type', choices=bloods, validators=[InputRequired()])
    
    first_name = StringField('First Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[InputRequired(), Length(min=2, max=20)])

    age = IntegerField('Age', validators=[InputRequired()])
    
    email = StringField('Email', validators=[InputRequired()])

    submit = SubmitField(f'Update Donor')

    def validate_email(self, email):
        donor = Donor.query.filter_by(email=email.data).first()
        if donor.email == self.email.data:
            return
        if donor.first_name == self.first_name.data and donor.last_name == self.last_name.data:
            return
        elif donor:
            raise ValidationError('A donor with that email already exists')



class DonorForm(FlaskForm):
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
    donate_blood = SubmitField()
    donate_plasma = SubmitField()
    update_donor = SubmitField()
    

class WithdrawForm(FlaskForm):
    bloods = ['O-',	'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']
    options = ['Blood', 'Plasma']
    blood_type = SelectField('blood_type', choices=bloods, validators=[DataRequired()])
    blood_or_plasma = SelectField('blood_or_plasma', choices=options, validators=[DataRequired()])
    units = StringField('units', validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def validate_units(self, units):
        try:
            if int(units.data):
                pass
        except Exception as e:
            if units.data.lower() != "all":
                raise ValidationError('Please enter the number of units you wish to have, or simply type "All"')
        

class CreateEmployeeForm(FlaskForm):
    
    banks = Bank.query.all()
    bank_names = [item.location for item in banks]

    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    password = StringField('Password',
                           validators=[DataRequired(), Length(min=5, max=20)])
    
    email = StringField('Email', validators=[DataRequired()])

    role = StringField('Role',
                           validators=[Length(min=2, max=25)])

    location = SelectField('location', choices=bank_names, validators=[DataRequired()])

    submit = SubmitField('Create Employee')

    def validate_email(self, email):
        staff = Staff.query.filter_by(email=email.data).first()
        if staff:
            raise ValidationError('An employee with that email already exists')

class UpdateEmployeeForm(FlaskForm):
    
    banks = Bank.query.all()
    bank_names = [item.location for item in banks]

    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    password = StringField('Password')
    
    email = StringField('Email', validators=[DataRequired()])

    role = StringField('Role',
                           validators=[Length(min=2, max=25)])

    location = SelectField('location', choices=bank_names, validators=[DataRequired()])

    submit = SubmitField('Update Employee')

    def validate_email(self, email):
        staff = Staff.query.filter_by(email=email.data).first()
        if staff.email == self.email.data:
            return
        if staff.first_name == self.first_name.data and staff.last_name == self.last_name.data:
            return
        elif staff:
            raise ValidationError('A donor with that email already exists')

