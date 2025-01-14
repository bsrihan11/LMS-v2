# Project Name: LMS

## Description:
This project is a web application built with Flask as the backend framework and Vue.js as the frontend framework. It is a Library management system.

## Features:

### Flask Backend:
1. RESTful API endpoints for handling data requests.
2. Integration with database (SQLite).
3. Authentication and authorization mechanisms.

### Vue Frontend:
1. Component-based architecture for modular development.
2. Single Page Application (SPA) routing.
3. State management using Vuex.
4. API communication using fetch.

## Setup Instructions:

### Backend Setup:

1. Create a virtual environment: `python3 -m venv venv`.
2. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`.
4. Set up environment variables:
    - For Windows: `set FLASK_APP=app.py`.
5. When Redis is installed, navigate to WSL and run the command `redis-server` before starting the backend (Redis is a prerequisite for its functioning).
6. Run the backend using `flask run`.
7. To start Celery workers, run command `celery -A lms:celery worker --loglevel=info -P solo` for workers and `celery -A lms:celery beat --loglevel=info` for starting periodic tasks.

### Frontend Setup:

1. Navigate to the `lms-ui` directory.
2. Install dependencies: `npm install`.
3. Run the development server: `npm run serve`.

## Accessing the Application:

Once both backend and frontend servers are running, you can access the application through your web browser.
The default URL for the frontend server is [http://localhost:8080].

## Project Snippets:

![image_1](https://github.com/user-attachments/assets/811a8693-bd90-41ec-be85-2539f39807c8)

![image_2](https://github.com/user-attachments/assets/1b9c8efb-4a4f-4378-b7bc-ec7f9ed0a48e)

![image_3](https://github.com/user-attachments/assets/5744b722-3721-4c00-a4d2-a0d9fa034c0d)

![image_5](https://github.com/user-attachments/assets/537781df-e4fe-4f93-a6e0-aa0b7713e544)

![image_4](https://github.com/user-attachments/assets/e9b5f0d8-8808-441d-a1bd-50b6bf06bd71)
