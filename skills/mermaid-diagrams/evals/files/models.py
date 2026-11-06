from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def save(self, entity: T) -> None: ...

    @abstractmethod
    def find_by_id(self, id: int) -> T | None: ...


@dataclass
class Product:
    id: int
    name: str
    price: float


@dataclass
class LineItem:
    product: Product  # the same product appears in many orders
    quantity: int


@dataclass
class Order:
    id: int
    items: list[LineItem] = field(default_factory=list)  # owned: deleted with the order

    def total(self) -> float:
        return sum(i.product.price * i.quantity for i in self.items)


class OrderRepository(Repository[Order]):
    def save(self, entity: Order) -> None: ...

    def find_by_id(self, id: int) -> Order | None: ...
