# from flask import Flask, flash, redirect, render_template, request, session, url_for
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash
# from helpers import login_required
# import datetime
# from cs50 import  SQL

# app = Flask(__name__)


# db = SQL("sqlite:///hospital.db")


# @app.afterrequest
# def afterrequest(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response

import os
from datetime import date
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hospital.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def main_page():
    return render_template("main-page.html")

@app.route("/staff_main")
def staff_main():
    return render_template("staff-main.html")

# about us page
@app.route("/aboutus")
def about_us_page():
    return render_template("about-us-page.html")

# services page
@app.route("/blog")
def blog_page():
    return render_template("blog-page.html")


#login function
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not (username := request.form.get("username")):
            warning = 1
            return render_template(
                "login-page.html",
                warning=warning,
            )

        # Ensure password was submitted
        elif not (password := request.form.get("password")):
            warning = 2
            return render_template(
                "login-page.html",
                warning=warning,
            )

        # Query database for username
        rows = db.execute(
            "SELECT * FROM user WHERE username = ?;", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            warning = 3
            return render_template(
                "login-page.html",
                warning=warning,
            )

        # Remember which user has logged in

        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/staff_main")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login-page.html")



@app.route('/clinic', methods=['GET', 'POST'])
def clinic():
    clinics = db.execute("SELECT clinic_id,name FROM clinic ;") 
    if request.method == 'POST':
        input_clinic = request.form.get('input_clinic')
        # Ensure clinic chosen was submitted
        if not (input_clinic := request.form.get("input_clinic")):
            warning = 1
            return render_template("clinic.html",warning = warning,clinics = clinics)
        
        session['clinic_input'] = input_clinic
        return redirect(url_for('doctor'))
    return render_template('clinic.html',clinics = clinics)

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    clinic_chosen_id = session.get('clinic_input')
    doctors = db.execute("SELECT doctor_id,first_name,last_name FROM doctor WHERE clinic_id = ?;",clinic_chosen_id)
    if request.method == 'POST':
        input_doctor = request.form.get('input_doctor')
        # Ensure doctor chosen was submitted
        if not (input_doctor := request.form.get("input_doctor")):
            warning = 2
            return render_template("doctor.html",warning = warning,doctors = doctors)

        session['doctor_input'] = input_doctor
        return redirect(url_for('appointment_chose'))
    return render_template('doctor.html',doctors = doctors)

@app.route('/appointment_chose', methods=['GET', 'POST'])
def appointment_chose():
    clinic_chosen_id = session.get('clinic_input')
    doctor_chosen_id = session.get('doctor_input')
    appointments = db.execute("""SELECT appointment_id, appointment_date, appointment_time, status 
                              FROM appointment WHERE clinic_id = ? AND doctor_id = ? AND status = ? ;"""
                              , clinic_chosen_id,doctor_chosen_id,"Available")

    if request.method == 'POST':
        input_appointment = request.form.get('input_appointment')
        # Ensure appointment chosen was submitted
        if not (input_appointment := request.form.get("input_appointment")):
            warning = 6
            return render_template("appointment_chose.html",warning = warning,appointments = appointments)

        session['input_appointment'] = input_appointment
    
        return redirect(url_for('patient_data'))
    return render_template('appointment_chose.html',appointments = appointments)

@app.route('/patient_data', methods=['GET', 'POST'])
def patient_data():
    appointment_chosen = session.get('input_appointment')
    if request.method == 'POST':

        input_patient_name = request.form.get('input_patient_name')
        # Ensure patient name was submitted
        if not (input_patient_name := request.form.get("input_patient_name")):
            warning = 3
            return render_template("patient_data.html",warning = warning,)
        
        session['input_patient_name'] = input_patient_name
        
        input_patient_phone = request.form.get('input_patient_phone')
        # Ensure patient_phone was submitted
        if not (input_patient_phone := request.form.get("input_patient_phone")):
            warning = 4
            return render_template("patient_data.html",warning = warning,)
        
        session['input_patient_phone'] = input_patient_phone

        input_patient_email = request.form.get('input_patient_email')
        # Ensure patient email was submitted
        if not (input_patient_email := request.form.get("input_patient_email")):
            warning = 5
            return render_template("patient_data.html",warning = warning,)    
        session['input_patient_email'] = input_patient_email
        return redirect(url_for('output'))
    return render_template('patient_data.html')

    
