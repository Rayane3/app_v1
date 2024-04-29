from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from ..models import Reservation
from .. import db
from sqlalchemy import and_, or_
from datetime import datetime, timedelta, date

booking = Blueprint('booking', __name__)


@booking.route('/booking')
@login_required
def view_booking():
    all_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    return render_template('booking.html', reservations=all_reservations, today=today, start_of_week=start_of_week)

@booking.route('/create_reservation', methods=['POST'])
@login_required
def create_reservation():
    booked_place = request.form['booked_place']
    date_of_reservation = datetime.strptime(request.form['date_of_reservation'], '%Y-%m-%d').date()
    start_time = datetime.strptime(request.form['time_of_reservation'], '%H:%M').time()
    end_time = datetime.strptime(request.form['end_time_of_reservation'], '%H:%M').time()
    user_id = current_user.id

    # Ensure end_time is within 1 hour of start_time
    max_end_time = (datetime.combine(date.min, start_time) + timedelta(hours=1)).time()
    if end_time > max_end_time:
        flash('End time must be within 1 hour of start time.')
        return redirect(url_for('booking'))
    
    # Check if the place is "Mur d'escalade"
    if booked_place == "Mur d'escalade":
        existing_reservations_count = Reservation.query.filter(
            Reservation.date_of_reservation == date_of_reservation,
            Reservation.booked_place == booked_place,
            or_(and_(Reservation.start_time <= start_time, Reservation.end_time > start_time),
                and_(Reservation.start_time < end_time, Reservation.end_time >= end_time))
        ).count()

        if existing_reservations_count >= 5:
            flash('Mur d\'escalade is fully booked for this time slot.', 'danger')
            return redirect(url_for('booking'))
        
    else:
        # For all other places, ensure no overlapping reservations
        existing_reservation = Reservation.query.filter(
            Reservation.date_of_reservation == date_of_reservation,
            Reservation.booked_place == booked_place,
            or_(and_(Reservation.time_of_reservation <= start_time, Reservation.end_time_of_reservation > start_time),
                and_(Reservation.time_of_reservation < end_time, Reservation.end_time_of_reservation >= end_time))
        ).first()

        if existing_reservation:
            flash('This place is already booked for the selected time slot.', 'danger')
            return redirect(url_for('booking'))

    new_reservation = Reservation(
        user_id=current_user.id,  # Set the user_id to the current user's ID
        date_of_reservation=date_of_reservation,
        time_of_reservation=start_time,
        end_time_of_reservation=end_time,
        booked_place=booked_place
    )

    db.session.add(new_reservation)
    db.session.commit()

    flash('Reservation successfully created!')
    return redirect(url_for('reservations'))


@booking.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def delete_reservation(reservation_id):
    print('Delete route called for ID:', reservation_id)
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation deleted successfully'})

@booking.route('/update_reservation/<int:reservation_id>', methods=['POST'])
@login_required
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

@booking.route('/reservations')
@login_required
def reservations():
    all_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('booking.html', reservations=all_reservations)
