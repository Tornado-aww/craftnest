from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    slug: str = Field(index=True, unique=True)
    price_usd: float = 0.0
    image_url: str | None = None
    short_desc: str | None = None
