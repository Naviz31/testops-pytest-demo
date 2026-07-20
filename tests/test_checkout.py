from decimal import Decimal
from unittest.mock import Mock

import allure
import pytest

from mock_autotests.shop import (
    Cart,
    CheckoutService,
    EmptyCartError,
    PaymentDeclinedError,
)


pytestmark = [
    pytest.mark.allure_label("naviz31", label_type="owner"),
    pytest.mark.allure_label("unit", label_type="layer"),
    pytest.mark.allure_label("checkout", label_type="component"),
    pytest.mark.allure_label("Моковый интернет-магазин", label_type="parentSuite"),
    pytest.mark.allure_label("Оформление заказа", label_type="suite"),
]


@allure.epic("Моковый интернет-магазин")
@allure.feature("Оформление заказа")
@allure.story("Успешная оплата")
@allure.title("Заказ сохраняется после успешной моковой оплаты")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("smoke", "unit", "offline")
@pytest.mark.smoke
@pytest.mark.unit
def test_checkout_saves_paid_order(
    cart: Cart,
    payment_gateway: Mock,
    order_repository: Mock,
) -> None:
    service = CheckoutService(
        payment_gateway=payment_gateway,
        order_repository=order_repository,
        order_id_factory=lambda: "order-001",
    )

    with allure.step("Оформить корзину для тестового покупателя"):
        order = service.checkout(cart, customer_id="customer-001")

    with allure.step("Проверить обращение к моковому платёжному шлюзу"):
        payment_gateway.charge.assert_called_once_with(
            "customer-001",
            Decimal("4099.80"),
        )

    with allure.step("Проверить созданный и сохранённый заказ"):
        assert order.order_id == "order-001"
        assert order.payment_id == "payment-001"
        order_repository.save.assert_called_once_with(order)


@allure.epic("Моковый интернет-магазин")
@allure.feature("Оформление заказа")
@allure.story("Ошибки оплаты")
@allure.title("Заказ не сохраняется, если моковая оплата отклонена")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("negative", "unit", "offline")
@pytest.mark.regression
@pytest.mark.unit
def test_checkout_does_not_save_order_when_payment_is_declined(
    cart: Cart,
    payment_gateway: Mock,
    order_repository: Mock,
) -> None:
    payment_gateway.charge.side_effect = PaymentDeclinedError("insufficient funds")
    service = CheckoutService(
        payment_gateway=payment_gateway,
        order_repository=order_repository,
        order_id_factory=lambda: "order-must-not-be-created",
    )

    with allure.step("Сымитировать отклонение платежа"):
        with pytest.raises(PaymentDeclinedError, match="insufficient funds"):
            service.checkout(cart, customer_id="customer-001")

    with allure.step("Убедиться, что заказ не сохранён"):
        order_repository.save.assert_not_called()


@allure.epic("Моковый интернет-магазин")
@allure.feature("Оформление заказа")
@allure.story("Валидация")
@allure.title("Пустую корзину нельзя оформить")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "unit", "offline")
@pytest.mark.regression
@pytest.mark.unit
def test_empty_cart_is_rejected_before_payment(
    payment_gateway: Mock,
    order_repository: Mock,
) -> None:
    service = CheckoutService(
        payment_gateway=payment_gateway,
        order_repository=order_repository,
        order_id_factory=lambda: "unused-order-id",
    )

    with allure.step("Попытаться оформить пустую корзину"):
        with pytest.raises(EmptyCartError, match="empty cart"):
            service.checkout(Cart(), customer_id="customer-001")

    payment_gateway.charge.assert_not_called()
    order_repository.save.assert_not_called()
