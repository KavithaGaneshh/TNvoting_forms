# main.py
import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_db, engine, Base
from models import Response

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    district: str = Form(...),
    candidate: str = Form(...),
    comments: str = Form(""),
    db=Depends(get_db)
):
    response = Response(name=name, email=email, district=district, candidate=candidate, comments=comments)
    db.add(response)
    await db.commit()
    return templates.TemplateResponse("thankyou.html", {"request": request, "name": name})

@app.get("/responses")
async def view_responses(db=Depends(get_db)):
    result = await db.execute("SELECT * FROM responses")
    rows = result.fetchall()
    return {"responses": [dict(row._mapping) for row in rows]}
