import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from domain.models import Product, Order

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session():
    session = SessionFactory()
    yield session
    session.close()


@pytest.fixture
def product_repo(session):
    return SqlAlchemyProductRepository(session)


@pytest.fixture
def order_repo(session):
    return SqlAlchemyOrderRepository(session)


class TestSqlAlchemyProductRepository:
    def test_add_product(self, product_repo):
        product = Product(name="Test Product", quantity=10, price=99.99)
        product_repo.add(product)
        assert product.id is not None

    def test_get_product(self, product_repo):
        product = product_repo.get(1)
        assert product is not None
        assert product.name == "Test Product"

    def test_list_products(self, product_repo):
        products = product_repo.list()
        assert len(products) > 0


class TestSqlAlchemyOrderRepository:
    def test_add_order(self, order_repo):
        product = Product(name="Test Product", quantity=10, price=99.99)
        order = Order(name="Test Order", products=[product])
        order_repo.add(order)
        assert order.id is not None

    def test_get_order(self, order_repo):
        order = order_repo.get(1)
        assert order is not None
        assert order.name == "Test Order"

    def test_list_orders(self, order_repo):
        orders = order_repo.list()
        assert len(orders) > 0
