# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor is tested to run in recent versions of
# Chrome, Firefox, and Safari.


# things to do:
# draw the player
# add space bar event for jumping


from Vector import Vector
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 960
HEIGHT = 540

speed = 3


class Player:

    def __init__(self):
        self.pos = Vector(50, HEIGHT / 2)
        self.vel = 0
        self.height = 100


class Obstacle:
    def __init__(self, obType, parentLength):
        self.obType = obType
        self.height = 20
        self.width = 20
        self.pos = Vector(random.randrange(self.width, parentLength - self.width), -self.height / 2)

    def draw(self, canvas, pos):
        x1 = self.pos + pos
        x2 = x1 + Vector(0, -self.height)
        x3 = x1 + Vector(self.width, -self.height)
        x4 = x1 + Vector(self.width, 0)
        canvas.draw_polygon([x1.getP(), x2.getP(), x3.getP(), x4.getP()], 12, 'Blue', 'Blue')


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

    def expireCheck(self):
        if self.pos.x + self.length <= 0:
            return True
        else:
            return False

    def createCheck(self):
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
        canvas.draw_polygon([x1.getP(), x2.getP(), x3.getP(), x4.getP()], 12, 'Green', 'Green')

        global speed
        self.pos.subtract(Vector(speed, 0.1))

    def interaction(self, player):

        if (player.pos.x == self.pos.x - 5):
            if (player.pos.y + player.height / 2 > self.pos.y):
                # run along the platform
                player.pos.y = self.pos.y + self.height + player.height / 2
            else:
                print("falls off")
        else:
            print("shouldnt ever get here, you havent initialised the player yet")

        if (player.pos.x >= self.pos.x and player.pos.x <= self.pos.x + self.length):
            if (player.pos.y + player.height / 2 > self.pos.y + self.height):
                if (player.vel < 0):
                    player.vel = 0
                    player.pos.y = self.pos.y + self.height + player.height / 2


class SideScroller:
    def __init__(self):
        self.floors = []
        self.floors.append(Floor(True))
        self.p = Player()

    def draw(self, canvas):
        maximum = len(self.floors)
        i = 0
        while (i < maximum):
            # print(str(i+1) + " of " + str(maximum))

            if (i == 0) & (self.floors[i].expireCheck()):
                self.floors.pop(0)
                i = i - 1
            else:
                if (i == maximum - 1) & (self.floors[i].createCheck()):
                    self.floors.append(Floor())

                self.floors[i].draw(canvas)
                self.floors[i].interaction(self.p)
                # self.p.draw(canvas)

            maximum = len(self.floors)
            i = i + 1


ss = SideScroller()


# Handler to draw on canvas
def draw(canvas):
    global speed
    ss.draw(canvas)
    speed += 0.0008
    # print(speed)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
