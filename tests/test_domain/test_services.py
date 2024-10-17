import pytest
from domain.models import Product, Order


class TestProduct:
    def test_create_product(self):
        product = Product(id=1, name="Test Product", price=100.0)
        assert product.id == 1
        assert product.name == "Test Product"
        assert product.price == 100.0

    def test_change_price(self):
        product = Product(id=1, name="Test Product", price=100.0)
        product.change_price(150.0)
        assert product.price == 150.0

    def test_change_price_invalid(self):
        product = Product(id=1, name="Test Product", price=100.0)
        with pytest.raises(ValueError, match="Price must be greater than zero"):
            product.change_price(-50)


class TestOrder:
    def test_create_order(self):
        product1 = Product(id=1, name="Test Product 1", price=100.0)
        product2 = Product(id=2, name="Test Product 2", price=150.0)
        order = Order(id=1, products=[product1, product2])
        assert order.id == 1
        assert len(order.products) == 2

    def test_calculate_total(self):
        product1 = Product(id=1, name="Test Product 1", price=100.0)
        product2 = Product(id=2, name="Test Product 2", price=150.0)
        order = Order(id=1, products=[product1, product2])
        total = order.calculate_total()
        assert total == 250.0
