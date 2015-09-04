"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from Card import *


class PokerHand(Hand):

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1
            
    def rank_hist(self):
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1
        
    def has_pair(self):
        self.rank_hist()
        for val in self.ranks.values():
            if (val >= 2):
                return True
        return False
        
    def has_two_pair(self):
        self.rank_hist()
        num_pairs = 0
        for val in self.ranks.values():
            if (val >= 2):
                num_pairs += 1
        if (num_pairs >= 2):
            return True
        else:
            return False
            
    def has_three_of_a_kind(self):
        self.rank_hist()
        for val in self.ranks.values():
            if (val >= 3):
                return True
        return False
        
    def has_straight(self):
        self.rank_hist()
        consecutive_ranks = 0
        max_consecutive_ranks = 0
        for i in range(1,14):
            val = self.ranks.get(i, 0)
            
            if (val > 0):
                consecutive_ranks += 1
            else:
                if (consecutive_ranks > max_consecutive_ranks):
                    max_consecutive_ranks = consecutive_ranks
                consecutive_ranks = 0
                
        if (self.ranks.get(1, 0) > 0):
            consecutive_ranks += 1
        
        if (consecutive_ranks > max_consecutive_ranks):
            max_consecutive_ranks = consecutive_ranks
                
        return max_consecutive_ranks >= 5
        
    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False
        
    def has_full_house(self):
        self.rank_hist()
        
        three_of_a_kind = False
        two_of_a_kind = False
        for val in self.ranks.values():
            if (val == 2):
                two_of_a_kind = True
        
            if (val == 3):
                three_of_a_kind = True
        return two_of_a_kind and three_of_a_kind
        
    def has_four_of_a_kind(self):
        self.rank_hist()
        for val in self.ranks.values():
            if (val >= 4):
                return True
        return False
        
    def has_straight_flush(self):
        self.rank_hist()
        self.suit_hist()
        curr_rank = -1
        curr_suit = -1
        
        for card in self.cards:
            if card.rank <= 10:         #If rank is jack or higher, we cannot have a straight flush beginning with it
                count = 1
                for i in range(1, 5):   #Check the next four cards higher in rank
                    if self.get_card_in_hand((card.rank + i) % card.rank, card.suit) is not None: #If there is such a card that has the same suit (we need the mod to check for a 10-J-Q-K-A combination)
                        count += 1      #Increment count
                        if count == 5:  #If we have found five cards, then we have a straight flush
                            return True
                    else:
                        break           #Otherwise check the next card
                
        return False

if __name__ == '__main__':
    # make a deck
    deck = Deck()
    deck.shuffle()

    # deal the cards and classify the hands
    for i in range(7):
        hand = PokerHand()
        deck.move_cards(hand, 7)
        hand.sort()
        print hand
        print 'Has pair', hand.has_pair()
        print 'Has two pair', hand.has_two_pair()
        print 'Has three of a kind', hand.has_three_of_a_kind()
        print 'Has straight', hand.has_straight()
        print 'Has flush', hand.has_flush()
        print 'Has full house', hand.has_full_house()
        print 'Has four of a kind', hand.has_four_of_a_kind()
        print 'Has straight flush', hand.has_straight_flush()
        print ''

