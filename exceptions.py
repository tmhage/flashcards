class FlashCardError(Exception):
    def __str__(self) -> str:
        return f"{super().__str__()}" or f"{self.__doc__}"


class InvalidInputError(FlashCardError):
    pass


class CommandDoesntExistError(InvalidInputError):
    """Not a valid command."""


class ItemError(InvalidInputError):
    def __init__(self, item):
        super().__init__(self.__doc__.format(item))


class CardExistsError(ItemError):
    """The card "{}" already exists."""


class DefinitionExistsError(ItemError):
    """The definition "{}" already exists."""


class RemoveCardError(ItemError):
    """Can't remove "{}": there is no such card."""


class NoCardsError(InvalidInputError):
    """There are no cards in the deck."""


class NoIntegerError(InvalidInputError):
    """That is not an integer."""
