from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from typing import List
from domain.models import Product, Order
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository


class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass


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


class WarehouseUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None
        self.product_repository = None
        self.order_repository = None
        self.committed = False

    def __enter__(self):
        self.session = self.session_factory()
        self.product_repository = SQLProductRepository(self.session)
        self.order_repository = SQLOrderRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        elif not self.committed:
            self.commit()
        self.session.close()

    def commit(self):
        try:
            self.session.commit()
            self.committed = True
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self):
        self.session.rollback()


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: Session):
        self.session = session
        self.product_repository = SqlAlchemyProductRepository(self.session)
        self.order_repository = SqlAlchemyOrderRepository(self.session)
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        elif not self.committed:
            self.commit()
        self.session.close()

    def commit(self):
        try:
            self.session.commit()
            self.committed = True
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self):
        self.session.rollback()
