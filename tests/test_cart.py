from decimal import Decimal

import allure
import pytest

from mock_autotests.shop import Cart, Product


pytestmark = [
    pytest.mark.allure_label("naviz31", label_type="owner"),
    pytest.mark.allure_label("unit", label_type="layer"),
    pytest.mark.allure_label("cart", label_type="component"),
    pytest.mark.allure_label("Моковый интернет-магазин", label_type="parentSuite"),
    pytest.mark.allure_label("Корзина", label_type="suite"),
]


@allure.epic("Моковый интернет-магазин")
@allure.feature("Корзина")
@allure.story("Расчёт стоимости")
@allure.title("Стоимость корзины рассчитывается по всем позициям")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "unit", "offline")
@pytest.mark.smoke
@pytest.mark.unit
def test_cart_total_contains_all_items(cart: Cart) -> None:
    with allure.step("Рассчитать итоговую стоимость корзины"):
        actual_total = cart.total()

    with allure.step("Проверить сумму всех товаров"):
        assert actual_total == Decimal("4099.80")


@allure.epic("Моковый интернет-магазин")
@allure.feature("Корзина")
@allure.story("Расчёт стоимости")
@allure.title("Скидка {discount}% применяется к стоимости корзины")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression", "unit", "offline")
@pytest.mark.regression
@pytest.mark.unit
@pytest.mark.parametrize(
    ("discount", "expected"),
    [
        pytest.param(Decimal("0"), Decimal("4099.80"), id="без-скидки"),
        pytest.param(Decimal("10"), Decimal("3689.82"), id="скидка-10"),
        pytest.param(Decimal("100"), Decimal("0.00"), id="скидка-100"),
    ],
)
def test_cart_applies_discount(
    cart: Cart,
    discount: Decimal,
    expected: Decimal,
) -> None:
    with allure.step(f"Применить скидку {discount}%"):
        actual_total = cart.total(discount)

    assert actual_total == expected


@allure.epic("Моковый интернет-магазин")
@allure.feature("Корзина")
@allure.story("Добавление товара")
@allure.title("Повторное добавление товара увеличивает его количество")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression", "unit", "offline")
@pytest.mark.regression
@pytest.mark.unit
def test_same_product_is_merged_into_one_line(book: Product) -> None:
    cart = Cart()

    with allure.step("Дважды добавить один товар"):
        cart.add(book)
        cart.add(book, quantity=2)

    with allure.step("Проверить единственную позицию и суммарное количество"):
        assert len(cart.lines) == 1
        assert cart.lines[0].quantity == 3


@allure.epic("Моковый интернет-магазин")
@allure.feature("Корзина")
@allure.story("Валидация")
@allure.title("Нельзя добавить товар в недопустимом количестве: {quantity}")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "unit", "offline")
@pytest.mark.regression
@pytest.mark.unit
@pytest.mark.parametrize("quantity", [0, -1], ids=["ноль", "отрицательное"])
def test_cart_rejects_invalid_quantity(book: Product, quantity: int) -> None:
    cart = Cart()

    with allure.step(f"Попытаться добавить {quantity} единиц товара"):
        with pytest.raises(ValueError, match="Quantity must be greater than zero"):
            cart.add(book, quantity=quantity)
