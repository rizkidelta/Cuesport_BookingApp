from extensions import db
from datetime import datetime

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    student_id = db.Column(db.String(20))
    telegram = db.Column(db.String(50))
    slot = db.Column(db.String(20))
    date = db.Column(db.Date)
    approval_status = db.Column(db.String(20), default="pending")  # new field


class CancellationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)

