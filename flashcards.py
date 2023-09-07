import csv
import itertools
import logging
import sys
from io import StringIO

from exceptions import InvalidInputError, DefinitionExistsError, RemoveCardError, \
    CommandDoesntExistError, CardExistsError
from controller import Controller


def get_term() -> str:
    printlog("Card:")
    while True:
        term = take_input()
        try:
            if controller.matching_term(term):
                raise CardExistsError(term)
        except CardExistsError as e:
            printlog(e, " Try again:")
        else:
            return term


def get_definition() -> str:
    printlog("Definition:")
    while True:
        definition = take_input()
        try:
            if controller.matching_definition(definition):
                raise DefinitionExistsError(definition)
        except DefinitionExistsError as e:
            printlog(e, "Try again:")
        else:
            return definition


def add_card() -> None:
    term = get_term()
    definition = get_definition()
    controller.add_card(term, definition)
    printlog(f"The pair (\"{term}\":\"{definition}\") has been added.")


def remove() -> None:
    term = take_input("Which card?\n")
    try:
        controller.remove_card_from_db(term)
    except RemoveCardError as e:
        printlog(e)
    else:
        printlog("The card has been removed.")


def export_cards() -> None:
    file_name = take_input("File name:\n")
    cards = controller.get_cards()
    with open(file_name, mode='w') as file:
        writer = csv.writer(file, delimiter="|")
        for term, card in cards.items():
            writer.writerow([term, card["definition"], card["mistakes"]])
    printlog(f"{len(cards)} cards have been saved.")


def load_cards_from_file(file_name: str) -> list:
    cards = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter="|")
        for row in reader:
            cards.append(row)
    return cards


def import_cards() -> None:
    file_name = take_input("File name:\n")

    try:
        logger.info("Loading cards from file %s", file_name)
        cards = load_cards_from_file(file_name)
        logger.info("%s cards found", len(cards))
        for card in cards:
            logger.info("Adding card: term=%s, definition=%s , mistakes=%s", card[0], card[1], card[2])
            controller.add_card(card[0], card[1], int(card[2]))
        printlog(f"{len(cards)} cards have been loaded.")
    except FileNotFoundError:
        printlog("File not found.")


def ask():
    amount = take_input("How many times to ask?\n")

    try:
        int_amount = int(amount)
        cards = controller.get_cards()
        card_iterator = itertools.cycle(cards.items())
    except ValueError:
        printlog("That is not a valid integer.")
    except InvalidInputError as e:
        printlog(e)
    else:
        for _ in range(int_amount):
            card = next(card_iterator)
            test_card(card[0], card[1]['definition'])


def test_card(term: str, definition: str) -> None:
    answer = take_input(f"Print the definition of \"{term}\":\n")

    if answer == definition:
        printlog("Correct!")
    else:
        related_term = controller.matching_definition(answer)
        if related_term:
            printlog(
                f"Wrong. The right answer is \"{definition}\", but your definition is correct for \"{related_term}\".")
        else:
            printlog(
                f"Wrong. The right answer is \"{definition}\".")
        controller.add_mistake(term)


def exit_program() -> None:
    printlog("Bye bye!")
    exit()


def hardest_card() -> None:
    hardest_cards = controller.hardest_cards()
    if hardest_cards:
        mistakes = hardest_cards["mistakes"]
        if len(hardest_cards["terms"]) > 1:
            joined = ', '.join(f'"{term}"' for term in hardest_cards["terms"])
            printlog(f"The hardest cards are {joined}. You have {mistakes} errors answering them.")
        else:
            printlog(f"The hardest card is \"{hardest_cards['terms'][0]}\". You have {mistakes} errors answering it.")
    else:
        printlog("There are no cards with errors.")


def save_logs() -> None:
    logger.info(
        f"Current logs:\n{log_stream.getvalue()}"
    )
    file_name = take_input("File name:\n")
    with open(file_name, mode='w') as file:
        file.write(log_stream.getvalue())
    printlog("The log has been saved.")


def log(log_text: str) -> None:
    log_stream.write(log_text + '\n')


def take_input(prompt: str = '') -> str:
    if prompt:
        log_stream.write(prompt)
    input_str = input(prompt)
    log(input_str)
    return input_str.strip()


def printlog(*args, **kwargs):
    print(*args, **kwargs)
    print(*args, **kwargs, file=log_stream)


def reset_stats() -> None:
    controller.reset_stats()
    printlog("Card statistics have been reset.")


def main():
    cmd_dict = {
        'exit': exit_program,
        'add': add_card,
        'remove': remove,
        'export': export_cards,
        'import': import_cards,
        'ask': ask,
        'hardest card': hardest_card,
        'log': save_logs,
        'reset stats': reset_stats
    }
    while True:
        printlog(
            "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):"
        )
        cmd = take_input()
        logging.debug(cmd)
        try:
            if cmd in cmd_dict:
                cmd_dict[cmd]()
            else:
                raise CommandDoesntExistError
        except InvalidInputError as e:
            printlog(e)


if __name__ == "__main__":
    controller = Controller()

    log_stream = StringIO()

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to the console
            logging.StreamHandler(log_stream),  # Log to the StringIO object
        ]
    )
    logger = logging.getLogger()

    main()
