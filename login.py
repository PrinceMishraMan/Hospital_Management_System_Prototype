from flask import Flask, render_template, request, redirect,flash,url_for,session,send_file
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from PIL import Image, ImageDraw, ImageFont
# from sqlalchemy import create_engine, func
# from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import string
import pytz
# import os




app = Flask(__name__)
app.config['SQLALCHEMY_BINDS'] = {
    'staff_db': 'sqlite:///staff_record.db',
    'patient_db': 'sqlite:///patient_record.db',
    'medicine_db': 'sqlite:///medicine_data.db',
    'bill_db': 'sqlite:///bill_record.db',
    'donor_db': 'sqlite:///blood_record.db',
    'certificate_db':'sqlite:///certificate_record.db',
    'doctor_db':'sqlite:///doctor_record.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
# template_path = os.path.join(app.root_path, 'static', 'Blood-donation-camp-certificate-in-psd-format.jpg')
# output_path = os.path.join(app.root_path, 'static', 'generated_certificate.png')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.','warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

class Staff(db.Model):
    __bind_key__ = 'staff_db'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, name, email, password, number):
        self.username = username
        self.name = name
        self.email = email
        self.number = number
        self.password = password

class Patient(db.Model):
    __bind_key__ = 'patient_db'
    sno = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(8), unique=True, nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    ward = db.Column(db.String(100), nullable=False)
    time_of_admission = db.Column(db.DateTime, default=datetime.utcnow)
    initial_deposit = db.Column(db.Float, default=0.0)
    treatment = db.Column(db.String(500), nullable=False)
    disease_diagnosed = db.Column(db.String(200), nullable=False)

    def __init__(self, patient_name, doctor_name, ward, initial_deposit, treatment, disease_diagnosed):
        self.patient_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.ward = ward
        self.initial_deposit = initial_deposit
        self.treatment = treatment
        self.disease_diagnosed = disease_diagnosed

# result = Patient.query.count()
def rooms_data():
    rooms = {
        'OT': {'vacants': 100 - Patient.query.count(), 'icon': 'fa-lightbulb'},
        'ICU': {'vacants': 100 - Patient.query.count(), 'icon': 'fa-heartbeat'},
        'General Ward': {'vacants': 100 - Patient.query.count(), 'icon': 'fa-bed'},
        'Emergency Ward': {'vacants': 100 - Patient.query.count(), 'icon': 'fa-plus-square'},
        'Pathology': {'vacants': 100 - Patient.query.count(), 'icon': 'fa-thermometer-three-quarters'},
        'Outdoor': {'vacants': 100 - Patient.query.count(), 'icon': 'fa-sign-out'}
    }
    return rooms

class Medicine(db.Model):
    __bind_key__ = 'medicine_db'
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String(100), nullable=False)
    batch_no = db.Column(db.String(100), nullable=False)
    manufacture_date = db.Column(db.String(20), nullable=False)
    expire_date = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    expire_check = db.Column(db.String(10), nullable=False)

class Bill(db.Model):
    __bind_key__ = 'bill_db'
    __tablename__ = 'bill record'
    id = db.Column(db.Integer, primary_key=True)
    doctor = db.Column(db.String(200), nullable=False)
    treat = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Donor(db.Model) :
    __bind_key__ = 'donor_db'
    sno = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    blood_group = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    __bind_key__ = 'doctor_db'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(200), nullable=False)
    consultation_fee = db.Column(db.Integer, nullable=False)
    icu_fee = db.Column(db.Integer, nullable=False)
    ward_fee = db.Column(db.Integer, nullable=False)

    # def __repr__(self) -> str:
    #     return (f"Doctor: {self.name}, Specialization: {self.specialization}, "
    #             f"Consultation Fee: {self.consultation_fee}, ICU Fee: {self.icu_fee}, "
    #             f"Ward Fee: {self.ward_fee}")

class BirthCertificate(db.Model):
    __bind_key__ = 'certificate_db'
    sno = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(10), nullable=False)
    certificate_id = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.String(200), nullable=False)
    place_of_birth = db.Column(db.String(200), nullable=False)
    mother_names = db.Column(db.String(400), nullable=False)
    father_names = db.Column(db.String(400), nullable=False)
    address = db.Column(db.String(400), nullable=True)
    weight = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(10), nullable=False)

