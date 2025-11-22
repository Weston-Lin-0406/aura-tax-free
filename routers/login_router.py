from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pyfk import Auth, UserDao, UserStatus, authorization
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

template = Jinja2Templates(directory="resources/frontend")

@router.get("/", response_class=HTMLResponse, description="登入畫面")
async def index(request: Request):
    return template.TemplateResponse(request, "login.html")

@router.post("/", response_model=Auth, description="登入")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = UserDao().get_user(form.username, form.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password.")
    
    # 過濾 user 狀態
    if user.status == UserStatus.UNVERIFIED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User unverified.")
    if user.status == UserStatus.DISABLED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User disabled.")
    
    return authorization.gen_jwt(user)