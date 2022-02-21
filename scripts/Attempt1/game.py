
import random, simplegui
from user305_o32FtUyCKk_0 import Vector


CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

class Wall:
    def __init__(self, x, border, color, wall_pos):
        self.x = x
        self.border = border
        self.color = color
        self.normal = Vector(1,0)
        
        self.wall_pos = wall_pos
        
        self.edge_r = x + self.border

    def draw(self, canvas):
        canvas.draw_line((self.x, 0),
                         (self.x, CANVAS_HEIGHT),
                         self.border*2+1,
                         self.color)

    def hit(self, ball):
        if self.wall_pos == "Left":
            h = (ball.offset_l() <= self.edge_r)
        
        if self.wall_pos == "Right":
            h = (ball.offset_l() >= self.edge_r)
        return h


class Ball:
    def __init__(self, pos, vel, radius, color,walls):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.color = color
        self.walls = walls
        
    def offset_l(self):
        for wall in self.walls:
            if wall.wall_pos == "Right":
                return self.pos.x + self.radius

            if wall.wall_pos == "Left":
                return self.pos.x - self.radius
        
    def bounce(self, normal):
        self.vel.reflect(normal)
        
    def update(self):
        self.pos.add(self.vel)
        
    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           1,
                           self.color,
                           self.color)
        
class Interaction:
    def __init__(self, balls,walls, background_image):
        self.balls = balls
        self.in_collision = set()
        self.walls = walls
        self.in_wall_collision = False
        self.background_image = simplegui.load_image(background_image)
        
        
    def hit(self, b1, b2):
        b1subb2 = b1.pos.copy().subtract(b2.pos)
        return b1subb2.length() < b1.radius + b2.radius
    
    def do_bounce(self, b1, b2):
        b1subb2 = b1.pos.copy().subtract(b2.pos)
       
        unit = b1subb2.copy().normalize()
        parallel1 = b1.vel.get_proj(unit)
        perpendicular1 = b1.vel.copy().subtract(parallel1)
        parallel2 = b2.vel.get_proj(unit)
        perpendicular2 = b2.vel.copy().subtract(parallel2)
         
        b1.vel = parallel2 + perpendicular1
        b2.vel = parallel1 + perpendicular2
        temp = b1.vel.get_p()
   
    def collide(self, b1, b2):
        if self.hit(b1, b2):
            ball1Againstball2 = (b1, b2) in self.in_collision
            ball2Againstball1 = (b2, b1) in self.in_collision
           
            if not ball1Againstball2 and not ball2Againstball1:
                self.do_bounce(b1, b2)
                
                self.in_collision.add((b1, b2))
        else:
            self.in_collision.discard((b1, b2))
            self.in_collision.discard((b2, b1))
        
    def update(self):
        
        for ball in self.balls:
            ball.update()
            for wall in self.walls:
                if wall.hit(ball):        
                    if not self.in_wall_collision:
                        ball.bounce(wall.normal)
                        in_wall_collision = True
                else:
                    self.in_wall_collision = False
        
        for ball1 in self.balls:
            
            for ball2 in self.balls:
                if ball1 != ball2:
                    
                    self.collide(ball1, ball2)
    
    def draw(self, canvas):
        self.update()
        canvas.draw_image(self.background_image, (1440/2, 900/2), (1440, 900), (300, 200), (600, 400))
        for wall in self.walls:
            wall.draw(canvas)
        for ball in self.balls:
           
            
            ball.draw(canvas)
        
def rand_col():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return "rgb({}, {}, {})".format(r, g, b)
       
def rand_pos():
    return Vector(random.randint(0, CANVAS_WIDTH),
                  random.randint(0, CANVAS_HEIGHT))

def rand_rad():
    return (random.randint(10,30))

def rand_vel():
    return Vector(random.randint(-5, 5),
                 random.randint(-5, 5))


def rand_ball():
    return Ball(rand_pos(),
                rand_vel(),
                rand_rad(),
                rand_col())


background_image = "https://img001.prntscr.com/file/img001/dW-nfqX4T_OmcM7QMKgJCQ.png"


Walls = [Wall(CANVAS_WIDTH, 5, 'red',"Right"),Wall(0, 5, 'red',"Left")]

balls = [ Ball(Vector(300,200), Vector(3,2),20,'White', Walls),
         Ball(Vector(0,200),Vector(0,0),20,'Red', Walls),
          Ball(Vector(600,200),Vector(0,0),20,'Red',Walls),
          Ball(Vector(300,100),Vector(0,0),20,'Red',Walls),
         Ball(Vector(500,300),Vector(0,0),20,'Pink',Walls),
         Ball(Vector(200,500),Vector(0,0),30,'Red',Walls),
         Ball(Vector(100,100),Vector(0,0),50,'Red',Walls),
         Ball(Vector(300,300),Vector(0,0),40,'Green',Walls),
         Ball(Vector(150,100),Vector(0,0),30,'Red',Walls),
         Ball(Vector(400,400),Vector(0,0),40,'Pink',Walls),
         Ball(Vector(450,400),Vector(0,0),10,'Pink',Walls),
        Ball(Vector(500,400),Vector(0,0),10,'Blue',Walls),
          Ball(Vector(540,300),Vector(0,0),20,'Pink',Walls),]
interaction = Interaction(balls,Walls,background_image)

frame = simplegui.create_frame("Balls", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)

frame.start()