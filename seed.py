from sqlmodel import select, Session
from models import Product


def ensure_seed(session: Session):
    # если уже есть товары — ничего не делаем
    count = session.exec(select(Product)).first()
    if count:
        return

    items = [
        Product(
            title="Azure Blossom Pendant",
            slug="azure-blossom-pendant",
            price_usd=12.00,
            image_url="https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3",
            short_desc="Handmade resin pendant with a delicate blue petal motif.",
        ),
        Product(
            title="Turquoise Charm",
            slug="turquoise-charm",
            price_usd=18.50,
            image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff",
            short_desc="Bohemian-style turquoise charm for necklaces or bracelets.",
        ),
        Product(
            title="Minimalist Silver Ring",
            slug="minimalist-silver-ring",
            price_usd=22.00,
            image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30",
            short_desc="Sleek sterling-silver ring for everyday wear.",
        ),
    ]
    session.add_all(items)
    session.commit()
