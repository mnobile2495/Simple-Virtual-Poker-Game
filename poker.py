import random

# Define card suits and ranks
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]


# Define payout multipliers for different hands
payouts = {
    "Royal Flush": 250,
    "Straight Flush": 50,
    "Four of a Kind": 25,
    "Full House": 9,
    "Flush": 6,
    "Straight": 4,
    "Three of a Kind": 3,
    "Two Pair": 2,
    "Jacks or Better": 1
}

# Player's initial balance
balance = 1000

def deal_hand(deck, num_cards):
    return random.sample(deck, num_cards)

def evaluate_hand(hand):
    ranks_count = {}
    suits_count = {}
    for card in hand:
        rank = card['rank']
        suit = card['suit']
        ranks_count[rank] = ranks_count.get(rank, 0) + 1
        suits_count[suit] = suits_count.get(suit, 0) + 1
    
    sorted_ranks = sorted(ranks_count.keys(), key=lambda x: ranks.index(x))

    is_flush = any(count >= 5 for count in suits_count.values())
    is_straight = len(sorted_ranks) >= 5 and ranks.index(sorted_ranks[-1]) - ranks.index(sorted_ranks[0]) == 4

    if is_flush and is_straight:
        if sorted_ranks[-1] == 'A' and sorted_ranks[-2] == 'K':
            return "Royal Flush"
        return "Straight Flush"
    
    for rank, count in ranks_count.items():
        if count == 4:
            return "Four of a Kind"
        if count == 3:
            for other_rank, other_count in ranks_count.items():
                if other_rank != rank and other_count == 2:
                    return "Full House"
            return "Three of a Kind"
        if count == 2:
            for other_rank, other_count in ranks_count.items():
                if other_rank != rank and other_count == 2:
                    return "Two Pair"
            return "Jacks or Better"
    
    if is_flush:
        return "Flush"
    if is_straight:
        return "Straight"
    
    return "No Win"



def main(deck):
    global balance
    print("Welcome to Simplified Video Poker!")

    while balance > 0:
        print(f"Your current balance: ${balance}")
        bet = int(input("Place your bet (1-5): "))
        if bet < 1 or bet > 5 or bet > balance:
            print("Invalid bet amount. Please try again.")
            continue
        
        balance -= bet
        
        player_hand = deal_hand(deck, 5)
        print("\nYour hand:")
        for i, card in enumerate(player_hand):
            print(f"{i+1}: {card['rank']} of {card['suit']}")
        
        # Evaluate the hand and determine the payout
        hand_result = evaluate_hand(player_hand)
        payout_multiplier = payouts.get(hand_result, 0)
        payout = bet * payout_multiplier
        
        if payout > 0:
            balance += payout
            print(f"\nCongratulations! You got a {hand_result} and won ${payout}!")
        else:
            print(f"\nSorry, you didn't win this time. Try again!")

        play_again = input("\nDo you want to play another hand? (y/n): ")
        if play_again.lower() != 'y':
            print("Thanks for playing!")
            break
    
    print("Game over. Your final balance: ${balance}")

if __name__ == "__main__":
    main(deck)

