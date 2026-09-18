from flask import render_template,request, redirect, flash
from pkg import app

@app.route("/",methods=["GET","POST"])
def register_page():
    if request.method == "POST":
        flash("you have registered sucessfully click on the login button below","success")
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

@app.route("/doctor")
def doctor():
    doctor = [{"name": "Dr. Samuel", "specialty": "Cardiology", "availability": "Available"},{"name": "Dr. lolu", "specialty": "optician", "availability": "Available"},{"name": "Dr. kelvin", "specialty": "Cardiology", "availability": "Not Available"}]
    return render_template("doctor.html", doctor=doctor) 