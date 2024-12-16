from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from endpoints.tasks import router as tasks_router
from endpoints.lists import router as lists_router
from endpoints.files import router as files_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(tasks_router)
app.include_router(lists_router)
app.include_router(files_router)


@app.get("/", response_class=HTMLResponse)
async def get_tasks_view(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
