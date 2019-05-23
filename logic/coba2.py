import random
#try
CARD_MAPPING = {str(i): i for i in range(2, 11)}
CARD_MAPPING['J'] = 11
CARD_MAPPING['Q'] = 12
CARD_MAPPING['K'] = 13
CARD_MAPPING['A'] = 14

print(CARD_MAPPING.items())

VAL_TO_CARD = {val: key for key, val in CARD_MAPPING.items()}
print(VAL_TO_CARD)

counter = [0] * 15
print(list(enumerate(counter)))

cards = list(range(2, 11))
print(cards)

cards1 = cards  + ['J', 'Q', 'K', 'A']
print(cards1)

# cards.append(['J', 'Q', 'K', 'A'])
cards.extend(['J', 'Q', 'K', 'A'])
print(cards)


decks = []
players = ['aldi', 'dandi', 'titut', 'lita']
for suit in ['spade', 'heart', 'diamond', 'club']:
    # for suit in ['spade']:
    for name in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
        # for name in list(range(2, 6)):
        decks.append([str(name), suit])
random.shuffle(decks)
print(decks)

player_decks = {}
for i, player in enumerate(players):
    temp_deck = decks[i * 13:(i + 1) * 13]
    print(player)
    print(temp_deck)

idx=1
idx+=1
print('[IDX]', idx)