#  Doctor-Patient Portal (Flask Project)

This is a simple **Flask-based web application** that provides a role-based login and dashboard system for **Doctors** and **Patients**.  
The project demonstrates **user authentication**, **role management**, and **dashboard redirection** using Flask.



##  Features

-  **User Authentication**
  - Register as a **Doctor** or **Patient**
  - Secure password hashing with **Werkzeug**
  - Role-based login system

-  **Doctor Dashboard**
  - View doctor profile details
  - Role badge: Doctor

-  **Patient Dashboard**
  - View patient profile details
  - Role badge: Patient

-  **Profile Image Upload**
  - Upload profile images (optional)
  - Display images on dashboards

-  **Session Management**
  - Login / Logout functionality
  - Flash messages for actions



##  Tech Stack

- **Python 3**
- **Flask**
- **Flask-SQLAlchemy**
- **Flask-WTF**
- **WTForms**
- **Flask-Migrate**
- **SQLite (default database)**

  ## Project Structure

doctor-patient-portal/
│── app.py                # Main Flask app
│── models.py             # Database models (User, db)
│── forms.py              # Flask-WTF forms
│── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── doctor_dashboard.html
│   └── patient_dashboard.html
│── static/               # CSS, JS, Images
│── migrations/           # Flask-Migrate files
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation



