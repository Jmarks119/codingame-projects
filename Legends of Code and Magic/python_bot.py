import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def find_playable_cards(hand, mana):
    sorted_hand = sorted(hand, key=lambda card: card.cost, reverse=True)
    print([card.cost for card in sorted_hand], file=sys.stderr)
    playables = []
    for card in sorted_hand:
        if card.cost <= mana:
            playables.append(card)
            sorted_hand.remove(card)
            remaining_mana = mana - card.cost
            additional_playables = find_playable_cards(sorted_hand, remaining_mana)
            if additional_playables:
                playables.extend(additional_playables)
            return(playables)

class Card:
    def __init__(self, card_number, instance_id, location, card_type, cost):
        self.card_number = card_number
        self.instance_id = instance_id
        self.location = location
        self.card_type = card_type
        self.cost = cost

class Creature(Card):
    def __init__(self, card_number, instance_id, location, cost, attack, defense, abilities, card_type=0):
        super().__init__(card_number, instance_id, location, card_type, cost)
        self.attack = attack
        self.defense = defense
        self.stat_total = attack + defense
        self.breakthrough = True if "B" in abilities else False
        self.charge = True if "C" in abilities else False
        self.guard = True if "G" in abilities else False

# game loop
while True:
    hand = []
    board = []
    opponent_board = []
    health, mana, deck, rune = [int(j) for j in input().split()]
    opponent_health, opponent_mana, opponent_deck, opponent_rune = [int(j) for j in input().split()]
    opponent_hand = int(input())
    card_count = int(input())
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
        card_number = int(card_number)
        instance_id = int(instance_id)
        location = int(location)
        card_type = int(card_type)
        cost = int(cost)
        attack = int(attack)
        defense = int(defense)
        if location == 0:
            if card_type == 0:
                hand.append(Creature(card_number, instance_id, location, cost, attack, defense, abilities))
        if location == 1:
            if card_type == 0:
                board.append(Creature(card_number, instance_id, location, cost, attack, defense, abilities))
        if location == -1:
            if card_type == 0:
                opponent_board.append(Creature(card_number, instance_id, location, cost, attack, defense, abilities))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    
    if card_count == 0:
        print("PASS")
    elif mana == 0:
        best_card = None
        best_score = -100
        for card in hand:
            if card.card_type == 0:
                stat_efficiency = (card.stat_total + card.charge + card.guard + card.breakthrough) / (card.cost + .5)
                score = stat_efficiency
                print(f"score for {card.card_number} is {score}", file=sys.stderr)
            if score > best_score:
                best_score = score
                best_card = card
        print(f"PICK {hand.index(best_card)}")
    else:
        actions = []
        summonable_cards = find_playable_cards(hand, mana)
        activatable_creatures = [card for card in board if card.card_type == 0 and card.attack > 0]
        enemy_blockers = sorted([card for card in opponent_board if card.guard], key=lambda card: card.attack)
        print(f"{summonable_cards}", file=sys.stderr)
        if summonable_cards != None:
            for card in summonable_cards:
                actions.append(f"SUMMON {card.instance_id}")
                if card.charge:
                    activatable_creatures.append(card)
        if len(activatable_creatures) > 0:
            for card in activatable_creatures:
                if len(enemy_blockers) > 0:
                    blocker = enemy_blockers[0]
                    actions.append(f'ATTACK {card.instance_id} {blocker.instance_id}')
                    blocker.defense -= card.attack
                    if blocker.defense <= 0:
                        enemy_blockers.remove(blocker)
                else:
                    for opponent_card in opponent_board:
                        if card.attack >= opponent_card.defense and opponent_card.defense < card.defense:
                            actions.append(f'ATTACK {card.instance_id} {opponent_card.instance_id}')
                            opponent_board.remove(opponent_card)
                            break
                    else:
                        actions.append(f'ATTACK {card.instance_id} -1')
        if len(actions) > 0:
            print(";".join(actions))
        else:
            print("PASS")
        