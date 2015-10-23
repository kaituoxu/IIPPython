# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
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

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        s = 'Hand contains '
        for idx in range(len(self.cards)):
            s += str(self.cards[idx]) + ' ' 
        return s


    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        flag_Aces = 0
        # if the hand has Aces, flag_Aces = 1
        for card in self.cards:
            hand_value += VALUES[card.rank]
            if card.rank == 'A':
                flag_Aces = 1
        if flag_Aces == 0:
            return hand_value
        else :
            if hand_value + 10 <= 21:
                return hand_value + 10
            else :
                return hand_value
                
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        cur_pos = list(pos)
        for card in self.cards:
            card.draw(canvas,cur_pos)
            cur_pos[0] += 100
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        card = self.cards.pop()
        return card
    
    def __str__(self):
        # return a string representing the deck
        s = 'Deck contains '
        for card in self.cards:
            s += str(card) + ' '
        return s


#define event handlers for buttons
def deal():
    global outcome, in_play
    # your code goes here
    global dealer, player
    global deck
    deck = Deck()
    dealer = Hand(); player = Hand()
    deck.shuffle()
    dealer.add_card(deck.deal_card());dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card());player.add_card(deck.deal_card())
    outcome = "Hit or stand?"  
    in_play = True

def hit():
    # replace with your code below
    global player, deck, outcome, score
    # if the hand is in play, hit the player
    if in_play:
        # Should this condition include equal to 21?
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            # if busted, assign a message to outcome, update in_play and score
            if player.get_value() > 21:
                outcome = "You have busted."
                score -= 1
    
       
def stand():
    # replace with your code below
    global dealer, deck, in_play, outcome, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    if in_play:
        if player.get_value() > 21:
            outcome = "You have busted!"
        else :
            while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())
            if dealer.get_value() > 21:
                outcome = "Dealer has busted!"
                score += 1
            else :
                if dealer.get_value() >= player.get_value():
                    outcome = "Dealer wins!"
                    score -= 1
                else :
                    outcome = "Player wins!"
                    score += 1    
    in_play = False
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    d_pos = [50, 200]
    p_pos = [50, 400]
    dealer.draw(canvas, d_pos)
    player.draw(canvas, p_pos)
    if in_play:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [d_pos[0] + CARD_CENTER[0], d_pos[1] + CARD_CENTER[1]], CARD_SIZE) 
    canvas.draw_text(outcome, [200, 150], 30, "White")
    canvas.draw_text("Blackjack", [50, 50], 50, "White")
    canvas.draw_text("Dealer", [50, 170], 30, "Yellow")
    canvas.draw_text("Player", [50, 370], 30, "Yellow")
    canvas.draw_text("score: "+str(score), [450, 100], 30, "White")
        

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
