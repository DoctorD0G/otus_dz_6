from typing import List

from domain.models import Product, Order
from domain.repositories import ProductRepository, OrderRepository


class WarehouseService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository):
        self.product_repo = product_repo
        self.order_repo = order_repo

    def create_product(self, name: str, quantity: int, price: float) -> Product:
        product = Product(name=name, quantity=quantity, price=price)
        self.product_repo.add(product)
        return product

    def create_order(self, products: List[Product]) -> List[Order]:
        order_list = []
        for product in products:
            order = Order(id=product.id, products=products, name=product.name, price=product.price)
            order_list.append(order)
            self.order_repo.add(order)
        return order_list