# contacts page
@app.route("/contactus", methods=["GET", "POST"])
def contacts_page():
    
    # get contact name from contact form
    contact_name = request.form.get("contact_name")
    # get contact email from contact form
    contact_email = request.form.get("contact_email")
    # get contact phone from contact form
    contact_phone = request.form.get("contact_phone")
    # get contact subject from from contact form
    contact_subject = request.form.get("contact_subject")
    # get contact_message from contact form
    contact_message = request.form.get("contact_message")
    

    # Ensure contact name was submitted
    if not (contact_name := request.form.get("contact_name")):
        warning = 1
        return render_template("contact-us-page.html",warning = warning,)
    
    # Ensure contact email was submitted
    elif not (contact_email := request.form.get("contact_email")):
        warning = 2
        return render_template("contact-us-page.html",warning = warning,)

    # Ensure contact phone was submitted
    elif not (contact_phone := request.form.get("contact_phone")):
        warning = 3
        return render_template("contact-us-page.html",warning = warning,)

    # Ensure contact subject was submitted
    elif not (contact_subject := request.form.get("contact_subject")):
        warning = 4
        return render_template("contact-us-page.html",warning = warning,)
    
    # Ensure contact message was submitted
    elif not (contact_message := request.form.get("contact_message")):
        warning = 5
        return render_template("contact-us-page.html",warning = warning,)    

    # inserting data into contact table
    db.execute("""INSERT INTO contact_information(name, email, phone, subject, message)
                VALUES (?, ?, ?, ?, ?);""",
                contact_name ,contact_email,contact_phone,contact_subject,contact_message)

    # return to main template after successful contact registration
    return render_template("contact_success.html")    


