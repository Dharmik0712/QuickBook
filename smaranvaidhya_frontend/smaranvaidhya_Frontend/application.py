from flask import Flask, render_template, request, url_for, jsonify, json, session, redirect, Response, send_file
from flask_cors import CORS, cross_origin
import json
import requests
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import io

app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True
app.secret_key = 'This_is_very_secret'
login_manager = LoginManager()
login_manager.init_app(app)
# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class User(UserMixin):
    def __init__(self, id, email, user_type):
        self.id = id
        self.email = email
        self.user_type = user_type

@login_manager.user_loader
def load_user(user_id):
    if 'user_id' in session:
        return User(session['user_id'], session['email'], session['user_type'])
    return None

def get_logged_in_user():
    user_login = False
    user_logged_in = None
    email = session.get('email')
    user_type = session.get('user_type')
    user_id = session.get('user_id')
    if email and user_type and user_id:
        user_login = True
        user_logged_in = {
            "email": email,
            "user_type": user_type,
            "user_id": user_id
        }
    return user_login, user_logged_in

@app.route('/Homepage')
def Homepage():
    user_login = get_logged_in_user()
    return render_template('homePage.html',user_login = user_login)

@app.route('/bookAppointment')
@login_required
def bookAppointment():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('bookAppointment.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/confirmBooking', methods=['GET', 'POST'])
@login_required
def confirmBooking():
    user_login, user_logged_in = get_logged_in_user()
    if request.method == 'POST':
        logger.debug("Received POST request to /confirmBooking")
        request_data = request.get_json()
        if not request_data:
            logger.error("No JSON data received")
            return jsonify({"status": "error", "message": "No data received"}), 400
        request_data['patient_id'] = session['user_id']
        url = get_service_url() + '/post_appointment_booking_data'
        response = post_api_function(url, request_data)
        if response and response.status_code == 200:
            logger.debug(f"Backend response: {response.json()}")
            return jsonify(response.json()), 200
        logger.error(f"Backend failed: {response.status_code if response else 'No response'}")
        return jsonify({"status": "error", "message": "Backend server error"}), 500
    # GET request: Render page with URL params
    logger.debug(f"Received GET request to /confirmBooking with args: {request.args}")
    return render_template('confirmBooking.html', user_login=user_login, user_type=user_logged_in['user_type'], user_info=user_logged_in['email'])

@app.route('/patientLoginPage')
def patientLoginPage():
    user_login, user_info = get_logged_in_user()
    user_id = session.get('user_id') if user_login else None
    return render_template('patientLoginPage.html', user_login=user_login, user_id=user_id,user_info=user_info)

@app.route('/aboutPage')
def aboutPage():
    user_login = get_logged_in_user()
    return render_template('aboutPage.html',user_login = user_login)

@app.route('/contactUsPage')
def contactUsPage():
    user_login = get_logged_in_user()
    return render_template('contactUsPage.html',user_login = user_login)

@app.route('/doctorsInfo')
@login_required
def doctorsInfo():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('doctorsInfo.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/doctorsView')
@login_required
def doctorsView():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('doctorView.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/Profile')
@login_required
def userProfile():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('profile.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/patientHistory')
@login_required
def patientHistory():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('patientHistory.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/raiseQuery')
@login_required
def raiseQuery():
    user_login, user_logged_in = get_logged_in_user()
    return render_template('querypage.html', user_login=user_login, user_type=user_logged_in['user_type'], user_info=user_logged_in['email'])

