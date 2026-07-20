"""Небольшая предметная область, не выполняющая сетевых обращений."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Callable, Protocol


MONEY_STEP = Decimal("0.01")


class EmptyCartError(ValueError):
    """Оформление пустой корзины запрещено."""


class PaymentDeclinedError(RuntimeError):
    """Платёж отклонён тестовым платёжным шлюзом."""


@dataclass(frozen=True, slots=True)
class Product:
    sku: str
    name: str
    price: Decimal

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("SKU must not be empty")
        if self.price < 0:
            raise ValueError("Product price must not be negative")


@dataclass(slots=True)
class CartLine:
    product: Product
    quantity: int

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity


class Cart:
    def __init__(self) -> None:
        self._lines: dict[str, CartLine] = {}

    @property
    def lines(self) -> tuple[CartLine, ...]:
        return tuple(self._lines.values())

    @property
    def is_empty(self) -> bool:
        return not self._lines

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if product.sku in self._lines:
            self._lines[product.sku].quantity += quantity
        else:
            self._lines[product.sku] = CartLine(product, quantity)

    def total(self, discount_percent: Decimal = Decimal("0")) -> Decimal:
        if not Decimal("0") <= discount_percent <= Decimal("100"):
            raise ValueError("Discount must be between 0 and 100")

        subtotal = sum((line.subtotal for line in self._lines.values()), Decimal("0"))
        multiplier = Decimal("1") - discount_percent / Decimal("100")
        return (subtotal * multiplier).quantize(MONEY_STEP, rounding=ROUND_HALF_UP)


@dataclass(frozen=True, slots=True)
class Order:
    order_id: str
    customer_id: str
    amount: Decimal
    payment_id: str


class PaymentGateway(Protocol):
    def charge(self, customer_id: str, amount: Decimal) -> str:
        """Возвращает идентификатор успешного платежа."""


class OrderRepository(Protocol):
    def save(self, order: Order) -> None:
        """Сохраняет заказ."""


class CheckoutService:
    def __init__(
        self,
        payment_gateway: PaymentGateway,
        order_repository: OrderRepository,
        order_id_factory: Callable[[], str],
    ) -> None:
        self._payment_gateway = payment_gateway
        self._order_repository = order_repository
        self._order_id_factory = order_id_factory

    def checkout(
        self,
        cart: Cart,
        customer_id: str,
        discount_percent: Decimal = Decimal("0"),
    ) -> Order:
        if cart.is_empty:
            raise EmptyCartError("Cannot checkout an empty cart")
        if not customer_id.strip():
            raise ValueError("Customer ID must not be empty")

        amount = cart.total(discount_percent)
        payment_id = self._payment_gateway.charge(customer_id, amount)
        order = Order(
            order_id=self._order_id_factory(),
            customer_id=customer_id,
            amount=amount,
            payment_id=payment_id,
        )
        self._order_repository.save(order)
        return order


class AccessPolicy:
    _permissions = {
        "admin": frozenset({"orders:read", "orders:edit", "users:manage"}),
        "manager": frozenset({"orders:read", "orders:edit"}),
        "viewer": frozenset({"orders:read"}),
    }

    def is_allowed(self, role: str, permission: str) -> bool:
        return permission in self._permissions.get(role, frozenset())
