from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from Flask.server.database import OpenConn

app = FastAPI()

templates = Jinja2Templates(directory="Flask/templates")

app.mount("/static", StaticFiles(directory="Flask/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, q: str | None = None):
    with OpenConn() as conn:
        if q:
            search_item = f"%{q}%"
            posts = conn.execute(
                "SELECT * FROM finalProjects WHERE title LIKE ? OR description LIKE ?",
                (search_item, search_item)
            ).fetchall()
        else:
            posts = conn.execute("SELECT * FROM finalProjects").fetchall()

        return templates.TemplateResponse(
            "index.html",
            context={
                "request": request,
                "posts": posts,
                "q": q or ""
            }
        )