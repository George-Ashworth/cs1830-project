# things to do:
# decide on player model size
# obstacle interaction
# artwork
# modify value of gravity for realism?
# shooting projectiles?
# high score calculation and display
# bouncing off left wall when falling



import random
import math

try:
    import simplegui
    from user303_wxSmFEVIaV_0 import Vector
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    from Vector import Vector

WIDTH = 960
HEIGHT = 540

SPEED = 3
GRAVITY = 0.080


class Chaser:

    def __init__(self):
        self.pos = Vector()
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0
        self.p4 = 0
        self.vel = Vector(SPEED * 0.8, 0)
        self.height = HEIGHT
        self.width = 55
        self.img = simplegui.load_image("https://docs.google.com/uc?id=1Nkn_brrWg14OfWvZZCZ8O-xyq0h9x2DI")

    def draw(self, canvas):
        canvas.draw_image(self.img, (150, 810), (300, 1620),
                          (self.pos + Vector(self.width-5, self.height / 2)).get_p(), (100, self.height))

    def move_chaser(self, distance):
        self.p3 = self.p3 + distance
        self.p4 = self.p4 + distance


class Player:

    def __init__(self):  # init the player of w x h halfway up the screen
        self.pos = Vector(80, HEIGHT / 2)
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
        self.img = simplegui.load_image("https://docs.google.com/uc?id=1nYT2SptZ9KmfQBL0uis_7BDYn69aDOZ6")
        self.ob_type = ob_type
        self.height = 40
        self.width = 40
        self.pos = Vector(random.randrange(self.width, parent_length - self.width), 0)
        self.parentPos = -1

    def draw(self, canvas, pos):
        self.parentPos = pos
        canvas.draw_image(self.img, (400, 400), (800, 800),
                          (self.pos + pos + Vector(self.width / 2, (-self.height / 2)+10)).get_p(),
                          (self.width, self.height), 3.14)


class Floor:
    def __init__(self, player, start=False):
        self.img = simplegui.load_image("https://docs.google.com/uc?id=1VzvuRJPH5tCuYfXYO-Paw5hgEL-weVqt")
        self.height = random.randrange(30, 70)
        self.obstacles = []
        self.inter_obs = []
        self.start = start
        if start:
            self.pos = Vector(0, HEIGHT - 15)
            self.length = WIDTH * 1.25
        else:
            self.pos = Vector(WIDTH + random.randrange(50, 200), HEIGHT - self.height)
            self.length = random.randrange(100, 500)
            for i in range(0, random.randint(0, self.length // 100)):
                o = Obstacle(1, self.length)
                self.obstacles.append(o)
                self.inter_obs.append(ObstacleInteraction(player, o))

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
        canvas.draw_image(self.img, (500, 791 // 2), (1000, 791),
                          (self.pos + Vector(self.length/2, self.height/2)).get_p(), (self.length, self.height))

        global SPEED
        self.pos.subtract(Vector(SPEED, 0))


class ObstacleInteraction:

    def __init__(self, player, other):
        self.player = player
        self.other = other
        self.inCollision = False

    def update(self):
        if type(self.other.parentPos) != type(1):
            xOffset = self.other.parentPos.x
            yOffset = self.other.parentPos.y

            #print(str(self.other.pos.x + xOffset) + " - " + str(self.player.pos.x) + " - " + str(self.other.pos.x + self.other.width + xOffset))

            # if player hits an object
            if self.player.pos.x >= self.other.pos.x + xOffset + 5and \
                    self.player.pos.x <= self.other.pos.x + self.other.width + xOffset - 5and \
                    self.player.pos.y >= self.other.pos.y - self.other.height + yOffset + 5:
                if not self.inCollision:
                    print("in collision")
                    self.inCollision = True
                    self.player.pos -= Vector(6, 0)
            elif self.inCollision:
                print("reverting")
                self.inCollision = False


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


class ChaserInteraction:
    def __init__(self, player, other):
        self.player = player
        self.other = other

    def update(self):
        if self.player.pos.x <= self.other.width:
            print("game over")
            frame.stop()


kbd = KeyHandler()


class SideScroller:
    def __init__(self):
        self.floors = []
        self.p = Player()
        self.floors.append(Floor(self.p, True))
        self.c = Chaser()

    def draw(self, canvas):
        global SPEED
        max_floor = len(self.floors)
        i = 0
        j = 0
        self.c.draw(canvas)
        inter_floor = FloorInteraction(self.p, self.floors[i])

        inter_chaser = ChaserInteraction(self.p, self.c)
        inter_chaser.update()

        self.c.move_chaser(5)
        self.p.movePlayer(GRAVITY)
        self.p.increment_score(SPEED)
        self.p.draw_score(canvas)

        self.p.draw(canvas)

        while i < max_floor:
            if (i == 0) & (self.floors[i].expire_check()):
                self.floors.pop(0)
                i = i - 1
            else:
                if (i == max_floor - 1) & (self.floors[i].create_check()):
                    self.floors.append(Floor(self.p))

            if inter_floor.update():  # if its colliding
                if kbd.space:
                    self.p.movePlayer(-5)
                    kbd.space = False

            for o in self.floors[i].inter_obs:
                o.update()

            inter_floor.update()

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
