from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 設定模板引擎
templates = Jinja2Templates(directory="templates")

# 首頁 (GET 請求)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """渲染首頁 (登入表單)。"""
    return templates.TemplateResponse("index.html", {"request": request})

# 登入處理 (GET 請求) - 僅檢查同意條款
@app.get("/login")
async def login(request: Request):
    """處理登入請求 (僅檢查同意條款)。"""
    username = request.query_params.get("username")
    agree_terms = request.query_params.get("agree_terms") == "on"  # 檢查複選框

    if not agree_terms:
        # 如果未勾選同意條款，重新渲染 index.html 並顯示錯誤訊息
        return templates.TemplateResponse("index.html", {"request": request, "error": "請勾選同意條款"})

    # 如果勾選了同意條款，直接渲染會員頁面 (無使用者名稱/密碼驗證)
    return templates.TemplateResponse("member.html", {"request": request, "username":username})

# 會員頁面 (GET 請求) - 成功頁面
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    """渲染會員頁面 (成功頁面)。"""
    username = request.query_params.get("username")
    return templates.TemplateResponse("member.html", {"request": request, "username":username})

# 錯誤頁面 (GET 請求)
@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request):
    """渲染錯誤頁面。"""
    message = request.query_params.get("message", "發生錯誤")
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

# 掛載靜態文件 (CSS, JavaScript 等)
app.mount("/static", StaticFiles(directory="static"), name="static")