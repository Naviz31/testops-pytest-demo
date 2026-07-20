"""Предсказуемые демонстрационные статусы для отображения в ТестОпс."""

import allure
import pytest


pytestmark = [
    pytest.mark.demo,
    pytest.mark.unit,
    pytest.mark.allure_label("naviz31", label_type="owner"),
    pytest.mark.allure_label("unit", label_type="layer"),
    pytest.mark.allure_label("result-statuses", label_type="component"),
    pytest.mark.allure_label("Демонстрация ТестОпс", label_type="parentSuite"),
    pytest.mark.allure_label("Статусы результатов", label_type="suite"),
]


@allure.epic("Демонстрация ТестОпс")
@allure.feature("Статусы результатов")
@allure.story("Успешный результат")
@allure.title("Демо: успешно пройденный тест")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("demo", "passed", "offline")
def test_demo_passed() -> None:
    with allure.step("Выполнить успешную проверку"):
        assert 2 + 2 == 4


@allure.epic("Демонстрация ТестОпс")
@allure.feature("Статусы результатов")
@allure.story("Проваленная проверка")
@allure.title("Демо: тест с намеренно неверным ожиданием")
@allure.description(
    "Тест намеренно завершается со статусом Failed, чтобы показать ошибку проверки."
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("demo", "failed", "offline")
def test_demo_failed() -> None:
    actual_order_status = "processing"

    with allure.step("Ожидать завершённый заказ при фактическом статусе processing"):
        assert actual_order_status == "completed", (
            "Демонстрационная ошибка: заказ ещё не завершён"
        )


@allure.epic("Демонстрация ТестОпс")
@allure.feature("Статусы результатов")
@allure.story("Ошибка выполнения")
@allure.title("Демо: тест с намеренной технической ошибкой")
@allure.description(
    "Тест намеренно завершается со статусом Broken, имитируя ошибку тестового кода."
)
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("demo", "broken", "offline")
def test_demo_broken() -> None:
    with allure.step("Сымитировать поломку тестовой фикстуры"):
        raise RuntimeError("Демонстрационная техническая ошибка фикстуры")


@allure.epic("Демонстрация ТестОпс")
@allure.feature("Статусы результатов")
@allure.story("Пропущенный тест")
@allure.title("Демо: тест пропущен по известной причине")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("demo", "skipped", "offline")
@pytest.mark.skip(reason="Демонстрационный пропуск: функциональность выключена")
def test_demo_skipped() -> None:
    raise AssertionError("Тело пропущенного теста не должно выполняться")


@allure.epic("Демонстрация ТестОпс")
@allure.feature("Статусы результатов")
@allure.story("Ожидаемый дефект")
@allure.title("Демо: известный дефект отмечен как ожидаемое падение")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("demo", "xfail", "offline")
@pytest.mark.xfail(
    reason="DEMO-101: известный демонстрационный дефект",
    strict=True,
)
def test_demo_expected_failure() -> None:
    with allure.step("Воспроизвести известный дефект DEMO-101"):
        assert "ожидаемый результат" == "фактический результат"
