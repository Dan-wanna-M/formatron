from typing import Optional

from attr import dataclass
from formatron.schemas.pydantic import ClassSchema


class Address(ClassSchema):
    street: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str

class LinkedList(ClassSchema):
    value: int
    next: Optional["LinkedList"]

class OrderItem(ClassSchema):
    product_id: int
    variant_id: int
    quantity: int
    price: float

class Customer(ClassSchema):
    id: int
    name: str
    phone: str
    address: str
    loyalty_points: int = 0
    is_active: bool = True

class Order(ClassSchema):
    id: int
    customer: Customer
    items: list[OrderItem]
    total_amount: float
    status: str

@dataclass
class BenchResult:
    t1:int
    s1:float
    t2:int
    s2:float

@dataclass
class Context:
    index:int
    tokens:int