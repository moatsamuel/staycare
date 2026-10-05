from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify,flash,make_response
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pkg.models import db, Patients

patient = Blueprint('patient', __name__, template_folder='templates', static_folder='static')


@patient.route("/register", methods=["GET", "POST"])
def pat_register():
    if request.method == "POST":
        first_name = request.form.get("patfname")
        last_name = request.form.get("patlname")
        email = request.form.get("patemail")
        password_hash = request.form.get("patpassword")
        confirm_password = request.form.get("patconfirmpassword")
        if not first_name or not last_name or not email or not password_hash:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("patient.pat_register"))
        if len(password_hash) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template("register_page.html")
        if password_hash and confirm_password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register_page.html")
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("Invalid email address.", "error")
            return render_template("register_page.html")
        existing_patient = Patients.query.filter_by(pat_email=email).first()
        if existing_patient:
            flash("Email already exists. Please use a different email.", "error")
            return render_template("register_page.html")
        try:
            password_hash = generate_password_hash(password_hash)
            new_patient = Patients(
                first_name=first_name,
                last_name=last_name,
                pat_email=email,
                password_hash=password_hash
            )
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for("patient.pat_login"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("An error occurred while creating the account. Please try again.", "error")
            return render_template("register_page.html")  

    return render_template("register_page.html")

@patient.route("/patient/login", methods=["GET", "POST"])
def pat_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            flash("Please fill in all required fields.", "error")
            return render_template("login.html")
        patient = Patients.query.filter_by(pat_email=email).first()
        if patient and check_password_hash(patient.password_hash, password):
            session['onlinepatient'] = patient.id
            return redirect(url_for("patient.patient_dashboard"))
        else:
            flash("Invalid email or password. Please try again.", "error")
            return render_template("login.html")
    return render_template("login.html")


@patient.route("/patient/dashboard/")
def patient_dashboard():
    if 'onlinepatient' not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for("patient.pat_login"))
    id = session['onlinepatient']
    patient = Patients.query.get(id)
    if patient is None:
        session.pop('onlinepatient', None)
        return redirect(url_for("patient.pat_login"))
    response= make_response(render_template("patient_dashboard.html", patient=patient))
    response.headers["Cache-Control"] = "no-store,no-cache, must-revalidate,"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@patient.route("/logout/",methods=["GET","POST"])
def logout():
    session.pop("onlinepatient",None)
    flash("you have being logout")
    return redirect(url_for("patient.pat_login"))

    
    