from decimal import Decimal
from unittest.mock import Mock

import allure
import pytest

from mock_autotests.shop import Cart, CheckoutService, Product


pytestmark = [
    pytest.mark.allure_label("naviz31", label_type="owner"),
    pytest.mark.allure_label("unit", label_type="layer"),
    pytest.mark.allure_label("payment", label_type="component"),
    pytest.mark.allure_label("Моковый интернет-магазин", label_type="parentSuite"),
    pytest.mark.allure_label("Оплата", label_type="suite"),
]


@allure.id("20")
@allure.testcase(
    "https://htcconf.qatools.cloud/project/1/test-cases/20",
    "ТестОпс: тест-кейс №20 «Провести платеж»",
)
@allure.epic("Моковый интернет-магазин")
@allure.feature("Оплата")
@allure.story("Проведение платежа")
@allure.title("Провести платеж за товар «{product_name}»")
@allure.description(
    "Автоматизация ручного тест-кейса ТестОпс №20. "
    "Проверяет успешную оплату товара и сохранение оплаченного заказа."
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "unit", "offline", "testops-linked")
@pytest.mark.smoke
@pytest.mark.unit
@pytest.mark.parametrize(
    ("product_name", "sku", "price"),
    [
        pytest.param("Молоко", "FOOD-MILK-001", Decimal("99.90"), id="молоко"),
        pytest.param("Яйцо", "FOOD-EGG-001", Decimal("129.90"), id="яйцо"),
    ],
)
def test_payment_for_product_is_completed(
    product_name: str,
    sku: str,
    price: Decimal,
    payment_gateway: Mock,
    order_repository: Mock,
) -> None:
    allure.dynamic.parameter("Товар", product_name)
    product = Product(sku=sku, name=product_name, price=price)
    cart = Cart()
    service = CheckoutService(
        payment_gateway=payment_gateway,
        order_repository=order_repository,
        order_id_factory=lambda: f"order-{sku.lower()}",
    )

    with allure.step(f"Добавить товар «{product_name}» в корзину"):
        cart.add(product)

    with allure.step("Провести оплату через моковый платёжный шлюз"):
        order = service.checkout(cart, customer_id="customer-case-20")

    with allure.step("Проверить сумму и успешный идентификатор платежа"):
        payment_gateway.charge.assert_called_once_with("customer-case-20", price)
        assert order.amount == price
        assert order.payment_id == "payment-001"

    with allure.step("Проверить сохранение оплаченного заказа"):
        order_repository.save.assert_called_once_with(order)
