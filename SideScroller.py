# things to do:
# decide on player model size
# obstacle interaction
# artwork
# modify value of gravity for realism?
# shooting projectiles?
# high score calculation and display
# bouncing off left wall when falling



from Vector import Vector
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 960
HEIGHT = 540

SPEED = 3
GRAVITY = 0.020



class Player:

    def __init__(self):  # init the player of w x h halfway up the screen
        self.pos = Vector(50, HEIGHT / 2)
        self.vel = Vector()
        self.height = 40
        self.width = 20
        self.gravity = Vector(0, 9.8)

    def draw(self, canvas):  # draw the player
        p1 = self.pos  # bottom left
        p2 = self.pos + Vector(0, -self.height)  # topleft
        p3 = self.pos + Vector(self.width, 0)  # bottom right
        p4 = self.pos + Vector(self.width, -self.height)  # top right

        canvas.draw_polygon([p1.get_p(), p2.get_p(), p4.get_p(), p3.get_p()], 5, 'Yellow', 'Yellow')

    def movePlayer(self, yVal):  # this moves the player in the y direction
        global GRAVITY
        self.vel = self.vel + Vector(0, yVal)
        self.pos.add(self.vel)


class KeyHandler: # when the player presses space, the character jumps

    def __init__(self):
        self.space = False

    def key_down(self, key):
        if key == simplegui.KEY_MAP['space']:
            self.space = True



class Obstacle:

    def __init__(self, ob_type, parent_length):
        self.ob_type = ob_type
        self.height = 20
        self.width = 20
        self.pos = Vector(random.randrange(self.width, parent_length - self.width), 0)

    def draw(self, canvas, pos):
        x1 = self.pos + pos
        x2 = x1 + Vector(0, -self.height)
        x3 = x1 + Vector(self.width, -self.height)
        x4 = x1 + Vector(self.width, 0)
        canvas.draw_polygon([x1.get_p(), x2.get_p(), x3.get_p(), x4.get_p()], 12, 'Blue', 'Blue')


class Floor:
    def __init__(self, start=False):
        self.height = random.randrange(30, 70)
        self.obstacles = []
        if start:
            self.pos = Vector(0, HEIGHT - 15)
            self.length = WIDTH * 1.25
        else:
            self.pos = Vector(WIDTH + random.randrange(50, 200), HEIGHT - self.height)
            self.length = random.randrange(100, 500)
            for i in range(0, random.randint(0, self.length // 100)):
                self.obstacles.append(Obstacle(1, self.length))

    def expire_check(self):
        if self.pos.x + self.length <= 0:
            return True
        else:
            return False

    def create_check(self):
        if self.pos.x + self.length <= WIDTH:
            return True
        else:
            return False

    def draw(self, canvas):
        for obstacle in self.obstacles:
            obstacle.draw(canvas, self.pos)

        x1 = self.pos
        x2 = self.pos + Vector(0, self.height)
        x3 = self.pos + Vector(self.length, self.height)
        x4 = self.pos + Vector(self.length, 0)
        canvas.draw_polygon([x1.get_p(), x2.get_p(), x3.get_p(), x4.get_p()], 12, 'Green', 'Green')

        global SPEED
        self.pos.subtract(Vector(SPEED, 0))


class Interaction:

    def __init__(self, player, other):

        self.player = player
        self.other = other
        self.inCollision = False

    def update(self):

        if self.on_platform_x():
            if self.player.pos.y >= self.other.pos.y - 1:
                self.no_clipping()
                self.inCollision = True
                self.player.vel = Vector()

        elif self.off_platform_x():
            if self.falling():
                if self.collide_left_wall():
                    print("left wall")
                else:
                    self.inCollision = False
                    print("game over")
                    frame.stop()

        return self.inCollision

    def no_clipping(self):
        self.player.pos.y = self.other.pos.y - 1

    def off_platform_x(self):
        return (self.player.pos.x < self.other.pos.x) or self.player.pos.x > self.other.pos.x + self.other.length

    def on_platform_x(self):
        return (self.player.pos.x + self.player.width >= self.other.pos.x) & (self.player.pos.x      <= self.other.pos.x + self.other.length)

    def falling(self):
        return self.player.pos.y - self.player.height - self.player.height > self.other.pos.y

    def collide_left_wall(self):
        return self.player.pos.x + self.player.width == self.other.pos.x


kbd = KeyHandler()


class SideScroller:

    def __init__(self):
        self.floors = []
        self.floors.append(Floor(True))
        self.p = Player()

    def draw(self, canvas):
        maximum = len(self.floors)
        i = 0
        inter = Interaction(self.p, self.floors[i ])

        if inter.update(): #if its colliding
            if kbd.space:
                self.p.movePlayer(-2.5)
                kbd.space = False


        while i < maximum:
            if (i == 0) & (self.floors[i].expire_check()):
                self.floors.pop(0)
                i = i - 1
            else:
                if (i == maximum - 1) & (self.floors[i].create_check()):
                    self.floors.append(Floor())

                self.floors[i].draw(canvas)
                self.p.draw(canvas)
                inter.update()
                self.p.movePlayer(GRAVITY)

            maximum = len(self.floors)
            i = i + 1


ss = SideScroller()


# Handler to draw on canvas
def draw(canvas):
    global SPEED
    ss.draw(canvas)
    SPEED += 0.001
    # print(SPEED)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.key_down)

# Start the frame animation
frame.start()
