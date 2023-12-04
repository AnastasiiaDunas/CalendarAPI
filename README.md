# CalendarAPI

Welcome to the CalendarAPI! This Django REST Framework project provides functionality for managing events and user authentication.

## Prerequisites

Before you begin, ensure you have the following software installed on your machine:

- Python (version 3.6 or later)
- PostgreSQL

## Getting Started

1. **Clone the Repository:**

    ```bash
    git clone git@github.com:AnastasiiaDunas/CalendarAPI.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd CalendarAPI\calendarapi
    ```

3. **Create and Activate a Virtual Environment (Optional but Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Configure Database:**

    - Create a PostgreSQL database.
    - Update the database settings in `events/settings.py` with your database configuration.

6. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

    The API should now be running at http://localhost:8000/.

## API Endpoints

Here are the main API endpoints provided by the Django Events API:

- **User Signup:**
  - Endpoint: `/api/user/signup/`
  - Method: `POST`

- **User Login:**
  - Endpoint: `/api/user/login/`
  - Method: `POST`

- **Get User Invitations:**
  - Endpoint: `/api/user/{token}/invitations/`
  - Method: `GET`

- **Create an Event:**
  - Endpoint: `/api/events/{token}/create/`
  - Method: `POST`

- **Get User Events:**
  - Endpoint: `/api/events/{token}/list/`
  - Method: `GET`

- **Update an Event:**
  - Endpoint: `/api/events/{token}/{event_title}/update/`
  - Method: `PUT`

- **Delete an Event:**
  - Endpoint: `/api/events/{token}/{event_title}/delete/`
  - Method: `DELETE`

- **Invite a User to an Event:**
  - Endpoint: `/api/events/{token}/{event_title}/invite/`
  - Method: `POST`

- **Get Users Invited to an Event:**
  - Endpoint: `/api/events/{event_title}/users/`
  - Method: `GET`

