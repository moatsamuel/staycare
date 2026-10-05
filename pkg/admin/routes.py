from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify,make_response,flash
from werkzeug.security import generate_password_hash,check_password_hash
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pkg.models import db, Admin, Doctor, Specialty, Patients, Appointment

admin = Blueprint('admin', __name__, template_folder= 'templates', static_folder= 'static')

@admin.route('/create/admin/')
def add_admin():
    name = input('Enter  username:')
    email = input("Enter email: ")
    password = input('Enter password: ')

    pwd_hash = generate_password_hash(password)

    admin = Admin(username=name, admin_email=email, password_hash=pwd_hash)
    db.session.add(admin)
    db.session.commit()
    return 'hhhh'

@admin.route("/dashboard")
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))
    all_doctors = Doctor.query.order_by(Doctor.last_name.asc()).all()
    all_specialties = Specialty.query.all()
    response= make_response( render_template("admin/admin_dashboard.html", doctors=all_doctors, specialties=all_specialties))
    response.headers["Cache-Control"] = "no-store,no-cache, must-revalidate,"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@admin.route("/", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("admin_email")
        password = request.form.get("admin_password")

        admin = Admin.query.filter_by(admin_email=email).first()

        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin.admin_dashboard'))
        else:
            error_message = "Invalid email or password"
            return render_template("admin/login.html", error=error_message)

    return render_template("admin/login.html")



@admin.route("/logout", methods=["GET", "POST"])
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin.admin_login'))