from datetime import datetime
from bloodapp import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def load_user(user_id):
    return Donor.query.get(int(user_id))

class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(25))
    location_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)


    def __repr__(self):
        return f"Staff ('{self.first_name}', '{self.last_name}', '{self.role}')"


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    last_blood_donation_date = db.Column(db.DateTime)
    last_plasma_donation_date = db.Column(db.DateTime)
    email = db.Column(db.String(30))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    eligible_for_blood_donation = db.Column(db.DateTime)
    eligible_for_plasma_donation = db.Column(db.DateTime)
    
    def __repr__(self):
        return f"Donor('{self.first_name}', '{self.last_name}', '{self.blood_type}')"


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    blood = db.Column(db.Boolean, nullable=False)
    plasma = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.blood_type},')"

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(25), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    def __repr__(self):
        return f"Bank('{self.location},')"
