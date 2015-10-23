# implementation of card game - Memory

import simplegui
import random

cards = []
exposed = range(16)
clicked_card_idx1 = -1
clicked_card_idx2 = -1
state = 0
turns = 0

# helper function to initialize globals
def new_game():
    global cards, exposed, turns, state
    # step 1.
    cards = range(8)
    lst2 = range(8)
    cards.extend(lst2)
    # step 3.
    random.shuffle(cards)
    # step 4.
    for i in range(16):
        exposed[i] = False
    # step 10.
    turns = 0
    state = 0


# step 5.
def find_card_idx(click_pos):
    '''
    find the index of the card that you clicked.
    '''
    for i in range(16):
        if i * 50 <= click_pos[0] and click_pos[0] < i * 50 + 50:
            return i
        
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global clicked_card_idx1, clicked_card_idx2
    global exposed, state, turns
    # step 5.
    clicked_card_idx = find_card_idx(pos)
    # step 6.
    # if the card is exposed, ignore the click
    if exposed[clicked_card_idx] == False:
        exposed[clicked_card_idx] = True    
    else:
        return
    # step 7.
    if state == 0:
        state = 1
        clicked_card_idx1 = clicked_card_idx
    elif state == 1:
        state = 2
        clicked_card_idx2 = clicked_card_idx
    elif state == 2:
        # step 8.
        if cards[clicked_card_idx1] != cards[clicked_card_idx2]:
            exposed[clicked_card_idx1] = False
            exposed[clicked_card_idx2] = False
        turns += 1
        state = 1
        clicked_card_idx1 = clicked_card_idx
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    # step 2.
    for i in range(16):
        if exposed[i] == False:
            canvas.draw_polygon([[i * 50, 0], [i * 50 + 50, 0],
                                [i * 50 + 50, 100], [i * 50, 100]],
                                2, "Black", "Green")
        else:
            canvas.draw_text(str(cards[i]), [8 + 50 * i, 75], 70, "White")
    # step 9.
    text = "Turns = " + str(turns)
    label.set_text(text)


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
