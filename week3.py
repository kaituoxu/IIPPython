# template for "Stopwatch: The Game"
import simplegui

# define global variables
time_count = 0
stop_count = 0
succ_count = 0
is_stop = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minute = t / 600
    second_h = t % 600 / 100
    second_l = t % 600 % 100 /10
    second_tenth = t % 600 % 10
    return str(minute) + ":" + \
        str(second_h) + str(second_l) + "." + \
        str(second_tenth)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_stop
    timer.start()
    is_stop = False
    
def stop():
    '''
    If you manage to stop the watch on a whole second, you win one score.
    Hitting the "Stop" button when the timer is already stopped 
    does not change your score
    '''
    global stop_count, succ_count, is_stop
    timer.stop()
    if is_stop == False:
        stop_count += 1
        if time_count % 10 == 0:
            succ_count += 1
        is_stop = True
    
    
def reset():
    '''
    reset timer and stop timer
    reset score
    if you want to start timer, you should press button "Start"
    '''
    global time_count, stop_count, succ_count
    time_count = 0
    stop_count = 0
    succ_count = 0
    timer.stop()

# define event handler for timer with 0.1 sec interval
def tick():
    global time_count
    time_count += 1

# define draw handler
def draw(canvas):
    '''
    draw time in middle of the canvas
    draw score in the upper right-hand part of the canvas
    '''
    canvas.draw_text(format(time_count), [80, 110], 48, "White")
    canvas.draw_text(str(succ_count), [220, 30], 24, "Yellow")
    canvas.draw_text("/", [245, 30], 26, "Yellow")
    canvas.draw_text(str(stop_count), [270, 30], 24, "Yellow")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
