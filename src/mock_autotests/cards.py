"""Автономная модель интерфейса товарных карточек."""

from __future__ import annotations

from dataclasses import dataclass


class CardNotFoundError(LookupError):
    """Карточка с указанным идентификатором не существует."""


@dataclass(slots=True)
class ProductCard:
    card_id: str
    name: str
    description: str

    def __post_init__(self) -> None:
        if not self.card_id.strip():
            raise ValueError("Card ID must not be empty")
        if not self.name.strip():
            raise ValueError("Card name must not be empty")


class CardsWorkspace:
    """Хранит карточки и имитирует переходы между экранами."""

    def __init__(self, cards: list[ProductCard]) -> None:
        self._cards = {card.card_id: card for card in cards}
        if len(self._cards) != len(cards):
            raise ValueError("Card IDs must be unique")
        self.active_view = "closed"

    def open_cards_tab(self) -> tuple[ProductCard, ...]:
        self.active_view = "cards"
        return tuple(self._cards.values())

    def open_card(self, card_id: str) -> CardDetailsView:
        if self.active_view != "cards":
            raise RuntimeError("Cards tab must be opened first")

        try:
            card = self._cards[card_id]
        except KeyError as error:
            raise CardNotFoundError(card_id) from error

        self.active_view = f"card:{card_id}"
        return CardDetailsView(self, card)


class CardDetailsView:
    def __init__(self, workspace: CardsWorkspace, card: ProductCard) -> None:
        self._workspace = workspace
        self.card = card

    def open_settings(self) -> CardSettingsDialog:
        self._workspace.active_view = f"settings:{self.card.card_id}"
        return CardSettingsDialog(self._workspace, self.card)


class CardSettingsDialog:
    def __init__(self, workspace: CardsWorkspace, card: ProductCard) -> None:
        self._workspace = workspace
        self._card = card
        self.is_open = True

    @property
    def current_name(self) -> str:
        return self._card.name

    @property
    def current_description(self) -> str:
        return self._card.description

    def save(self, *, name: str, description: str) -> ProductCard:
        if not self.is_open:
            raise RuntimeError("Settings dialog is already closed")
        if not name.strip():
            raise ValueError("Card name must not be empty")

        self._card.name = name
        self._card.description = description
        self.is_open = False
        self._workspace.active_view = f"card:{self._card.card_id}"
        return self._card
