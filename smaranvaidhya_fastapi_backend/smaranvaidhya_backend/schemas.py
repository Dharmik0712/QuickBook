from pydantic import BaseModel
from datetime import date,time
from typing import List, Optional

class UserRegistration(BaseModel):
    first_name : str
    last_name : str
    date_of_birth : date
    gender : str
    email : str
    phone_number : int
    password : str
    state : str
    city : str 
    zip_code : int
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class LoginForUser(BaseModel):
    user_login_type : str
    email : str
    password : str
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class ContactData(BaseModel):
    full_name : str
    email : str
    message : str
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class DoctorRegistration(BaseModel):
    first_name: str 
    last_name: str 
    date_of_birth: date
    gender: str 
    email: str
    phone_number: str 
    state: str 
    city: str 
    zip_code: int 
    clinic_hospital: str 
    specialist: str
    available_from: time       
    available_to: time         
    time_per_patient: int 
    max_appointments: int 
    highest_qualification: str
    years_of_experience: int   
    in_person_fee: int  
    video_fee: int       
    phone_fee: int       
    emergency_availability: str   
    emergency_contact: str  
    doctor_image: str  
    hospital_clinic_address: str 
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str
    upi_id: str

    class Config:
        from_attributes = True #orm_mode = True
        arbitrary_types_allowed = True

class AppointmentData(BaseModel):
    patient_id: str
    doctor_id: str
    patient_name: str
    contact_number: int
    gender: str
    age: int
    reason_for_visit: str
    pre_existing_conditions: str
    current_medications: str
    allergies: str
    date_of_appointment: date  
    slot_of_appointment: time  
    mode_of_payment: str
    consultancytype: str  
    fees: int  

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class UpdateUserProfileSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: int
    password: str
    state: str
    city: str 
    zip_code: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class QueryData(BaseModel):
    user_id: str
    appointment_id: int
    subject: str
    query: str
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class QueryStatusUpdate(BaseModel):
    status: str
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class DoctorProfileUpdate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    state: str
    city: str
    zip_code: str
    clinic_hospital: str
    specialist: str
    available_days: str
    available_from: str
    available_to: str
    time_per_patient: int
    max_appointments: int
    highest_qualification: str
    years_of_experience: int
    in_person_fee: int
    video_fee: int
    phone_fee: int
    emergency_availability: str
    emergency_contact: str
    hospital_clinic_address: str
    upi_id: str
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class RescheduleData(BaseModel):
    date: str
    slot: str
    consultancytype: str
    fees: int
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class VisitedRequest(BaseModel):
    visited: bool
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class PrescriptionRequest(BaseModel):
    prescription: str
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True