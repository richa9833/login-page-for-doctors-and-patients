from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # role: 'P' (Patient) or 'D' (Doctor)
    role = db.Column(db.String(1), nullable=False)

    # profile image filename (stored under static/uploads)
    profile_image = db.Column(db.String(255))

    # address fields
    address_line1 = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    pincode = db.Column(db.String(12), nullable=False)

    def is_patient(self):
        return self.role == "P"

    def is_doctor(self):
        return self.role == "D"
