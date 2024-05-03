import pygame as pg
import numpy as np

SCREEN_SIZE = (1000,800)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)




class Pendulum:
    def __init__(self, start_pos, length, subdivisions = 2):
        self.top_pos =  np.array(start_pos)
        self.points = np.zeros((subdivisions,2),float)
        self.last_points = self.points
        self.points[:,0] += start_pos[0]
        self.points[:,1] += self.top_pos[1] + (np.arange(subdivisions).astype(float)+1)*length/subdivisions
        self.drag = 1
        self.gravity = 1
        self.distance = length/subdivisions
    def disp(self, scr):
        pg.draw.lines(scr, WHITE, False, self.points,3)
        pg.draw.line(scr,WHITE, self.top_pos, self.points[0],3)
        pg.draw.circle(scr, (0,100,255), self.top_pos, 5)
        for i in range(self.points.shape[0]):
            pg.draw.circle(scr, RED, self.points[i], 6)
    def tick(self, dt):
        tmp = np.copy(self.points)
        self.points += self.drag*(self.points - self.last_points)
        self.points[:,1] += self.gravity * 1000 * dt ** 2
        for i in range(30):
            self.distanceJoints()
        self.last_points = tmp
    def distanceJoints(self):
        v=self.points[0] - self.top_pos
        norm = np.linalg.norm(v)
        if norm !=0:
            v = (self.distance - norm) * (v) / norm
        self.points[0] += v
        for i in range(self.points.shape[0]-1):
            v=self.points[i+1] - self.points[i]
            norm = np.linalg.norm(v)
            if norm !=0:
                v = (self.distance - norm) * (v) / norm
            self.points[i] -= v/2
            self.points[i+1] += v/2

    def set_top_position(self, new_pos):
        self.top_pos = new_pos


pg.init()

N= 20

initial_pendulum_position = np.array((500, 50))
pendulum = Pendulum(initial_pendulum_position, 800, N)
scr = pg.display.set_mode(SCREEN_SIZE)
running = True

rps = 0.1
direction_of_oscillations = np.array([30,0])
i = 0

fps = 60
dt = 1/fps
clock = pg.time.Clock()

s = pg.Surface(SCREEN_SIZE)
s.set_alpha(250)
s.fill(BLACK)

c = np.array((500,500))
r = 100

def f(i):
    return

while running:
    s.fill(BLACK)
    pendulum.disp(s)
    scr.blit(s,(0,0))
    pendulum.tick(dt)
    i+=1
    #pendulum.set_top_position(c + r * np.array((np.sin(2*i*np.pi*rps) ,np.cos(2*i*np.pi*rps))) + 0.5*r * np.array((np.sin((2*i*(1.5 * rps) +0.2)*np.pi) ,np.cos((2*i*(1.5 * rps) +0.2)*np.pi))))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False ; print("STOP")

    if pg.mouse.get_pressed()[0]:
        pendulum.set_top_position(np.array(pg.mouse.get_pos()))

    pg.display.flip()
    dtt = clock.tick(fps)
    pg.display.set_caption(str(round(1000/dtt)) + ' fps')
pg.quit()
