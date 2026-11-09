import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# --- Loader simples de arquivo OBJ ---
def load_obj(filename):
    vertices = []
    faces = []
    texcoords = []

    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.strip().split()
        if not values: continue

        if values[0] == 'v':  # vértices
            vertices.append(tuple(map(float, values[1:4])))
        elif values[0] == 'vt':  # coordenadas de textura
            texcoords.append(tuple(map(float, values[1:3])))
        elif values[0] == 'f':
            face = []
            for v in values[1:]:
                w = v.split('/')
                face.append((int(w[0]), int(w[1]) if len(w) > 1 and w[1] else 0))
            faces.append(face)

    return vertices, texcoords, faces

# --- Função para desenhar ---
def draw_obj(vertices, texcoords, faces, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            if vertex[1]:
                glTexCoord2fv(texcoords[vertex[1]-1])
            glVertex3fv(vertices[vertex[0]-1])
    glEnd()

# --- Carregar textura ---
def load_texture(filename):
    surf = pygame.image.load(filename)
    image = pygame.image.tostring(surf, "RGB", 1)
    ix, iy = surf.get_rect().size
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    return texid

# --- Programa principal ---
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_TEXTURE_2D)

    vertices, texcoords, faces = load_obj("unoTest.obj")
    texture = load_texture("unodelado.png")

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_obj(vertices, texcoords, faces, texture)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
