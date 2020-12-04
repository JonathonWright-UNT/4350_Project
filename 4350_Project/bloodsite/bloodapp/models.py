from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bloodapp import db, loginManager, app
from flask_login import UserMixin

@loginManager.user_loader
def load_user(staff_id):
    return Staff.query.get(int(staff_id))

class Staff(db.Model, UserMixin):
    """This is the model for the Staff:
    Args:
       first_name (str): The first name of the staff
       last_name (str): the last name
       password (str): their password for their account
       email (str): Their email address
       role (str): Their job title
       location (str): The branch they work in """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(30))
    role = db.Column(db.String(25))
    location = db.Column(db.String(25), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        """Generates a token for an employee"""
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """Verifies a token for an employee
        Args:
            token(str): the token"""
        s = Serializer(app.config['SECRET_KEY'])
        try:
            staff_id = s.loads(token)['staff_id']
        except:
            return None
        return Staff.query.get(user_id)

    def __repr__(self):
        return f"Staff ('{self.first_name}', '{self.last_name}', '{self.role}')"


class Donor(db.Model):
    """This is the model for the Donor:
    Args:
       first_name (str): The first name of the donor
       last_name (str): the last name
       last_blood_donation_date (date): the last time they donated blood
       last_plasma_donation_date (date): the last time they donated plasma
       blood_type(str): Their blood type
       age (int): their age
       email (str): Their email address """
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    last_blood_donation_date = db.Column(db.DateTime)
    last_plasma_donation_date = db.Column(db.DateTime)
    email = db.Column(db.String(30))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Donor('{self.first_name}', '{self.last_name}', '{self.blood_type}')"


class Donation(db.Model):
    """This is the model for the Donor:
    Args:
       blood_type(str): Their blood type
       blood (bool): if the donation is blood
       plasma (bool): if the donation is plasma
       date (date): The date
       location (str): The branch the donation is in """
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    blood = db.Column(db.Boolean, nullable=False)
    plasma = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"Post('{self.blood_type},')"

class Bank(db.Model):
    """This is the model for Bank
    Args:
        location (str): The location of the bank
        manager_id (int) (FK): This is the id of the manager of the bank"""
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(25), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    def __repr__(self):
        return f"Bank('{self.location},')"
