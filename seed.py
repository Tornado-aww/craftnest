from sqlmodel import Session, select
from .models import Product

def seed_products(session: Session) -> None:
    """
    Seeds demo products once. If at least one product exists, does nothing.
    """
    if session.exec(select(Product)).first():
        return

    items = [
        # 1
        dict(
            title="Azure Blossom Pendant",
            slug="azure-blossom-pendant",
            price_usd=12.00,
            image_url="https://images.unsplash.com/photo-1509099836639-18ba1795216d?q=80&w=1200&auto=format&fit=crop",
            short_desc="Handmade resin pendant with a delicate blue petal motif.",
        ),
        # 2
        dict(
            title="Turquoise Charm",
            slug="turquoise-charm",
            price_usd=18.50,
            image_url="https://images.unsplash.com/photo-1551135049-8a33b5883816?q=80&w=1200&auto=format&fit=crop",
            short_desc="Bohemian-style turquoise charm for necklaces or bracelets.",
        ),
        # 3
        dict(
            title="Minimalist Silver Ring",
            slug="minimalist-silver-ring",
            price_usd=22.00,
            image_url="https://images.unsplash.com/photo-1521391406205-c83d71b6a626?q=80&w=1200&auto=format&fit=crop",
            short_desc="Sleek sterling-silver ring for everyday wear.",
        ),
        # 4
        dict(
            title="Ocean Blue Earrings",
            slug="ocean-blue-earrings",
            price_usd=19.00,
            image_url="https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?q=80&w=1200&auto=format&fit=crop",
            short_desc="Lightweight dangling earrings with ocean-blue stones.",
        ),
        # 5
        dict(
            title="Rose Quartz Bracelet",
            slug="rose-quartz-bracelet",
            price_usd=24.00,
            image_url="https://images.unsplash.com/photo-1522335789203-9c3f1e2fd0f1?q=80&w=1200&auto=format&fit=crop",
            short_desc="Calming rose quartz beads on a stretchy cord.",
        ),
        # 6
        dict(
            title="Vintage Copper Necklace",
            slug="vintage-copper-necklace",
            price_usd=28.00,
            image_url="https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=1200&auto=format&fit=crop",
            short_desc="Antique-finish copper chain with hand-forged pendant.",
        ),
        # 7
        dict(
            title="Leaf Stud Earrings",
            slug="leaf-stud-earrings",
            price_usd=14.00,
            image_url="https://images.unsplash.com/photo-1518544801976-3e7e32e78e2a?q=80&w=1200&auto=format&fit=crop",
            short_desc="Tiny botanical studs — subtle and elegant.",
        ),
        # 8
        dict(
            title="Pearl Drop Necklace",
            slug="pearl-drop-necklace",
            price_usd=29.00,
            image_url="https://images.unsplash.com/photo-1543294001-f7cd5d7fb516?q=80&w=1200&auto=format&fit=crop",
            short_desc="Classic drop pearl on a fine chain.",
        ),
        # 9
        dict(
            title="Matte Black Bracelet",
            slug="matte-black-bracelet",
            price_usd=17.00,
            image_url="https://images.unsplash.com/photo-1512428559087-560fa5ceab42?q=80&w=1200&auto=format&fit=crop",
            short_desc="Matte onyx beads — minimal, unisex design.",
        ),
        # 10
        dict(
            title="Golden Horizon Ring",
            slug="golden-horizon-ring",
            price_usd=26.00,
            image_url="https://images.unsplash.com/photo-1522335789203-9e8d0a6c8e9b?q=80&w=1200&auto=format&fit=crop",
            short_desc="Gold-tone ring with a slim horizon bar.",
        ),
        # 11
        dict(
            title="Emerald Cut Pendant",
            slug="emerald-cut-pendant",
            price_usd=27.50,
            image_url="https://images.unsplash.com/photo-1516637090014-cb1ab0d08fc7?q=80&w=1200&auto=format&fit=crop",
            short_desc="Glass crystal in emerald cut — bright and crisp.",
        ),
        # 12
        dict(
            title="Braided Leather Strap",
            slug="braided-leather-strap",
            price_usd=21.00,
            image_url="https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=1200&auto=format&fit=crop",
            short_desc="Hand-braided leather strap with metal clasp.",
        ),
    ]

    for data in items:
        session.add(Product(**data))
    session.commit()
