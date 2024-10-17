from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Product:
    name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    id: Optional[int] = None

    def change_price(self, new_price: float):
        if new_price <= 0:
            raise ValueError("Price must be greater than zero")
        self.price = new_price

    def reduce_quantity(self, amount: int):
        if amount > self.quantity:
            raise ValueError("Insufficient quantity in stock")
        self.quantity -= amount


@dataclass
class Order:
    id: Optional[int] = None
    price: Optional[float] = 0.0
    name: Optional[str] = ""
    products: Optional[List[Product]] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)
        self.price += product.price * product.quantity

    def calculate_total(self) -> float:
        return sum(product.price * product.quantity for product in self.products)

    def remove_product(self, product: Product):
        if product in self.products:
            self.products.remove(product)
            self.price -= product.price * product.quantity
        else:
            raise ValueError("Product not found in order")

    def clear_order(self):
        self.products.clear()
        self.price = 0.0
