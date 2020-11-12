import pygame
import pandas as pd

#Variables
WIDTH=1200
HEIGHT=600
BORDER=20
VELOCITY=15
FRAMERATE=35

#Define classes
class Ball:

    RADIUS = 15

    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def show(self, color):
        global screen
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)

    def update(self):
        global bgColor, ballColor

        newx = self.x + self.vx
        newy = self.y + self.vy

        if newx < BORDER + self.RADIUS or (newx > WIDTH-paddle.WIDTH-self.RADIUS\
        and paddle.y-newy<=paddle.HEIGHT and paddle.y-newy>=-paddle.HEIGHT):
            self.vx = -self.vx
        elif newy < BORDER + self.RADIUS or newy > HEIGHT - BORDER - self.RADIUS:
            self.vy = -self.vy
        else: 
            self.show(bgColor)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.show(ballColor)

class Paddle:
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, y):
        self.y = y

    def show(self, color):
        global screen
        pygame.draw.rect(screen, color, pygame.Rect(WIDTH - self.WIDTH,self.y- self.HEIGHT//2,self.WIDTH,self.HEIGHT))

    def update(self, newY):
        #newY = pygame.mouse.get_pos()[1]
        if newY - self.HEIGHT//2 >= BORDER and newY + self.HEIGHT//2 <= HEIGHT - BORDER:
            self.show(pygame.Color("black"))
            self.y = newY
            self.show(pygame.Color("white"))



#Draw the scenario
pygame.init()

screen = pygame.display.set_mode(size=(WIDTH, HEIGHT), flags=0, depth=0, display=0, vsync=0)

fgColor=pygame.Color("blue")
bgColor=pygame.Color("black")
ballColor=pygame.Color("white")

#filling the background
screen.fill(bgColor)

#drawing the walls
pygame.draw.rect(screen, fgColor, pygame.Rect(0,0,WIDTH,BORDER))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,0,BORDER,HEIGHT))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,HEIGHT-BORDER,WIDTH,BORDER))

#draw the ball and the paddle

ball = Ball(WIDTH - Ball.RADIUS - Paddle.HEIGHT,HEIGHT//2, -VELOCITY, -VELOCITY)
ball.show(ballColor)

paddle = Paddle(HEIGHT//2)
paddle.show(ballColor)

clock = pygame.time.Clock()

#sample = open("game.csv","w")

#print("x,y,vx,vy,Paddle.y", file=sample)

pong = pd.read_csv('game1.csv')
pong = pong.drop_duplicates()

X = pong.drop(columns="Paddle.y")
y = pong['Paddle.y']

from sklearn.neighbors import KNeighborsRegressor

clf = KNeighborsRegressor(n_neighbors=3)
clf = clf.fit(X,y)

df = pd.DataFrame(columns=['x','y','vx','vy'])

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
       
    clock.tick(FRAMERATE)
    #visualise the changes you just made
    pygame.display.flip()

    toPredict = df.append({'x' : ball.x, 'y' : ball.y, 'vx' : ball.vx, 'vy' : ball.vy}, ignore_index=True)

    shouldMove = clf.predict(toPredict)

    paddle.update(shouldMove)

    ball.update()

    #print("{},{},{},{},{}".format(ball.x,ball.y,ball.vx,ball.vy,paddle.y), file=sample)
    
pygame.quit()