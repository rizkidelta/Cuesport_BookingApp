from flask import Blueprint, request, jsonify
from extensions import db
from models import Booking, CancellationRequest
from utils.slot_limits import SLOT_LIMITS
from datetime import datetime

bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("/book", methods=["POST"])
def book_slot():
    data = request.json

    try:
        selected_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
    except:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

    slot = data.get("slot")  # e.g., "7-9pm"

    # Check if the selected date is Monday or Wednesday
    weekday_index = selected_date.weekday()  # 0 = Monday, 2 = Wednesday
    if weekday_index not in [0, 2]:
        return jsonify({"message": "You can only book for Monday or Wednesday."}), 400

    # Construct key like "Monday 7-9pm"
    day_name = selected_date.strftime("%A")
    slot_key = f"{day_name} {slot}"

    # Debugging logs (you'll see this in terminal)
    print("Checking slot limit for:", slot_key)

    # Count current bookings for that slot + date (both approved and pending)
    existing = Booking.query.filter_by(slot=slot, date=selected_date).count()
    limit = SLOT_LIMITS.get(slot_key, 0)

    print("Existing bookings:", existing)
    print("Allowed limit:", limit)

    if existing >= limit:
        return jsonify({"message": "Slot is full"}), 400

    # Create the booking with approval_status = "pending"
    booking = Booking(
        name=data.get("name"),
        student_id=data.get("student_id"),
        telegram=data.get("telegram"),
        slot=slot,
        date=selected_date,
        approval_status="pending"
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Booking request submitted for approval."})


@bookings_bp.route("/availability", methods=["POST"])
def check_availability():
    data = request.json
    try:
        selected_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
    except:
        return jsonify({"message": "Invalid date format"}), 400

    if selected_date.weekday() not in [0, 2]:  # 0 = Monday, 2 = Wednesday
        return jsonify({"message": "Only Monday and Wednesday are valid."}), 400

    day_name = selected_date.strftime("%A")
    availability = {}

    for key in SLOT_LIMITS:
        if key.startswith(day_name):
            slot_time = key.split(" ", 1)[1]  # e.g., "7-9pm"
            limit = SLOT_LIMITS[key]
            count = Booking.query.filter_by(slot=slot_time, date=selected_date).count()  # count all bookings
            availability[slot_time] = max(0, limit - count)

    return jsonify(availability)


@bookings_bp.route("/cancel-request", methods=["POST"])
def cancel_request():
    data = request.json
    booking_id = data.get("booking_id")

    if not booking_id:
        return jsonify({"message": "Booking ID is required."}), 400

    # Find the booking by ID
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found."}), 404

    # Check if a pending cancellation request already exists
    existing_request = CancellationRequest.query.filter_by(booking_id=booking.id, status="pending").first()
    if existing_request:
        return jsonify({"message": "Cancellation request already submitted."}), 400

    # Create a new cancellation request
    request_entry = CancellationRequest(booking_id=booking.id)
    db.session.add(request_entry)
    db.session.commit()

    return jsonify({"message": "Cancellation request submitted."})


@bookings_bp.route("/my-bookings", methods=["POST"])
def my_bookings():
    data = request.json
    student_id = data.get("student_id")
    telegram = data.get("telegram")

    if not student_id or not telegram:
        return jsonify({"message": "Student ID and Telegram are required."}), 400

    bookings = Booking.query.filter_by(student_id=student_id, telegram=telegram).all()

    if not bookings:
        return jsonify({"message": "No bookings found for this student."}), 404

    booking_list = []
    for b in bookings:
        # Check for pending cancellation request
        pending_cancel = CancellationRequest.query.filter_by(booking_id=b.id, status="pending").first()
        if pending_cancel:
            status = "pending cancellation"
        else:
            status = b.approval_status  # "pending" or "approved"

        booking_list.append({
            "id": b.id,
            "slot": b.slot,
            "date": b.date.strftime("%d-%m-%Y"),
            "status": status
        })


    return jsonify(booking_list)
