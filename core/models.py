from dataclasses import dataclass
from datetime import date

@dataclass
class PriceRecord:
    product_id: str
    date: date
    price: float
    sales: int
    category_id: str

@dataclass
class PriceIndexResult:
    date: date
    category_id: str
    weighted_price: float
    price_index: float