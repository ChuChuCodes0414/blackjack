import random

class Card:
    '''
        A class that defines any card.

        It has two values, one for the suit and one for the value of the card.
    '''
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
class Deck:
    '''
        A class that defines the deck of cards in play.

        It is comprised of mainly a list of all playable cards.
    '''
    def __init__(self):
        # initialize the cards with list comprehension
        self.cards = [Card(suit, val) for suit in ["♠", "♣", "♥", "♦"] for val in
                      ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]

    # Shuffle the list of the cards
    def shuffle(self):
        random.shuffle(self.cards)

    # Draw a card from the deck, and remove it so it cannot be played again.
    def draw(self):
        return self.cards.pop(0)

class Hand:
    '''
        A class that defines the hand of the player or dealer. 

        It comprises of the list of cards, the value of the cards, and if the cards should be hidden.
    '''
    def __init__(self,hide):
        self.cards =  []
        self.hide = hide
        self.value = 0

    # Add a new card to the hand.
    def pull_card(self,card):
        self.cards.append(card)

    # Calculate and return the value of the hand.
    def get_value(self):
        self.value = 0
        ace = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value in ["J", "Q", "K"]:
                    self.value += 10
                else:
                    ace += 1

        for count in range(0,ace):
            if self.value >= 11:
                self.value += 1
            else:
                self.value += 11

        return self.value
    
    # Return a nicely formatted hand
    def get_hand(self,show=False):
        build = ""
        if not self.hide or show:
            for card in self.cards:
                build += f'{card.suit}{card.value}  '
            build += f"\nCard Value: {self.get_value()}"
            return build
        else:
            build += self.cards[0].suit + self.cards[0].value + "  ?\nCard Value: ?"
            return build


class game_loop:
    '''
        This class is the main game loop. It holds the loops to run the game, as well as methods to determine game winning conditions.
    '''

    def __init__(self):
        pass

    # This class is the main game loop.
    def main_game(self):
        active = True
        
        while active: # While the player still wants to play
            self.game_deck = Deck() # Get a deck of cards
            self.game_deck.shuffle() # Shuffle the deck of cards
            self.player = Hand(False) # Initialize the hand object for the player
            self.dealer = Hand(True) # Initialize the dealer object for the player

            # Draw the intial two cards for both the dealer and the player.
            for count in range(0,2):
                self.player.pull_card(self.game_deck.draw())
                self.dealer.pull_card(self.game_deck.draw())

            # If the dealer starts out with a 21, discard the first card and draw again.
            while self.dealer.get_value() == 21:
                self.dealer.cards.pop(0)
                self.dealer.pull_card(self.game_deck.draw())

            # If the player starts out with a 21, discard the first card and draw again.
            while self.player.get_value() == 21:
                self.player.cards.pop(0)
                self.player.pull_card(self.game_deck.draw())

            # Display initial hand information.
            print(f"-----------------------------------------")
            print(f"You have: \n{self.player.get_hand()}")
            print(f"\nDealer has: \n{self.dealer.get_hand()}")
            print(f"-----------------------------------------")
            
            not_blackjack = True

            while not_blackjack: # While a win condition is not reached
                choice = input("What do you want to do? (hit,stand): ") # Prompt the user for their choice

                if choice.lower() == "hit": # If the user chooses to hit, draw another card and check win conditions
                    self.player.pull_card(self.game_deck.draw())
                    if self.check_5cards():
                        not_blackjack = False
                    elif self.check_21():
                        not_blackjack = False
                    elif self.check_bust():
                        not_blackjack = False
                elif choice.lower() == "stand": # If the user chooses to stand, have the dealer draw until it is at or past 17. Then check win conditions
                    while self.dealer.get_value() <= 17:
                        self.dealer.pull_card(self.game_deck.draw())
                        if self.check_5cards():
                            not_blackjack = False
                        elif self.check_21():
                            not_blackjack = False
                        elif self.check_bust():
                            not_blackjack = False
                    if not_blackjack: #If the game is still active (meaning the above conditions have failed), check who has the higher hand value
                        self.check_stand()
                        not_blackjack = False
                else: # Invalid input, prompt again
                    print("\nThat does not look like a valid option, please try again.")

                if not_blackjack: # The game is still active, show the current hand status.
                    print(f"-----------------------------------------")
                    print(f"You have: \n{self.player.get_hand()}")
                    print(f"\nDealer has: \n{self.dealer.get_hand()}")
                    print(f"-----------------------------------------")
                else: # The game is over, show what you and the dealer had at the end.
                    print(f"You Had: \n{self.player.get_hand()}")
                    print(f"\nDealer had: \n{self.dealer.get_hand(True)}")

                    # Force the user to input if they want to play again. Does not accept invalid input
                    while True:
                        again = input("\nDo you want to play again? (yes,no): ")

                        if again.lower() == "yes":
                            break
                        elif again.lower() == "no":
                            active =False
                            break
                        
    # This method checks if either the dealer or player has 21, and if the game has ended.
    def check_21(self):
        if self.player.get_value() == 21 and self.dealer.get_value() != 21:
            print(f"-----------------------------------------")
            print("You have 21! You win!")
            return True
        elif self.dealer.get_value() == 21:
            print(f"-----------------------------------------")
            print("The dealer has 21! You lose!")
            return True
        elif self.dealer.get_value() == 21 and self.player.get_value() == 32:
            print(f"-----------------------------------------")
            print("Both you and the dealer have 21! You tie.")
            return True
        else:
            return False

    # This method checks if either the dealer or the player has busted, and if the game has ended.
    def check_bust(self):
        if self.player.get_value() >= 21:
            print(f"-----------------------------------------")
            print("You went over 21, busted!")
            return True
        elif self.dealer.get_value() >= 21:
            print(f"-----------------------------------------")
            print("The dealer went over 21, you win!")
            return True
        else:
            return False

    # This method checks if the dealer or the player has the higher value if the player stands.
    def check_stand(self):
        if self.player.get_value() == self.dealer.get_value():
            print(f"-----------------------------------------")
            print("You both have the same value! You tie.")
        elif self.player.get_value() >= self.dealer.get_value():
            print(f"-----------------------------------------")
            print("You have a higher value than the dealer. You win!")
        else:
            print(f"-----------------------------------------")
            print("The dealer has a higher value than you. You lose!")

    # This method checks if the dealer or the player has drawed 5 cards without reaching or going over 21, and if the game has ended.
    def check_5cards(self):
        if len(self.player.cards) == 5:
            print(f"-----------------------------------------")
            print("You took 5 cards without going over 21. You win!")
            return True
        elif len(self.dealer.cards) == 5:
            print(f"-----------------------------------------")
            print("The dealer took 5 cards without going over 21. You lose!")
            return True
        else:
            return False
        
# This method creates an object of the game_loop class, and begins the game.
if __name__ == "__main__":
    game = game_loop()
    game.main_game()

