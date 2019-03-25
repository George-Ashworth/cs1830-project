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

frame_count = 0


MENU_IMG = simplegui.load_image("https://docs.google.com/uc?id=1iz6dwcVkAMKCy0bpfLWoI4WVukMnVLaQ")
CHASER_IMG = simplegui.load_image("https://docs.google.com/uc?id=1Nkn_brrWg14OfWvZZCZ8O-xyq0h9x2DI")
OB1_IMG = simplegui.load_image("https://docs.google.com/uc?id=1nYT2SptZ9KmfQBL0uis_7BDYn69aDOZ6")
OB2_IMG = simplegui.load_image("https://docs.google.com/uc?id=17Aeo3JKUsQy6k5qfHhT1zvIPXqhZfIQ7")
FLOOR_IMG = simplegui.load_image("https://docs.google.com/uc?id=1VzvuRJPH5tCuYfXYO-Paw5hgEL-weVqt")
BG_IMG = simplegui.load_image("https://docs.google.com/uc?id=166IXgm_n_i_4CL1JroWUJzqtL5cjkHsk")
UFO_IMG = simplegui.load_image("https://docs.google.com/uc?id=1xlSZB5-LkXBxtAx7eFPPKeX-WBDYEwMf")

# https://drive.google.com/file/d/1xlSZB5-LkXBxtAx7eFPPKeX-WBDYEwMf/view?usp=sharing

# Sprite sheet class that will iterate through a sheet horizontally
# assumes equal spacing

class SpriteSheet:
    def __init__(self, url, height, width, rows, cols):
        self.img = simplegui.load_image(url)
        self.height = height
        self.width = width
        self.rows = rows
        self.cols = cols
        self.frameIndex = [0, 0]
        self.frameWidth = width / rows
        self.frameHeight = height / cols
        self.frameCentreX = self.frameWidth / 2
        self.frameCentreY = self.frameHeight / 2

    def draw(self, canvas, pos_x, pos_y):
        canvas.draw_image(self.img, (self.frameWidth * self.frameIndex[0] + self.frameCentreX,
                                     self.frameHeight * self.frameIndex[1] + self.frameCentreY),
                          (self.frameWidth, self.frameHeight), (pos_x, pos_y), (self.frameWidth, self.frameHeight))

    def next_frame(self):
        if self.frameIndex[0] == self.rows - 1:
            if self.frameIndex[1] == self.cols - 1:
                self.frameIndex = [0, 0]
            else:
                self.frameIndex[1] = self.frameIndex[1] + 1
                self.frameIndex[0] = 0
        else:
            self.frameIndex[0] = self.frameIndex[0] + 1


class Chaser:

    def __init__(self):
        self.pos = Vector()
        self.height = HEIGHT
        self.width = 55
        self.rising = False
        self.counter = 0
        self.rotation = 0

    def draw(self, canvas):
        global CHASER_IMG
        canvas.draw_image(CHASER_IMG, (150, 810), (300, 1620),
                          (self.pos + Vector(self.width-5, self.height / 2)).get_p(),
                          (100, self.height), self.rotation)

    def move_chaser(self, distance):
        if self.rising:
            distance *= -1
        self.pos += Vector(0, distance)

        if self.pos.y < 0:
            self.rising = False

        if self.pos.y > 20:
            self.rising = True

        if self.counter % 5 == 0:
            self.rotation = random.randrange(-1, 1)/100
        self.counter += 1


class Player:

    def __init__(self):  # init the player of w x h halfway up the screen
        self.pos = Vector(80, HEIGHT / 2)
        self.score = 0
        self.vel = Vector()
        self.height = 40
        self.width = 20
        self.gravity = Vector(0, 9.8)
        self.running = SpriteSheet("https://docs.google.com/uc?id=1wPK7fHRx4zOP-AgjnRRNUiQvLD55ajms", 123, 126, 3, 3)
        self.jumping = SpriteSheet("https://docs.google.com/uc?id=1l8VgfNeWr4yVC1hgTF_dVnrZvN0xosRv", 123, 126, 3, 3)


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

    def player_running(self, canvas):
        global WIDTH, HEIGHT, frame_count
        if frame_count % 3 == 0:
            print(self.running.frameIndex)
            self.running.next_frame()
            if self.running.frameIndex == [2, 2]:
                self.running.frameIndex = [0, 0]
        self.running.draw(canvas, self.pos.x + self.width/2, self.pos.y - self.height/2 + 5)


