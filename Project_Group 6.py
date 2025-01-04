from datetime import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


ship_x,ship_y=450,150
boss_x,boss_y,boss_health=450,700,100
wave1,wave2,wave3,power_ups=[],[],[],[]
wave1_state=True
wave2_state=False
wave3_state=False
power_ups_state=False
boss_state=False
pause = False
start_time=time.time()
bullets=[]
boss_bullet=[]
bullet_count=1
bullet_speed=2
score=0
life=3
last_boss_shot = time.time()


def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx <= 0 <= dy:
            zone = 3
        elif dx <= 0 and dy <= 0:
            zone = 4
        elif dx >= 0 >= dy:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx <= 0 <= dy:
            zone = 2
        elif dx <= 0 and dy <= 0:
            zone = 5
        elif dx >= 0 >= dy:
            zone = 6
    return zone


def zone0(zone, x, y):
    if zone == 0:
        x1 = x
        y1 = y
    elif zone == 1:
        x1 = y
        y1 = x
    elif zone == 2:
        x1 = y
        y1 = -x
    elif zone == 3:
        x1 = -x
        y1 = y
    elif zone == 4:
        x1 = -x
        y1 = -y
    elif zone == 5:
        x1 = -y
        y1 = -x
    elif zone == 6:
        x1 = -y
        y1 = x
    elif zone == 7:
        x1 = x
        y1 = -y
    return x1, y1

def originalzone(zone, x, y):
    if zone == 0:
        x1 = x
        y1 = y
    elif zone == 1:
        x1 = y
        y1 = x
    elif zone == 2:
        x1 = -y
        y1 = x
    elif zone == 3:
        x1 = -x
        y1 = y
    elif zone == 4:
        x1 = -x
        y1 = -y
    elif zone == 5:
        x1 = -y
        y1 = -x
    elif zone == 6:
        x1 = y
        y1 = -x
    elif zone == 7:
        x1 = x
        y1 = -y
    return (x1, y1)



def draw8way(x, y, center):
    c = center[0]
    c = center[1]
    glBegin(GL_POINTS)
    glVertex2f(x + c, y + c)
    glVertex2f(y + c, x + c)
    glVertex2f(x + c, -y + c)
    glVertex2f(y + c, -x + c)
    glVertex2f(-y + c, x + c)
    glVertex2f(-x + c, y + c)
    glVertex2f(-y + c, -x + c)
    glVertex2f(-x + c, -y + c)
    glEnd()


def draw_line(x1, y1, x2, y2):
    zone = findzone(x1, y1, x2, y2)
    x1, y1 = zone0(zone, x1, y1)
    x2, y2 = zone0(zone, x2, y2)
    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    x = x1
    y = y1
    glPointSize(2)
    glBegin(GL_POINTS)
    while x <= x2:
        xo, yo = originalzone(zone, x, y)
        glVertex2f(xo, yo)

        if d <= 0:
            d += incrE
        else:
            d += incrNE
            y += 1
        x += 1
    glEnd()


def CirclePoints(x,y,cx,cy):
    glBegin(GL_POINTS)
    glVertex2f(x+cx,y+cy)
    glVertex2f(y+cx,x+cy)
    glVertex2f(y+cx,-x+cy)
    glVertex2f(x+cx,-y+cy)
    glVertex2f(-x+cx,-y+cy)
    glVertex2f(-y+cx,-x+cy)
    glVertex2f(-y+cx,x+cy)
    glVertex2f(-x+cx,y+cy)
    glEnd()

def MidpointCircle(radius,cx,cy):
    d=1-radius
    x=0
    y=radius
    CirclePoints(x,y,cx,cy)
    while x<y:
        if d<0:
            d=d+2*x+3
            x=x+1
        else:
            d=d+2*x-2*y+5
            x=x+1
            y=y-1
        CirclePoints(x,y,cx,cy)


def spaceship():
    global ship_x,ship_y
    glColor3f(1.0, 1.0, 1.0)
    draw_line(ship_x, ship_y, ship_x + 50, ship_y - 50)
    draw_line(ship_x + 50, ship_y - 50, ship_x, ship_y - 100)
    draw_line(ship_x, ship_y - 100, ship_x - 50, ship_y - 50)
    draw_line(ship_x - 50, ship_y - 50, ship_x, ship_y)
    MidpointCircle(15, ship_x, ship_y-50)
    draw_line(ship_x + 25, ship_y - 25, ship_x + 75, ship_y)
    draw_line(ship_x + 75, ship_y, ship_x + 25, ship_y - 50)
    draw_line(ship_x - 25, ship_y - 25, ship_x - 75, ship_y)
    draw_line(ship_x - 75, ship_y, ship_x - 25, ship_y - 50)
    draw_line(ship_x + 25, ship_y - 75, ship_x + 75, ship_y - 100)
    draw_line(ship_x + 75, ship_y - 100, ship_x + 25, ship_y - 50)
    draw_line(ship_x - 25, ship_y - 75, ship_x - 75, ship_y - 100)
    draw_line(ship_x - 75, ship_y - 100, ship_x - 25, ship_y - 50)

