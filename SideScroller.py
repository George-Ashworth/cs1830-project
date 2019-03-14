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
        self.vel = Vector()
        self.height = 100
        self.width = 75
        self.gravity = Vector(0, 9.8)

    def draw(self, canvas):

        p1 = self.pos    #bottom left
        p2 = self.pos + Vector(0, -self.height)  #topleft
        p3 = self.pos + Vector(self.width, 0)  #bottom right
        p4 = self.pos + Vector(self.width, -self.height) #top right

        canvas.draw_polygon([p1.get_p(), p2.get_p(), p4.get_p(), p3.get_p()], 5, 'Yellow', 'Yellow')




    def movePlayer(self):

        acceleration = 0.025
        self.vel = self.vel + Vector(0, acceleration)
        self.pos.add(self.vel)



class KeyHandler:

    def __init__(self):
        self.space_down = False
        frame.set_keydown_handler(self.key_down)
        frame.set_keyup_handler(self.key_up)

    def key_down(self, key):
        if key == simplegui.KEY_MAP['space']:
            self.space_down = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP['space']:
            self.space_down = True


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

        global speed
        self.pos.subtract(Vector(speed, 0))

    def interaction(self, player,obstacle):

        if (player.pos.y < obstacle.pos.y):
            player.pos.y =



class SideScroller:
    def __init__(self):
        self.floors = []
        self.floors.append(Floor(True))
        self.p = Player()


    def draw(self, canvas):
        maximum = len(self.floors)
        i = 0
        while i < maximum:
            # print(str(i+1) + " of " + str(maximum))

            if (i == 0) & (self.floors[i].expire_check()):
                self.floors.pop(0)
                i = i - 1
            else:
                if (i == maximum - 1) & (self.floors[i].create_check()):
                    self.floors.append(Floor())

                self.floors[i].draw(canvas)
                self.p.draw(canvas)
                self.floors[i].interaction(self.p)
                self.p.movePlayer()

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
