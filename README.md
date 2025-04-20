QuickBook
QuickBook is a web-based healthcare appointment booking system that connects patients with doctors. It allows users to register, book appointments, manage prescriptions, and raise queries, with a user-friendly interface powered by Flask (Python) and jQuery (JavaScript).
Features

User Registration: Patients and doctors can register with personal details.
Appointment Booking: Book, cancel, or reschedule appointments with doctors.
Prescription Management: Doctors can upload prescriptions; patients can download them.
Query System: Patients can raise queries about appointments.
Doctor Dashboard: View and manage appointments and patient details.
Responsive UI: Built with Bootstrap and jQuery for a seamless experience.

Tech Stack

Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript (jQuery, Bootstrap)
Database: MySQL
Deployment: Render or AWS Elastic Beanstalk
Other: Moment.js for date/time handling

Prerequisites

Python 3.8+
MySQL 8.0+
Git
Render or AWS account for deployment

Installation

Clone the Repository
git clone https://github.com/your-username/QuickBook.git
cd QuickBook


Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies
pip install -r requirements.txt


Configure Environment VariablesCreate a .env file in the project root:
DATABASE_URL=mysql+mysqlconnector://user:password@localhost/QuickBook
FLASK_ENV=development
SECRET_KEY=your-secret-key


Set Up the Database

Create a MySQL database named QuickBook.
Run the schema setup (e.g., from database.py or a provided SQL script).
Update DATABASE_URL with your MySQL credentials.


Run the Application Locally
flask run

Access the app at http://localhost:5000.


Deployment
Deploying on Render

Create a Render AccountSign up at Render and create a new Web Service.

Connect GitHub Repository

Link your GitHub repository (QuickBook) to Render.
Select the repository and branch (e.g., main).


Configure the Web Service

Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
Environment Variables:
DATABASE_URL: Your MySQL database URL (e.g., hosted on Render or another provider).
FLASK_ENV: production
SECRET_KEY: A secure random string.


Add a Render-managed MySQL database if needed (Render provides this option).


Deploy

Click Create Web Service. Render will build and deploy your app.
Access the app at the provided URL (e.g., https://QuickBook.onrender.com).



Deploying on AWS Elastic Beanstalk

Set Up AWS AccountCreate an AWS account and install the AWS CLI (awscli).

Initialize Elastic Beanstalk
eb init -p python-3.8 QuickBook --region us-east-1

Select Python 3.8 and your AWS region.

Configure EnvironmentCreate a .ebextensions/options.config file:
option_settings:
  aws:elasticbeanstalk:environment:process:default:
    Port: 8000
  aws:elasticbeanstalk:application:environment:
    DATABASE_URL: "mysql+mysqlconnector://user:password@host/QuickBook"
    FLASK_ENV: "production"
    SECRET_KEY: "your-secret-key"


Deploy
eb create QuickBook-env
eb deploy

Access the app at the provided Elastic Beanstalk URL.

Set Up RDS (MySQL)

Create an RDS MySQL instance in AWS.
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
For issues or questions, open an issue on GitHub or contact [your-email@example.com].
