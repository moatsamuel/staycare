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

@admin.route("/doctor/edit/<int:doctor_id>", methods=["GET", "POST"])
def admin_edit_doctor(doctor_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))
    target_doctor = Doctor.query.get_or_404(doctor_id)
    
    if request.method == "POST":
        target_doctor.first_name = request.form.get("first_name")
        target_doctor.last_name = request.form.get("last_name")
        target_doctor.email = request.form.get("email")
        target_doctor.licence_number = request.form.get("licence_number")
        target_doctor.consultation_fee = request.form.get("consultation_fee")
        target_doctor.availability = request.form.get("availability")
        target_doctor.specialty_id = int(request.form.get("specialty_id"))
        
        try:
            db.session.commit()
            flash("Doctor updated successfully.", "success")
            return redirect(url_for("admin/admin_dashboard"))
        except Exception:
            db.session.rollback()
            flash("Invalid information submitted.", "danger")
            return redirect(url_for("admin/admin_dashboard"))
            
    all_specialties = Specialty.query.all()
    
    response= make_response( render_template("admin/edit_doctor.html", doc=target_doctor, specialties=all_specialties))
    response.headers["Cache-Control"] = "no-store,no-cache, must-revalidate,"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@admin.route("/doctor/delete/<int:doctor_id>", methods=["POST"])
def admin_delete_doctor(doctor_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))
    target_doctor = Doctor.query.get(doctor_id)
    if not target_doctor:
        flash("Doctor not found.", "danger")
        return redirect(url_for("admin/admin_dashboard"))
        
    try:
        db.session.delete(target_doctor)
        db.session.commit()
        flash("Doctor deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Could not complete delete operation due to database constraints.", "danger")
        
    response= make_response( redirect(url_for("admin/admin_dashboard")))
    response.headers["Cache-Control"] = "no-store,no-cache, must-revalidate,"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
