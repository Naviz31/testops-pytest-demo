from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import platform
import socket
from unittest.mock import Mock

import pytest

from mock_autotests.shop import Cart, OrderRepository, PaymentGateway, Product


@pytest.fixture(autouse=True)
def block_network_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    """Любая случайная попытка сетевого соединения немедленно ломает тест."""

    def network_is_forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("Network calls are forbidden in autonomous mock tests")

    monkeypatch.setattr(socket, "socket", network_is_forbidden)
    monkeypatch.setattr(socket, "create_connection", network_is_forbidden)


@pytest.fixture
def book() -> Product:
    return Product(sku="BOOK-001", name="Книга", price=Decimal("799.90"))


@pytest.fixture
def headphones() -> Product:
    return Product(sku="AUDIO-002", name="Наушники", price=Decimal("2500.00"))


@pytest.fixture
def cart(book: Product, headphones: Product) -> Cart:
    result = Cart()
    result.add(book, quantity=2)
    result.add(headphones)
    return result


@pytest.fixture
def payment_gateway() -> Mock:
    gateway = Mock(spec=PaymentGateway)
    gateway.charge.return_value = "payment-001"
    return gateway


@pytest.fixture
def order_repository() -> Mock:
    return Mock(spec=OrderRepository)


def pytest_sessionfinish(session: pytest.Session) -> None:
    """Добавляет сведения об автономном окружении к Allure-результатам."""
    config = session.config
    results_dir = config.getoption("allure_report_dir", default=None)
    if not results_dir:
        return

    output_dir = Path(results_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "environment.properties").write_text(
        "\n".join(
            (
                "test.type=mock",
                "network.calls=blocked",
                "framework=pytest",
                f"python.version={platform.python_version()}",
                f"os={platform.system()}",
                "",
            )
        ),
        encoding="utf-8",
    )
