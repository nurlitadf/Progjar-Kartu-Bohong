def start_draw_position(n_cards):
    return (1200 - 20*(n_cards-1) -90)/2 , 20

def get_position_my_cards(n_cards):
    pos = []

    if n_cards <= 26:
        x_start, space = start_draw_position(n_cards)
        hit = 0

        for i in range(n_cards):
            pos.append((x_start + space*hit, 555))
            hit+=1
    
    else:
        x_start, space = start_draw_position(n_cards - 26)
        hit = 0
        
        for i in range(n_cards - 26):
            pos.append((x_start + space*hit, 525))
            hit+=1
        
        x_start, space = start_draw_position(26)
        hit = 0

        for i in range(26):
            pos.append((x_start + space*hit, 585))
            hit+=1
    
    return pos


def draw_cards(paths):
    my_cards = []

    if len(paths) <= 26:
        x_start, space = start_draw_position(len(paths))
        hit = 0

        for p in paths:
            my_cards.append(Card(p, x_start + space*hit, 555))
            hit+=1
    else:
        x_start, space = start_draw_position(len(paths) - 26)
        hit = 0
        
        for i in range(len(paths) - 26):
            my_cards.append(Card(paths[i], x_start + space*hit, 525))
            hit+=1
        
        x_start, space = start_draw_position(26)
        hit = 0

        for i in range(len(paths) - 26, len(paths)):
            my_cards.append(Card(paths[i], x_start + space*hit, 585))
            hit+=1
    
    return my_cards
