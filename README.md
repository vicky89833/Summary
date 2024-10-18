# Report Generation
 
Python Assignment - Django File Upload and Report Generation
This project is developed as part of a Django intern role assignment. It is a web-based application that allows users to upload an Excel/CSV file, generates a summary report of the uploaded data, and sends the report via email.

Features
File Upload: Users can upload an Excel or CSV file via a web interface.
Data Summary: The application generates a summary report for the uploaded data, including row count, column count, column names, and basic statistics.
Email Report: The generated summary report is emailed to tech@themedius.ai with the subject "Python Assignment - {Your Name}".
Git Branch: The code is pushed to a Git branch named after the developer.
Deployment: The project is deployed on an open-source server (like Heroku).
Prerequisites
To run this project locally, you’ll need the following installed:

Python 3.x
Django 4.x
Pandas
Gunicorn (for deployment)
Git
Email Configuration
Before running the project, make sure to configure the email settings in settings.py with valid SMTP details.

python
Copy code
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_password'
Installation
Clone the Repository:

bash
Copy code
git clone <repository-url>
cd <repository-folder>
Create and activate a virtual environment:

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Run Migrations:

bash
Copy code
python manage.py migrate
Run the Server:

bash
Copy code
python manage.py runserver
Visit http://127.0.0.1:8000 in your browser to access the application.

Usage
Upload an Excel/CSV file through the provided form on the web page.
The system will process the file and generate a summary report.
The summary report will be sent via email to tech@themedius.ai with the subject: Python Assignment - Vicky Kumar Maurya.
