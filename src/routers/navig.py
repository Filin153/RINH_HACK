from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=['First'],
)

tmp = Jinja2Templates(directory="src/static")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return tmp.TemplateResponse("index.html", {"request": request})

@router.get("/main", response_class=HTMLResponse)
async def index(request: Request):
    return tmp.TemplateResponse("main.html", {"request": request})