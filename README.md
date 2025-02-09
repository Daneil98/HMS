
HOSPITAL MANAGEMENT SYSTEM WEB-APP

A Hospital Management web application enabling registered users and patients to schedule appointments with doctors, manage prescriptions through the pharmacy, and access tailored services. The platform incorporates role-based access control, ensuring doctors, pharmacists, and front desk staff have secure access to role-specific functionalities. Additionally, the application leverages Celery, RabbitMQ, and Docker to facilitate efficient asynchronous task processing, enhancing performance and scalability.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

Django, 
Python 3,
django rest framework,
Celery,
RabbitMQ.



## Run Locally

Clone the project

```bash
  git clone https://github.com/Daneil98/HMS
```

Go to the project directory

```bash
  cd HMS
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```


## Features

- User Authentication: Sign-up, login, and logout functionality with secure password storage.
- Role-based Access: Different access levels for doctors, patients, pharmacists and other roles.
- Search and Filter: Advanced search and filtering options for patient and drugs info for doctors and pharmacists respectively.
- Real Time updates: Real time updates about patient appointments, pharmacy inventory, patient profiles.

CELERY_BROKER_URL = ''
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

