from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

NUM_PARTICLES = 500
particles = []

class SmokeParticle:
    def __init__(self):
        self.reset()

    def reset(self):
        # Começa próximo da base
        self.x = random.uniform(-1.0, 1.0)
        self.y = -1.2  # sempre de baixo
        self.z = random.uniform(-1.0, 1.0)
        self.vx = random.uniform(-0.01, 0.01)   # espalha para os lados
        self.vy = random.uniform(0.01, 0.03)    # sobe devagar
        self.vz = random.uniform(-0.01, 0.01)
        self.life = random.uniform(2.0, 4.0)    # tempo de vida
        self.age = 0.0
        self.size = random.uniform(0.05, 0.12)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.age += 0.02

        if self.age >= self.life:
            self.reset()

def init_particles():
    global particles
    particles = [SmokeParticle() for _ in range(NUM_PARTICLES)]

def draw_particle(p: SmokeParticle):
    # cor vai ficando mais transparente com o tempo
    fade = max(0.0, 1.0 - (p.age / p.life))
    glColor4f(0.5 * fade, 0.5 * fade, 0.5 * fade, fade * 0.7)

    # desenha como quadradinho (poderia ser ponto também)
    glBegin(GL_QUADS)
    glVertex3f(p.x - p.size, p.y - p.size, p.z)
    glVertex3f(p.x + p.size, p.y - p.size, p.z)
    glVertex3f(p.x + p.size, p.y + p.size, p.z)
    glVertex3f(p.x - p.size, p.y + p.size, p.z)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)

    for p in particles:
        p.update()
        draw_particle(p)

    glutSwapBuffers()

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def reshape(w, h):
    # Ao minimizar a janela o GLUT pode mandar altura 0 (divisão por zero abaixo)
    h = max(h, 1)
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w)/float(h), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Fumaça com Partículas".encode())

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    init_particles()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
