import random
import pygame as pg
pg.init()

blocks=[
    [
        [0,1,0],
        [0,1,1],
        [0,1,0]],
    [
        [0,1,1],
        [0,1,0],
        [0,1,0]
    ],
    [
        [1,1,0],
        [0,1,0],
        [0,1,0],
    ],
    [
        [0,0,0],
        [0,1,1],
        [1,1,0],
    ],
    [
        [0,0,0],
        [1,1,0],
        [0,1,1],
    ],
    [
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
    ],
    [
        [1,1],
        [1,1]
    ]
]

w,h=8,20
x,y=w//2,-3
c=pg.display.set_mode((w*16+84,h*16))
score=0
tet=pg.image.load('tiles\\tet.png')

nums=[
    pg.image.load('tiles\\0.png'),
    pg.image.load('tiles\\1.png'),
    pg.image.load('tiles\\2.png'),
    pg.image.load('tiles\\3.png'),
    pg.image.load('tiles\\4.png'),
    pg.image.load('tiles\\5.png'),
    pg.image.load('tiles\\6.png'),
    pg.image.load('tiles\\7.png'),
    pg.image.load('tiles\\8.png'),
    pg.image.load('tiles\\9.png'),
    ]
GO = pg.image.load('tiles\\game_over.png')
sc = pg.image.load('tiles\\score.png')

field = []
for i in range(h):
    field.append([0]*w)

def collide(b,x,y):
    global field
    for i in range(len(b)):
        for j in range(len(b[i])):
            #if i+y>=0:
            if j+x>=0:
                if (i+y>=len(field) or j+x>=len(field[0])) and b[i][j]==1:
                    return(False)
                if not(i+y>=len(field) or j+x>=len(field[0])):
                    if i+y>=0:
                        if b[i][j]+field[i+y][j+x]>1:
                            return(False)
            elif b[i][j]==1:
                return(False)
    return(True)
def rot_l(b):
    nb=[]
    for i in range(len(b)):
        nb.append([])
        for j in range(len(b[0])):
            nb[i].append(0)
    for i in range(len(b)):
        for j in range(len(b)):
            nb[i][j]=b[j][len(b)-1-i]
    return(nb)

def rot_r(b):
    nb=[]
    for i in range(len(b)):
        nb.append([])
        for j in range(len(b[0])):
            nb[i].append(0)
    for i in range(len(b)):
        for j in range(len(b)):
            nb[i][j]=b[len(b)-1-j][i]
    return(nb)

def stop(b,x,y):
    global field
    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j]==1:
                field[i+y][j+x]+=b[i][j]
def check():
    global field,score
    k=[]
    t=[1]*len(field[0])
    d=[0]*len(field[0])
    for i in range(len(field)):
        if field[i]==t:
            k.append(i)
    for i in range(len(k)):
        field.remove(field[k[i]])
        field.insert(1,d)
    score+=10*len(k)
run=True
b=random.choice(blocks)
k=0
fg=True
while run:
    delay=int(50-(score/100))
    pg.time.delay(delay)
    k+=1
    t=True
    for ev in pg.event.get():
        if ev.type==pg.QUIT:
            run=False
            fg=False
    keys=pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        if collide(b,x-1,y):
            x-=1
    if keys[pg.K_RIGHT]:
        if collide(b,x+1,y):
            x+=1
    if keys[pg.K_DOWN]:
        if collide(b,x,y+1):
            y+=1
        elif y<0:
            run=False
        else:
            stop(b,x,y)
            score+=1
            b=random.choice(blocks)
            x,y=w//2,-4
    elif k%25==0:
        if collide(b,x,y+1):
            y+=1
        elif y<0:
            run=False
        else:
            stop(b,x,y)
            score+=1
            b=random.choice(blocks)
            x,y=w//2,-4
    if keys[pg.K_UP] and k%2==0:
        nb=rot_r(b)
        if collide(nb,x,y):
            b=nb
    check()
    c.fill((144,144,171))
    pg.draw.rect(c,(0,0,140),(0,0,w*16,h*16))
    for i in range(h):
        for j in range(w):
            if field[i][j]==1:
                c.blit(tet,(j*16,i*16))
            elif (i>=y and i<y+len(b)) and (j>=x and j<x+len(b)):
                if field[i][j]+b[i-y][j-x]>=1:
                    c.blit(tet,(j*16,i*16))
    c.blit(sc,(w*16+2,2))
    t=str(score).zfill(6)
    for i in range(len(t)):
        c.blit(nums[int(t[i])],(w*16+2+9*i,15))
    pg.display.update()
if fg:
    c.blit(GO,((w//2)*16-28,(h//2)*16-6))
    pg.display.update()
else:
    pg.quit()
