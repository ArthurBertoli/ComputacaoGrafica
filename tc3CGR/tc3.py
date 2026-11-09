import sys
import random
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

# --- CONFIGURAÇÕES GERAIS ---
window_width = 800
window_height = 600
num_birds = 40
max_speed = 3.0
max_force = 0.05
mouse_pos = None

# --- CLASSE VETOR 2D ---
class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other): return Vector2D(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vector2D(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar): return Vector2D(self.x * scalar, self.y * scalar)
    def __truediv__(self, scalar): return Vector2D(self.x / scalar, self.y / scalar)
    def length(self): return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        l = self.length()
        return self / l if l > 0 else Vector2D()
    
    def limit(self, max_val):
        l = self.length()
        if l > max_val:
            return self.normalize() * max_val
        return self
    
    def distance(self, other):
        return (self - other).length()
    
    def copy(self):
        return Vector2D(self.x, self.y)
    
    def tuple(self):
        return (self.x, self.y)
    
    def angle(self):
        return math.degrees(math.atan2(self.y, self.x))

# --- CLASSE PÁSSARO ---
class Bird:
    def __init__(self):
        self.position = Vector2D(random.uniform(0, window_width), random.uniform(0, window_height))
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = Vector2D(math.cos(angle), math.sin(angle)) * max_speed
        self.acceleration = Vector2D()
    
    def apply_force(self, force):
        self.acceleration += force
    
    def update(self):
        self.velocity += self.acceleration
        self.velocity = self.velocity.limit(max_speed)
        self.position += self.velocity
        self.acceleration = Vector2D()

        # Mantém os pássaros dentro da janela
        if self.position.x > window_width: self.position.x = 0
        if self.position.x < 0: self.position.x = window_width
        if self.position.y > window_height: self.position.y = 0
        if self.position.y < 0: self.position.y = window_height

    def separate(self, birds):
        desired_separation = 25
        steer = Vector2D()
        count = 0
        for other in birds:
            d = self.position.distance(other.position)
            if 0 < d < desired_separation:
                diff = (self.position - other.position).normalize()
                diff /= d
                steer += diff
                count += 1
        if count > 0:
            steer /= count
        if steer.length() > 0:
            steer = steer.normalize() * max_speed - self.velocity
            steer = steer.limit(max_force)
        return steer

    def align(self, birds):
        neighbor_dist = 50
        sum_vel = Vector2D()
        count = 0
        for other in birds:
            d = self.position.distance(other.position)
            if 0 < d < neighbor_dist:
                sum_vel += other.velocity
                count += 1
        if count > 0:
            avg = sum_vel / count
            avg = avg.normalize() * max_speed
            steer = avg - self.velocity
            return steer.limit(max_force)
        return Vector2D()

    def cohesion(self, birds):
        neighbor_dist = 50
        center_mass = Vector2D()
        count = 0
        for other in birds:
            d = self.position.distance(other.position)
            if 0 < d < neighbor_dist:
                center_mass += other.position
                count += 1
        if count > 0:
            center_mass /= count
            return self.seek(center_mass)
        return Vector2D()

    def seek(self, target):
        desired = (target - self.position).normalize() * max_speed
        steer = (desired - self.velocity).limit(max_force)
        return steer

    def flee(self, target):
        desired = (self.position - target).normalize() * max_speed
        steer = (desired - self.velocity).limit(max_force)
        return steer

    def run(self, birds):
        sep = self.separate(birds) * 1.8
        ali = self.align(birds) * 1.0
        coh = self.cohesion(birds) * 1.0

        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

        # Fugir do mouse
        if mouse_pos is not None:
            d = self.position.distance(mouse_pos)
            if d < 150:
                flee_force = self.flee(mouse_pos) * (1.5 * (150 - d) / 150)
                self.apply_force(flee_force)

        self.update()

# --- DESENHO DOS PÁSSAROS ---
def draw_bird(bird):
    pos = bird.position
    angle = bird.velocity.angle()

    glPushMatrix()
    glTranslatef(pos.x, pos.y, 0)
    glRotatef(angle, 0, 0, 1)
    
    # Corpo do pássaro (triângulo afilado)
    glBegin(GL_TRIANGLES)
    glColor3f(0.2, 0.2, 0.2)  # corpo cinza
    glVertex2f(12, 0)
    glColor3f(0.4, 0.4, 0.4)
    glVertex2f(-8, 5)
    glVertex2f(-8, -5)
    glEnd()

    # Asas (pequena oscilação para simular bater de asas)
    wing_flap = math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.008 + pos.x * 0.1) * 3
    glBegin(GL_TRIANGLES)
    glColor3f(0.1, 0.1, 0.1)
    glVertex2f(-4, 0)
    glVertex2f(-15, 5 + wing_flap)
    glVertex2f(-15, -5 - wing_flap)
    glEnd()

    glPopMatrix()

# --- FUNÇÕES DE OPENGL ---
def load_texture(path):
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes()
    width, height = img.size
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id

def draw_background():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(window_width, 0)
    glTexCoord2f(1, 1); glVertex2f(window_width, window_height)
    glTexCoord2f(0, 1); glVertex2f(0, window_height)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

# --- EVENTOS ---
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_background()
    for b in birds:
        b.run(birds)
        draw_bird(b)
    glutSwapBuffers()

def reshape(w, h):
    global window_width, window_height
    window_width = w
    window_height = h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def timer(v):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 1)

def mouse_motion(x, y):
    global mouse_pos
    mouse_pos = Vector2D(x, window_height - y)

# --- MAIN ---
def main():
    global birds, background_texture
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("Bando de Pássaros - Boids".encode('utf-8'))

    glClearColor(0.5, 0.7, 1.0, 1.0)

    background_texture = load_texture("ceu.jpg")
    birds = [Bird() for _ in range(num_birds)]

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(16, timer, 1)
    glutPassiveMotionFunc(mouse_motion)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glutMainLoop()

if __name__ == "__main__":
    main()
