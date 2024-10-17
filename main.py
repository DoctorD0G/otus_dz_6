from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.services import WarehouseService
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL


engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    uow = SqlAlchemyUnitOfWork(session)
    warehouse_service = WarehouseService(product_repo, order_repo)

    with uow:
        new_product = warehouse_service.create_product(name="test1", quantity=1, price=100)
        uow.commit()
        print(f"Created product: {new_product}")

        retrieved_product = product_repo.get(new_product.id)
        print(f"Retrieved product: {retrieved_product}")

        all_products = product_repo.list()
        print(f"All products: {all_products}")

        new_order = warehouse_service.create_order([retrieved_product])
        uow.commit()
        print(f"Created order: {new_order}")


if __name__ == "__main__":
    main()
