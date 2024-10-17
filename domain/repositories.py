from abc import ABC, abstractmethod
from typing import List
from .models import Product, Order


class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        pass

    @abstractmethod
    def get(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def list(self) -> List[Product]:
        pass


class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order):
        pass

    @abstractmethod
    def get(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def list(self) -> List[Order]:
        pass


class SQLProductRepository(ProductRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product: Product):
        self.session.add(product)

    def get(self, product_id: int) -> Product:
        return self.session.query(Product).filter_by(id=product_id).first()

    def list(self) -> List[Product]:
        return self.session.query(Product).all()


class SQLOrderRepository(OrderRepository):
    def __init__(self, session):
        self.session = session

    def add(self, order: Order):
        self.session.add(order)

    def get(self, order_id: int) -> Order:
        return self.session.query(Order).filter_by(id=order_id).first()

    def list(self) -> List[Order]:
        return self.session.query(Order).all()
