from flask import render_template,request, redirect, flash, url_for
from pkg import app
from pkg.models import db, Doctor, Admin, Patients, Specialty, Appointment

@app.route("/",methods=["GET","POST"])
def register_page():
    if request.method == "POST":
        flash("you have registered successfully click on the login button below","success")
        redirect ("/")
    return render_template("register_page.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/patient")
def patient():
    return render_template("patient_dashboard.html")


@app.route("/specialties")
def specialties():
    return render_template("specialties.html") 

@app.route("/doctor/add/")
def doctor():
    fname = input('Enter first name: ')
    lname = input('Enter last name: ')
    email = input('Enter email name: ')
    ph = input('Enter phone: ')
    lnum = input('Enter license: ')
    ava = input('Enter avail: ')
    cf = input('Enter consult: ')
    sid = input('Enter sesh id: ')
    doc = Doctor(first_name = fname, last_name = lname, email = email ,phone = ph, licence_number = lnum , availability = ava, consultation_fee = cf,specialty_id = sid)
    db.session.add(doc)
    db.session.commit()
    # return render_template("doctor.html", doctors_db_list=doctors_db_list)
    return 'added doctors' 


@app.route('/doctors/')
def doc():
    doctors_database_list = Doctor.query.all()

    return  render_template("doctor.html", doctor=doctors_database_list)

@app.route('/specialty/add/')
def add_specialty():
    specialty = input('Enter specialty: ')
    desc = input('Enter description: ')
    special = Specialty(name = specialty, description = desc)
    db.session.add(special)
    db.session.commit()
    return 'added speciality'

@app.route("/admin/dashboard")
def admin_dashboard():
    all_doctors = Doctor.query.order_by(Doctor.last_name.asc()).all()
    all_specialties = Specialty.query.all()
    return render_template("admin_dashboard.html", doctors=all_doctors, specialties=all_specialties)

@app.route("/admin/doctor/add", methods=["POST"])
def admin_add_doctor():
    try:
        new_doc = Doctor(
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            email=request.form.get("email"),
            licence_number=request.form.get("licence_number"),
            consultation_fee=request.form.get("consultation_fee") if request.form.get("consultation_fee") else 0.00,
            specialty_id=int(request.form.get("specialty_id")),
            availability="Available"
        )
        db.session.add(new_doc)
        db.session.commit()
        flash("Doctor created successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Invalid information submitted.", "danger")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/doctor/edit/<int:doctor_id>", methods=["GET", "POST"])
def admin_edit_doctor(doctor_id):
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
            return redirect(url_for("admin_dashboard"))
        except Exception:
            db.session.rollback()
            flash("Invalid information submitted.", "danger")
            return redirect(url_for("admin_dashboard"))
            
    all_specialties = Specialty.query.all()
    
    return render_template("edit_doctor.html", doc=target_doctor, specialties=all_specialties)

@app.route("/admin/doctor/delete/<int:doctor_id>", methods=["POST"])
def admin_delete_doctor(doctor_id):
    target_doctor = Doctor.query.get(doctor_id)
    if not target_doctor:
        flash("Doctor not found.", "danger")
        return redirect(url_for("admin_dashboard"))
        
    try:
        db.session.delete(target_doctor)
        db.session.commit()
        flash("Doctor deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Could not complete delete operation due to database constraints.", "danger")
        
    return redirect(url_for("admin_dashboard"))
