from fastapi import FastAPI, Request, Body, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
import secrets
import mysql.connector

app = FastAPI()

# Session Middleware
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# --- Database Connection and Initialization ---

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "week6_db"

def get_db_connection():
    """Gets a *new* database connection."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

def initialize_database():
    """Creates the database and table if they don't exist, and inserts the default user."""
    try:
        # Connect without specifying the database first.
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()

        # Now connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                account VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Check and insert default user
        cursor.execute("SELECT * FROM members WHERE account = 'test'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO members (username, account, password) VALUES (%s, %s, %s)",
                ("彭彭", "test", "test")
            )
            conn.commit()
            print("Default user 'test' created.")

    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")
        raise  # Re-raise to stop the application
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

initialize_database()  # Initialize on startup

# --- Helper Function ---

def get_user_by_account(account: str):
    """Retrieve a user by account."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE account = %s", (account,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Database error in get_user_by_account: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# --- Routes ---

# Home Page (GET)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """渲染首頁 (登入和註冊表單)。"""
    return templates.TemplateResponse("index.html", {"request": request})

# Sign-up (POST)
@app.post("/signup")
async def signup(
    request: Request,
    username: Annotated[str, Form()],
    account: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    """Handles signup form submission."""

    if get_user_by_account(account):
        error_message = "帳號已經存在"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO members (username, account, password) VALUES (%s, %s, %s)",
            (username, account, password)
        )
        conn.commit()
        return RedirectResponse(url="/", status_code=303)  # Redirect to home
    except mysql.connector.Error as err:
        print(f"Error inserting user: {err}")
        if conn:  # Check if connection exists
            conn.rollback()
        error_message = "註冊失敗"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Sign-in (POST)
@app.post("/signin")
async def signin(
    request: Request,
    account: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    """Handles signin form submission."""
    user = get_user_by_account(account)
    if user:
        if user[3] == password:  # Assuming password is the 4th column
            request.session["SIGNED_IN"] = True
            request.session["username"] = user[1]  # Assuming username is the 2nd column
            return RedirectResponse(url="/member", status_code=303)

    error_message = "帳號或密碼輸入錯誤"
    return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

# Member Page (GET)
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    """Renders the member page (success page)."""
    if not request.session.get("SIGNED_IN", False):
        return RedirectResponse(url="/", status_code=303)  # Redirect to home if not signed in

    username = request.session.get("username", "會員")  # Get username, default to "會員"
    return templates.TemplateResponse("member.html", {"request": request, "username": username})

# Sign-out (GET)
@app.get("/signout")
async def signout(request: Request):
    """Handles sign-out requests."""
    request.session["SIGNED_IN"] = False  # Set signed-in status to False
    request.session.pop("username", None)  # Remove username (if any)
    return RedirectResponse(url="/", status_code=303)  # Redirect to home page

# Error Page (GET)
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    """Renders the error page, displaying an error message."""
    message = request.query_params.get("message", "未知的錯誤")  # Get message, default to "未知的錯誤"
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.on_event("shutdown")
def shutdown_event():
    if 'conn' in globals() and conn:
        conn.close()
        print("Database connection closed.")