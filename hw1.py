# hw1.py
# Name: Connor Durkin
# netID : cwd28
# Date: 29 September 2015
# Class: CPSC 458
# Instructor: Prof. Stephen Slade

import random
import numpy
import json

# initialize some useful global variables
global in_play
in_play = False
global outcome
outcome = " start game"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

# define hand class
       
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans
        # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)
        # add a card object to a hand

    def get_value(self):
        value = 0
        aces = False
        for c in self.cards:
            rank = c.get_rank()
            v = VALUES[rank]
            if rank == 'A': aces = True
            value += v
        if aces and value < 12: value += 10
        return value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        # create a Deck object
    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle the deck 
    def deal_card(self):
        return self.deck.pop()
        # deal a card object from the deck
    
    def __str__(self):
        ans = "The deck: "
        for c in self.deck:
            ans += str(c) + " "
        return ans
        # return a string representing the deck

#define event handlers for buttons
def deal():
    global outcome, in_play, theDeck, playerhand, househand, score
    if in_play:
        outcome = "House winds by default!"
        score -= 1
    else:
        outcome = "Hit or stand?"
    in_play = True
    theDeck = Deck()
    theDeck.shuffle()
    #print theDeck
    playerhand = Hand()
    househand = Hand()
    playerhand.add_card(theDeck.deal_card())
    playerhand.add_card(theDeck.deal_card())
    househand.add_card(theDeck.deal_card())
    househand.add_card(theDeck.deal_card())
    #print "Player", playerhand, "Value:", playerhand.get_value()
    #print "House",  househand, "Value:", househand.get_value()
    #print theDeck

def hit():
    global in_play, score, outcome
    if in_play:
        playerhand.add_card(theDeck.deal_card())
        val = playerhand.get_value()
        #print "Player", playerhand, "Value:", val
        if val > 21: 
            outcome = "You are busted! House wins!"
            in_play = False
            score -= 1
            #print outcome, "Score:", score
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global score, in_play, outcome
    if playerhand.get_value() > 21:
        outcome = "You are busted."
        return None
    if not in_play:
        outcome = "Game is over."
        return None
    val = househand.get_value()
    while(val < 17):
        househand.add_card(theDeck.deal_card())
        val = househand.get_value()  
        #print "House:", househand, "Value:", val
    if (val > 21):
        # print "House is busted!"
        if playerhand.get_value() > 21:
            outcome = "House is busted, but House wins tie game!"
            score -= 1
        else: 
            outcome = "House is busted! Player wins!"
            score += 1
    else:
        if (val == playerhand.get_value()):
            outcome = "House wins ties!"
            score -= 1
        elif (val > playerhand.get_value()):
            outcome = "House wins!"
            score -= 1
        else:
            outcome = "Player wins!"
            score += 1
    in_play = False
    #print outcome, "Score:", score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

# sim
# performs Monte Carlo simulation to generate transcript 

def sim(trials):
    transcript = {}
    
    for dealer_face_score in range(1,11):
        for player_hand_value in range(1,22):
            matrix_key = '{0}{1}'.format(player_hand_value,dealer_face_score)
            transcript[matrix_key] = 0.0

    for i in range(trials):
        s = score
        bust = False
        deal()
        matrix_key = '{0}{1}'.format(playerhand.get_value(),VALUES[househand.cards[0].get_rank()])
        while not bust:
            hit()
            if (score-s) >= 0:
                try:
                    transcript[matrix_key] = transcript[matrix_key] + [1]
                except:
                    transcript[matrix_key] = [1]
            else:
                try:
                    transcript[matrix_key] = transcript[matrix_key] + [0]
                except:
                    transcript[matrix_key] = [0]
                bust = True
            matrix_key = '{0}{1}'.format(playerhand.get_value(),VALUES[househand.cards[0].get_rank()])
    # Convert created dictionary to boolean lookup table
    transcript.update({n: (numpy.mean(transcript[n])) for n in transcript.keys()})
    json.dump(transcript, open("transcript",'w'))

# hitme
# performs lookup function to transcript
def hitme(player_hand,dealerfacecard):
    transcript = json.load(open("transcript","r"))
    matrix_key = '{0}{1}'.format(player_hand,dealerfacecard)
    hit = (transcript[matrix_key] > .5)
    return hit

# play
# plays blackjack many times using the hitme function to determine whether or 
# not to hit and returns win ratio
wins = []
def play(trials):
    global in_play, score
    score = 0
    in_play = False
    for i in range(trials):
        deal()
        s = score
        while in_play:
            player_hand = playerhand.get_value()
            dealerfacecard = VALUES[househand.cards[0].get_rank()]
            if hitme(player_hand,dealerfacecard):
                hit()
            else:
                stand()
        if (score-s) > 0:
            wins.append(1)
        else:
            wins.append(0)
    print numpy.mean(wins)
    return numpy.mean(wins)
