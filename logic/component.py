import json

CARD_MAPPING = {str(i): i for i in range(2, 11)}
CARD_MAPPING['J'] = 11
CARD_MAPPING['Q'] = 12
CARD_MAPPING['K'] = 13
CARD_MAPPING['A'] = 14


class Card:
    """
    Class for single card
    Example a King-Spade Card(name="K", suit="spade")
    """

    def __init__(self, name: str, suit: str):
        self.name = str(name)
        self.suit = suit
        self.value = CARD_MAPPING[self.name]

    def __lt__(self, card):
        return self.value < card.value

    # def __eq__(self, card):
    #     return self.value == card.value

    def __str__(self):
        return "{}-{}".format(self.name, self.suit)


class Deck:
    """
    Class for deck of cards (owned by each player)
    """

    def __init__(self):
        self.cards = []

    def add(self, card: Card):
        self.cards.append(card)

    def remove_quad(self):
        counter = [0] * 15
        for card in self.cards:
            counter[card.value] += 1
        quad = [i for i, val in enumerate(counter) if val == 4]
        temp_cards = [card for card in self.cards if card.value not in quad]

        del self.cards
        self.cards = temp_cards

    def __str__(self):
        return str([str(card) for card in self.cards])

    def pick(self, indexes: list):
        temp = [card for i, card in enumerate(self.cards) if i not in indexes]
        selected = [card for i, card in enumerate(self.cards) if i in indexes]

        self.cards = temp
        return selected


class CardPlaced:
    """
    Class for stack of cards in the middle of table (to be checked as TRUTH or LIE)
    cards: list = list of list of Cards
    values: list = list of card values
    """

    def __init__(self):
        self.cards = []
        self.values = []

    def check(self) -> bool:
        card_temp = self.cards[-1]
        value_temp = self.values[-1]
        for card in card_temp:
            if card.value != value_temp:
                return False
        return True

    def add(self, cards: list, value: int):
        self.cards.append(cards)
        self.values.append(value)

    def get_cards(self) -> list:
        return [card for cards in self.cards for card in cards]

    def empty(self):
        self.cards = []
        self.values = []


if __name__ == "__main__":
    card = Card(name="2", suit="spade")
    deck = Deck()
    for i in range(2, 11):
        deck.add(Card(str(i), "spade"))
    print(deck)

    card_placed = CardPlaced()

    card_placed.add(cards=[Card("2", "spade"), Card("3", "spade")], value=2)
    print(card_placed.check())  # False

    card_placed.add(cards=[Card("3", "spade"), Card("3", "spade")], value=3)
    print(card_placed.check())  # True

    cards = card_placed.get_cards()
    print([str(card) for card in cards])