import Vector, random, SimpleGUICS2Pygame.simpleguics2pygame as simplegui
WIDTH = 1000
HEIGHT = 500

speed = 3


class Floor:
    def __init__(self, start=False):
        if start:
            self.pos = Vector((0, HEIGHT - 15))
            self.length = WIDTH * 1.25
        else:
            self.pos = Vector(WIDTH + random.randrange(50, 200), HEIGHT - 15)
            self.length = random.randrange(100, 500)

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
        x1 = self.pos
        x2 = self.pos + Vector(0, 30)
        x3 = self.pos + Vector(self.length, 30)
        x4 = self.pos + Vector(self.length, 0)
        canvas.draw_polygon([x1.getP(), x2.getP(), x3.getP(), x4.getP()], 12, 'Green', 'Green')

        self.pos.subtract(Vector(3, 0))


class Ground:
    def __init__(self):
        self.floors = []
        self.floors.append(Floor(True))

    def draw(self, canvas):
        maximum = len(self.floors)
        i = 0
        while (i < maximum):
            print(self.floors)
            print(i)
            self.floors[i].draw(canvas)
            if self.floors[i].expireCheck():
                self.floors.pop(0)

            if (i == maximum - 1) & (self.floors[i].createCheck()):
                self.floors.append(Floor())

            maximum = len(self.floors)
            i = i + 1


ground = Ground()


# Handler to draw on canvas
def draw(canvas):
    ground.draw(canvas)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
