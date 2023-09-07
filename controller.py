from exceptions import RemoveCardError, NoCardsError

class Controller:

    def __init__(self):
        self.cards = {}

    def matching_term(self, term: str) -> dict:
        return self.cards.get(term)

    def matching_definition(self, definition: str) -> str:
        for term, card in self.cards.items():
            if card.get("definition") == definition:
                return term
        return None

    def add_card(self, term: str, definition: str, mistakes: int = 0) -> None:
        self.cards[term] = {
            "definition": definition,
            "mistakes": mistakes
        }

    def get_cards(self) -> dict:
        cards = self.cards
        if cards:
            return cards
        else:
            raise NoCardsError

    def remove_card_from_db(self, term: str) -> None:
        if term in self.cards:
            del self.cards[term]
        else:
            raise RemoveCardError(term)

    def hardest_cards(self) -> dict:
        if self.cards:
            max_mistakes = max(card["mistakes"] for card in self.cards.values())
            if max_mistakes > 0:
                hardest_cards = {
                    "mistakes": max_mistakes,
                    "terms": [term for term, card in self.cards.items() if card["mistakes"] == max_mistakes]
                }
                return hardest_cards
        return {}

    def add_mistake(self, term: str) -> None:
        self.cards[term]['mistakes'] += 1

    def reset_stats(self) -> None:
        if self.cards:
            for term, value in self.cards.items():
                value["mistakes"] = 0


