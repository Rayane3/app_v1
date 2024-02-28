from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'mdrr'

db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    date_of_reservation = db.Column(db.Date, nullable=False)
    time_of_reservation = db.Column(db.Time, nullable=False)
    end_time_of_reservation = db.Column(db.Time, nullable=False)
    booked_place = db.Column(db.String(50), nullable=False)

    def __init__(self, date_of_reservation, time_of_reservation, end_time_of_reservation, booked_place):
        self.date_of_reservation = date_of_reservation
        self.time_of_reservation = time_of_reservation
        self.end_time_of_reservation = end_time_of_reservation
        self.booked_place = booked_place

    # Getters
    def get_id(self):
        return self.id

    def get_date_of_reservation(self):
        return self.date_of_reservation

    def get_time_of_reservation(self):
        return self.time_of_reservation
    
    def get_end_time_of_reservation(self):
        return self.end_time_of_reservation

    def get_booked_place(self):
        return self.booked_place

    # Setters
    def set_date_of_reservation(self, date_of_reservation):
        self.date_of_reservation = date_of_reservation

    def set_time_of_reservation(self, time_of_reservation):
        self.time_of_reservation = time_of_reservation
    
    def set_end_time_of_reservation(self, end_time_of_reservation):
        self.end_time_of_reservation = end_time_of_reservation

    def set_booked_place(self, booked_place):
        self.booked_place = booked_place


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract the data from the AJAX request
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Here, you would include your authentication logic, for example:
        # user = User.query.filter_by(username=username).first()
        # if user and user.check_password(password):
        #     # Login success
        #     return jsonify({'success': True}), 200
        # else:
        #     # Login failed
        #     return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # For demonstration, let's just assume success:
        return jsonify({'success': True}), 200

    # If it's a GET request, just render the template (or handle it however you want)
    return render_template('index.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        booked_place = request.form['booked_place']
        date_of_reservation = datetime.strptime(request.form['date_of_reservation'], '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form['time_of_reservation'], '%H:%M').time()
        end_time = datetime.strptime(request.form['end_time_of_reservation'], '%H:%M').time()

        # Ensure end_time is within 1 hour of start_time
        max_end_time = (datetime.combine(datetime.min, start_time) + timedelta(hours=1)).time()
        if end_time > max_end_time:
            flash('End time must be within 1 hour of start time.')
        else:
            # Create and save the new reservation
            new_reservation = Reservation(
                date_of_reservation=date_of_reservation,
                time_of_reservation=start_time,
                end_time_of_reservation=end_time,
                booked_place=booked_place
            )
            db.session.add(new_reservation)
            db.session.commit()
            flash('Reservation successfully created!')

    # Fetch all reservations regardless of the method
    all_reservations = Reservation.query.all()
    return render_template('booking.html', reservations=all_reservations)


@app.route('/reservations')
def reservations():
    all_reservations = Reservation.query.all()
    return render_template('booking.html', reservations=all_reservations)

@app.route('/create_reservation', methods=['POST'])
def create_reservation():
    booked_place = request.form['booked_place']
    date_of_reservation = datetime.strptime(request.form['date_of_reservation'], '%Y-%m-%d').date()
    start_time = datetime.strptime(request.form['time_of_reservation'], '%H:%M').time()
    end_time = datetime.strptime(request.form['end_time_of_reservation'], '%H:%M').time()

    # Ensure end_time is within 1 hour of start_time
    max_end_time = (datetime.combine(date.min, start_time) + timedelta(hours=1)).time()
    if end_time > max_end_time:
        flash('End time must be within 1 hour of start time.')
        return redirect(url_for('booking'))

    new_reservation = Reservation(
        date_of_reservation=date_of_reservation,
        time_of_reservation=start_time,
        end_time_of_reservation=end_time,
        booked_place=booked_place
    )

    db.session.add(new_reservation)
    db.session.commit()

    flash('Reservation successfully created!')
    return redirect(url_for('reservations'))


# Delete a reservation
@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    print('Delete route called for ID:', reservation_id)
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation deleted successfully'})


# Update a reservation
@app.route('/update_reservation/<int:reservation_id>', methods=['POST'])
def update_reservation(reservation_id):
    # Flask-WTF: Validate CSRF token
    if not request.json:
        return jsonify({'message': 'Invalid JSON data'}), 400

    data = request.json
    reservation = Reservation.query.get_or_404(reservation_id)

    # Update reservation with the new details
    reservation.booked_place = data.get('booked_place')
    reservation.date_of_reservation = datetime.strptime(data.get('date_of_reservation'), '%Y-%m-%d').date()
    reservation.time_of_reservation = datetime.strptime(data.get('time_of_reservation'), '%H:%M').time()
    reservation.end_time_of_reservation = datetime.strptime(data.get('end_time_of_reservation'), '%H:%M').time()

    # Update the database
    db.session.commit()
    return jsonify({'message': 'Reservation updated successfully'})


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)