class DeathCertificate(db.Model):
    __bind_key__ = 'certificate_db'
    sno = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(10), nullable=False)
    certificate_id = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    date_of_death = db.Column(db.String(200), nullable=False)
    time_of_death = db.Column(db.String(200), nullable=True)
    place_of_death = db.Column(db.String(200), nullable=False)
    cause_of_death = db.Column(db.String(400), nullable=False)
    age = db.Column(db.Integer, nullable=True)

def expiry_check(expire_date):
    expire_date_obj = datetime.strptime(expire_date, "%Y-%m-%d")
    current_date = datetime.now()
    return "❌" if current_date > expire_date_obj else "✔️"

def update_rooms_data():
    patient_count = Patient.query.count()
    return {
        'OT': {'vacants': 100 - patient_count, 'icon': 'fa-lightbulb'},
        'ICU': {'vacants': 100 - patient_count, 'icon': 'fa-heartbeat'},
        'General Ward': {'vacants': 100 - patient_count, 'icon': 'fa-bed'},
        'Emergency Ward': {'vacants': 100 - patient_count, 'icon': 'fa-plus-square'},
        'Pathology': {'vacants': 100 - patient_count, 'icon': 'fa-thermometer-three-quarters'},
        'Outdoor': {'vacants': 100 - patient_count, 'icon': 'fa-sign-out'}
    }

