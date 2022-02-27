try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math

WIDTH = 600*2
HEIGHT = 400*2
ball_pos = [WIDTH / 2, HEIGHT / 2]
BALL_RADIUS = 15
ball_color = "Red"
background = "https://img001.prntscr.com/file/img001/RqF7IWXpTcyjd51G4YkfQw.png"


class Ball:    
    def  __init__(self, pos, vel, radius, color, background):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color
        self.background = simplegui.load_image(background)

b1 = Ball((0,0), 5, BALL_RADIUS, ball_color, background)

def distance(pt1, pt2):
    return math.sqrt( (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

def click(pos):
    global ball_pos, ball_color
    ball_pos = list(pos)
    ball_color = "Red"
    if 500 < ball_pos[0] < 695 and 215 < ball_pos[1] < 590:
        print("Nice!")


    
    
def draw(canvas):
    canvas.draw_image(b1.background, (1440/2, 900/2), (1440, 900), (300*2, 200*2), (600*2, 400*2))
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "Black", ball_color)

    
def start():
    frame = simplegui.create_frame("Main Menu", WIDTH, HEIGHT)
    frame.set_mouseclick_handler(click)
    frame.set_draw_handler(draw)
    frame.start()
    
start()
