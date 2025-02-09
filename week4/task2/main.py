from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI()

# 掛載靜態文件 (CSS, JavaScript 等)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 設定 Jinja2 模板引擎
templates = Jinja2Templates(directory="templates")

# --- 路由 ---

# 首頁 (GET)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """渲染首頁 (登入表單)。"""
    return templates.TemplateResponse("index.html", {"request": request})

# 登入驗證 (POST, 使用 Body 參數)
@app.post("/signin")
async def signin(request: Request,
                 username: Annotated[str | None, Body()] = None,
                 password: Annotated[str | None, Body()] = None,
                 agree_terms: Annotated[bool | None, Body()] = None
                 ):
    """處理登入表單提交。使用Body驗證"""

    # 檢查是否勾選同意條款
    if not agree_terms:
        error_message = "Please check the checkbox first" 
        return RedirectResponse(url=f"/error?message={error_message}", status_code=307)

    # 檢查帳號和密碼是否皆未輸入
    if not username and not password:
        error_message = "請輸入帳號密碼" 
        return RedirectResponse(url=f"/error?message={error_message}", status_code=307)

    # 檢查使用者名稱或密碼是否為空
    if not username or not password:
        error_message = "請輸入帳號密碼" 
        return RedirectResponse(url=f"/error?message={error_message}", status_code=307)

    # 檢查使用者名稱和密碼是否都為 "test"
    if username == "test" and password == "test":
        return RedirectResponse(url="/member", status_code=307)  # 重定向到會員頁面
    else:
        error_message = "帳號或密碼不正確"  # 錯誤訊息 (中文)
        return RedirectResponse(url=f"/error?message={error_message}", status_code=307)

# 會員頁面 (GET) - 成功頁面
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    """渲染會員頁面 (成功頁面)。"""
    return templates.TemplateResponse("member.html", {"request": request})

# 錯誤頁面 (GET)
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    """渲染錯誤頁面，顯示錯誤訊息。"""
    message = request.query_params.get("message", "未知的錯誤")  # 獲取訊息，預設為 "未知的錯誤"
    return templates.TemplateResponse("error.html", {"request": request, "message": message})