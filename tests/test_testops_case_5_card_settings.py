import allure
import pytest

from mock_autotests.cards import CardsWorkspace, ProductCard


pytestmark = [
    pytest.mark.allure_label("naviz31", label_type="owner"),
    pytest.mark.allure_label("unit", label_type="layer"),
    pytest.mark.allure_label("product-cards", label_type="component"),
    pytest.mark.allure_label("Моковый интернет-магазин", label_type="parentSuite"),
    pytest.mark.allure_label("Карточки товаров", label_type="suite"),
]


@allure.id("5")
@allure.testcase(
    "https://htcconf.qatools.cloud/project/1/test-cases/5",
    "ТестОпс: тест-кейс №5 «Настройки карточки»",
)
@allure.epic("Моковый интернет-магазин")
@allure.feature("Карточки товаров")
@allure.story("Настройки карточки")
@allure.title("Настройки карточки")
@allure.description(
    "Автоматизация ручного тест-кейса ТестОпс №5. Проверяет открытие карточки "
    "и модального окна настроек, а также сохранение нового названия и описания."
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "unit", "offline", "testops-linked")
@pytest.mark.smoke
@pytest.mark.unit
def test_card_name_and_description_are_changed_from_settings() -> None:
    card = ProductCard(
        card_id="card-001",
        name="Молоко",
        description="Молоко, 1 литр",
    )
    workspace = CardsWorkspace([card])

    with allure.step("Перейти во вкладку Карточки"):
        cards = workspace.open_cards_tab()
        assert workspace.active_view == "cards"
        assert cards == (card,)

    with allure.step("Открыть любую карточку"):
        card_view = workspace.open_card(cards[0].card_id)
        assert workspace.active_view == "card:card-001"
        assert card_view.card is card

    with allure.step("Нажать на шестерёнку в правом верхнем углу"):
        settings = card_view.open_settings()
        assert settings.is_open
        assert workspace.active_view == "settings:card-001"
        assert settings.current_name == "Молоко"
        assert settings.current_description == "Молоко, 1 литр"

    with allure.step("Изменить название и описание карточки товара"):
        settings.save(
            name="Молоко фермерское",
            description="Фермерское молоко, 1 литр",
        )

    with allure.step("Проверить карточку во вкладке Карточки"):
        updated_cards = workspace.open_cards_tab()
        assert not settings.is_open
        assert updated_cards[0].name == "Молоко фермерское"
        assert updated_cards[0].description == "Фермерское молоко, 1 литр"
