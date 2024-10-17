from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    id: int
    name: str
    qunatity: int
    price: float



@dataclass
class Order:
    id: int
    price: int
    name: str
    products: List[Product] = None

    def add_product(self, product: Product):
        self.products.append(product)
