from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .db import init_db, get_session, engine
from .models import Product, Order, OrderItem
from .seed import seed_products
from .auth import admin_guard
from .schemas import CheckoutRequest

app = FastAPI(title="CraftNest")

# static & templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup() -> None:
    """Create tables and seed demo products on first run."""
    init_db()
    with Session(engine) as s:
        seed_products(s)


# ===================== PAGES =====================

@app.get("/", response_class=HTMLResponse)
def index(request: Request, session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})


@app.get("/product/{slug}", response_class=HTMLResponse)
def product_page(slug: str, request: Request, session: Session = Depends(get_session)):
    p = session.exec(select(Product).where(Product.slug == slug)).first()
    if not p:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("product.html", {"request": request, "p": p})


@app.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request):
    return templates.TemplateResponse("checkout.html", {"request": request})


@app.get("/checkout/success", response_class=HTMLResponse)
def checkout_success(request: Request):
    return templates.TemplateResponse("checkout_success.html", {"request": request})


# ===================== ADMIN (HTTP Basic) =====================

@app.get("/admin", response_class=HTMLResponse)
def admin_page(
    request: Request,
    session: Session = Depends(get_session),
    _: bool = Depends(admin_guard),
):
    products = session.exec(select(Product)).all()
    return templates.TemplateResponse("admin.html", {"request": request, "products": products})


@app.post("/admin/add")
def admin_add(
    title: str = Form(...),
    slug: str = Form(...),
    price_usd: float = Form(...),
    image_url: str = Form(...),
    short_desc: str = Form(...),
    session: Session = Depends(get_session),
    _: bool = Depends(admin_guard),
):
    session.add(
        Product(
            title=title,
            slug=slug,
            price_usd=price_usd,
            image_url=image_url,
            short_desc=short_desc,
        )
    )
    session.commit()
    return RedirectResponse(url="/admin", status_code=303)


@app.post("/admin/delete/{pid}")
def admin_delete(
    pid: int,
    session: Session = Depends(get_session),
    _: bool = Depends(admin_guard),
):
    p = session.get(Product, pid)
    if p:
        session.delete(p)
        session.commit()
    return RedirectResponse(url="/admin", status_code=303)


# ===================== API =====================

@app.get("/api/products")
def api_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products


@app.post("/api/checkout")
def api_checkout(payload: CheckoutRequest, session: Session = Depends(get_session)):
    if not payload.items:
        return JSONResponse({"error": "No items"}, status_code=400)

    total = sum(i.qty * i.unit_price for i in payload.items)

    order = Order(
        customer_name=payload.customer_name,
        email=payload.email,
        phone=payload.phone,
        currency=payload.currency,
        total_amount=total,
    )
    session.add(order)
    session.commit()

    for it in payload.items:
        session.add(
            OrderItem(
                order_id=order.id,
                product_id=it.product_id,
                qty=it.qty,
                unit_price=it.unit_price,
            )
        )
    session.commit()

    return {"ok": True, "order_id": order.id}