@app.route('/adminQueries')
@login_required
def adminQueries():
    user_login, user_logged_in = get_logged_in_user()
    if user_logged_in['user_type'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    return render_template('adminQueryView.html', user_login=user_login, user_type=user_logged_in['user_type'], user_info=user_logged_in['email'])

@app.route('/doctorProfile')
def doctorProfile():
    print("Session email:", session.get('email'))
    if 'email' not in session:
        return redirect('/login')
    return render_template('DoctorProfile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('patientLoginPage'))

def post_api_function(url, data):
    try:
        logger.debug(f"Posting to {url} with data: {data}")
        response = requests.post(url, json=data)
        return response
    except Exception as e:
        logger.error(f"Exception in post_api_function: {str(e)}")
        return None

def get_api_function(url):
    try:
        logger.debug(f"Getting from {url}")
        response = requests.get(url)
        return response
    except Exception as e:
        logger.error(f"Exception in get_api_function: {str(e)}")
        return None

def get_service_url():
    return 'http://127.0.0.1:2000'

@app.route('/attempt_to_login_for_user', methods=['POST'])
def attempt_to_login_for_user():
    url = get_service_url() + '/attempt_to_login_for_user'
    request_data = request.json
    response = requests.post(url, json=request_data)
    response_data = response.json()
    print("Login Response Data:", response_data)  
    if response_data["status"] == "Login Successful":
        if "user_id" not in response_data:
            return jsonify({"status": "error", "message": "User ID missing in response"}), 500
        session["email"] = request_data["email"]
        session["user_type"] = request_data["user_login_type"]
        session["user_id"] = response_data["user_id"]
        user = User(request_data["email"], response_data["user_id"], request_data["user_login_type"])
        login_user(user)
    else:
        session.clear()
    return jsonify(response_data)

@app.route('/save_user_registration_details', methods=['POST'])
def save_user_registration_details():
    url = get_service_url() + '/save_user_registration_details'
    request_data = request.json
    print(request_data)
    response = post_api_function(url, request_data)
    return response.json() if response else jsonify({"status": "error", "message": "Server error."})

@app.route('/post_contact_us_data', methods=['POST'])   
def post_contact_us_data():
    url = get_service_url() + '/post_contact_us_data'
    request_data = request.json
    print(request_data)
    response = post_api_function(url, request_data)
    return response.json() if response else jsonify({"status": "error", "message": "Server error."})

@app.route('/post_doctor_information_data', methods=['POST'])
def post_doctor_information_data():
    url = get_service_url() + '/post_doctor_information_data'
    form_data = request.form.to_dict()
    if 'doctor_image' in request.files:
        image_file = request.files['doctor_image']
        form_data['doctor_image'] = base64.b64encode(image_file.read()).decode('utf-8')
    response = post_api_function(url, form_data)
    return response.json() if response else jsonify({"status": "error", "message": "Server error."})

@app.route('/get_doctor_data', methods=['GET'])
def get_doctor_data():
    url = get_service_url() + '/get_doctor_data'
    response = get_api_function(url)
    return json.dumps(response.json())

@app.route('/post_appointment_booking_data', methods=['POST'])
def post_appointment_booking_data():
    logger.debug("Received POST request to /post_appointment_booking_data")
    if 'user_id' not in session:
        logger.warning("User not logged in")
        return jsonify({"status": "error", "message": "User not logged in"}), 401
    request_data = request.get_json()
    if not request_data:
        logger.error("No JSON data received")
        return jsonify({"status": "error", "message": "No data received"}), 400
    request_data['patient_id'] = session['user_id']
    url = get_service_url() + '/post_appointment_booking_data'
    response = post_api_function(url, request_data)
    if response:
        logger.debug(f"Backend response: {response.json()}")
        return jsonify(response.json()), response.status_code
    logger.error("Backend server error")
    return jsonify({"status": "error", "message": "Backend server error"}), 500

@app.route('/get_doctor_view_data', methods=['GET'])
def get_doctor_view_data():
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    doctor_id = user_logged_in["user_id"]
    if not doctor_id:
        return jsonify({'error': 'Doctor ID not found'}), 400
    url = get_service_url() + f'/get_doctor_view_data?doctor_id={doctor_id}'
    response = get_api_function(url)
    return jsonify(response.json())  

@app.route('/get_user_profile', methods=['GET'])
def get_user_profile():
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    user_id = user_logged_in.get("user_id")  
    if not user_id:
        return jsonify({'error': 'Patient ID not found'}), 400
    url = get_service_url() + f'/get_user_profile?user_id={user_id}'
    response = get_api_function(url)
    if response.status_code == 200:
        return jsonify(response.json())  
    else:
        return jsonify({'error': 'Failed to fetch user profile'}), response.status_code

@app.route('/update_user_profile/<user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    user_id = request.view_args.get("user_id")  
    data = request.get_json(silent=True)
    url = get_service_url() + f'/update_user_profile/{user_id}'
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({'error': response.json().get('detail', 'Update failed')}), response.status_code

@app.route('/get_user_history', methods=['GET'])
def get_user_history():
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    user_id = user_logged_in.get("user_id")  
    if not user_id:
        return jsonify({'error': 'Patient ID not found'}), 400
    url = get_service_url() + f'/get_user_history?user_id={user_id}'
    response = get_api_function(url)
    if response.status_code == 200:
        return jsonify(response.json())  
    else:
        return jsonify({'error': 'Failed to fetch user profile'}), response.status_code

def save_prescription(appointment_id, file_content, mime_type):
    try:
        url = get_service_url() + f'/upload_prescription/{appointment_id}'
        files = {'file': ('prescription', file_content, mime_type)}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            return "Success"
        else:
            return f"Failed: {response.json().get('data', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error saving prescription: {str(e)}")
        return f"Failed: {str(e)}"

@app.route('/upload_prescription/<int:appointment_id>', methods=['POST'])
def upload_prescription(appointment_id):
    try:
        if 'file' not in request.files:
            return jsonify({'data': 'No file provided'}), 400
        file = request.files['file']
        if not file.filename:
            return jsonify({'data': 'No file selected'}), 400
        allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
        if file.content_type not in allowed_types:
            return jsonify({'data': 'Invalid file type. Only JPEG, PNG, or PDF allowed.'}), 400
        file_content = file.read()
        result = save_prescription(appointment_id, file_content, file.content_type)
        if result == "Success":
            return jsonify({'data': 'Prescription uploaded successfully'}), 200
        else:
            return jsonify({'data': result}), 500
    except Exception as e:
        logger.error(f"Error uploading prescription: {str(e)}")
        return jsonify({'data': f'Error: {str(e)}'}), 500

@app.route('/download_prescription/<int:appointment_id>', methods=['GET'])
def download_prescription(appointment_id):
    try:
        url = get_service_url() + f'/download_prescription/{appointment_id}'
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return jsonify({'data': response.json().get('data', 'Error downloading prescription')}), response.status_code
        
        content_type = response.headers.get('content-type')
        content_disposition = response.headers.get('content-disposition', '')
        filename = content_disposition.split('filename=')[1].strip('"') if 'filename=' in content_disposition else f'prescription_{appointment_id}.pdf'
        
        return Response(
            response.content,
            mimetype=content_type,
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        logger.error(f"Error downloading prescription: {str(e)}")
        return jsonify({'data': f'Error: {str(e)}'}), 500

@app.route('/raise_query', methods=['POST'])
def raise_query():
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'No data provided'}), 400
    request_data['user_id'] = user_logged_in['user_id']
    url = get_service_url() + '/raise_query'
    response = post_api_function(url, request_data)
    if response and response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Failed to raise query'}), response.status_code if response else 500

@app.route('/get_queries', methods=['GET'])
def get_queries():
    user_login, user_logged_in = get_logged_in_user()
    if not user_login or user_logged_in['user_type'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    url = get_service_url() + '/get_queries'
    response = get_api_function(url)
    if response and response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Failed to fetch queries'}), response.status_code if response else 500

@app.route('/update_query_status/<int:query_id>', methods=['POST'])
def update_query_status(query_id):
    user_login, user_logged_in = get_logged_in_user()
    if not user_login or user_logged_in['user_type'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    request_data = request.get_json()
    if not request_data or 'status' not in request_data:
        return jsonify({'error': 'Status not provided'}), 400
    url = get_service_url() + f'/update_query_status/{query_id}'
    response = post_api_function(url, {'status': request_data['status']})
    if response and response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Failed to update query status'}), response.status_code if response else 500

@app.route('/get_doctor_profile', methods=['GET'])
def proxy_get_doctor_profile():
    email = request.args.get('email')
    if not email:
        logger.error("Email parameter missing in get_doctor_profile request")
        return {"detail": "Email parameter required"}, 400
    
    try:
        response = requests.get(f'http://localhost:2000/get_doctor_profile?email={email}', timeout=5)
        logger.info(f"FastAPI response - Status: {response.status_code}, Headers: {response.headers}, Body: {response.text}")
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Failed to connect to FastAPI: {str(e)}")
        return {"detail": "Backend server is unreachable. Please ensure FastAPI is running on port 2000."}, 503
    except requests.exceptions.HTTPError as e:
        logger.error(f"FastAPI returned an error: {str(e)}, Response: {response.text}")
        return {"detail": f"Backend error: {response.text}"}, response.status_code
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Invalid JSON from FastAPI: {str(e)}, Response: {response.text}")
        return {"detail": f"Failed to parse backend response: {str(e)}"}, 500
    except requests.exceptions.RequestException as e:
        logger.error(f"Error proxying to FastAPI: {str(e)}")
        return {"detail": f"Failed to connect to backend: {str(e)}"}, 500

@app.route('/update_doctor_profile/<doctor_id>', methods=['PUT'])
def proxy_update_doctor_profile(doctor_id):
    try:
        response = requests.put(
            f'http://localhost:2000/update_doctor_profile/{doctor_id}',
            json=request.get_json(),
            timeout=5
        )
        logger.info(f"FastAPI update response - Status: {response.status_code}, Headers: {response.headers}, Body: {response.text}")
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Failed to connect to FastAPI for update: {str(e)}")
        return {"detail": "Backend server is unreachable. Please ensure FastAPI is running on port 2000."}, 503
    except requests.exceptions.HTTPError as e:
        logger.error(f"FastAPI update returned an error: {str(e)}, Response: {response.text}")
        return {"detail": f"Backend error: {response.text}"}, response.status_code
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Invalid JSON from FastAPI update: {str(e)}, Response: {response.text}")
        return {"detail": f"Failed to parse backend response: {str(e)}"}, 500
    except requests.exceptions.RequestException as e:
        logger.error(f"Error proxying to FastAPI for update: {str(e)}")
        return {"detail": f"Failed to connect to backend: {str(e)}"}, 500

@app.route('/get_booked_slots', methods=['GET'])
def get_booked_slots():
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    response = requests.get(f'{get_service_url()}/get_booked_slots?doctor_id={doctor_id}&date={date}')
    return jsonify(response.json())

@app.route('/cancel_appointment/<int:appointment_id>', methods=['DELETE'])
def proxy_cancel_appointment(appointment_id):
    try:
        response = requests.delete(f'{get_service_url()}/cancel_appointment/{appointment_id}')
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reschedule_appointment/<int:appointment_id>', methods=['PUT'])
def proxy_reschedule_appointment(appointment_id):
    try:
        request_data = request.get_json()
        if not request_data:
            logger.error("No JSON data received for reschedule")
            return jsonify({'error': 'No data provided'}), 400
        required_fields = ['date', 'slot', 'consultancytype', 'fees']
        if not all(field in request_data for field in required_fields):
            logger.error(f"Missing required fields: {request_data}")
            return jsonify({'error': 'Missing required fields'}), 400
        url = f'{get_service_url()}/reschedule_appointment/{appointment_id}'
        response = requests.put(url, json=request_data)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        logger.error(f"Error proxying reschedule request: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error in reschedule: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/mark_appointment_visited/<int:appointment_id>', methods=['POST'])
def proxy_mark_appointment_visited(appointment_id):
    try:
        request_data = request.get_json()
        if not request_data or 'visited' not in request_data:
            logger.error("Missing 'visited' field in request body")
            return jsonify({'error': "Visited status not provided"}), 400
        logger.debug(f"Forwarding to FastAPI: /mark_appointment_visited/{appointment_id} with data: {request_data}")
        response = requests.post(
            f'{get_service_url()}/mark_appointment_visited/{appointment_id}',
            json=request_data
        )
        response.raise_for_status()
        logger.debug(f"FastAPI response: {response.json()}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as e:
        logger.error(f"FastAPI error: {str(e)}, Response: {e.response.text}")
        try:
            error_data = e.response.json()
            return jsonify(error_data), e.response.status_code
        except ValueError:
            return jsonify({'error': str(e)}), e.response.status_code
    except requests.RequestException as e:
        logger.error(f"Error proxying to FastAPI: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/update_prescription_text/<int:appointment_id>', methods=['POST'])
def proxy_update_prescription_text(appointment_id):
    try:
        request_data = request.get_json()
        if not request_data or 'prescription' not in request_data:
            logger.error("Missing 'prescription' field in request body")
            return jsonify({'error': "Prescription text not provided"}), 400
        logger.debug(f"Forwarding to FastAPI: /update_prescription_text/{appointment_id} with data: {request_data}")
        response = requests.post(
            f'{get_service_url()}/update_prescription_text/{appointment_id}',
            json=request_data
        )
        response.raise_for_status()
        logger.debug(f"FastAPI response: {response.json()}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as e:
        logger.error(f"FastAPI error: {str(e)}, Response: {e.response.text}")
        try:
            error_data = e.response.json()
            return jsonify(error_data), e.response.status_code
        except ValueError:
            return jsonify({'error': str(e)}), e.response.status_code
    except requests.RequestException as e:
        logger.error(f"Error proxying to FastAPI: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=7078)