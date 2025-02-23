from fastapi import FastAPI, Request, Body, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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

# --- 資料庫連線與初始化---

# 直接連線
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "week6_db"

# 初始化資料庫連線 (全域)
conn = None
cursor = None

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME  # 直接指定資料庫
    )
    cursor = conn.cursor()
    print("成功連接到資料庫。")

    # # 檢查並建立表格、插入預設使用者 (只在應用程式啟動時執行一次)
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS members (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         username VARCHAR(255) NOT NULL,
    #         account VARCHAR(255) UNIQUE NOT NULL,
    #         password VARCHAR(255) NOT NULL
    #     )
    # """)

    # cursor.execute("SELECT * FROM members WHERE account = 'test'")
    # if not cursor.fetchone():
    #     cursor.execute(
    #         "INSERT INTO members (username, account, password) VALUES (%s, %s, %s)",
    #         ("彭彭", "test", "test")
    #     )
    #     conn.commit()
    #     print("已建立預設使用者 'test'。")

except :
    print("資料庫連線或初始化錯誤")


# --- 輔助函式 (簡化) ---
def get_user_by_account(account: str):
    """依帳號擷取使用者 (使用全域連線)。"""
    # 使用cursor
    try:
        cursor.execute("SELECT * FROM members WHERE account = %s", (account,))
        user = cursor.fetchone()
        return user
    except :
        print("get_user_by_account 中的資料庫錯誤")
        return None

# --- 路由 ---

# 首頁 (GET)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """渲染首頁 (登入和註冊表單)。"""
    return templates.TemplateResponse("index.html", {"request": request})

# 註冊 (POST)
@app.post("/signup")
async def signup(
    request: Request,
    username: Annotated[str, Form()],
    account: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    """處理註冊表單提交。"""

    if get_user_by_account(account):
        error_message = "帳號已經存在"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    try:
        cursor.execute(
            "INSERT INTO members (username, account, password) VALUES (%s, %s, %s)",
            (username, account, password)
        )
        conn.commit()
        return RedirectResponse(url="/", status_code=303)  # 註冊成功後重定向到主頁
    except :
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
    """處理登入表單提交。"""
    user = get_user_by_account(account)
    if user:
        if user[3] == password:  # 假設密碼是第 4 個欄位
            request.session["SIGNED_IN"] = True
            request.session["username"] = user[1]  # 假設使用者名稱是第 2 個欄位
            return RedirectResponse(url="/member", status_code=303)

    error_message = "帳號或密碼輸入錯誤"
    return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

# 會員頁面 (GET)
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    """渲染會員頁面 (成功頁面)。"""
    if not request.session.get("SIGNED_IN", False):
        return RedirectResponse(url="/", status_code=303)  # 如果未登入，重定向到首頁

    username = request.session.get("username", "會員")  # 取得使用者名稱，預設為 "會員"
    return templates.TemplateResponse("member.html", {"request": request, "username": username})

# 登出 (GET)
@app.get("/signout")
async def signout(request: Request):
    """處理登出請求。"""
    request.session["SIGNED_IN"] = False  # 設定登入狀態為 False
    request.session.pop("username", None)  # 移除使用者名稱 (如果有的話)
    return RedirectResponse(url="/", status_code=303)  # 重定向到首頁

# 錯誤頁面 (GET)
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    """渲染錯誤頁面，顯示錯誤訊息。"""
    message = request.query_params.get("message", "未知的錯誤")  # 取得訊息，預設為 "未知的錯誤"
    return templates.TemplateResponse("error.html", {"request": request, "message": message})
    
@app.on_event("shutdown")
def shutdown_db_connection():
    """應用程式關閉時關閉資料庫連線"""
    if conn:
        conn.close()
        print("資料庫連線已關閉")