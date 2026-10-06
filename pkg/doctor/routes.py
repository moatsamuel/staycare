from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from pkg.models import db, Doctor, Specialty, Appointment 
from werkzeug.security import generate_password_hash, check_password_hash

doc = Blueprint('doc', __name__, template_folder='templates', static_folder='static')

@doc.route('/register-doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        licence = request.form.get('licence_number')
        phone_number = request.form.get('phone_number')
        specialty_id = request.form.get('specialty_id')
        if Doctor.query.filter_by(email=email).first():
            return render_template('doctor/register_doctor.html', error="Email already registered.")
            
        new_doctor = Doctor(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=generate_password_hash(password),
            licence_number=licence,
            phone=phone_number,
            specialty_id=specialty_id
        )
        
        db.session.add(new_doctor)
        db.session.commit()
        
        return redirect(url_for('doc.doctor_dashboard')) 
    specialties = Specialty.query.all()
    return render_template('doctor/register_doctor.html', specialties=specialties)


@doc.route('/login', methods=['GET', 'POST'])
def login():
    if 'doctor_id' in session:
        return redirect(url_for('doc.doctor_dashboard'))

    if request.method == 'POST':
        email = request.form.get('doc_email')
        password = request.form.get('doc_password')
        doctor = Doctor.query.filter_by(email=email).first()
        if doctor and check_password_hash(doctor.password_hash, password):
            session['doctor_id'] = doctor.id
            session['doctor_name'] = f"{doctor.first_name} {doctor.last_name}"
            
            return redirect(url_for('doc.doctor_dashboard'))
        else:
            return render_template('doctor/login.html', error="Invalid Email or Password.")

    
    return render_template('doctor/login.html')


@doc.route('/dashboard', methods=['GET','POST'])
def doctor_dashboard():
    if 'doctor_id' not in session:
        return redirect(url_for('doc.login'))
    
    current_doctor_id = session.get('doctor_id')
    
    current_doctor = Doctor.query.get_or_404(current_doctor_id)
    appointments = Appointment.query.filter_by(doctor_id=current_doctor_id).all()
    
    return render_template(
        'doctor/doc_dashboard.html', 
        doctor=current_doctor,
        appointments=appointments
    )
@doc.route('/logout', methods=["GET", "POST"])
def logout():
    
    session.pop('doctor_id', None)
    session.pop('doctor_name', None)
    
    return redirect(url_for('doc.login'))

