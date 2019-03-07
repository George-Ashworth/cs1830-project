try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame as simplegui

message = "Welcome!"


def click():
    global message
    message = "Good job!"


def draw(canvas):
    canvas.draw_text(message, [50, 112], 48, "Red")


frame = simplegui.create_frame("Home", 300, 200)
frame.add_button("Click me", click)
frame.set_draw_handler(draw)

frame.start()
