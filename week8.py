# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
MAX_ROCKS = 12
score = 0
lives = 3
time = 0
started = False
num_of_rock = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.ANGLE_VLE_CHANGE = 0.05
        self.FRICTION = 0.01
        
    def draw(self,canvas):
        if self.thrust == False:
            self.image_center[0] = self.image_size[0] / 2
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            self.image_center[0] = self.image_size[0] + self.image_size[0] / 2
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0])%WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])%HEIGHT
        self.angle += self.angle_vel
        if self.thrust == True:
            acc = angle_to_vector(self.angle)
        else :
            acc = [0, 0]
        self.vel[0] *= (1 - self.FRICTION)
        self.vel[1] *= (1 - self.FRICTION)
        self.vel[0] += acc[0] * .1
        self.vel[1] += acc[1] * .1
        
    def angle_vel_inc(self):
        self.angle_vel += self.ANGLE_VLE_CHANGE
    
    def angle_vel_dec(self):
        self.angle_vel -= self.ANGLE_VLE_CHANGE
        
    def thrust_on(self):
        self.thrust = True
        ship_thrust_sound.play()
        
    def thrust_off(self):
        self.thrust = False
        ship_thrust_sound.rewind()
        
    def shoot(self):
        global missile_group
        acc = angle_to_vector(self.angle)
        # shoot from the tip of ship's 'caanon'
        pos = [self.pos[0] + acc[0] * self.radius, self.pos[1] + acc[1] * self.radius]
        # make the speed of missile is appropriate
        vel = [self.vel[0] + acc[0] * 3, self.vel[1] + acc[1] * 3]
        a_missile = Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound) 
        missile_group.add(a_missile)
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, 
                              [self.image_center[0] + self.age*self.image_size[0], self.image_center[1]],
                              self.image_size,
                              self.pos, self.image_size, self.angle)
            self.age += 1          
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
     
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0])%WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])%HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        # return False means remove this sprite
        if self.age >= self.lifespan:
            return False
        else:
            return True
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_obj):
        if (dist(self.pos, other_obj.get_position()) < self.radius + other_obj.get_radius()):
            return True
        else :
            return False

# help function
def group_collide(group, other_obj):
    global explosion_group
    state = False
    for elem in set(group):
        if elem.collide(other_obj):
            # show explosion
            a_explosion = Sprite(elem.pos, [0, 0], elem.angle, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(a_explosion)
            # remove element
            group.remove(elem)
            state = True
    return state

def group_group_collide(groupa, groupb):
    cnt = 0
    for elem in set(groupa):
        if group_collide(groupb, elem):
            cnt += 1
            groupa.remove(elem)
    return cnt

def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        # if sprite.update return False, then remove it.
        if not sprite.update():
            group.remove(sprite)

# draw handler           
def draw(canvas):
    global time, lives, score, started, num_of_rock
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
  
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    my_ship.update()
    
    # ship and rock collide
    if group_collide(rock_group, my_ship):
        if started and lives > 0:
            lives -= 1
        else:
            started = False
            # destory all rocks
            for elem in set(rock_group):
                rock_group.remove(elem)
            num_of_rock = 0
        
    # missile and rock collide
    cnt = group_group_collide(missile_group, rock_group)
    if cnt > 0:
        if started:
            score += 30
    elif score >= 30* MAX_ROCKS:
        started = False

    # restart
    if started and lives < 3 and len(rock_group) == 0:
        started = False
    
    
    # draw lives and score
    canvas.draw_text("Lives", (50, 50), 30, "White")
    canvas.draw_text(str(lives), (80, 80), 26, "White")
    canvas.draw_text("Socre", (WIDTH - 150, 50), 30, "White")
    canvas.draw_text(str(score), (WIDTH - 120, 80), 26, "White")

    # draw splash screen
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), 
                          [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    
    
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, num_of_rock
    num_of_rock += 1
    if num_of_rock <= MAX_ROCKS:
        pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        if started:
            # the vel of rock is belong to [-1, 1]
            vel = [random.random() * 2 - 1, random.random() * 2 - 1]
        else :
            vel = [0, 0]
        # the angle vel of rock is belong to [-0.2 ~ 0.2]
        ang_vel = random.random() * .4 - 0.2
        a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
        
# keyup handler
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_off()
    else :
        pass
    
# keydown handler
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel_dec()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel_inc()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_on()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    else :
        pass

# mouse click handler
def clickstart(pos):
    global started, lives, score, num_of_rock, rock_group    
    upper_left = [0, 0]
    splash_size = splash_info.get_size()
    upper_left[0] = (WIDTH - splash_size[0]) / 2
    upper_left[1] = (HEIGHT - splash_size[1]) / 2
    if upper_left[0] < pos[0] < upper_left[0] + splash_size[0] \
        and upper_left[1] < pos[1] < upper_left[1] + splash_size[1]:
        started = True
        lives = 3
        score = 0
        rock_group = set()
        num_of_rock = 0
        soundtrack.rewind()
        soundtrack.play()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(clickstart)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
