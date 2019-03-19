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
import math

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 960
HEIGHT = 540

SPEED = 3
GRAVITY = 0.020


class Chaser:

    def __init__(self):
        self.pos = Vector()
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0
        self.p4 = 0
        self.vel = Vector(SPEED * 0.8, 0)
        self.height = HEIGHT
        self.width = 50

    def draw(self, canvas):
        p1 = self.pos  # bottom left
        p2 = self.pos + Vector(0, + self.height)  # topleft
        p3 = self.pos + Vector(self.width, 0)  # bottom right
        p4 = self.pos + Vector(self.width, + self.height)  # top right
        canvas.draw_polygon([p1.get_p(), p2.get_p(), p4.get_p(), p3.get_p()], 5, 'Red', 'Red')

    def move_chaser(self, distance):
        self.p3 = self.p3 + distance
        self.p4 = self.p4 + distance


class Player:

    def __init__(self):  # init the player of w x h halfway up the screen
        self.pos = Vector(75, HEIGHT / 2)
        self.score = 0
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


    def draw_score(self, canvas):
        global WIDTH
        canvas.draw_text(str(self.score), (WIDTH - 100, 20), 12, 'White')


    def movePlayer(self, yVal):  # this moves the player in the y direction
        global GRAVITY
        self.vel = self.vel + Vector(0, yVal)
        self.pos.add(self.vel)


    def increment_score(self, speed):
        self.score += speed * 1.5
        self.score = math.floor(self.score)


class KeyHandler:  # when the player presses space, the character jumps

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


class ObstacleInteraction:

    def __init__(self, player, other):
        self.player = player
        self.other = other
        self.inCollision = False

    def update(self):
        # if player hits an object
        if self.player.pos.x == self.other.pos.x and self.player.pos.y == self.other.pos.y:
            self.inCollision = True
            print("colliding with obstacle")


class FloorInteraction:

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
                self.inCollision = False
                print("game over")
                frame.stop()

        return self.inCollision

    def no_clipping(self):
        self.player.pos.y = self.other.pos.y - 1

    def off_platform_x(self):
        return (self.player.pos.x < self.other.pos.x) or self.player.pos.x > self.other.pos.x + self.other.length

    def on_platform_x(self):
        return (self.player.pos.x + self.player.width >= self.other.pos.x) & (self.player.pos.x <= self.other.pos.x + self.other.length)

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
        self.c = Chaser()


    def draw(self, canvas):
        global SPEED
        max_floor = len(self.floors)
        i = 0
        j = 0

        inter_floor = FloorInteraction(self.p, self.floors[i])

        while i < max_floor:
            if (i == 0) & (self.floors[i].expire_check()):
                self.floors.pop(0)
                i = i - 1
            else:
                if (i == max_floor - 1) & (self.floors[i].create_check()):
                    self.floors.append(Floor())

            if inter_floor.update():  # if its colliding
                if kbd.space:
                    self.p.movePlayer(-2.5)
                    kbd.space = False

            for o in self.floors[i].obstacles:
                inter_obs = ObstacleInteraction(self.p, o)

                inter_obs.update()

            inter_floor.update()
            self.c.move_chaser(5)
            self.p.movePlayer(GRAVITY)
            self.p.increment_score(SPEED)
            self.p.draw_score(canvas)
            self.c.draw(canvas)
            self.p.draw(canvas)
            self.floors[i].draw(canvas)

            max_floor = len(self.floors)
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
