from flask import Blueprint, jsonify, request
from extensions import db
from models import CancellationRequest, Booking
import os
from datetime import datetime

admin_bp = Blueprint("admin", __name__)

# -------------------------------
# ✅ 1. View & Approve Cancellations
# -------------------------------

@admin_bp.route("/admin/cancellations", methods=["GET"])
def get_cancellations():
    requests = CancellationRequest.query.filter_by(status="pending").all()
    result = []

    for r in requests:
        booking = Booking.query.get(r.booking_id)
        if booking:
            result.append({
                "request_id": r.id,
                "booking_id": booking.id,
                "name": booking.name,
                "student_id": booking.student_id,
                "telegram": booking.telegram,
                "slot": booking.slot,
                "date": booking.date.strftime("%d-%m-%Y")
            })

    return jsonify(result)

@admin_bp.route("/admin/cancellations/approve", methods=["POST"])
def approve_request():
    data = request.json
    request_id = data.get("id")
    req = CancellationRequest.query.get(request_id)

    if req:
        req.status = "approved"
        booking = Booking.query.get(req.booking_id)
        if booking:
            db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Cancellation approved."})
    return jsonify({"message": "Request not found."}), 404

# -------------------------------
# ✅ 2. View & Approve Bookings
# -------------------------------

@admin_bp.route("/admin/bookings/pending", methods=["GET"])
def get_pending_bookings():
    pending = Booking.query.filter_by(approval_status="pending").all()
    result = [{
        "id": b.id,
        "name": b.name,
        "student_id": b.student_id,
        "telegram": b.telegram,
        "slot": b.slot,
        "date": b.date.strftime("%d-%m-%Y")
    } for b in pending]

    return jsonify(result)

@admin_bp.route("/admin/bookings/approve", methods=["POST"])
def approve_booking():
    data = request.json
    booking_id = data.get("id")

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found."}), 404

    booking.approval_status = "approved"
    db.session.commit()
    return jsonify({"message": "Booking approved."})

# -------------------------------
# ✅ 3. Remove any booking manually
# -------------------------------

@admin_bp.route("/admin/bookings/remove", methods=["POST"])
def remove_booking():
    data = request.json
    booking_id = data.get("id")

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found."}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking removed successfully."})


@admin_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.json
    if not data or data.get("password") != "secret":
        return jsonify({"success": False, "message": "Invalid password"}), 401
    return jsonify({"success": True})

    

@admin_bp.route("/admin/bookings/by-date", methods=["POST"])
def get_bookings_by_date():
    data = request.json
    date_str = data.get("date")  # Expected format: YYYY-MM-DD

    try:
        from datetime import datetime
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return jsonify({"message": "Invalid date format"}), 400

    bookings = Booking.query.filter_by(date=selected_date, approval_status="approved").all()
    result = [{
        "name": b.name,
        "student_id": b.student_id,
        "telegram": b.telegram,
        "slot": b.slot
    } for b in bookings]

    return jsonify(result)

@admin_bp.route("/admin/attendees", methods=["POST"])
def get_attendees_by_date():
    data = request.json
    try:
        selected_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
    except:
        return jsonify({"message": "Invalid date format"}), 400

    bookings = Booking.query.filter_by(date=selected_date, approval_status="approved").all()

    result = [{
        "name": b.name,
        "student_id": b.student_id,
        "telegram": b.telegram,
        "slot": b.slot
    } for b in bookings]

    return jsonify(result)

