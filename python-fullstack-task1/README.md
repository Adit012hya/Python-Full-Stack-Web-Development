# User Management Web Application

## Project Description

The User Management Web Application is a simple web-based application developed using Flask and SQLite. The application allows users to add, view, and delete user records through a user-friendly interface. It demonstrates the implementation of basic database operations using Flask as the backend framework and SQLite as the database management system.

---

## Project Objectives

- To develop a web application using Flask.
- To perform Create, Read, and Delete operations on user data.
- To integrate SQLite database with a Python web application.
- To understand routing, form handling, and database management in Flask.

---

## Project Flow

### 1. Application Startup
- The Flask application starts when the user runs `app.py`.
- The application automatically checks whether the SQLite database and the `users` table exist.
- If the table does not exist, it is created automatically.

### 2. Add User
- The user enters their Name and Email in the input form.
- The application validates that both fields contain values.
- The entered information is stored in the SQLite database.

### 3. View Users
- The application retrieves all records from the database.
- The user details are displayed on the homepage.

### 4. Delete User
- A delete option is available for each user record.
- When the delete button is clicked, the corresponding record is removed from the database.
- The updated user list is displayed immediately.

---

## Technologies Used

### Backend
- Python
- Flask Framework

### Database
- SQLite

### Frontend
- HTML
- CSS
- Jinja2 Template Engine

### Python Libraries
- Flask
- sqlite3
- pathlib

---

## Database Structure

### Table: users

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| id | INTEGER | Primary Key |
| name | TEXT | Stores User Name |
| email | TEXT | Stores User Email |

---

## Features

- Add new user records
- Display all user records
- Delete existing user records
- Automatic database initialization
- Lightweight SQLite database integration
- Simple and user-friendly interface

---

## Project Files

```text
Project Folder
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
├── screenshots
│   ├── homepage.png
│   ├── add-user.png
│   ├── user-list.png
│   └── delete-user.png
└── templates
    └── index.html
```

---

## Installation and Execution

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

### Step 3: Open in Browser

Visit:

```text
http://127.0.0.1:5000
```

---

## Screenshots


### Add User Form

Insert the screenshot showing user details being entered.

<img width="1153" height="708" alt="Screenshot 2026-06-01 211200" src="https://github.com/user-attachments/assets/a9a46543-a9a5-4958-bdae-ca0dbf8e6535" />

---

### User List Display

Insert the screenshot showing the list of users stored in the database.

<img width="1152" height="932" alt="Screenshot 2026-06-01 211248" src="https://github.com/user-attachments/assets/fc0563bf-647d-4793-986a-1a2703c131ef" />

---

## Output

The application provides:

- A form for entering user details.
- Storage of user information in a SQLite database.
- Display of all stored user records.
- Deletion of user records.
- Automatic database management.

---

## Future Enhancements

- Edit and update user records.
- Add form validation using Flask-WTF.
- Implement user authentication and login.
- Improve UI using Bootstrap or React.
- Add search and filtering functionality.

---

## Conclusion

The User Management Web Application successfully demonstrates the integration of Flask and SQLite to perform database operations in a web environment. The project implements essential CRUD functionalities, including adding, viewing, and deleting user records. It serves as a foundational project for understanding web development concepts, database connectivity, and backend application development using Python.
