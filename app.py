import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from models import db, User
from forms import SignupForm, LoginForm

# --- App setup ---
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# ensure folders exist
os.makedirs(os.path.dirname(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///","")), exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# init db + login
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    # Flask-Login passes a string id; convert to int for SQLAlchemy primary key.
    return db.session.get(User, int(user_id))

# --- Helpers ---
def allowed_image(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in app.config["ALLOWED_IMAGE_EXTENSIONS"]

# --- CLI: first-run init ---
@app.cli.command("init-db")
def init_db():
    """Create tables."""
    with app.app_context():
        db.create_all()
        print("Database initialized.")

# --- Routes ---
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("route_after_login"))

    form = SignupForm()
    if form.validate_on_submit():
        # check uniqueness
        if User.query.filter_by(username=form.username.data).first():
            flash("Username is already taken.", "danger")
            return render_template("signup.html", form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash("Email is already registered.", "danger")
            return render_template("signup.html", form=form)

        # handle profile image (optional)
        image_filename = None
        file = request.files.get("profile_image")
        if file and file.filename:
            if allowed_image(file.filename):
                safe_name = secure_filename(file.filename)
                name, ext = os.path.splitext(safe_name)
                # make unique filename
                unique = f"{name}_{int(datetime.utcnow().timestamp())}{ext}"
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique)
                file.save(save_path)
                image_filename = unique
            else:
                flash("Unsupported image type. Allowed: png, jpg, jpeg, gif", "warning")

        # hash password
        pw_hash = generate_password_hash(form.password.data)

        user = User(
            role=form.role.data,
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            password_hash=pw_hash,
            profile_image=image_filename,
            address_line1=form.address_line1.data.strip(),
            city=form.city.data.strip(),
            state=form.state.data.strip(),
            pincode=form.pincode.data.strip(),
        )
        db.session.add(user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("route_after_login"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("route_after_login"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def route_after_login():
    if current_user.role == "D":
        return redirect(url_for("doctor_dashboard"))
    return redirect(url_for("patient_dashboard"))

@app.route("/patient")
@login_required
def patient_dashboard():
    if not current_user.is_patient():
        flash("Patients only.", "warning")
        return redirect(url_for("route_after_login"))
    return render_template("dashboard_patient.html", user=current_user)

@app.route("/doctor")
@login_required
def doctor_dashboard():
    if not current_user.is_doctor():
        flash("Doctors only.", "warning")
        return redirect(url_for("route_after_login"))
    return render_template("dashboard_doctor.html", user=current_user)

# serve uploaded images (simple demo; in production, serve via web server)
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)

if __name__ == "__main__":
    # For local dev only
    with app.app_context():
        db.create_all()
    app.run(debug=True)
