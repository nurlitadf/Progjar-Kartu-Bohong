import random
import operator
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
        self.sorted_score_list = []
        self.previous_card = None

    def add_players(self, name: str):
        self.players.append(name)

    def create_decks(self):
        decks = []
        for suit in ['spade', 'heart', 'diamond', 'club']:
            # for suit in ['spade']:
            for name in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
                # for name in list(range(2, 6)):
                decks.append([str(name), suit])
        random.shuffle(decks)

        player_decks = {}
        for i, player in enumerate(self.players):
            temp_deck = decks[i * 13:(i + 1) * 13]
            # temp_deck = decks[i * 1:(i + 1) * 1]
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
        while self.player_decks[self.players[idx]].empty():
            print('[IDX]', idx)
        print('[IDX]', idx)
        self.turn = self.players[idx]

    def loop(self):
        pass

    def update_score(self):
        scores = {}
        self.sorted_score_list = []
        for i, player in enumerate(self.winner):
            score = 300 - i*300
            self.sorted_score_list.append((player, score))
        self.save_score()

    def save_score(self):
        with open("score.txt", "r") as f:
            file_content = f.readlines()
        scores = {}
        for row in file_content:
            name, score = row.split(' ')
            scores[name] = int(score)

        for player, score in self.sorted_score_list:
            if player in scores:
                scores[player] += score
            else:
                scores[player] = score
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        with open("score.txt", "w") as f:
            for data in sorted_scores:
                text = "{} {}\n".format(data[0], data[1])
                f.write(text)

    def is_someone_win(self, player):
        if self.player_decks[player].empty():
            # self.players.remove(player)
            # self.player_decks.pop(player, None)
            self.winner.append(player)
            print(player+" win!!")
        return

    def is_everyone_win(self):
        print("hehe")
        if len(self.winner) == 4:
            print("yay")
            return True
        return False


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
