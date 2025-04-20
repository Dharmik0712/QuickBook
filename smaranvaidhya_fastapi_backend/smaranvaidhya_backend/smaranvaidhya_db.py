import psycopg2
import json
import psycopg2.extras
from datetime import datetime

def connection():
        conn = psycopg2.connect(
                database="healthcare_db", user='healthcare_user', password='12345678', host='127.0.0.1', port= '5432'
        )
        return conn

def get_latest_appointment_id(patient_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = """
                SELECT appointment_id
                FROM smaranvaidhya.appointment_data
                WHERE patient_id = %s
                ORDER BY appointment_id DESC
                LIMIT 1
                """
                cursor.execute(QUERY, (patient_id,))
                record = cursor.fetchone()
                return record['appointment_id'] if record else None
        except Exception as e:
                print(f"Error fetching latest appointment ID: {str(e)}")
                return None
        finally:
                cursor.close()
                conn.close()

def get_appointment_email_data(appointment_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = """
                SELECT 
                a.appointment_id,
                p.first_name AS patient_first_name,
                p.last_name AS patient_last_name,
                p.email AS patient_email,
                p.phone_number AS patient_phone,
                TO_CHAR(a.date_of_appointment, 'DD-MON-YYYY') AS date_of_appointment,
                TO_CHAR(a.slot_of_appointment, 'HH24:MI:SS') AS slot_of_appointment,
                a.mode_of_payment,
                a.consultancytype,
                a.fees,
                d.first_name AS doctor_first_name,
                d.last_name AS doctor_last_name,
                d.specialist,
                d.emergency_contact,
                d.phone_number AS doctor_phone,
                d.email AS doctor_email,
                d.hospital_clinic_address AS doctor_clinic_address,
                d.years_of_experience,
                d.highest_qualification
                FROM 
                smaranvaidhya.appointment_data a
                INNER JOIN 
                smaranvaidhya.doctor_information d ON a.doctor_id = d.id
                INNER JOIN 
                smaranvaidhya.patient_registration p ON a.patient_id = p.patient_id
                WHERE 
                a.appointment_id = %s
                """
                cursor.execute(QUERY, (appointment_id,))
                record = cursor.fetchone()
                return record if record else None
        except Exception as e:
                print(f"Error fetching appointment email data: {str(e)}")
                return None
        finally:
                cursor.close()
                conn.close()

def update_email_status(appointment_id):
        conn = connection()
        cursor = conn.cursor()
        try:
                QUERY = """
                UPDATE smaranvaidhya.appointment_data
                SET email_sent = TRUE
                WHERE appointment_id = %s
                """
                cursor.execute(QUERY, (appointment_id,))
                conn.commit()
                print(f"Email status updated for appointment ID {appointment_id}")
        except Exception as e:
                print(f"Failed to update email status: {e}")
                conn.rollback()
        finally:
                cursor.close()
                conn.close()
        
def validate_login_details(login_data):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        valid_user = False
        user_id = None  
        email = login_data["email"]
        user_type = login_data["user_login_type"]
        try:
                if user_type == "patient":
                        QUERY = "SELECT patient_id, email, password FROM smaranvaidhya.patient_login WHERE email = %s"
                elif user_type == "doctor":
                        QUERY = "SELECT doctor_id, email, password FROM smaranvaidhya.doctor_login WHERE email = %s"
                elif user_type == "admin":
                        QUERY = "SELECT admin_id, email, password FROM smaranvaidhya.admin_login WHERE email = %s"
                else:
                        return valid_user, None
                cursor.execute(QUERY, (email,))
                reg_records = cursor.fetchall()
                for row in reg_records:
                        if login_data["email"] == row["email"] and login_data["password"] == row["password"]:
                                valid_user = True
                                user_id = row["patient_id"] if user_type == "patient" else row["doctor_id"] if user_type == "doctor" else row["admin_id"]
        except Exception as e:
                print("Error:", str(e))
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return valid_user, user_id  

def save_user_registration_details(request_data):
        conn = connection()
        cursor = conn.cursor()
        try:
                QUERY1 = '''
                SELECT count(patient_id) FROM smaranvaidhya.patient_registration
                '''
                reg_result = cursor.execute(QUERY1)
                reg_records = cursor.fetchall()
                for row in reg_records:
                        no_of_patients = row[0]
                patients_reg_no = ''
                if(no_of_patients < 9):
                        patients_id_no = 'P' + '00' + str(no_of_patients+1)
                elif(no_of_patients < 99):
                        patients_id_no = 'P' + '0' + str(no_of_patients+1)
                else:
                        patients_id_no = 'P' + str(no_of_patients+1)
                print(patients_id_no)
                current_date = datetime.now().date()
                formatted_date = current_date.strftime('%Y-%m-%d')
                print("formmatted date" ,formatted_date )

                INSERT_QUERY = '''
                        INSERT INTO smaranvaidhya.patient_registration(
                        patient_id,
                        first_name,
                        last_name,  
                        date_of_birth,
                        gender,
                        email,
                        phone_number,
                        password,
                        state,
                        city,
                        zip_code,
                        registration_date
                        ) 
                        VALUES('{}','{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(
                                patients_id_no,
                                request_data['first_name'],
                                request_data['last_name'],
                                request_data['date_of_birth'],
                                request_data['gender'],
                                request_data['email'],
                                request_data['phone_number'],
                                request_data['password'],
                                request_data['state'],
                                request_data['city'],
                                request_data['zip_code'],
                                formatted_date
                        )
                print(INSERT_QUERY)
                cursor.execute(INSERT_QUERY)
                conn.commit()
                INSERT_QUERY1 = '''
                        INSERT INTO smaranvaidhya.patient_login(
                        patient_id,
                        email,
                        password
                        ) 
                        VALUES('{}','{}','{}')'''.format(
                                patients_id_no,
                                request_data['email'],
                                request_data['password']
                        )
                cursor.execute(INSERT_QUERY1)
                conn.commit()
        except Exception as e:
                print("Error", str(e), "Occurred")
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return "Success"

def post_contact_us_data(request_data):
        conn = connection()
        cursor = conn.cursor()
        try:
                INSERT_QUERY = '''
                        INSERT INTO smaranvaidhya.contact_us_data(
                        full_name,
                        email,
                        message 
                        ) 
                        VALUES('{}','{}', '{}')'''.format(
                                request_data['full_name'],
                                request_data['email'],
                                request_data['message'],
                        )
                print(INSERT_QUERY)
                cursor.execute(INSERT_QUERY)
                conn.commit()
        except Exception as e:
                print("Error", str(e), "Occurred")
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return "Success"

def post_doctor_information_data(request_data):
        conn = connection()  
        cursor = conn.cursor()
        try:
                QUERY1 = '''
                        SELECT count(id) FROM smaranvaidhya.doctor_information
                        '''
                reg_result = cursor.execute(QUERY1)
                reg_records = cursor.fetchall()
                for row in reg_records:
                        no_of_doctors = row[0]
                doctor_id_no = ''
                if no_of_doctors < 9:
                        doctor_id_no = 'D' + '00' + str(no_of_doctors + 1)
                elif no_of_doctors < 99:
                        doctor_id_no = 'D' + '0' + str(no_of_doctors + 1)
                else:
                        doctor_id_no = 'D' + str(no_of_doctors + 1)
                print(doctor_id_no)
                current_date = datetime.now().date()
                formatted_date = current_date.strftime('%Y-%m-%d')
                print("formatted date", formatted_date)
                INSERT_QUERY = '''
                        INSERT INTO smaranvaidhya.doctor_information (
                        id,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        email,
                        phone_number,
                        state,
                        city,
                        zip_code,
                        clinic_hospital,
                        specialist,
                        available_from,
                        available_to,
                        time_per_patient,
                        max_appointments,
                        highest_qualification,
                        years_of_experience,
                        in_person_fee,
                        video_fee,
                        phone_fee,
                        emergency_availability,
                        emergency_contact,
                        doctor_image,
                        hospital_clinic_address,
                        monday, 
                        tuesday,
                        wednesday,
                        thursday,
                        friday,
                        saturday,
                        sunday,
                        upi_id
                        ) 
                        VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(
                                doctor_id_no,
                                request_data['first_name'],
                                request_data['last_name'],
                                request_data['date_of_birth'],
                                request_data['gender'],
                                request_data['email'],
                                request_data['phone_number'],
                                request_data['state'],
                                request_data['city'],
                                request_data['zip_code'],
                                request_data['clinic_hospital'],
                                request_data['specialist'],
                                request_data['available_from'],
                                request_data['available_to'],
                                request_data['time_per_patient'],
                                request_data['max_appointments'],
                                request_data['highest_qualification'],
                                request_data['years_of_experience'],
                                request_data['in_person_fee'],
                                request_data['video_fee'],
                                request_data['phone_fee'],
                                request_data['emergency_availability'],
                                request_data['emergency_contact'],
                                request_data['doctor_image'],
                                request_data['hospital_clinic_address'],
                                request_data['monday'],
                                request_data['tuesday'],
                                request_data['wednesday'],
                                request_data['thursday'],
                                request_data['friday'],
                                request_data['saturday'],
                                request_data['sunday'],
                                request_data['upi_id']
                        )
                print(INSERT_QUERY)
                cursor.execute(INSERT_QUERY)
                conn.commit()
                doctorPassword = str(request_data['dob'])[:4] + str(request_data['mobile_no'])[5:]
                print(doctorPassword)
                print(request_data['mobile_no'], request_data['dob'])
                LOGIN_QUERY1 = '''
                        INSERT INTO smaranvaidhya.doctor_login(
                        doctor_id,
                        email_id,
                        password
                        ) 
                        VALUES('{}','{}','{}')'''.format(
                                doctor_id_no,
                                request_data['email'],
                                doctorPassword
                        )
                cursor.execute(LOGIN_QUERY1)
                conn.commit()
        except Exception as e:
                print("Error", str(e), "Occurred")
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return "Success"

def get_doctor_data():
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = '''
                        SELECT 
                        id,
                        first_name,
                        last_name,
                        TO_CHAR(date_of_birth, 'DD-MON-YYYY') AS date_of_birth,
                        gender,
                        email,
                        phone_number,
                        state,
                        city,
                        zip_code,
                        clinic_hospital,
                        specialist,
                        TO_CHAR(available_from, 'HH24:MI:SS') AS available_from,
                        TO_CHAR(available_to, 'HH24:MI:SS') AS available_to,
                        time_per_patient,
                        max_appointments,
                        highest_qualification,
                        years_of_experience,
                        in_person_fee,
                        video_fee,
                        phone_fee,
                        emergency_availability,
                        emergency_contact,
                        doctor_image,
                        hospital_clinic_address,
                        monday, 
                        tuesday,
                        wednesday,
                        thursday,
                        friday,
                        saturday,
                        sunday,
                        upi_id
                        FROM smaranvaidhya.doctor_information
                        '''
                print(QUERY)
                cursor.execute(QUERY)
                records = cursor.fetchall()
                for record in records:
                        if record["doctor_image"] is not None:
                                record["doctor_image"] = record["doctor_image"].tobytes().decode("utf-8")
                json_result = json.dumps(records, indent=2)
                print(json_result)
        except Exception as e:
                print("Error", str(e), "Occurred")
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return json_result

def post_appointment_booking_data(request_data):
        conn = connection()
        cursor = conn.cursor()
        try:
                INSERT_QUERY = """
                INSERT INTO smaranvaidhya.appointment_data (
                doctor_id,
                patient_id,
                patient_name,
                contact_number,
                gender,
                age,
                date_of_appointment,
                slot_of_appointment,
                reason_for_visit,
                pre_existing_conditions,
                current_medications,
                allergies,
                mode_of_payment,
                consultancytype,
                fees,
                email_sent
                ) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', FALSE)
                """.format(
                request_data['doctor_id'],
                request_data['patient_id'],
                request_data['patient_name'],
                request_data['contact_number'],
                request_data['gender'],
                request_data['age'],
                request_data['date_of_appointment'],
                request_data['slot_of_appointment'],
                request_data['reason_for_visit'],
                request_data['pre_existing_conditions'],
                request_data['current_medications'],
                request_data['allergies'],
                request_data['mode_of_payment'],
                request_data['consultancytype'],
                request_data['fees']
                )
                print(INSERT_QUERY)  
                cursor.execute(INSERT_QUERY)
                conn.commit()
                return "Success"
        except Exception as e:
                print("Error:", str(e))
                return "Failed: " + str(e)
        finally:
                if conn:
                        cursor.close()
                        conn.close()

def get_user_profile(user_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = '''
                SELECT 
                patient_id,
                first_name,
                last_name,  
                TO_CHAR(date_of_birth, 'DD-MON-YYYY') AS date_of_birth,
                gender,
                email,
                phone_number,
                password,
                state,
                city,
                zip_code
                FROM smaranvaidhya.patient_registration
                WHERE patient_id = %s
                '''
                cursor.execute(QUERY, (user_id,))
                record = cursor.fetchone()  
                if not record:
                        return None  
                print(json.dumps(record, indent=2)) 
                return record  
        except Exception as e:
                print("Error", str(e), "Occurred")
                raise e
        finally:
                if conn:
                        cursor.close()
                        conn.close()

def update_user_profile(user_id, data):
        conn = None
        cursor = None
        try:
                conn = connection()  
                cursor = conn.cursor()
                QUERY = '''
                UPDATE smaranvaidhya.patient_registration
                SET first_name = %s, last_name = %s, email = %s, phone_number = %s, 
                password = %s, city = %s, state = %s, zip_code = %s
                WHERE patient_id = %s
                RETURNING patient_id
                '''
                cursor.execute(QUERY, (
                data["first_name"], 
                data["last_name"], 
                data["email"],
                data["phone_number"], 
                data["password"], 
                data["city"],
                data["state"], 
                data["zip_code"], 
                user_id
                ))
                updated_row = cursor.fetchone()  
                conn.commit() 
                return bool(updated_row) 
        except psycopg2.Error as e:
                print(f"Database Error: {e.pgcode} - {e.pgerror}")
                if conn:
                        conn.rollback()  
                raise
        finally:
                if cursor:
                        cursor.close()
                if conn:
                        conn.close()

def get_user_history(user_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = '''
                SELECT 
                appointment_id,
                doctor_id,
                patient_name,
                gender,
                age,
                TO_CHAR(date_of_appointment, 'DD-MON-YYYY') AS date_of_appointment,
                TO_CHAR(slot_of_appointment, 'HH24:MI:SS') AS slot_of_appointment,
                mode_of_payment,
                contact_number,
                reason_for_visit,
                pre_existing_conditions,
                current_medications,
                allergies,
                prescription_file IS NOT NULL AS has_prescription,
                prescription,
                visited
                FROM smaranvaidhya.appointment_data
                WHERE patient_id = %s
                '''
                cursor.execute(QUERY, (user_id,))
                record = cursor.fetchall()
                if not record:
                        return None
                return record
        except Exception as e:
                print("Error", str(e), "Occurred")
                raise e
        finally:
                cursor.close()
                conn.close()

def get_doctor_view_data(doctor_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)   
        try:
                QUERY = '''
                SELECT 
                appointment_id,
                patient_id,
                patient_name,
                gender,
                age,
                TO_CHAR(date_of_appointment, 'YYYY-MM-DD') AS date_of_appointment,
                TO_CHAR(slot_of_appointment, 'HH24:MI:SS') AS slot_of_appointment,
                mode_of_payment,
                contact_number,
                reason_for_visit,
                pre_existing_conditions,
                current_medications,
                allergies,
                prescription_file IS NOT NULL AS has_prescription,
                prescription,
                visited
                FROM smaranvaidhya.appointment_data
                WHERE doctor_id = %s
                '''
                cursor.execute(QUERY, (doctor_id,))
                record = cursor.fetchall()
                if not record:
                        return None
                return record
        except Exception as e:
                print("Error", str(e), "Occurred")
                raise e
        finally:
                cursor.close()
                conn.close()

def get_user_doctor_appointment_data():
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = '''
                SELECT 
                a.appointment_id,
                p.first_name AS patient_first_name,
                p.last_name AS patient_last_name,
                p.email AS patient_email,
                p.phone_number AS patient_phone,
                a.date_of_appointment,
                a.slot_of_appointment,
                a.mode_of_payment,
                a.consultancytype,
                a.fees,
                d.first_name AS doctor_first_name,
                d.last_name AS doctor_last_name,
                d.specialist,
                d.emergency_contact,
                d.phone_number AS doctor_phone,
                d.email AS doctor_email,
                d.hospital_clinic_address AS doctor_clinic_address,
                d.years_of_experience,
                d.highest_qualification
                FROM 
                smaranvaidhya.appointment_data a
                INNER JOIN 
                smaranvaidhya.doctor_information d ON a.doctor_id = d.id
                INNER JOIN 
                smaranvaidhya.patient_registration p ON a.patient_id = p.patient_id
                WHERE 
                a.email_sent = FALSE;       
                '''
                cursor.execute(QUERY)
                record = cursor.fetchall() 
                record = cursor.fetchone()
                if record and record['prescription_file']:
                        record['prescription_file'] = bytes(record['prescription_file'])
                        return record
                print(json.dumps(record, indent=2))  
                return record 
        except Exception as e:
                print("Error", str(e), "Occurred")
                raise e
        finally:
                if conn:
                        cursor.close()
                        conn.close()

def save_prescription(appointment_id, file_content, mime_type):
        conn = connection()
        cursor = conn.cursor()
        try:
                QUERY = """
                UPDATE smaranvaidhya.appointment_data
                SET prescription_file = %s, prescription_mime_type = %s
                WHERE appointment_id = %s
                """
                cursor.execute(QUERY, (psycopg2.Binary(file_content), mime_type, appointment_id))
                if cursor.rowcount == 0:
                        return "Failed: Appointment not found"
                conn.commit()
                return "Success"
        except Exception as e:
                print(f"Error saving prescription: {str(e)}")
                conn.rollback()
                return f"Failed: {str(e)}"
        finally:
                cursor.close()
                conn.close()

def get_prescription(appointment_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = """
                SELECT prescription_file, prescription_mime_type
                FROM smaranvaidhya.appointment_data
                WHERE appointment_id = %s
                """
                cursor.execute(QUERY, (appointment_id,))
                record = cursor.fetchone()
                if not record:
                        return None
                result = {
                'prescription_file': record['prescription_file'].tobytes() if record['prescription_file'] else None,
                'prescription_mime_type': record['prescription_mime_type']
                }
                return result
        except Exception as e:
                print(f"Error fetching prescription: {str(e)}")
                raise e
        finally:
                cursor.close()
                conn.close()

def save_query_data(request_data):
        conn = connection()
        cursor = conn.cursor()
        try:
                INSERT_QUERY = """
                INSERT INTO smaranvaidhya.query_data (
                user_id,
                appointment_id,
                subject,
                query,
                status
                ) VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(INSERT_QUERY, (
                request_data['user_id'],
                request_data['appointment_id'],
                request_data['subject'],
                request_data['query'],'pending'
                ))
                conn.commit()
                return "Success"
        except Exception as e:
                print(f"Error saving query: {str(e)}")
                conn.rollback()
                return f"Failed: {str(e)}"
        finally:
                cursor.close()
                conn.close()

def get_query_data():
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = """
                SELECT 
                query_id,
                user_id,
                appointment_id,
                subject,
                query,
                status,
                TO_CHAR(created_at, 'DD-MON-YYYY HH24:MI:SS') AS created_at
                FROM smaranvaidhya.query_data
                ORDER BY created_at DESC
                """
                cursor.execute(QUERY)
                records = cursor.fetchall()
                return records
        except Exception as e:
                print(f"Error fetching queries: {str(e)}")
                raise e
        finally:
                cursor.close()
                conn.close()

def update_query_status(query_id, status):
        conn = connection()
        cursor = conn.cursor()
        try:
                QUERY = """
                UPDATE smaranvaidhya.query_data
                SET status = %s
                WHERE query_id = %s
                """
                cursor.execute(QUERY, (status, query_id))
                if cursor.rowcount == 0:
                        return "Failed: Query not found"
                conn.commit()
                return "Success"
        except Exception as e:
                print(f"Error updating query status: {str(e)}")
                conn.rollback()
                return f"Failed: {str(e)}"
        finally:
                cursor.close()
                conn.close()

def get_booked_slots(doctor_id, date):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = """
                SELECT TO_CHAR(slot_of_appointment, 'HH24:MI:SS') AS slot_of_appointment
                FROM smaranvaidhya.appointment_data
                WHERE doctor_id = %s AND date_of_appointment = %s
                """
                cursor.execute(QUERY, (doctor_id, date))
                records = cursor.fetchall()
                booked_slots = [record['slot_of_appointment'] for record in records]
                return booked_slots
        except Exception as e:
                print(f"Error fetching booked slots: {str(e)}")
                return []
        finally:
                cursor.close()
                conn.close()

def cancel_appointment(appointment_id):
        print(f"DEBUG: cancel_appointment called with appointment_id={appointment_id}")
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY_CHECK = '''
                SELECT FROM smaranvaidhya.appointment_data
                WHERE appointment_id = %s
                '''
                cursor.execute(QUERY_CHECK, (appointment_id,))
                result = cursor.fetchone()
                if not result:
                        raise ValueError(f"Appointment ID {appointment_id} not found")
                QUERY_DELETE = '''
                DELETE FROM smaranvaidhya.appointment_data
                WHERE appointment_id = %s
                RETURNING appointment_id
                '''
                cursor.execute(QUERY_DELETE, (appointment_id,))
                result = cursor.fetchone()
                print(f"DEBUG: Delete result: {result}")
                conn.commit()
                return True
        except Exception as e:
                print(f"ERROR: Failed to cancel appointment: {str(e)}")
                conn.rollback()
                raise Exception(f"Failed to cancel appointment: {str(e)}")
        finally:
                cursor.close()
                conn.close()

def reschedule_appointment(appointment_id, date, slot, consultancytype, fees):
        print(f"DEBUG: reschedule_appointment called with appointment_id={appointment_id}, date={date}, slot={slot}, consultancytype={consultancytype}, fees={fees}")
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY_CHECK_VISITED = '''
                SELECT FROM smaranvaidhya.appointment_data
                WHERE appointment_id = %s
                '''
                cursor.execute(QUERY_CHECK_VISITED, (appointment_id,))
                result = cursor.fetchone()
                if not result:
                        raise ValueError(f"Appointment ID {appointment_id} not found")
                QUERY_CHECK_SLOT = '''
                SELECT appointment_id FROM smaranvaidhya.appointment_data
                WHERE doctor_id = (
                SELECT doctor_id FROM smaranvaidhya.appointment_data WHERE appointment_id = %s
                ) AND date_of_appointment = %s AND slot_of_appointment = %s AND appointment_id != %s
                '''
                cursor.execute(QUERY_CHECK_SLOT, (appointment_id, date, slot, appointment_id))
                if cursor.fetchone():
                        print("DEBUG: Slot is already booked")
                        raise ValueError("Selected slot is already booked")
                # Update the appointment
                QUERY_UPDATE = '''
                UPDATE smaranvaidhya.appointment_data
                SET date_of_appointment = %s, slot_of_appointment = %s, consultancytype = %s, fees = %s
                WHERE appointment_id = %s
                RETURNING appointment_id
                '''
                cursor.execute(QUERY_UPDATE, (date, slot, consultancytype, fees, appointment_id))
                result = cursor.fetchone()
                print(f"DEBUG: Update result: {result}")
                if not result:
                        raise ValueError(f"Failed to update appointment ID {appointment_id}")
                conn.commit()
                return True
        except Exception as e:
                print(f"ERROR: Failed to reschedule appointment: {str(e)}")
                conn.rollback()
                raise Exception(f"Failed to reschedule appointment: {str(e)}")
        finally:
                cursor.close()
                conn.close()

def update_visited(appointment_id, visited):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = """
                UPDATE smaranvaidhya.appointment_data
                SET visited = %s
                WHERE appointment_id = %s
                RETURNING appointment_id
                """
                cursor.execute(QUERY, (visited, appointment_id))
                result = cursor.fetchone()
                print(f"DEBUG: Update visited result: {result}")
                if not result:
                        raise ValueError(f"Appointment ID {appointment_id} not found")
                conn.commit()
                return True
        except Exception as e:
                print(f"ERROR: Failed to update visited status: {str(e)}")
                conn.rollback()
                raise Exception(f"Failed to update visited status: {str(e)}")
        finally:
                cursor.close()
                conn.close()

def update_prescription_text(appointment_id, prescription):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = """
                UPDATE smaranvaidhya.appointment_data
                SET prescription = %s
                WHERE appointment_id = %s
                RETURNING appointment_id
                """
                print(f"DEBUG: Executing query with params: prescription='{prescription}', appointment_id={appointment_id}")
                cursor.execute(QUERY, (prescription, appointment_id))
                result = cursor.fetchone()
                print(f"DEBUG: Update prescription result: {result}")
                if not result:
                        raise ValueError(f"Appointment ID {appointment_id} not found")
                conn.commit()
                print(f"DEBUG: Committed update for appointment_id={appointment_id}")
                return True
        except Exception as e:
                print(f"ERROR: Failed to update prescription: {str(e)}")
                conn.rollback()
                raise Exception(f"Failed to update prescription: {str(e)}")
        finally:
                cursor.close()
                conn.close()