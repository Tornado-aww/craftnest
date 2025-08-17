from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlmodel import select, Session
from typing import List, Optional
import os

from db import init_db, get_session
from models import Product
from auth import admin_guard
from seed import ensure_seed

app = FastAPI(title="CraftNest")

# static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def _startup():
    init_db()
    with get_session() as s:
        ensure_seed(s)


# ----------------- PAGES -----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_session)):
    products = session.exec(select(Product).order_by(Product.id)).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "products": products, "currency": "USD"},
    )


@app.get("/product/{slug}", response_class=HTMLResponse)
def product_page(slug: str, request: Request, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.slug == slug)).first()
    if not product:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "product.html",
        {"request": request, "p": product, "currency": "USD"},
    )


@app.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request):
    return templates.TemplateResponse("checkout.html", {"request": request})


@app.get("/checkout/success", response_class=HTMLResponse)
def checkout_success(request: Request):
    return templates.TemplateResponse("checkout_success.html", {"request": request})


# ----------------- API -----------------
@app.get("/api/products", response_model=List[Product])
def api_products(session: Session = Depends(get_session)):
    return session.exec(select(Product).order_by(Product.id)).all()


# ----------------- ADMIN -----------------
@app.get("/admin", response_class=HTMLResponse, name="admin")
def admin(request: Request, user=Depends(admin_guard), session: Session = Depends(get_session)):
    products = session.exec(select(Product).order_by(Product.id)).all()
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "products": products, "user": user},
    )


@app.post("/admin/add", name="admin_add")
def admin_add(
    title: str = Form(...),
    slug: str = Form(...),
    price_usd: float = Form(...),
    image_url: str = Form(...),
    short_desc: str = Form(...),
    user=Depends(admin_guard),
    session: Session = Depends(get_session),
):
    exists = session.exec(select(Product).where(Product.slug == slug)).first()
    if exists:
        # просто вернёмся на /admin — в реале можно показать флэш-сообщение
        return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)

    p = Product(title=title, slug=slug, price_usd=price_usd,
                image_url=image_url, short_desc=short_desc)
    session.add(p)
    session.commit()
    return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)


@app.post("/admin/delete/{pid}", name="admin_delete")
def admin_delete(pid: int, user=Depends(admin_guard), session: Session = Depends(get_session)):
    p = session.get(Product, pid)
    if p:
        session.delete(p)
        session.commit()
    return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)