@app.route('/')
@login_required
def home():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        staff_record = Staff.query.filter_by(username=username, password=password).first()

        if staff_record:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!')
            redirect(url_for('login'))

    return render_template('login2.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        print("Username:", username)
        print("Name:", name)
        print("Email:", email)
        print("Number:", number)
        print("Password:", password)
        print("Confirm Password:", confirm_password)

        if confirm_password == password:
            existing_user = Staff.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists!')
            else:
                staff_record = Staff(username=username, name=name, email=email, number=number, password=password)
                db.session.add(staff_record)
                db.session.commit()
                session['username'] = username
                return redirect(url_for('home'))
        else:
            flash('Passwords do not match!')
            redirect(url_for('signup'))

    return render_template('signup2.html')

# @app.route('/signout')
# def signout():
#     session.pop('username', None)
#     return redirect(url_for('signup'))

@app.route('/front')
@login_required
def bed_tracking():
    rooms = rooms_data()
    return render_template('front3.html', rooms_data=rooms)

@app.route('/room/<ward_name>')
def room_detail(ward_name):
    return redirect(url_for('admission', ward=ward_name))

@app.route('/index', methods=['GET', 'POST'])
@login_required
def admission():
    selected_ward = request.args.get('ward', '')
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        ward = request.form['ward']
        initial_deposit = float(request.form['initial_deposit']) if request.form['initial_deposit'] else 0.0
        treatment = request.form['treatment']
        disease_diagnosed = request.form['disease_diagnosed']
        patient_record = Patient(
            patient_name=patient_name,
            doctor_name=doctor_name,
            ward=ward,
            initial_deposit=initial_deposit,
            treatment=treatment,
            disease_diagnosed=disease_diagnosed
        )
        db.session.add(patient_record)
        db.session.commit()

    all_patients = Patient.query.all()
    all_doctors = Doctor.query.all()
    wards = ["ICU", "General", "OT"]
    ist = pytz.timezone('Asia/Kolkata')
    for patient_record in all_patients:
        patient_record.time_of_admission = patient_record.time_of_admission.replace(tzinfo=pytz.utc).astimezone(ist)

    return render_template('index.html', all_patients=all_patients, doctors=all_doctors, wards=wards, selected_ward=selected_ward)


@app.route('/patient')
@login_required
def patient():
    all_patients = Patient.query.all()
    ist = pytz.timezone('Asia/Kolkata')
    for patient_record in all_patients:
        patient_record.time_of_admission = patient_record.time_of_admission.replace(tzinfo=pytz.utc).astimezone(ist)
    return render_template('patient.html',all_patients=all_patients)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    patient_record = Patient.query.get_or_404(sno)
    all_doctors = Doctor.query.all()
    wards = ["ICU", "General", "OT"]

    if request.method == 'POST':
        patient_record.patient_name = request.form['patient_name']
        patient_record.doctor_name = request.form['doctor_name']
        patient_record.ward = request.form['ward']
        # patient_record.initial_deposit = float(request.form['initial_deposit']) if request.form['initial_deposit'] else 0.0
        patient_record.treatment = request.form['treatment']
        patient_record.disease_diagnosed = request.form['disease_diagnosed']
        db.session.commit()
        return redirect(url_for("home"))

    return render_template('update.html', patient_record=patient_record, doctors=all_doctors, wards=wards)



@app.route('/delete/<int:sno>')
def delete(sno):
    patient_record = Patient.query.filter_by(sno=sno).first()
    db.session.delete(patient_record)
    db.session.commit()
    return redirect("/index")

@app.route('/medicine_home')
@login_required
def medicine_home():
    session.pop('_flashes', None)
    expired_meds = Medicine.query.filter_by(expire_check="❌").all()
    for med in expired_meds:
        flash(f"Medicine '{med.drug_name}' with Batch No '{med.batch_no}' has expired!", 'warning')
    all_medicine = Medicine.query.all()
    return render_template('medicine.html', medicine=all_medicine)

@app.route('/medicine', methods=['GET', 'POST'])
# @login_required
def medicine():
    if request.method == 'POST':
        drug_name = request.form['drug_name']
        batch_no = request.form['batch_no']
        manufacture_date = request.form['manufacture_date']
        expire_date = request.form['expire_date']
        stock = int(request.form['stock'])

        expire_check_result = expiry_check(expire_date)

        new_medicine = Medicine(
            drug_name=drug_name,
            batch_no=batch_no,
            manufacture_date=manufacture_date,
            expire_date=expire_date,
            stock=stock,
            expire_check=expire_check_result
        )

        db.session.add(new_medicine)
        db.session.commit()

        return redirect(url_for('medicine_home'))

    return render_template('medicine.html')

@app.route('/bill', methods=['GET', 'POST'])
@login_required
def bill():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        patient_record = Patient.query.filter_by(patient_id=patient_id).first()

        if patient_record:
            treatment = patient_record.treat
            doctor = patient_record.doctor
            bill_record = Bill.query.filter_by(doctor=doctor, treat=treatment).first()

            if bill_record:
                return render_template('billing.html', patient=patient_record, bill=bill_record)
            else:
                flash('No billing record found for this treatment and doctor.')
                return redirect(url_for('bill'))
        else:
            flash('Patient not found.')
            return redirect(url_for('bill'))

    return render_template('billing.html')

@app.route('/doctors_record', methods=['GET', 'POST'])
@login_required
def doctors_record():
    all_doctors = Doctor.query.all()
    return render_template('doctors_record.html', all_doctors=all_doctors)
@app.route('/blood_bank_front')
@login_required
def blood_bank():
    return render_template('blood_bank_front.html')

@app.route('/blood_record', methods=['GET', 'POST'])
@login_required
def blood_record():
    all_donors = Donor.query.all()
    return render_template('blood_record.html', all_donors=all_donors)

@app.route('/blood_bank', methods=['GET', 'POST'])
@login_required
def generate_certificate():
    if request.method == 'POST':
        name = request.form['name']
        donor_id = ''.join(random.choices(string.digits, k=8))
        address = request.form['address']
        blood_group = request.form['blood_group']
        donor_record = Donor(name=name, donor_id=donor_id, address=address, blood_group=blood_group)
        db.session.add(donor_record)
        db.session.commit()
        date = datetime.now().strftime("%d/%m/%Y")
        template_path = '/home/PrinceMishra/mysite/static/images/blood_donation.jpg'
        output_path = '/home/PrinceMishra/mysite/static/images/generated_certificate.png'
        image = Image.open(template_path)
        draw = ImageDraw.Draw(image)
        font_path = '/home/PrinceMishra/mysite/static/fonts/Arial.ttf'
        name_font = ImageFont.truetype(font_path, 100)
        other_font = ImageFont.truetype(font_path, 80)
        serial_no_position = (300, 955)
        name_position = (1390, 1050)
        address_position = (310, 1190)
        date_position = (140, 1455)
        blood_group_position = (1395, 1760)
        draw.text(serial_no_position, donor_id, font=other_font, fill="black")
        draw.text(name_position, name, font=name_font, fill="black")
        draw.text(address_position, address, font=other_font, fill="black")
        draw.text(date_position, date, font=other_font, fill="black")
        draw.text(blood_group_position, blood_group, font=other_font, fill="black")
        image.save(output_path)
        # print(f"Certificate generated for {name}, Serial No: {donor_id}, Date: {date}")
        return send_file(output_path, as_attachment=True, attachment_filename='certificate')

    return render_template('blood_bank.html')

@app.route('/certification_front')
@login_required
def certificate():
    return render_template('certification_front.html')

@app.route('/birth_front')
@login_required
def birth():
    return render_template('birth_front.html')

@app.route('/death_front')
@login_required
def death():
    return render_template('death_front.html')

@app.route('/birth_record', methods=['GET', 'POST'])
@login_required
def birth_record():
    all_births = BirthCertificate.query.all()
    return render_template('birth_record.html', all_births=all_births)

@app.route('/generate_birth_certificate', methods=['GET', 'POST'])
def generate_birth_certificate():
    if request.method == 'POST':
        name = request.form['child_name']
        date_of_birth = request.form['dob']
        place_of_birth = request.form['birth_place']
        mother_names = request.form['mother_name']
        father_names = request.form['father_name']
        address = request.form['address']
        weight = request.form['weight']
        sex = request.form['sex']
        certificate_id = ''.join(random.choices(string.digits, k=8))

        birth_record = BirthCertificate(record_type='birth', name=name, certificate_id=certificate_id,
                                        date_of_birth=date_of_birth,
                                        place_of_birth=place_of_birth,
                                        mother_names=mother_names,
                                        father_names=father_names,
                                        address=address,
                                        weight=weight,
                                        sex=sex)
        db.session.add(birth_record)
        db.session.commit()
        temp_path_2 = '/home/PrinceMishra/mysite/static/images/Birth Certificate Template.jpg'
        output_2 = '/home/PrinceMishra/mysite/static/images/generated_birth_certificate.png'
        image = Image.open(temp_path_2)
        draw = ImageDraw.Draw(image)
        font_path = '/home/PrinceMishra/mysite/static/fonts/Arial.ttf'
        font = ImageFont.truetype(font_path, 40)
        draw.text((100, 200), certificate_id, font=font, fill="black")
        draw.text((450, 800), name, font=font, fill="black")
        draw.text((650, 1000), date_of_birth, font=font, fill="black")
        draw.text((1050, 2070), place_of_birth, font=font, fill="black")
        draw.text((750, 1250), mother_names, font=font, fill="black")
        draw.text((750, 1375), father_names, font=font, fill="black")
        draw.text((820, 1570), address, font=font, fill="black")
        draw.text((750, 1870), weight, font=font, fill="black")
        draw.text((1900, 1870), sex, font=font, fill="black")
        image.save(output_2)
        return send_file(output_2, as_attachment=True, attachment_filename='birth_certificate.png')
    return render_template('birth_certificate.html')

@app.route('/death_record', methods=['GET', 'POST'])
@login_required
def death_record():
    all_deaths = DeathCertificate.query.all()
    return render_template('death_record.html', all_deaths=all_deaths)

@app.route('/generate_death_certificate', methods=['GET', 'POST'])
def generate_death_certificate():
    if request.method == 'POST':
        name = request.form['deceased_name']
        date_of_death = request.form['date_of_death']
        time_of_death = request.form['time_of_death']
        place_of_death = request.form['place_of_death']
        cause_of_death = request.form['cause_of_death']
        age = request.form['age']
        certificate_id = ''.join(random.choices(string.digits, k=8))
        death_record = DeathCertificate(
            record_type='death',
            name=name, certificate_id=certificate_id,
            date_of_death=date_of_death, time_of_death=time_of_death,
            place_of_death=place_of_death, cause_of_death=cause_of_death, age=age
        )
        db.session.add(death_record)
        db.session.commit()
        temp_path_1 = '/home/PrinceMishra/mysite/static/images/Death Certificate Template.jpg'
        output_1 = '/home/PrinceMishra/mysite/static/images/generated_death_certificate.png'
        image = Image.open(temp_path_1)
        draw = ImageDraw.Draw(image)
        font_path = '/home/PrinceMishra/mysite/static/fonts/Arial.ttf'
        font = ImageFont.truetype(font_path, 40)
        draw.text((100, 200), certificate_id, font=font, fill="black")
        draw.text((770, 800), name, font=font, fill="black")
        draw.text((650, 1000), date_of_death, font=font, fill="black")
        draw.text((650, 1400), time_of_death, font=font, fill="black")
        draw.text((650, 1780), place_of_death, font=font, fill="black")
        draw.text((750, 1200), cause_of_death, font=font, fill="black")
        draw.text((850, 1585), age, font=font, fill="black")
        image.save(output_1)

        return send_file(output_1, as_attachment=True, attachment_filename='death_certificate.png')

    return render_template('death_certificate.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)