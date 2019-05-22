import random
from component import Card, CardPlaced, Deck

'''
{
    'decks' : {
        'player_1' : Deck(), ...
    },
    'turn' : 'player_x',
    'counter' : increment,
    'card_placed' : CardPlaced(),
    'players' : ['name_1', ...],
    'winner' : [],

}
'''


class Game:
    def __init__(self):
        self.players = []
        self.card_placed = CardPlaced()
        self.player_decks = {}
        self.start = False
        self.finish = False
        self.state = ""
        self.turn = ""
        self.winner = []

    def add_players(self, name: str):
        self.players.append(name)

    def create_decks(self):
        decks = []
        for suit in ['spade', 'heart', 'diamond', 'club']:
            for name in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
                decks.append([str(name), suit])
        random.shuffle(decks)

        player_decks = {}
        for i, player in enumerate(self.players):
            temp_deck = decks[i * 13:(i + 1) * 13]
            new_deck = Deck()
            for card in temp_deck:
                new_deck.add(Card(card[0], card[1]))
            player_decks[player] = new_deck
        self.player_decks = player_decks

    def check_quad_deck(self):
        for player in self.player_decks:
            self.player_decks[player].remove_quad()

    def next_turn(self):
        if self.turn != "":
            idx = self.players.index(self.turn)
        else:
            idx = -1
        idx = (idx + 1) % len(self.players)
        self.turn = self.players[idx]

    def loop(self):
        pass

    def update_score(self):
        pass

    def save_score(self):
        pass

    def isSomeoneWin(self):
        for player in self.player_decks:
            if self.player_decks[player].empty():
                self.winner.append(player)
                print(player+" win!!")


if __name__ == "__main__":
    game = Game()
    game.add_players("a")
    game.add_players("b")
    game.add_players("c")
    game.add_players("d")
    game.create_decks()
    game.start = True
    print(game.__dict__)
    game2 = Game()
    game2.__dict__.update(game.__dict__)
    game2.__dict__.update({'players': [1, 2, 3, 4]})
    print(game2.players, game2.start, game2.finish)
