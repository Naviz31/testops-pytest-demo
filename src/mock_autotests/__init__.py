"""Демонстрационный домен для автономных автотестов."""

from .shop import (
    AccessPolicy,
    Cart,
    CheckoutService,
    EmptyCartError,
    Order,
    PaymentDeclinedError,
    Product,
)

__all__ = [
    "AccessPolicy",
    "Cart",
    "CheckoutService",
    "EmptyCartError",
    "Order",
    "PaymentDeclinedError",
    "Product",
]
