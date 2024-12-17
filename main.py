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
    """
    Render the main tasks view.

    This endpoint serves the main HTML page for the application, rendering
    the "index.html" template. It provides the request context to the template
    for rendering dynamic content.

    Args:
        request (Request): The request object containing request data.

    Returns:
        TemplateResponse: An HTML response with the rendered template.
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
