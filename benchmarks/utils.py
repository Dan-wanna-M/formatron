import gc
import json
from dataclasses import dataclass
from typing import Optional

import torch
from formatron.schemas.pydantic import ClassSchema
from lmformatenforcer import JsonSchemaParser


class Address(ClassSchema):
    street: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str

address_lfe = JsonSchemaParser(Address.model_json_schema())

class LinkedList(ClassSchema):
    value: int
    next: Optional["LinkedList"]

linked_list_lfe = JsonSchemaParser(LinkedList.model_json_schema())

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

order_lfe = JsonSchemaParser(Order.model_json_schema())

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

def log(func_name:str, data:BenchResult,f):
    a = f"{func_name} generated {data.t1} tokens with {data.t1 / data.s1} tps (with warm up)\n"
    b = (f"{func_name} unconstrained generated {data.t2} tokens with"
          f" {data.t2 / data.s2} tps\n")
    c = f"{func_name} overhead per token: {((data.s1 / data.t1) - (data.s2 / data.t2)) * 1000:.2f} ms\n"
    print(a)
    print(b)
    print(c)
    f.writelines([a,b,c])


def load_address()->list[str]:
    return json.load(open("address.json"))["sentences"]

def load_linkedlist()->list[str]:
    return json.load(open("linkedlist.json"))["sentences"]

def load_orders()->list[str]:
    return json.load(open("orders.json"))["orders"]

def force_gc():
    torch.cuda.empty_cache()
    gc.collect()