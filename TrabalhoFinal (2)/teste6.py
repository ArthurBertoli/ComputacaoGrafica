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
WORLD_X = 5
WORLD_Y = 1
WORLD_Z = 5


class PhysicsObject:
    def __init__(self, pos, radius=0.7):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.zeros(3)
        self.radius = radius

    def update(self, dt):
        self.vel[1] -= 9.8 * dt * 0.35
        self.vel *= 0.99
        self.pos += self.vel * dt

        if self.pos[0] - self.radius < -WORLD_X:
            self.pos[0] = -WORLD_X + self.radius
            self.vel[0] *= -0.5
        if self.pos[0] + self.radius > WORLD_X:
            self.pos[0] = WORLD_X - self.radius
            self.vel[0] *= -0.5

        if self.pos[1] - self.radius < -WORLD_Y:
            self.pos[1] = -WORLD_Y + self.radius
            self.vel[1] *= -0.5
        if self.pos[1] + self.radius > WORLD_Y:
            self.pos[1] = WORLD_Y - self.radius
            self.vel[1] *= -0.5

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

        b.pos += normal * overlap * 0.5
        a.pos -= normal * overlap * 0.5

        impulse = normal * 2.0
        b.vel += impulse
        a.vel -= impulse * 0.4


# ============================================================
# OPENGL
# ============================================================
def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
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

    gluPerspective(45, display[0] / display[1], 0.1, 100.0)
    glTranslatef(0, 0, -15)

    init_opengl()

    # ==========================
    # MEDIAPIPE - MÃO
    # ==========================
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )
    cap = cv2.VideoCapture(0)

    head = PhysicsObject([0, 0, 0], radius=1.3)

    objects = []
    for i in range(12):
        x = random.uniform(-5, 5)
        y = random.uniform(-3, 3)
        z = random.uniform(-4, 4)
        objects.append(PhysicsObject([x, y, z], radius=0.7))

    clock = pygame.time.Clock()

    grabbed_obj = None
    last_hand_pos = np.array([0.0, 0.0, 0.0])

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                return

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        res = hands.process(rgb)

        hand_pos = None
        pinching = False

        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]

            palm = hand.landmark[9]
            thumb = hand.landmark[4]
            index = hand.landmark[8]

            cx, cy, cz = palm.x, palm.y, palm.z
            target_x = (cx - 0.5) * 10
            target_y = -(cy - 0.5) * 7
            target_z = (cz + 0.1) * -30

            hand_pos = np.array([target_x, target_y, target_z])
            head.pos = head.pos * 0.8 + hand_pos * 0.2

            pinch_dist = np.sqrt((thumb.x - index.x)**2 + (thumb.y - index.y)**2)
            pinching = pinch_dist < 0.04

        # =======================
        # SISTEMA DE PEGAR OBJETO
        # =======================
        if pinching and grabbed_obj is None and hand_pos is not None:
            for obj in objects:
                if np.linalg.norm(obj.pos - head.pos) < 1.5:
                    grabbed_obj = obj
                    break

        if grabbed_obj:
            grabbed_obj.pos = head.pos.copy()
            grabbed_obj.vel = (head.pos - last_hand_pos) * 30

            if not pinching:
                grabbed_obj = None

        last_hand_pos = head.pos.copy()

        for obj in objects:
            if obj != grabbed_obj:
                obj.update(dt)

        for obj in objects:
            if obj != grabbed_obj:
                collide_spheres(head, obj)

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                if objects[i] != grabbed_obj and objects[j] != grabbed_obj:
                    collide_spheres(objects[i], objects[j])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(45, display[0] / display[1], 0.1, 100)
        glTranslatef(0, 0, -15)

        glColor3f(0.4, 0.7, 1.0)
        glPushMatrix()
        glTranslatef(*head.pos)
        draw_sphere(head.radius)
        glPopMatrix()

        glColor3f(1.0, 0.4, 0.15)
        for obj in objects:
            glPushMatrix()
            glTranslatef(*obj.pos)
            draw_sphere(obj.radius)
            glPopMatrix()

        pygame.display.flip()


main()