def boss():
    global boss_x,boss_y
    glColor3f(1.0, 0, 0)
    draw_line(boss_x-300,boss_y+100,boss_x+300,boss_y+100)
    draw_line(boss_x - 300, boss_y + 100, boss_x - 300, boss_y -50 )
    draw_line(boss_x + 300, boss_y + 100, boss_x + 300, boss_y - 50)
    draw_line(boss_x - 300, boss_y -50, boss_x - 150, boss_y )
    draw_line(boss_x - 150, boss_y , boss_x , boss_y -50)
    draw_line(boss_x , boss_y -50, boss_x +150, boss_y)
    draw_line(boss_x + 150, boss_y , boss_x + 300, boss_y-50 )

def boss_fight():
        global bullets, boss_bullet, last_boss_shot, boss_health, score, pause, life
        position = True
        new_boss_bullets = []
        for bx, by in boss_bullet:
            if by > 0:
                new_boss_bullets.append((bx, by - 3))
        boss_bullet[:] = new_boss_bullets
        for bx, by in boss_bullet:
            if abs(bx - ship_x) < 50 and abs(by - ship_y) < 50:
                life-=1
                print("Noob got hit by the boss!")
                boss_bullet.remove((bx, by))
                if life==0:
                    pause = True
                    print(f"Game Over For You! Your final score is: {score}")
                return
        current_time = time.time()
        if current_time - last_boss_shot >= 5:
            if position:
                boss_bullet.append((boss_x, boss_y - 50))
                boss_bullet.append((boss_x - 300, boss_y - 50))
                boss_bullet.append((boss_x + 300, boss_y - 50))
            else:
                boss_bullet.append((boss_x - 150, boss_y))
                boss_bullet.append((boss_x + 150, boss_y))
            last_boss_shot = current_time
            position=not position

        new_bullets = []
        for bullet in bullets:
            x, y = bullet
            if y < 1000:
                new_bullets.append((x, y + 2))
        bullets[:] = new_bullets

        for bullet_x, bullet_y in bullets:
            if boss_x - 300 <= bullet_x <= boss_x + 300 and bullet_y >= boss_y:
                score += 10
                bullets.remove((bullet_x, bullet_y))
                boss_health -= 1
                if boss_health <= 0:
                    pause = True
                    print(f"Congratulations! You defeated the boss. Final score: {score}")
                    break


def animate():
        global wave1,wave2,wave3,power_ups,pause,start_time,bullets,score,wave1_state,wave2_state
        global wave3_state,boss_state,life,bullet_speed,boss_health
        for x in wave1:
            if collision(x):
                life-=1
            if life==0:
                pause=True
                return
        if 20<=score<40:
            wave1_state=False
            boss_state=True
            wave1.clear()
        elif 40<=score<60:
            wave2_state = False
            wave3_state = True
            wave2.clear()
        elif 60<=score<80:
            wave3_state=False
            boss_state=True
            wave3.clear()
        if wave1_state:
            if not pause:
                new_wave =[]
                for new in wave1:
                    x,y= new
                    if y>0:
                        new_wave.append((x-0.3,y-0.3))
                wave1 = new_wave
                if len(wave1)<20:
                    while True:
                        new_x=random.randint(900,1600)
                        new_y=random.randint(1100,1500)
                        overlap=False
                        for x,y in wave1:
                            if (((new_x-x)**2+(new_y-y)**2)**0.5)<70:
                                overlap=True
                                break
                        if not overlap:
                            wave1.append((new_x,new_y))
                            break
                new_bullets=[]
                for bullet in bullets:
                    x,y=bullet
                    if y<1000:
                        new_bullets.append((x,y+bullet_speed))
                bullets=new_bullets
                for bullet in bullets:
                    for meteor in wave1:
                        bullet_x,bullet_y=bullet
                        meteor_x,meteor_y=meteor
                        if (((bullet_x-meteor_x)**2+(bullet_y-meteor_y)**2)**0.5)<=30:
                            score+=1
                            print("Score: ", score)
                            bullets.remove(bullet)
                            wave1.remove(meteor)
                            break
        if wave2_state:
            if not pause:
                new_wave = []
                for new in wave2:
                    x, y = new
                    if y > 0:
                        new_wave.append((x - 0.3, y - 0.3))
                wave2 = new_wave
                if len(wave2) < 20:
                    while True:
                        new_x = random.randint(900, 1600)
                        new_y = random.randint(1100, 1500)
                        overlap = False
                        for x, y in wave2:
                            if (((new_x - x) ** 2 + (new_y - y) ** 2) ** 0.5) < 70:
                                overlap = True
                                break
                        if not overlap:
                            wave2.append((new_x, new_y))
                            break
                new_bullets = []
                for bullet in bullets:
                    x, y = bullet
                    if y < 1000:
                        new_bullets.append((x, y + bullet_speed))
                bullets = new_bullets
                for bullet in bullets:
                    for meteor in wave2:
                        bullet_x, bullet_y = bullet
                        meteor_x, meteor_y = meteor
                        if (((bullet_x - meteor_x) ** 2 + (bullet_y - meteor_y) ** 2) ** 0.5) <= 30:
                            score += 1
                            print("Score: ", score)
                            bullets.remove(bullet)
                            wave2.remove(meteor)
                            break
        if power_ups_state:
            if not pause:
                new_power =[]
                for new in power_ups:
                    x,y,type= new
                    if y>0:
                        new_power.append((x-0.3,y-0.3))
                power_ups = new_power
                if len(power_ups)<20:
                    while True:
                        new_x=random.randint(900,1600)
                        new_y=random.randint(1100,1500)
                        overlap=False
                        for x,y in power_ups:
                            if (((new_x-x)**2+(new_y-y)**2)**0.5)<70:
                                overlap=True
                                break
                        if not overlap:
                            power_ups.append((new_x,new_y,random.choice(["Speed",'bullet','life'])))
                            break
                new_bullets=[]
                for bullet in bullets:
                    x,y=bullet
                    if y<1000:
                        new_bullets.append((x,y+bullet_speed))
                bullets=new_bullets
                for bullet in bullets:
                    for meteor in power_ups:
                        bullet_x,bullet_y=bullet
                        meteor_x,meteor_y=meteor
                        if (((bullet_x-meteor_x)**2+(bullet_y-meteor_y)**2)**0.5)<=30:
                            score+=1
                            print("Score: ", score)
                            bullets.remove(bullet)
                            wave3.remove(meteor)
                            break

        if boss_state:
            if not pause:
                boss_fight()
        glutPostRedisplay()
