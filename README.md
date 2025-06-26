# 🎱 Cuesport Booking App

This is a simple full-stack web application designed for students to book slots for cuesport recreational training sessions. Built with **React** on the frontend and **Flask** on the backend, the app allows slot booking, cancellation, and admin approval through a sleek calendar-based interface.

> ⚠️ **Note**: This is a **demo application**. It is not an official live service.  
> For demonstration purposes, you may access the admin dashboard using the default password:  
> **admin:admin**

---

## 🚀 Features

### ✅ For Students
- 📅 **Calendar View**: Book slots by selecting available Monday or Wednesday dates.
- ⏳ **Pending Approval**: All bookings are subject to admin approval.
- ❌ **Cancel Request**: Request cancellation of approved bookings.
- 📋 **Check Status**: View your bookings and their current status.

### 🔐 For Admins
- 🔒 **Password-Protected Access**
- ✅ **Approve Bookings**: View and approve pending booking requests.
- 🗑 **Remove Bookings**: Delete unnecessary or invalid bookings.
- ❌ **Approve Cancellations**: Handle student-initiated cancellation requests.
- 📆 **Calendar Dashboard**: View all attendees by selecting a date.

---

## 🧭 User Guide

### 👤 For Students
1. **Visit the App Homepage**
2. **Click on `Book a Slot`**
   - Select a **Monday** or **Wednesday** on the calendar.
   - Choose an available time slot and fill in your **name**, **student ID**, and **Telegram handle**.
3. **Submit Booking**
   - Your booking will be **pending approval**.
4. **Check Status**
   - Navigate to `Check Status` and enter your credentials to view the booking status.
5. **Request Cancellation**
   - Go to `Cancel a Booking` and submit a cancellation request for your existing booking.

### 👨‍💼 For Admins
1. Click on the `Admin` button in the top right.
2. Enter the admin password: `admin`
3. On the dashboard:
   - View and approve/reject bookings.
   - View and approve cancellation requests.
   - Use the calendar to check attendees on a specific date.

---

## 🌐 Technologies Used

- **Frontend**: React, React Calendar, Axios
- **Backend**: Flask, Flask-CORS, SQLite
- **Deployment**: Heroku

---

## 📱 Coming Soon
- **Mobile-Responsive Layout** for better experience on phones and tablets.

---

## 🔗 Live Demo

[https://cuesport-booking-app-4cb92a6b4bf8.herokuapp.com/](https://cuesport-booking-app-4cb92a6b4bf8.herokuapp.com/)

---

## 📬 Contact Me

Telegram: [@whiskey83](https://t.me/whiskey83)
