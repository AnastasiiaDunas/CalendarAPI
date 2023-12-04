
# Calendar API

## Description
The Calendar API is a Django-based RESTful API designed for managing calendar events and invitations. It provides functionalities for user management, event creation, updating, deletion, and invitations.

## Installation

### Prerequisites
- Python 3.x
- Django
- Django REST Framework
- Other dependencies listed in `requirements.txt`

### Cloning the Repository
To clone the repository from GitHub and set up the project on your local machine, follow these steps:
1. Navigate to the main page of the repository on GitHub.
2. Above the list of files, click the green button labeled "Code".
3. To clone the repository using HTTPS, under "Clone with HTTPS", click the clipboard icon. To clone using an SSH key, including a certificate issued by your organization's SSH certificate authority, click Use SSH, then click the clipboard icon. To clone a repository using GitHub CLI, click Use GitHub CLI, then click the clipboard icon.
4. Open your terminal.
5. Change the current working directory to the location where you want the cloned directory.
6. Type `git clone`, and then paste the URL you copied earlier.
   ```
   git clone git@github.com:AnastasiiaDunas/CalendarAPI.git
   ```
7. Press `Enter` to create your local clone.

### Setting Up
After cloning the repository, install the required packages:
```bash
pip install -r requirements.txt
```

## Running the API
To run the API server, navigate to the project directory and execute:
```bash
python manage.py runserver
```

## API Endpoints
Below are the key API endpoints available:

- User Signup
  - **Method:** POST
  - **Endpoint:** `/signup/`
  - **Body:** `{"username": "your_username", "password": "your_password", "email": "your_email@example.com"}`

- User Login
  - **Method:** POST
  - **Endpoint:** `/login/`
  - **Body:** `{"username": "your_username", "password": "your_password"}`

- Create Event
  - **Method:** POST
  - **Endpoint:** `/event/create/`
  - **Body:** `{"title": "Event Title", "description": "Event Description", "date": "YYYY-MM-DD HH:MM"}`

- Update Event
  - **Method:** PUT
  - **Endpoint:** `/event/update/{pk}/`
  - **Body:** `{"title": "New Event Title", "description": "New Description", "date": "YYYY-MM-DD HH:MM"}`

- Delete Event
  - **Method:** DELETE
  - **Endpoint:** `/event/delete/{pk}/`

- Invite to Event
  - **Method:** POST
  - **Endpoint:** `/event/invite/`
  - **Body:** `{"event_id": event_id, "invitee_id": user_id}`

- View Created Events
  - **Method:** GET
  - **Endpoint:** `/events/created/`

- View Events User is Invited To
  - **Method:** GET
  - **Endpoint:** `/events/invited/`

- View Users Invited to an Event
  - **Method:** GET
  - **Endpoint:** `/event/invited-users/{event_id}/`

## Swagger Documentation
For a detailed overview of API endpoints, request parameters, and response formats, please refer to the Swagger documentation.

## Testing
Execute the following command to run tests:
```bash
python manage.py test
```
