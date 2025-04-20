import psycopg2
from datetime import datetime
import smtplib
from pydantic import BaseModel
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import smaranvaidhya_db as smv_db
import schemas
import base64
import io
import json
from typing import Optional
from email.mime.base import MIMEBase
from email import encoders
import os
# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# SMTP Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'quickbook.appointments@gmail.com'
EMAIL_PASSWORD = 'duyi temb getf vimq'  # Replace with your Gmail App Password

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        logger.debug(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

@app.post("/post_appointment_booking_data")
async def post_appointment_booking_data(appointment_data: schemas.AppointmentData):
    logger.debug(f"Received appointment data: {appointment_data.dict()}")
    try:
        result = smv_db.post_appointment_booking_data(appointment_data.dict())
        if result == "Success":
            appointment_id = smv_db.get_latest_appointment_id(appointment_data.patient_id)
            logger.debug(f"Retrieved appointment_id: {appointment_id}")
            if appointment_id:
                appointment_details = smv_db.get_appointment_email_data(appointment_id)
                if appointment_details:
                    subject = f"Appointment Confirmation with Dr. {appointment_details['doctor_first_name']} {appointment_details['doctor_last_name']}"
                    body = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
                            <h2 style="color: #2c3e50;">Appointment Confirmation</h2>
                            <p>Dear {appointment_details['patient_first_name']} {appointment_details['patient_last_name']},</p>
                            <p>Your appointment with <b>Dr. {appointment_details['doctor_first_name']} {appointment_details['doctor_last_name']}</b> ({appointment_details['specialist']}) has been successfully confirmed. Below are the details:</p>
                            <h3 style="color: #2c3e50;">Appointment Details</h3>
                            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; width: 40%;">Appointment ID:</td>
                                    <td style="padding: 8px;">{appointment_details['appointment_id']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Date:</td>
                                    <td style="padding: 8px;">{appointment_details['date_of_appointment']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Time:</td>
                                    <td style="padding: 8px;">{appointment_details['slot_of_appointment']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Mode of Payment:</td>
                                    <td style="padding: 8px;">{appointment_details['mode_of_payment']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Consultancy Type:</td>
                                    <td style="padding: 8px;">{appointment_details['consultancytype']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Fees:</td>
                                    <td style="padding: 8px;">₹{appointment_details['fees']}</td>
                                </tr>
                            </table>
                            <h3 style="color: #2c3e50;">Doctor's Contact Information</h3>
                            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Clinic Address:</td>
                                    <td style="padding: 8px;"><a href="{appointment_details['doctor_clinic_address']}">{appointment_details['doctor_clinic_address']}</a></td>
                                </tr>
                            </table>
                            <p>Please make sure to <b>arrive on time</b> for your appointment. In case of any emergencies or urgent queries, feel free to reach out to the doctor's <b>emergency contact number</b>: {appointment_details['emergency_contact']}.</p>
                            <p>If you encounter any inconveniences or require assistance, you can <b>raise a query</b> with us, and our <b>technical team</b> will reach out to you promptly to address the issue.</p>
                            <p>Thank you for choosing our services. If you have any questions or need to reschedule, feel free to contact us.</p>
                            <p style="margin-top: 20px;">Best regards,<br>Your QuickBook Healthcare Team</p>
                            <hr style="border: 0; border-top: 1px solid #eee;">
                            <p style="font-size: 12px; color: #777;">This is an automated email. Please do not reply directly to this message.</p>
                        </body>
                    </html>
                    """
                    if send_email(appointment_details['patient_email'], subject, body):
                        smv_db.update_email_status(appointment_details['appointment_id'])
                        logger.debug(f"Email sent and status updated for appointment {appointment_details['appointment_id']}")
                    else:
                        logger.error(f"Failed to send email for appointment {appointment_details['appointment_id']}")
                else:
                    logger.error(f"No appointment details found for appointment_id {appointment_id}")
            else:
                logger.error("Failed to retrieve appointment_id")
            return JSONResponse(content={"data": "Success"}, status_code=200)
        else:
            logger.error(f"Failed to save appointment: {result}")
            raise HTTPException(status_code=500, detail=result)
    except Exception as e:
        logger.error(f"Error processing appointment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fastapi")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/attempt_to_login_for_user")
def attempt_to_login_for_user(login_data: schemas.LoginForUser):
    valid_user, user_id = smv_db.validate_login_details(login_data.dict())
    if valid_user:
        return JSONResponse(content={"status": "Login Successful", "user_id": user_id}, status_code=200)
    else:
        return JSONResponse(content={"status": "Login Failed"}, status_code=401)

@app.post("/save_user_registration_details")
def save_user_registration_details(reg_details: schemas.UserRegistration):
    print(reg_details)
    result = smv_db.save_user_registration_details(reg_details.dict())
    response = {"data": result}
    return JSONResponse(content=response, status_code=200)

@app.post("/post_contact_us_data")
def post_contact_us_data(contact_data: schemas.ContactData):
    print(contact_data)
    result = smv_db.post_contact_us_data(contact_data.dict())
    response = {"data": result}
    return JSONResponse(content=response, status_code=200)

@app.post("/post_doctor_information_data")
async def post_doctor_information_data(doc_reg_details: schemas.DoctorRegistration):
    print(doc_reg_details)
    result = smv_db.post_doctor_information_data(doc_reg_details.dict())
    print(doc_reg_details.dict())
    response = {"data": result}
    return JSONResponse(content=response, status_code=200)

@app.get("/get_doctor_data")
def get_doctor_data():
    result = smv_db.get_doctor_data()
    response = {"data": result}
    return JSONResponse(content=response, status_code=200)

@app.get("/get_doctor_view_data")
def get_doctor_view_data(doctor_id: str = Query(...)):
    result = smv_db.get_doctor_view_data(doctor_id)
    return JSONResponse(content=result, status_code=200)

@app.get("/get_user_profile")
def get_user_profile(user_id: str = Query(...)):
    result = smv_db.get_user_profile(user_id)
    if result is None:
        return JSONResponse(content={"error": "User not found"}, status_code=404)
    return JSONResponse(content=result, status_code=200)

@app.put("/update_user_profile/{user_id}")
async def update_user_profile(user_id: str, user: schemas.UpdateUserProfileSchema):
    try:
        result = smv_db.update_user_profile(user_id, user.dict())
        if result:
            return {"message": "Profile updated successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_user_history")
def get_user_history(user_id: str = Query(...)):
    result = smv_db.get_user_history(user_id)
    if result is None:
        return JSONResponse(content={"error": "User not found"}, status_code=404)
    return JSONResponse(content=result, status_code=200)

# SQL Migration to ensure email_sent column exists
def ensure_email_sent_column():
    conn = smv_db.connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            ALTER TABLE smaranvaidhya.appointment_data
            ADD COLUMN IF NOT EXISTS email_sent BOOLEAN DEFAULT FALSE;
        """)
        conn.commit()
        logger.debug("Ensured email_sent column exists")
    except Exception as e:
        logger.error(f"Error adding email_sent column: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
ensure_email_sent_column()

@app.post("/upload_prescription/{appointment_id}")
async def upload_prescription(appointment_id: int, file: UploadFile = File(...)):
    logger.debug(f"Uploading prescription for appointment_id: {appointment_id}")
    try:
        if file.content_type not in ['image/jpeg', 'image/png', 'application/pdf']:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, or PDF allowed.")
        file_content = await file.read()
        result = smv_db.save_prescription(appointment_id, file_content, file.content_type)
        if result == "Success":
            return JSONResponse(content={"data": "Prescription uploaded successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=500, detail=result)
    except Exception as e:
        logger.error(f"Error uploading prescription: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download_prescription/{appointment_id}")
async def download_prescription(appointment_id: int):
    logger.debug(f"Downloading prescription for appointment_id: {appointment_id}")
    try:
        prescription = smv_db.get_prescription(appointment_id)
        if not prescription or not prescription['prescription_file']:
            raise HTTPException(status_code=404, detail="Prescription not found")
        file_content = prescription['prescription_file']
        mime_type = prescription['prescription_mime_type']
        file_extension = {
            "application/pdf": "pdf",
            "image/jpeg": "jpg",
            "image/png": "png"
        }.get(mime_type, "bin")
        filename = f"prescription_{appointment_id}.{file_extension}"
        return Response(
            content=file_content,
            media_type=mime_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(file_content))
            }
        )
    except Exception as e:
        logger.error(f"Error downloading prescription: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading prescription: {str(e)}")

@app.post("/raise_query")
async def raise_query(request_data: schemas.QueryData):
    result = smv_db.save_query_data(request_data.dict())
    if result == "Success":
        return {"data": "Query raised successfully"}
    else:
        raise HTTPException(status_code=500, detail=result)

@app.get("/get_queries")
async def get_queries():
    data = smv_db.get_query_data()
    if data:
        return {"data": data}
    else:
        raise HTTPException(status_code=404, detail="No queries found")

@app.post("/update_query_status/{query_id}")
async def update_query_status(query_id: int, update_data: schemas.QueryStatusUpdate):
    logger.info(f"Received request to update query {query_id} with status: {update_data.status}")
    valid_statuses = ['pending', 'solved']
    if update_data.status not in valid_statuses:
        logger.error(f"Invalid status: {update_data.status}")
        raise HTTPException(status_code=422, detail=f"Status must be one of {valid_statuses}")
    try:
        connection = smv_db.connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE smaranvaidhya.query_data SET status = %s WHERE query_id = %s RETURNING query_id",
            (update_data.status, query_id)
        )
        updated_query = cursor.fetchone()
        connection.commit()
        if not updated_query:
            logger.error(f"Query ID {query_id} not found")
            raise HTTPException(status_code=404, detail="Query not found")
        logger.info(f"Query {query_id} status updated to {update_data.status}")
        return {"data": "Query status updated successfully"}
    except Exception as e:
        logger.error(f"Error updating query {query_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.get("/get_doctor_profile")
async def get_doctor_profile(email: str):
    logger.info(f"Received request for doctor profile with email: {email}")
    if not email:
        logger.error("Email parameter missing")
        raise HTTPException(status_code=400, detail="Email parameter required")
    try:
        connection = smv_db.connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, first_name, last_name, date_of_birth, gender, email, phone_number,
                    state, city, zip_code, clinic_hospital, specialist,
                    available_from, available_to, time_per_patient, max_appointments,
                    highest_qualification, years_of_experience, in_person_fee, video_fee,
                    phone_fee, emergency_availability, emergency_contact,
                    hospital_clinic_address, upi_id,
                    monday, tuesday, wednesday, thursday, friday, saturday, sunday
            FROM smaranvaidhya.doctor_information
            WHERE email = %s
        """, (email,))
        doctor = cursor.fetchone()
        if not doctor:
            logger.error(f"No doctor found for email: {email}")
            raise HTTPException(status_code=404, detail=f"No doctor profile found for email: {email}")
        columns = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'email',
                    'phone_number', 'state', 'city', 'zip_code', 'clinic_hospital',
                    'specialist', 'available_from', 'available_to', 'time_per_patient',
                    'max_appointments', 'highest_qualification', 'years_of_experience',
                    'in_person_fee', 'video_fee', 'phone_fee', 'emergency_availability',
                    'emergency_contact', 'hospital_clinic_address', 'upi_id',
                    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        result = dict(zip(columns, doctor))
        days = []
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            if result[day] == '1':
                days.append(day)
        result['available_days'] = ','.join(days) if days else ''
        result.pop('monday', None)
        result.pop('tuesday', None)
        result.pop('wednesday', None)
        result.pop('thursday', None)
        result.pop('friday', None)
        result.pop('saturday', None)
        result.pop('sunday', None)
        logger.info(f"Fetched profile for doctor ID {result['id']} with email {email}")
        return result
    except Exception as e:
        logger.error(f"Error fetching doctor profile for email {email}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.put("/update_doctor_profile/{doctor_id}")
async def update_doctor_profile(doctor_id: str, update_data: schemas.DoctorProfileUpdate):
    try:
        connection = smv_db.connection()
        cursor = connection.cursor()
        days = update_data.available_days.split(',') if update_data.available_days else []
        day_fields = {
            'monday': '1' if 'monday' in days else '0',
            'tuesday': '1' if 'tuesday' in days else '0',
            'wednesday': '1' if 'wednesday' in days else '0',
            'thursday': '1' if 'thursday' in days else '0',
            'friday': '1' if 'friday' in days else '0',
            'saturday': '1' if 'saturday' in days else '0',
            'sunday': '1' if 'sunday' in days else '0'
        }
        cursor.execute("""
            UPDATE smaranvaidhya.doctor_information
            SET first_name = %s, last_name = %s, phone_number = %s, state = %s,
                city = %s, zip_code = %s, clinic_hospital = %s, specialist = %s,
                available_from = %s, available_to = %s, time_per_patient = %s,
                max_appointments = %s, highest_qualification = %s, years_of_experience = %s,
                in_person_fee = %s, video_fee = %s, phone_fee = %s,
                emergency_availability = %s, emergency_contact = %s,
                hospital_clinic_address = %s, upi_id = %s,
                monday = %s, tuesday = %s, wednesday = %s, thursday = %s,
                friday = %s, saturday = %s, sunday = %s
            WHERE id = %s
            RETURNING id
        """, (
            update_data.first_name, update_data.last_name, update_data.phone_number,
            update_data.state, update_data.city, update_data.zip_code,
            update_data.clinic_hospital, update_data.specialist,
            update_data.available_from, update_data.available_to,
            update_data.time_per_patient, update_data.max_appointments,
            update_data.highest_qualification, update_data.years_of_experience,
            update_data.in_person_fee, update_data.video_fee, update_data.phone_fee,
            update_data.emergency_availability, update_data.emergency_contact,
            update_data.hospital_clinic_address, update_data.upi_id,
            day_fields['monday'], day_fields['tuesday'], day_fields['wednesday'],
            day_fields['thursday'], day_fields['friday'], day_fields['saturday'],
            day_fields['sunday'], doctor_id
        ))
        updated_doctor = cursor.fetchone()
        connection.commit()
        if not updated_doctor:
            logger.error(f"Doctor ID {doctor_id} not found")
            raise HTTPException(status_code=404, detail="Doctor not found")
        logger.info(f"Updated profile for doctor ID {doctor_id}")
        return {"data": "Doctor profile updated successfully"}
    except Exception as e:
        logger.error(f"Error updating doctor profile for ID {doctor_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.get("/get_booked_slots")
async def get_booked_slots(doctor_id: str = Query(...), date: str = Query(...)):
    logger.debug(f"Fetching booked slots for doctor_id: {doctor_id}, date: {date}")
    try:
        booked_slots = smv_db.get_booked_slots(doctor_id, date)
        return JSONResponse(content={"booked_slots": booked_slots}, status_code=200)
    except Exception as e:
        logger.error(f"Error fetching booked slots for doctor_id {doctor_id} on date {date}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cancel_appointment/{appointment_id}")
async def cancel_appointment(appointment_id: int):
    logger.debug(f"Cancelling appointment ID: {appointment_id}")
    try:
        result = smv_db.cancel_appointment(appointment_id)
        return JSONResponse(content={"data": "Appointment cancelled successfully"}, status_code=200)
    except Exception as e:
        logger.error(f"Error cancelling appointment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/reschedule_appointment/{appointment_id}")
async def reschedule_appointment(appointment_id: int, data: schemas.RescheduleData):
    logger.debug(f"Rescheduling appointment ID: {appointment_id} with data: {data.dict()}")
    try:
        result = smv_db.reschedule_appointment(appointment_id, data.date, data.slot, data.consultancytype, data.fees)
        return JSONResponse(content={"data": "Appointment rescheduled successfully"}, status_code=200)
    except Exception as e:
        logger.error(f"Error rescheduling appointment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mark_appointment_visited/{appointment_id}")
async def mark_appointment_visited(appointment_id: int, request: schemas.VisitedRequest):
    try:
        logger.debug(f"Received request for /mark_appointment_visited/{appointment_id} with data: {request}")
        success = smv_db.update_visited(appointment_id, request.visited)
        if success:
            logger.debug(f"Successfully updated visited status for appointment_id {appointment_id}")
            return {"data": "Appointment visited status updated successfully"}
        raise HTTPException(status_code=404, detail="Appointment not found")
    except Exception as e:
        logger.error(f"Error updating visited status for appointment_id {appointment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update visited status: {str(e)}")

@app.post("/update_prescription_text/{appointment_id}")
def update_prescription_text(appointment_id: int, request: schemas.PrescriptionRequest):
    try:
        logger.debug(f"Received request for /update_prescription_text/{appointment_id} with data: {request}")
        if not request.prescription.strip():
            raise HTTPException(status_code=400, detail="Prescription text cannot be empty")
        success = smv_db.update_prescription_text(appointment_id, request.prescription)
        if success:
            logger.debug(f"Successfully updated prescription for appointment_id {appointment_id}")
            return {"data": "Prescription updated successfully"}
        raise HTTPException(status_code=404, detail="Appointment not found")
    except Exception as e:
        logger.error(f"Error updating prescription for appointment_id {appointment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update prescription: {str(e)}")