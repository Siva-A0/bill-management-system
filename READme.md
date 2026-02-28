# Bill Management System

Bill Management System is a Flask + SQLite web app to track personal bills with user authentication.

## Features

- User registration and login with hashed passwords
- Session-based authentication
- Add, view, pay, and delete bills
- Bill ownership enforced per logged-in user
- Payment timestamp (`paid_at`) saved when a bill is marked as paid

## Tech Stack

- Python
- Flask
- SQLite
- Werkzeug security helpers

## Project Structure

```text
bill-management-system/
|-- app.py
|-- bills.db
|-- requirements.txt
|-- static/
|   `-- style.css
`-- templates/
    |-- index.html
    |-- add_bill.html
    |-- login.html
    `-- register.html
```

## Requirements

- Python 3.10+
- `pip`

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
python app.py
```

3. Open in browser:

```text
http://127.0.0.1:5000
```

## Database Schema

`app.py` initializes the SQLite database automatically.

### `users`

- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `username` TEXT UNIQUE NOT NULL
- `password` TEXT NOT NULL

### `bills`

- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `user_id` INTEGER NOT NULL (FK -> `users.id`)
- `title` TEXT NOT NULL
- `amount` REAL NOT NULL
- `due_date` TEXT NOT NULL
- `status` TEXT DEFAULT `'Pending'`
- `paid_at` TEXT

## Routes

- `GET /register`, `POST /register`
- `GET /login`, `POST /login`
- `GET /logout`
- `GET /` (home/dashboard)
- `GET /add`, `POST /add`
- `POST /pay/<bill_id>`
- `POST /delete/<bill_id>`

## Notes

- The app currently uses a hardcoded Flask secret key in `app.py`. For production, use an environment variable.
- Error responses for login/register are plain text and can be improved with flash messages/templates.
