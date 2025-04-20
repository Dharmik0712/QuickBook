QuickBook
QuickBook is a web-based healthcare appointment booking system that connects patients with doctors. It enables patients to register, book appointments, manage prescriptions, and raise queries, while doctors can manage appointments and patient interactions. Built with Flask (Python), JavaScript (jQuery), and PostgreSQL, QuickBook ensures a fast, intuitive, and reliable experience.
Features

User Registration: Patients and doctors can register with personal details.
Appointment Booking: Book, cancel, or reschedule appointments with doctors.
Prescription Management: Doctors can upload and update prescriptions; patients can download them.
Query System: Patients can raise queries about appointments.
Doctor Dashboard: View and manage appointments and patient details.
Responsive UI: Built with Bootstrap and jQuery for a seamless experience.

Tech Stack

Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript (jQuery, Bootstrap)
Database: PostgreSQL
Deployment: Render or AWS Elastic Beanstalk
Other: Moment.js for date/time handling

Prerequisites

Python 3.8+
PostgreSQL 13+
Git
Render or AWS account for deployment

Installation

Clone the Repository
git clone https://github.com/your-username/quickbook.git
cd quickbook


Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies
pip install -r requirements.txt


Configure Environment VariablesCreate a .env file in the project root:
DATABASE_URL=postgresql://user:password@localhost:5432/quickbook
FLASK_ENV=development
SECRET_KEY=your-secret-key


Set Up the Database

Create a PostgreSQL database named quickbook.
Run the schema setup (e.g., from database.py or a provided SQL script).
Update DATABASE_URL with your PostgreSQL credentials.


Run the Application Locally
flask run

Access the app at http://localhost:5000.


Deployment
Deploying on Render

Create a Render AccountSign up at Render and create a new Web Service.

Connect GitHub Repository

Link your GitHub repository (quickbook) to Render.
Select the repository and branch (e.g., main).


Configure the Web Service

Region: Select Frankfurt (EU) for proximity to the UK.
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
Environment Variables:
DATABASE_URL: Your PostgreSQL database URL (e.g., Render’s PostgreSQL or external).
FLASK_ENV: production
SECRET_KEY: A secure random string.


Add a Render-managed PostgreSQL database (select Frankfurt region).


Deploy

Click Create Web Service. Render will build and deploy your app.
Access the app at the provided URL (e.g., https://quickbook.onrender.com).



Deploying on AWS Elastic Beanstalk

Set Up AWS AccountCreate an AWS account and install the AWS CLI (awscli) and EB CLI (awsebcli).

Initialize Elastic Beanstalk
eb init -p python-3.8 quickbook --region eu-west-2

Select Python 3.8 and the London (eu-west-2) region.

Configure EnvironmentCreate a .ebextensions/options.config file:
option_settings:
  aws:elasticbeanstalk:environment:process:default:
    Port: 8000
  aws:elasticbeanstalk:application:environment:
    DATABASE_URL: "postgresql://user:password@host:5432/quickbook"
    FLASK_ENV: "production"
    SECRET_KEY: "your-secret-key"


Deploy
eb create quickbook-env
eb deploy


Set Up RDS (PostgreSQL)

Create an RDS PostgreSQL instance in eu-west-2.
Update DATABASE_URL in .ebextensions/options.config with RDS credentials.



Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For issues or questions, open an issue on GitHub or contact dharmiksompura1212@gmail.com.
