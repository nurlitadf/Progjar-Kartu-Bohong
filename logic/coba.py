import random

from component import Card, Deck, CardPlaced, CARD_MAPPING

player_names = []
player_decks = None
card_placed = CardPlaced()


def create_decks(names: list):
    decks = []
    for suit in ['spade', 'heart', 'diamond', 'club']:
        for name in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
            decks.append([str(name), suit])
    random.shuffle(decks)

    player_decks = {}
    for i, player in enumerate(names):
        temp_deck = decks[i * 13:(i + 1) * 13]
        new_deck = Deck()
        for card in temp_deck:
            new_deck.add(Card(card[0], card[1]))
        player_decks[player] = new_deck
    # for key, val in player_decks.items():
    #     print(key, val)
    return player_decks


def init():
    global player_decks
    for i in range(1, 5):
        player_name = input("Player {} name >>".format(i))
        player_names.append(player_name)
    player_decks = create_decks(player_names)
    # for key, val in player_decks.items():
    #     print(key, val)


def loop():
    global player_decks, card_placed
    turn = -1
    while True:
        turn += 1
        i = turn % 4
        cnt = 0
        while cnt < len(player_names):
            player = player_names[i]
            print('[PLAYER {} TURN]'.format(player), i, turn, turn % 4)
            player_decks[player].remove_quad()

            if (turn % 4) == i:
                for j, card in enumerate(player_decks[player].cards):
                    print('[{} {}]'.format(j, card), end=" ")
                print()
                selected = input("Select cards >>")
                selected = list(map(int, selected.split()))
                print(selected)
                selected = player_decks[player].pick(selected)

                statement = input("Statement>>")
                statement = CARD_MAPPING[statement]
                print(statement)
                card_placed.add(selected, statement)
            else:
                action = input("action>>")
                if action == "lie":
                    print(card_placed.check())

            cnt += 1
            i += 1
            i %= 4
            a = input("continue>>")


if __name__ == "__main__":
    init()
    loop()
