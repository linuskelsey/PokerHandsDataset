faceCards = ['T', 'J', 'Q', 'K', 'A']
suits = ['c', 's', 'd', 'h']

def encode_card(card: str) -> int:
    nout = 0

    rank = card[0].upper()
    suit = card[1].lower()

    nout += suits.index(suit) * 13
    if rank in faceCards:
        nout += 10 + faceCards.index(rank)
    else:
        nout += int(rank)

    return nout

def encode_hand(cards: list[str]) -> list[int]:
    encoded = []
    for card in cards:
        encoded.append(encode_card(card))

    return encoded