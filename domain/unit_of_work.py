from abc import ABC, abstractmethod


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


class WarehouseUnitOfWork(UnitOfWork):
    def __init__(self, repository, session_factory):
        self.repository = repository
        self.session_factory = session_factory
        self.session = None
        self.committed = False

    def __enter__(self):
        self.session = self.session_factory()
        self.repository.session = self.session
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