def keyboardListener(key,x,y):
    global ship_x,ship_y,pause
    if not pause:
        if key==b"a":
            if ship_x>=100:
                ship_x-=30
        elif key==b"d":
            if ship_x<=800:
                ship_x+=30
        elif key==b"w":
            if ship_y<=900:
                ship_y+=30
        elif key==b"s":
            if ship_y>=160:
                ship_y-=30
        elif key==b' ':
            bullets.append((ship_x,ship_y))

def mouseListener(button, state, x, y):
    global wave1,wave2,wave3,power_ups,pause,start_time,bullets,score,wave1_state,wave2_state,wave3_state,boss_state,life,bullet_speed,boss_health,ship_x,ship_y,boss_x,boss_y,boss_bullet,bullet_count
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 20 <= x <= 70 and 920 <= (1000-y) <= 970:
            ship_x, ship_y = 450, 150
            boss_x, boss_y, boss_health = 450, 700, 100
            wave1, wave2, wave3, power_ups = [], [], [], []
            wave1_state = True
            wave2_state = False
            wave3_state = False
            boss_state = False
            pause = False
            start_time = time.time()
            bullets = []
            boss_bullet = []
            bullet_count = 1
            bullet_speed = 2
            score = 0
            life = 1

        elif 450 <= x <= 500 and 920 <= (1000-y) <= 970:
            pause = not pause
            if not pause:
                glutTimerFunc(100, animate, 0)
        elif 830 <= x <= 880 and 920 <= (1000-y) <= 970:
            print(f"Your final score is: {score}")
            glutLeaveMainLoop()
def draw_buttons():
    if not pause:
        glColor3f(0, 1, 0)
        draw_line(450, 920, 450, 970)
        draw_line(500, 920, 500, 970)
    else:
        glColor3f(0, 0, 1)
        draw_line(20, 950, 70, 950)
        draw_line(20, 950, 40, 980)
        draw_line(20, 950, 40, 920)

        glColor3f(0, 1, 0)
        draw_line(450, 920, 450, 970)
        draw_line(450, 970, 500, 950)
        draw_line(500, 950, 450, 920)

        glColor3f(1, 0, 0)
        draw_line(830, 920, 880, 970)
        draw_line(830, 970, 880, 920)
def bullet_spawn():
    global bullets, boss_bullet

    glColor3f(1, 0, 0)
    for x, y in bullets:
        MidpointCircle(3, x, y)

    glColor3f(1, 1, 0)  # Yellow for boss bullets
    for x, y in boss_bullet:
        MidpointCircle(5, x, y)  # Boss bullets larger


def wave_spawn():
    global wave1,wave2,wave3,power_ups,wave1_state,wave2_state,wave3_state,boss_state
    glColor3f(.5, .5, .5)
    for j in wave1:
        MidpointCircle(30,j[0],j[1])
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    spaceship()
    draw_buttons()
    if boss_state==True:
        wave1.clear()
        wave2.clear()
        wave3.clear()
        power_ups.clear()
        boss()
    wave_spawn()
    bullet_spawn()
    glutSwapBuffers()
def collision(a):
    global ship_x,ship_y
    result= (ship_x - 150/2) < (a[0] + 30/2) and (ship_x + 150/2) > (a[0] - 30/2) and (ship_y - 100/2) < (a[1] + 30/2) and (ship_y + 100/2) > (a[1] - 30/2)
    if result==True:
        wave1.remove(a)
    return result

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(900, 1000)
glutCreateWindow(b"Asteroid Destroyer")
glClearColor(0.0, 0.0, 0.0, 0.0)
gluOrtho2D(0, 900, 0, 1000)
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
