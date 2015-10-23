# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

flag = 0
#if range is [0, 1000), flag = 1

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, remain, flag
    if flag == 0:
        range100()
    else:
        range1000()
    # print secret_number


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_number, remain, flag
    secret_number = random.randrange(0, 100)
    remain = 7
    flag = 0
    print "===================="
    print "New game. Range is [0,100)"
    print "Number of remaining guesses is 7"
    print ""



def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number, remain, flag
    secret_number = random.randrange(0, 1000)
    remain = 10
    flag = 1
    print "===================="
    print "New game. Range is [0,1000)"
    print "Number of remaining guesses is 10"
    print ""
    
    
def input_guess(guess):
    # main game logic goes here	
    global secret_number, remain
    guess_number = int(guess)
    remain -= 1
    print "Guess was", guess_number
    if remain < 0:
        print "You ran out of guesses. The number was", secret_number
        new_game()
    else:
        print "Number of remaining guesses is", remain
        if guess_number == secret_number:
            print "Correct!"
            new_game()
        elif guess_number < secret_number:#PS here
            print "Higher!"
        else:
            print "Lower!"
    print ""

    
# create frame
frame = simplegui.create_frame("Guess the number", 300, 300)

# register event handlers for control elements and start frame
frame.add_input("Enter Your Guess", input_guess, 200)
frame.add_button("New Game", new_game, 200)
frame.add_button("Range is [0,100)", range100, 200)
frame.add_button("Range is [0,1000)", range1000, 200)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