@app.route("/patientregisteration", methods=["GET", "POST"])
@login_required
def patientregisteration():
    # get phone2 from form
    phone2 = request.form.get("phone2")
    # get patient middle name from form

    middlename = request.form.get("middlename")
    # get emergency contact address from form
    emergencycontactaddress = request.form.get("emergencycontactaddress")
    # get email from form
    email = request.form.get("email")

    title = request.form.get("title")
    firstname = request.form.get("firstname")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    nationality = request.form.get("country")
    gender = request.form.get("gender")
    phone1 = request.form.get("phone1")
    phone2 = request.form.get("phone2")
    emergencycontactname = request.form.get("emergencycontactname")
    emergencycontactrelation = request.form.get("emergencycontactrelation")
    emergencycontactphone = request.form.get("emergencycontactphone")


    # birthdate group
    # get birthdate from website
    birthdate = datetime.datetime.strptime(request.form.get("birthdate"), "%Y-%m-%d")
    # birthdate day
    birthdateday = birthdate.day
    # birthdate month
    birthdatemonth = birthdate.month
    # birthdate year
    birthdateyear = birthdate.year
    # calculate age ***
    # def age(birthdate):
    today = datetime.today()
    # calculating age
    age = (
        today.year
        - birthdateyear
        - ((today.month, today.day) < (birthdatemonth, birthdateday))
    )

    # inserting data into patient table
    db.execute(
        """INSERT INTO patient(firstname, middlename, lastname,
                                  birthdate, age, gender, userid,
                                  phone1, phone2,
                                  emergencycontactname, emergencyontactrelation,
                                  emergencyontactphone,
                                  emergencycontactadress, Email,Patientreservationstatus)
                                  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",
        firstname,
        middlename,
        lastname,
        birthdate,
        age,
        gender,
        session["userid"],
        phone1,
        phone2,
        emergencycontactname,
        emergencycontactrelation,
        emergencycontactphone,
        emergencycontactaddress,
        email,
        "wait for a room",
    )

    sucessed = 1
    # return to main tempalte after sucsessful patient regestration
    return render_template(
        "staff-main-page.html",
        sucessed=sucessed,
    )

# Employees report
@app.route("/printreport")
@login_required
def printreport():
    # get employee's data from database
    employee_info = db.execute("SELECT first_name,role,status FROM user WHERE id = ?;",session["user_id"])
    # if status is not "Working"
    if (employee_info[0]["status"] != "Working"):
        # return to tmplate role,status,name
        return render_template(
            "emplyoeereport.html",
            employee_info = employee_info,
        )

    actions_of_employees = db.execute(
        """SELECT user.first_name AS first_name,
                  user.middle_name As middle_name,
                  user.last_name AS last_name,
                  user.status As status,
                  user.role AS role,
                  Employee_Check_In_Record.user_id AS user_id, 
                  Employee_Check_In_Record.number_of_reservations AS number_of_reservations
                  FROM Employee_Check_In_Record JOIN user ON user.id = Employee_Check_In_Record.user_id 
                  WHERE user.role NOT IN ('Reporter', 'Reception manager');"""
    )
    
    return render_template(
        "emplyoeereport.html",
        actions_of_employees=actions_of_employees,
        employee_info = employee_info,
    )


# @app.route("/checkrooms", methods=["GET", "POST"])
# @login_required
# def checkrooms():
#     # select rooms data from database
#     roomsdata = db.execute("SELECT roomnumber,status,price FROM room;")
#     # return data got from database to check rooms template
#     return render_template(
#         "checkrooms.html",
#         roomsdata=roomsdata,
#     )


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any userid
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/checkin", methods=["GET", "POST"])
@login_required
def checkin():
    # patients data from database
    patient = db.execute(
        "SELECT id,first_name,middle_name,last_name FROM patient WHERE Patient_reservation_status = ?;",
        "wait for a room"
    )

    #  Select price of room choosen
    priceofroom = db.execute(
        "SELECT price FROM room WHERE roomnumber = ? and status = ?;",  "open"
    )
    daysofreservations = request.form.get("days")
    # multiply price with days
    totalprice = priceofroom[0]["price"] * daysofreservations
    # select patient id selected
    patientid = db.execute("SELECT id FROM patient WHERE id = ?;",
                            patient[0]["id"])
    room = request.form("room")
    checkindate = request.form("checkindate")
    checkoutdate = request.form("checkoutdate")


    # select id of room selected
    roomid = db.execute("SELECT id FROM rooms WHERE roomnumber = ? ;", room)
    # insert reservation information --error
    db.execute(
        """INSERT INTO reservation(roomid, userid,patientid, price,
                                           checkin, checkout, days,
                                           reservationstatus)
                                           VALUES (?,?,?,?,?,?,?,?);""",
        roomid,
        session,
        patient,
        totalprice,
        checkindate,
        checkoutdate,
        daysofreservations,
        "Done",

    )

    # Type of Medical Care: Specify the type of medical care needed (e.g., general consultation, specialist visit, surgery, emergency care).
    purpose = ["general consultation", "specialist visit", "surgery", "emergency care"]
    today_date = date.today()
    # payment values allowed
    payment_values = ["Cash", "Visa ,Mastercard"]
    # if status is not "Working"
    if (employee_info[0]["status"] != "Working"):
        # return to tmplate role,status,name
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )

    # if room no is null
    if not (room_no := request.form.get("room")):
        warning = 1
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            warning=warning,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )

    # if patient is null
    elif not (patient := request.form.get("patient")):
        warning = 2
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            warning=warning,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )
    # if room is null
    if not (room := request.form.get("room")):
        warning = 3
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            warning=warning,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )
    # if checkin_date is null
    elif not (checkin_date := request.form.get("checkin_date")):
        warning = 4
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            warning=warning,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )
    # if checkout_date is null
    elif not (checkout_date := request.form.get("checkout_date")):
        warning = 5
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            warning=warning,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )
    # if payment is null
    elif not (payment := request.form.get("payment")):
        warning = 6
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            warning=warning,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )
    # if purpose is null
    elif not (purpose_get := request.form.get("purpose_get")):
        warning = 6
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            warning=warning,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )
    # if room is not in rooms
    elif not (room not in rooms):
        warning = 7
        return render_template(
            "checkin.html",
            payment_values=payment_values,
            warning=warning,
            today_date=today_date,
            patients_data=patients_data,
            rooms_data=rooms_data,
            employee_info = employee_info,
            purpose = purpose
        )
    
    # dates of check in and check out
    # check in group
    # get check in from website
    checkin_date = datetime.datetime.strptime(
        request.form.get("checkin_date"), "%Y-%m-%d"
    )
    # checkin_date = datetime.datetime.strptime(request.form.get("checkin_date"),"%Y-%m-%d")

    # check in day
    checkin_day = checkin_date.day
    # check in month
    checkin_month = checkin_date.month
    # check in year
    checkin_year = checkin_date.year
    # check out group
    # get check out from website

    checkout_date = datetime.datetime.strptime(
        request.form.get("checkout_date"), "%Y-%m-%d"
    )
    # check out day
    checkout_day = checkout_date.day
    # check out month
    checkout_month = checkout_date.month
    # check out year
    checkout_year = checkout_date.year
    # calculate days of reservation
    # subtract checkin and check out dates
    delta = checkout_date - checkin_date
    # # days of reservation
    days_of_reservations = delta.days

    #
    #  Select price of room choosen
    price_of_room = db.execute(
        "SELECT price FROM room WHERE room_number = ? and status = ?;", room, "open"
    )
    # multiply price with days
    total_price = price_of_room[0]["price"] * days_of_reservations
    # select patient id selected
    # patient_id = db.execute("SELECT id FROM patient WHERE id = ?;",
    #                         patient[0]["id"])

    # select id of room selected
    room_id = db.execute("SELECT id FROM room WHERE room_number = ? ;", room)
    # insert reservation information --error
    db.execute(
        """INSERT INTO reservation(roomid, user_id,patient_id, price,
                                           checkin, checkout, days,
                                           reservation_status, payment,purpose)
                                           VALUES (?,?,?,?,?,?,?,?,?,?);""",
        room_id[0]["id"],
        session["user_id"],
        patient,
        total_price,
        checkin_date,
        checkout_date,
        days_of_reservations,
        "Done",
        payment,
        purpose_get
    )
    # update status of room to be "reserved"
    db.execute(
        """UPDATE room SET
                  status = ? WHERE id = ?;
    """,
        "reserved",
        patient,
    )
    # update status of room to be "reserved"
    db.execute(
        """UPDATE patient SET
                  Patient_reservation_status = ? WHERE id = ?;
    """,
        "checked in",
        patient,
    )

    # get number of reservations of user
    number_of_reservation_get = db.execute(
        "SELECT number_of_reservation FROM action_report WHERE user_id = ?;",
        session["user_id"],
    )
    # add one to number of reservations of user
    number_of_reservations_sent = (
        number_of_reservation_get[0]["number_of_reservations"] + 1
    )
    # update the number of reservations to the new one
    db.execute(
        """UPDATE action_report SET
                  number_of_reservations = ? WHERE user_id = ?;
    """,
        number_of_reservations_sent,
        session["user_id"],
    )

    # make condition to return if check in sucessed
    sucessed = 1
    # # return to main after sucessful check in
    # return render_template(
    #     "staff-main-page.html",
    #     sucessed=sucessed,
    #     employee_info = employee_info,
    # )

    # update status of room to be "reserved"
    db.execute(
        """UPDATE room SET
                  status = ? WHERE id = ?;
    """,
        "reserved",
        patient,
    )
    # update status of room to be "reserved"
    db.execute(
        """UPDATE patient SET
                  Patientreservationstatus = ? WHERE id = ?;
    """,
        "checked in",
        patient,
    )

    # get number of reservations of user
    numberofreservationget = db.execute(
        "SELECT numberofreservations FROM actionreport WHERE userid = ?;",
        session["userid"],
    )
    # add one to number of reservations of user
    numberofreservationssent = (
        numberofreservationget[0]["numberofreservations"] + 1
    )
    # update the number of reservations to the new one
    db.execute(
        """UPDATE Employee_Check_In_Record SET
                  numberofreservations = ? WHERE userid = ?;
    """,
        numberofreservationssent,
        session["userid"],
    )

    # make condition to return if check in sucessed
    sucessed = 1
    # return to main after sucessful check in
    return render_template(
        "staff-main-page.html",
        sucessed=sucessed,
    )



@app.route("/addnewuser", methods=["GET", "POST"])
@login_required
def addnewuser():

    fname = request.form.get("middlename")
    lname = request.form.get("middlename")
    password = request.form.get("password")
    username = request.form.get("username")
    rolein = request.form.get("rolein")

    # Inserting new added user's data into users table in database
    db.execute(""" INSERT INTO user(firstname, middlename, username, hash, role,status)
                                VALUES (?,?,?,?,?,?);""",
                                fname,lname,
                                username,generate_password_hash(password),
                                rolein,"Working")
    # Adding user to users report 
    # Selecting id of new user
    newuserid = db.execute(""" SELECT id FROM user WHERE firstname = ? AND lastname = ? 
                                            AND username = ?
                                            AND role = ? AND status = ?;""",
                                            fname,lname,username,
                                            rolein,"Working")
    userid = newuserid[0]["id"]
    # Inserting new added user's data into action report table in database 
    db.execute(""" INSERT INTO Employee_Check_In_Record(action ,userid, numberofreservations, Actionsnotesofemployee)
                               VALUES (?,?,?,?);""","none",userid,0,"none")
    sucessed = 1
    # return to main page after a sucessful adding user
    return render_template("staff-main-page.html",sucessed = sucessed)

@app.route("/changinguserstatus", methods=["GET", "POST"])
@login_required
def changinguserstatus():

    # for Admin
    usersdataforadmin = db.execute("SELECT * FROM user WHERE role != ? AND role != ? AND role != ?;","Admin","Reception manager","Reporter")

    # for Admin
    usersdataforadmincount = db.execute("SELECT COUNT(id) FROM user WHERE role != ?;","Admin")
    
    # Update status according to the status selected
    db.execute(""" UPDATE user SET status = ? WHERE id= ?;""",usersdataforadmin,usersdataforadmincount)
    sucessed = 1
    # Return to main page after a sucessfully changing users status
    return render_template("staff-main-page.html",sucessed = sucessed)
    # return render_template("staff-main-page.html",sucessed = sucessed)

@app.route("/reservationshistory", methods=["GET", "POST"])
@login_required
def reservationshistory():
    reservationdata = db.execute("""SELECT reservation.exitdate AS exitdate,
                                  reservation.registrationtime AS registrationtime,
                                  reservation.payment AS payment,
                                  reservation.reservationstatus AS reservationstatus,
                                  reservation.checkin AS checkin,
                                  reservation.checkout AS checkout,
                                  reservation.price AS price,
                                  room.roomnumber AS roomnumber,
                                  patient.firstname AS pateintfirstname ,
                                  patient.middlename AS pateintmiddlename ,
                                  patient.lastname AS pateintlastname ,
                                  user.firstname AS userfirstname , 
                                  user.role AS userrole
                                  FROM reservation 
                                  JOIN patient ON patient.id = reservation.patientid
                                  JOIN room ON room.id = reservation.roomid
                                  JOIN user ON user.id = reservation.userid
                                ;""")

    return render_template("reservationshistory.html",reservationdata= reservationdata)


@app.route("/clinicreservationshistory", methods=["GET", "POST"])
@login_required
def clinicreservationshistory():
    # 
    
    # clinic data for Womens Health and Obstetrics
    clinicreservationdata = db.execute("""SELECT 
                                  bookedappointment.appointmentid as appointmentid,          
                                  clinic.name AS clinicname,
                                  doctor.firstname AS doctorfirstname,
                                  doctor.lastname AS doctorlastname,
                                  doctor.consultationfee AS appointmentfees,
                                  appointment.appointmentdate AS appointmentdate ,
                                  appointment.appointmenttime AS appointmenttime,
                                  bookedappointment.status AS status,
                                  bookedappointment.patientname AS patientname,
                                  bookedappointment.patientphone AS patientphone ,
                                  bookedappointment.patientemail AS patientemail 
                                  FROM clinic 
                                  JOIN bookedappointment ON appointment.appointmentid = bookedappointment.appointmentfromtableid
                                  JOIN appointment ON clinic.clinicid = bookedappointment.clinicid
                                  JOIN doctor ON doctor.doctorid = bookedappointment.doctorid
                                  GROUP BY clinic.name
                                ;""",)

    return render_template("clinicreservationhistory.html",clinicreservationdata= clinicreservationdata)

@app.route("/show_contact_messages", methods=["GET", "POST"])
@login_required
def show_contact_messages():
    employee_info = db.execute("SELECT first_name,role,status FROM user WHERE id = ?;",session["user_id"])

    contact_messages = db.execute(""" SELECT * FROM contact_information;""")
    return render_template("show_contact_messages.html",contact_messages = contact_messages,employee_info = employee_info)