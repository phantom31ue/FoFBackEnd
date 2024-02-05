from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
import datetime

import smtplib
from email.message import EmailMessage


PASSWORD = "vkbdvirlcbfikfwq"
SENDER = "codetestjayy@gmail.com"

# Set frequency to 2000 Hertz
frequency = 2000
# Set duration to 1500 milliseconds (1.5 seconds)
duration = 300

def send_email(mail):
    # print("Sending email...")
    # Make beep sound on Windows
    # winsound.Beep(frequency, duration)
    # pass
    RECEIVER = mail
    
    email_message = EmailMessage()
    email_message["Subject"] = "New Donation"
    email_message.set_content("Hey, a new donation has been listed in your area. Check it out now in our website!")
    
    #port for gmail is 587
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    
    
if __name__ == "_main_":
    send_email()
    pass

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

CORS(app)

class NGO(db.Model):
    __tablename__ = 'ngo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    noOfDonations = db.Column(db.Integer, nullable=False, default=0)
    noOfPlates = db.Column(db.Integer, nullable=False, default=0)
    noOfActiveDonations = db.Column(db.Integer, nullable=False, default=0) 

class donor(db.Model):
    __tablename__ = 'donor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    noOfDonations = db.Column(db.Integer, nullable=False, default=0)
    noOfPlatesDonated = db.Column(db.Integer, nullable=False, default=0)
    noOfActiveDonations = db.Column(db.Integer, nullable=False, default=0)
    donations = db.relationship('donation', backref='donor', lazy=True)     

class donation(db.Model):
    __tablename__ = 'donation'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    foods = db.relationship('food', backref='donation', lazy=True)

class food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    serving = db.Column(db.Integer, nullable=False)
    expiry = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    donation_id = db.Column(db.Integer, db.ForeignKey('donation.id'), nullable=False)  # Corrected ForeignKey reference

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Food Donation Portal"})

@app.route('/registerNGO', methods=['POST'])
def registerNGO():
    data = request.get_json()
    print(data)
    name = data['name']
    email = data['email']
    password = data['password']
    confirm = data['confirm']
    if(password != confirm):
        return jsonify({"message": "Passwords do not match"})
    password = hashlib.md5(password.encode()).hexdigest()
    phone = data['phone']
    address = data['address']
    city = data['city']
    state = data['state']
    pincode = data['pincode']
    country = data['country']
    new_ngo = NGO(name=name, email=email, password=password, phone=phone, address=address, city=city, state=state, pincode=pincode, country=country)
    db.session.add(new_ngo)
    db.session.commit()
    return jsonify({"message": "NGO registered successfully"})

@app.route('/registerDonor', methods=['POST'])
def registerDonor():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']
    phone = data['phone']
    confirm = data['confirm']
    if(password != confirm):
        return jsonify({"message": "Passwords do not match"})
    password = hashlib.md5(password.encode()).hexdigest()
    new_donor = donor(name=name, email=email, password=password, phone=phone)
    db.session.add(new_donor)
    db.session.commit()
    return jsonify({"message": "Donor registered successfully"})

@app.route('/loginNGO', methods=['POST'])
def loginNGO():
    data = request.json
    print(data)
    email = data['email']
    password = data['password']
    ngo = NGO.query.filter_by(email=email).first()
    # for key, value in ngo.__dict__.items():
    #     print(key, value)
    if ngo:
        if ngo.password == hashlib.md5(password.encode()).hexdigest():
            return jsonify({"message": "NGO logged in successfully", "id":ngo.id})
        else:
            return jsonify({"message": "Invalid email or password"})
    else:
        return jsonify({"message": "Invalid email or password"})
    
@app.route('/loginDonor', methods=['POST'])
def loginDonor():
    data = request.json
    email = data['email']
    password = data['password']
    donorr = donor.query.filter_by(email=email).first()
    if donorr:
        if donorr.password == hashlib.md5(password.encode()).hexdigest():
            return jsonify({"message": "Donor logged in successfully", "id":donorr.id})
        else:
            return jsonify({"message": "Invalid email or password"})
    else:
        return jsonify({"message": "Invalid email or password"})
    
@app.route('/addDonation/<int:donor_id>', methods=['POST'])
def addDonation(donor_id):
    donor_id = int(donor_id)
    data = request.json['data']
    print(data)
    print(data[0])
    address = data[0]['address']
    city = data[0]['city']
    state = data[0]['state']
    pincode = data[0]['pincode']
    country = data[0]['country']
    phone = data[0]['phone']

    print('Donation details adding....')

    new_donation = donation(address=address, city=city, state=state, pincode=pincode, country=country, donor_id=donor_id, phone=phone)    
    print('Donation details adding....1')
    db.session.add(new_donation)
    print('Donation details adding....2')
    db.session.commit()
    print('Donation details adding....3')
    donation_id = new_donation.id

    print('Donation details added successfully')

    donations = 0
    plates = 0
    for i in data:
        donations += 1
        plates += int(i['serving'])
        foodName = i['name']
        serving = int(i['serving'])
        quantity = int(i['quantity'])
        expiry = i['expiry']
        new_food = food(name=foodName, serving=serving, quantity=quantity, expiry=expiry, donation_id=donation_id)
        db.session.add(new_food)
        db.session.commit()

    donorr = donor.query.get(donor_id)
    donorr.noOfDonations += donations
    donorr.noOfPlatesDonated += plates
    donorr.noOfActiveDonations += 1
    db.session.commit()

    # send email to all ngo in the area
    allNGO = NGO.query.all()
    for i in allNGO:
        if i.pincode == pincode:
            send_email(i.email)

    return jsonify({"message": "Donation added successfully"})

