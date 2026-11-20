import cv2
import mediapipe as mp
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random


# ============================================================
# DESENHO DA ESFERA
# ============================================================
def draw_sphere(radius=1, slices=16, stacks=16):
    for i in range(stacks):
        lat0 = np.pi * (-0.5 + i / stacks)
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)

        lat1 = np.pi * (-0.5 + (i + 1) / stacks)
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(slices + 1):
            lng = 2 * np.pi * j / slices
            x = np.cos(lng)
            y = np.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(radius * x * zr0, radius * y * zr0, radius * z0)

            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(radius * x * zr1, radius * y * zr1, radius * z1)
        glEnd()


# ============================================================
# FÍSICA
# ============================================================
WORLD_X = 5   # bordas no eixo X
WORLD_Y = 1   # bordas no eixo Y
WORLD_Z = 5     # bordas no eixo Z


class PhysicsObject:
    def __init__(self, pos, radius=0.7):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.zeros(3)
        self.radius = radius

    def update(self, dt):
        # Gravidade
        self.vel[1] -= 9.8 * dt * 0.35

        # Atrito
        self.vel *= 0.99

        # Atualiza posição
        self.pos += self.vel * dt

        # --------------- LIMITES ---------------

        # Limite X
        if self.pos[0] - self.radius < -WORLD_X:
            self.pos[0] = -WORLD_X + self.radius
            self.vel[0] *= -0.5

        if self.pos[0] + self.radius > WORLD_X:
            self.pos[0] = WORLD_X - self.radius
            self.vel[0] *= -0.5

        # Limite Y
        if self.pos[1] - self.radius < -WORLD_Y:
            self.pos[1] = -WORLD_Y + self.radius
            self.vel[1] *= -0.5

        if self.pos[1] + self.radius > WORLD_Y:
            self.pos[1] = WORLD_Y - self.radius
            self.vel[1] *= -0.5

        # Limite Z
        if self.pos[2] - self.radius < -WORLD_Z:
            self.pos[2] = -WORLD_Z + self.radius
            self.vel[2] *= -0.5

        if self.pos[2] + self.radius > WORLD_Z:
            self.pos[2] = WORLD_Z - self.radius
            self.vel[2] *= -0.5


# ============================================================
# COLISÕES
# ============================================================
def collide_spheres(a, b):
    delta = b.pos - a.pos
    dist = np.linalg.norm(delta)
    min_dist = a.radius + b.radius

    if dist < min_dist and dist > 0:
        normal = delta / dist
        overlap = min_dist - dist

        # Corrige posição (empurra)
        b.pos += normal * overlap * 0.5
        a.pos -= normal * overlap * 0.5

        # Resposta física
        impulse = normal * 2.0
        b.vel += impulse
        a.vel -= impulse * 0.4


# ============================================================
# OPENGL
# ============================================================
def setup_projection(display):
    # A perspectiva vai na matriz de PROJEÇÃO; a câmera (translação) vai na
    # MODELVIEW. Antes as duas iam juntas na MODELVIEW, o que distorce a
    # iluminação (as normais eram transformadas também pela perspectiva).
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display[0] / display[1], 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def open_camera(indices=(0, 1, 2)):
    """Abre a primeira webcam que entregar imagem; devolve None se não houver."""
    for i in indices:
        cap = cv2.VideoCapture(i)
        if cap.isOpened() and cap.read()[0]:
            print(f"Usando a câmera {i}.")
            return cap
        cap.release()
    print("Nenhuma webcam encontrada: a cena roda, mas a esfera azul fica parada.")
    return None


def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
    glEnable(GL_COLOR_MATERIAL)
    glClearColor(0, 0, 0, 1)


# ============================================================
# MAIN
# ============================================================
def main():
    pygame.init()
    display = (900, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    pygame.display.set_caption("Trabalho Final CGR - Esferas controladas pelo rosto")
    setup_projection(display)

    # Luz direcional definida com a MODELVIEW identidade (espaço da câmera)
    init_opengl()

    # MediaPipe
    mp_face = mp.solutions.face_detection
    detector = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6)
    cap = open_camera()

    # Cabeça controlada pela webcam
    head = PhysicsObject([0, 0, 0], radius=1.3)

    # Bolinhas maiores
    objects = []
    for i in range(12):
        x = random.uniform(-5, 5)
        y = random.uniform(-3, 3)
        z = random.uniform(-4, 4)
        objects.append(PhysicsObject([x, y, z], radius=0.7))

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                if cap is not None:
                    cap.release()
                detector.close()
                pygame.quit()
                return

        # ---- Webcam ----
        # Se a câmera falhar, a simulação continua (antes o "continue" pulava
        # também a física, o desenho e o tratamento de eventos e a janela travava)
        res = None
        if cap is not None:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                res = detector.process(rgb)

        if res is not None and res.detections:
            d = res.detections[0]
            box = d.location_data.relative_bounding_box

            cx = box.xmin + box.width / 2
            cy = box.ymin + box.height / 2
            size = box.width * box.height

            target_x = (cx - 0.5) * 10
            target_y = -(cy - 0.5) * 7
            target_z = (size - 0.035) * 80

            # Suavização
            head.pos = head.pos * 0.8 + np.array([target_x, target_y, target_z]) * 0.2

        # ---- Física ----
        for obj in objects:
            obj.update(dt)

        # colisão da cabeça com objetos
        for obj in objects:
            collide_spheres(head, obj)

        # colisões entre objetos
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                collide_spheres(objects[i], objects[j])

        # ---- Render ----
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -15)

        # Esfera da cabeça
        glColor3f(0.4, 0.7, 1.0)
        glPushMatrix()
        glTranslatef(*head.pos)
        draw_sphere(head.radius)
        glPopMatrix()

        # Objetos
        glColor3f(1.0, 0.4, 0.15)
        for obj in objects:
            glPushMatrix()
            glTranslatef(*obj.pos)
            draw_sphere(obj.radius)
            glPopMatrix()

        pygame.display.flip()


if __name__ == "__main__":
    main()
