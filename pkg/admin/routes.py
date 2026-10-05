from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pkg.models import db, Admin

admin = Blueprint('admin', __name__, template_folder= 'admin/templates', static_folder= 'admin/static')

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