@app.route('/DashboardNGO/<int:ngo_id>', methods=['GET'])
def DashboardNGO(ngo_id):
    ngo = NGO.query.get(ngo_id)

    foodList = []

    current_datetime=datetime.datetime.now()
    str_date = current_datetime.strftime("%Y-%m-%d")

    donations = donation.query.all()
    
    for i in donations:
        if not (i.pincode == ngo.pincode and i.city == ngo.city and i.state == ngo.state and i.country == ngo.country):
            continue
        donationDetails = {
            "address": i.address,
            "city": i.city,
            "state": i.state,
            "pincode": i.pincode,
            "country": i.country,
            "items": [],
            "id" : i.id,
            "phone": i.phone
        }

        current_datetime=datetime.datetime.now()
        str_date = current_datetime.strftime("%Y-%m-%d")

        availFood = food.query.filter_by(donation_id=i.id).all()
        for foood in availFood:
            if str_date < foood.expiry:
                mydict = {key: value for key, value in foood.__dict__.items() if not key.startswith('_')}
                mydict.pop('donation_id', None)
                mydict.pop('_sa_instance_state', None)  
                donationDetails["items"].append(mydict)

        if donationDetails["items"]:
            foodList.append(donationDetails)

    print('foodList:', foodList)

    return jsonify({"foodList": foodList, "name": ngo.id, "email": ngo.email, "phone": ngo.phone, "noOfDonations": ngo.noOfDonations, "noOfPlates": ngo.noOfPlates, "noOfActiveDonations": ngo.noOfActiveDonations, "address": ngo.address, "city": ngo.city, "state": ngo.state, "pincode": ngo.pincode, "country": ngo.country})   


@app.route('/DashboardDonor/<int:donor_id>', methods=['GET'])
def DashboardDonor(donor_id):
    donorr = donor.query.get(donor_id)
    noOfDonations = donorr.noOfDonations
    noOfPlatesDonated = donorr.noOfPlatesDonated
    noOfActiveDonations = donorr.noOfActiveDonations

    donations = donation.query.all()
    t = []
    for i in donations:
        if i.donor_id == donor_id:
            t.append(i)
    donations = t

    jsonDonations = []

    current_datetime=datetime.datetime.now()
    str_date = current_datetime.strftime("%Y-%m-%d")
    for i in donations:     
        donationDetails = {}
        donationDetails["address"] = i.address
        donationDetails["city"] = i.city
        donationDetails["state"] = i.state
        donationDetails["pincode"] = i.pincode
        donationDetails["country"] = i.country

        foood = food.query.filter_by(donation_id=i.id).all()
        if not foood:
            continue
        items = []
        for item in foood:
            if item.expiry > str_date:
                for key, value in item.__dict__.items():
                    item = {key: value}
                items.append(item)
        donationDetails["items"] = items
        jsonDonations.append(donationDetails)
    
    return jsonify({ "donations" : jsonDonations, "name" : donorr.name, "email":donorr.email, "phone" : donorr.phone , "noOfDonations": noOfDonations, "noOfPlatesDonated": noOfPlatesDonated, "noOfActiveDonations": noOfActiveDonations})

@app.route('/DeleteDonation/<int:donation_id>', methods=['DELETE'])
def DeleteDonation(donation_id):
    availFood = food.query.filter_by(donation_id=donation_id).all()
    
    donorr = donor.query.get(donation.query.get(donation_id).donor_id)
    donorr.noOfActiveDonations -= 1
    db.session.commit()

    plates = 0
    for i in availFood:
        plates += i.serving
    
    #add to ngo plates
    ngo = NGO.query.get(donorr.id)
    ngo.noOfPlates += plates
    ngo.noOfDonations += 1
    ngo.noOfActiveDonations += 1
    db.session.commit()
    
    for i in availFood:
        db.session.delete(i)
        db.session.commit()
    donationn = donation.query.get(donation_id)
    db.session.delete(donationn)
    db.session.commit()
    return jsonify({"message": "Donation deleted successfully"})

def initialize_database():
    with app.app_context():
        try:
            db.create_all()
            print("Database initialized.")
        except Exception as e:
            print(f"An error occurred while initializing the database: {e}")


if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', debug=True, port=5000)