class KeyHandler:  # when the player presses space, the character jumps

    def __init__(self):
        self.space = False

    def key_down(self, key):
        if key == simplegui.KEY_MAP['space']:
            self.space = True


class Obstacle:

    def __init__(self, ob_type, parent_length):
        self.ob_type = ob_type
        self.height = 40
        self.width = 40
        self.pos = Vector(random.randrange(self.width, parent_length - self.width), 0)
        self.parentPos = -1
        print(ob_type)

    def draw(self, canvas, pos):
        self.parentPos = pos
        global OB1_IMG
        global OB2_IMG

        if self.ob_type == 1:
            canvas.draw_image(OB1_IMG, (400, 400), (800, 800),
                              (self.pos + pos + Vector(self.width / 2, (-self.height / 2) + 10)).get_p(),
                              (self.width, self.height), 3.14)

        if self.ob_type == 2:
            canvas.draw_image(OB2_IMG, (125, 125), (250, 250),
                              (self.pos + pos + Vector(self.width / 2, (-self.height / 2) + 10)).get_p(),
                              (self.width, self.height), 1.59)

    def get_type(self):
        return self.ob_type


class Floor:
    def __init__(self, player, start=False):
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
                gen_ob = random.randrange(1, 3)
                o = Obstacle(gen_ob, self.length)
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
        global FLOOR_IMG
        canvas.draw_image(FLOOR_IMG, (500, 791 // 2), (1000, 791),
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


            # if player hits an object
            if self.player.pos.x >= self.other.pos.x + xOffset + 5 and \
                    self.player.pos.x <= self.other.pos.x + self.other.width + xOffset - 5 and \
                    self.player.pos.y >= self.other.pos.y - self.other.height + yOffset + 5:

                if not self.inCollision:
                    print("in collision")
                    self.inCollision = True
                    if self.other.ob_type == 1:

                        self.player.pos -= Vector(6, 0)
                    elif self.other.ob_type == 2:

                        self.player.pos += Vector(6, 0)
            elif self.inCollision:
                print("reverting")
                self.inCollision = False


class FloorInteraction:

    def __init__(self, player, other):
        self.player = player
        self.other = other
        self.inCollision = False

    def update(self):
        global ss




        if self.on_platform_x():
            if self.player.pos.y >= self.other.pos.y - 1:
                self.no_clipping()
                self.inCollision = True
                self.player.vel = Vector()

        elif self.off_platform_x():
            if self.falling():
                self.inCollision = False
                print("game over")
                ss.state = 0

        elif self.on_platform_x() and self.below_platform():
            ss.state = 0

        return self.inCollision

    def no_clipping(self):
        self.player.pos.y = self.other.pos.y - 1

    def off_platform_x(self):
        return (self.player.pos.x < self.other.pos.x) or self.player.pos.x > self.other.pos.x + self.other.length

    def on_platform_x(self):
        return (self.player.pos.x + self.player.width >= self.other.pos.x) & (self.player.pos.x <= self.other.pos.x + self.other.length)

    def below_platform(self):
        return self.player.pos.y + self.player.height > self.other.pos.y

    def falling(self):
        return self.player.pos.y - self.player.height  > self.other.pos.y

    def collide_left_wall(self):
        return self.player.pos.x + self.player.width == self.other.pos.x


class ChaserInteraction:
    def __init__(self, player, other):
        self.player = player
        self.other = other

    def update(self):
        if self.player.pos.x <= self.other.width:
            print("game over")
            global ss
            ss.state = 0


class Welcome:

    def __init__(self, frame):
        class UFO:
            def __init__(self):
                self.pos = Vector(random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
                self.vel = Vector(random.randrange(-WIDTH, WIDTH), random.randrange(-HEIGHT, HEIGHT)).get_normalized()*2
                self.rotation = 0
                self.counter = 0

            def draw(self, canvas):
                global UFO_IMG
                canvas.draw_image(UFO_IMG, (150, 62), (300, 124),
                                  self.pos.get_p(), (100, 41), self.rotation)

            def update(self):
                if self.pos.y >= HEIGHT:
                    self.vel = Vector(random.randrange(-WIDTH, 0),
                                      random.randrange(-HEIGHT, HEIGHT)).get_normalized() * 2
                    self.pos.y = HEIGHT
                elif self.pos.y <= 0:
                    self.vel = Vector(random.randrange(0, WIDTH),
                                      random.randrange(-HEIGHT, HEIGHT)).get_normalized() * 2
                    self.pos.y = 0

                if self.pos.x >= WIDTH:
                    self.vel = Vector(random.randrange(-WIDTH, WIDTH),
                                      random.randrange(-HEIGHT, 0)).get_normalized() * 2
                    self.pos.x = WIDTH
                elif self.pos.x <= 0:
                    self.vel = Vector(random.randrange(-WIDTH, WIDTH),
                                      random.randrange(0, HEIGHT)).get_normalized() * 2
                    self.pos.x = 0

                if self.vel.x >= 0:
                    self.rotation = 0.1
                else:
                    self.rotation = -0.1
                self.pos += self.vel
               # if self.counter % 5 == 0:
                #    self.rotation = random.randrange(-5, 5) / 100
               # self.counter += 1

        class Button:
            def __init__(self, x, y, width, height, frame):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.frame = frame

            def clickCheck(self, pos):
                global ss, SPEED
                if ss.state == 0:
                    if ((pos[0] >= self.x) & (pos[0] <= self.x + self.width) & (pos[1] >= self.y) & (
                            pos[1] <= self.y + self.height)):
                        ss = SideScroller(self.frame)
                        ss.state = 1
                        SPEED = 3
                        print("click")
                    else:
                        print("noClick")

        self.start = Button(400, 267, 150, 68, frame)
        self.ufos = []
        for i in range(0, 10):
            self.ufos.append(UFO())

        frame.set_mouseclick_handler(self.start.clickCheck)

    def draw(self, canvas):
        global WIDTH, HEIGHT, MENU_IMG
        for ufo in self.ufos:
            ufo.draw(canvas)
            ufo.update()
        canvas.draw_image(MENU_IMG, (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT), (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))


kbd = KeyHandler()


class SideScroller:
    def __init__(self, frame):
        self.floors = []
        self.p = Player()
        self.floors.append(Floor(self.p, True))
        self.c = Chaser()
        self.w = Welcome(frame)
        self.state = 0

    def draw(self, canvas):
        global SPEED, BG_IMG, WIDTH, HEIGHT, frame_count
        canvas.draw_image(BG_IMG, (960, 540), (1920, 1080),
                           (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))


        if self.state == 0:
            self.w.draw(canvas)

        elif self.state == 1:
            max_floor = len(self.floors)
            i = 0
            self.c.draw(canvas)
            inter_floor = FloorInteraction(self.p, self.floors[i])

            inter_chaser = ChaserInteraction(self.p, self.c)
            inter_chaser.update()

            self.c.move_chaser(0.5)
            self.p.movePlayer(GRAVITY)
            self.p.increment_score(SPEED)
            self.p.draw_score(canvas)
            self.p.player_running(canvas)



            while i < max_floor:
                if (i == 0) & (self.floors[i].expire_check()):
                    self.floors.pop(0)
                    i = i - 1
                else:
                    if (i == max_floor - 1) & (self.floors[i].create_check()):
                        self.floors.append(Floor(self.p))

                if inter_floor.update():  # if its colliding
                    if kbd.space:
                        self.p.movePlayer(-3.5)
                        kbd.space = False

                for o in self.floors[i].inter_obs:
                    o.update()

                inter_floor.update()

                self.floors[i].draw(canvas)

                max_floor = len(self.floors)
                i = i + 1

        frame_count += 1


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

ss = SideScroller(frame)

# Start the frame animation
frame.start()
