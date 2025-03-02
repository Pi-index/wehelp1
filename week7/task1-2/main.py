from fastapi import FastAPI, Request, Body, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
import secrets
import mysql.connector

app = FastAPI()

# Session 
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))

# 靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 模板
templates = Jinja2Templates(directory="templates")

# 直接使用提供的連線參數
conn = mysql.connector.connect(
    user="root",
    password="12345678",
    host="localhost",
    database="week6_db"
)
cursor = conn.cursor()

print("資料庫連線成功")

# --- 輔助函式 ---

def get_user_by_account(account: str):
    """依帳號擷取使用者。"""
    try:
        cursor.execute("SELECT * FROM members WHERE account = %s", (account,))
        user = cursor.fetchone()
        return user
    except :
        print("get_user_by_account 中的資料庫錯誤")
        return None

def get_user_by_id(user_id: int):
    """根據使用者 ID 取得使用者資訊。"""
    try:
        cursor.execute("SELECT * FROM members WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print("get_user_by_id 中的資料庫錯誤")
        return None


def get_all_messages():
    """取得所有留言，包含留言者名稱。"""
    try:
        cursor.execute("""
            SELECT messages.content, members.username
            FROM messages
            INNER JOIN members ON messages.member_id = members.id
            ORDER BY messages.id DESC
        """)
        messages = cursor.fetchall()
        return messages
    except mysql.connector.Error as err:
        print("get_all_messages 中的資料庫錯誤")
        return []

# --- 路由 ---

# 首頁 (GET)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 註冊 (POST)
@app.post("/signup")
async def signup(
    request: Request,
    username: Annotated[str, Form()],
    account: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    if get_user_by_account(account):
        error_message = "帳號已經存在"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    try:
        cursor.execute(
            "INSERT INTO members (username, account, password) VALUES (%s, %s, %s)",
            (username, account, password)
        )
        conn.commit()
        return RedirectResponse(url="/", status_code=303)
    except mysql.connector.Error as err:
        print("signup 中的資料庫錯誤")
        conn.rollback()
        error_message = "註冊失敗"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

# 登入 (POST)
@app.post("/signin")
async def signin(
    request: Request,
    account: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    user = get_user_by_account(account)
    if user:
        if user[3] == password:
            request.session["SIGNED_IN"] = True
            request.session["username"] = user[1]
            request.session["user_id"] = user[0]
            return RedirectResponse(url="/member", status_code=303)

    error_message = "帳號或密碼輸入錯誤"
    return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

# 會員頁面 (GET)
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if not request.session.get("SIGNED_IN", False):
        return RedirectResponse(url="/", status_code=303)

    username = request.session.get("username", "會員")
    messages = get_all_messages()
    return templates.TemplateResponse(
        "member.html",
        {"request": request, "username": username, "messages": messages}
    )

# 建立留言 (POST)
@app.post("/createMessage", response_class=RedirectResponse)
async def create_message(request: Request, content: Annotated[str, Form()]):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/", status_code=303)

    try:
        cursor.execute(
            "INSERT INTO messages (member_id, content) VALUES (%s, %s)",
            (user_id, content)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print("createMessage 中的資料庫錯誤")
        conn.rollback()
        error_message = "留言失敗"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    return RedirectResponse(url="/member", status_code=303)

# 登出 (GET)
@app.get("/signout")
async def signout(request: Request):
    request.session["SIGNED_IN"] = False
    request.session.pop("username", None)
    request.session.pop("user_id", None)
    return RedirectResponse(url="/", status_code=303)

# 錯誤頁面 (GET)
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    message = request.query_params.get("message", "未知的錯誤")
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get("/api/member")
async def get_member(username: str = Query(...)):
    print("接收到的查詢帳號:", username)  # 除錯用，確認接收到的參數

    user = get_user_by_account(username)
    print("資料庫查詢結果:", user)  # 除錯用，確認資料庫查詢結果

    if user:
        return JSONResponse(content={"data": {"id": user[0], "name": user[1], "username": user[2]}})
    else:
        return JSONResponse(content={"data": None})

@app.on_event("shutdown")
def shutdown_db_connection():
    """應用程式關閉時關閉資料庫連線"""
    if conn:
        conn.close()
        print("資料庫連線已關閉")