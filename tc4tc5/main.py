import os

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Pasta deste arquivo: os modelos e texturas são procurados aqui, então o
# programa funciona mesmo se for executado a partir de outra pasta.
PASTA = os.path.dirname(os.path.abspath(__file__))


def _indice(valor, total):
    """Converte um índice do OBJ (começa em 1; negativo conta do fim) para base 0."""
    i = int(valor)
    return i - 1 if i > 0 else total + i


# --- Loader simples de arquivo OBJ ---
def load_obj(filename):
    """Lê vértices (v), coordenadas de textura (vt) e faces (f).

    Faces com 4 ou mais vértices (o Blender exporta quadriláteros por padrão)
    são trianguladas em leque (fan): (v0, v1, v2), (v0, v2, v3), ...
    Assim todas as faces devolvidas são triângulos e podem ser desenhadas com
    GL_TRIANGLES. Cada vértice da face é (índice_vértice, índice_textura ou
    None), ambos já em base 0.
    """
    vertices = []
    faces = []
    texcoords = []

    with open(filename, "r", encoding="utf-8") as arquivo:
        for line in arquivo:
            if line.startswith('#'):
                continue
            values = line.strip().split()
            if not values:
                continue

            if values[0] == 'v':  # vértices
                vertices.append(tuple(map(float, values[1:4])))
            elif values[0] == 'vt':  # coordenadas de textura
                texcoords.append(tuple(map(float, values[1:3])))
            elif values[0] == 'f':
                face = []
                for v in values[1:]:
                    w = v.split('/')
                    vi = _indice(w[0], len(vertices))
                    ti = _indice(w[1], len(texcoords)) if len(w) > 1 and w[1] else None
                    face.append((vi, ti))
                # Triangulação em leque
                for k in range(1, len(face) - 1):
                    faces.append((face[0], face[k], face[k + 1]))

    return vertices, texcoords, faces


def normalize_vertices(vertices, tamanho=2.5):
    """Centraliza o modelo na origem e o escala para caber num cubo de lado `tamanho`.

    O unoTest.obj vai de -8 a +8 unidades; sem isso a câmera (a 5 unidades da
    origem) ficava dentro do modelo.
    """
    if not vertices:
        return vertices
    mins = [min(c) for c in zip(*vertices)]
    maxs = [max(c) for c in zip(*vertices)]
    centro = [(a + b) / 2 for a, b in zip(mins, maxs)]
    maior = max(b - a for a, b in zip(mins, maxs)) or 1.0
    escala = tamanho / maior
    return [tuple((p - c) * escala for p, c in zip(v, centro)) for v in vertices]


# --- Função para desenhar ---
def draw_obj(vertices, texcoords, faces, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vi, ti in face:
            if ti is not None:
                glTexCoord2fv(texcoords[ti])
            glVertex3fv(vertices[vi])
    glEnd()


# --- Carregar textura ---
def load_texture(filename):
    surf = pygame.image.load(filename)
    # tobytes (pygame 2.1.3+); tostring é o nome antigo, já obsoleto
    to_bytes = getattr(pygame.image, "tobytes", None) or pygame.image.tostring
    image = to_bytes(surf, "RGB", True)
    ix, iy = surf.get_rect().size
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    # Linhas RGB nem sempre têm tamanho múltiplo de 4 bytes
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    return texid


# --- Programa principal ---
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Carregador de OBJ com textura")

    # Perspectiva na matriz de projeção; câmera e rotação na modelview
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_TEXTURE_2D)
    # Sem o teste de profundidade as faces de trás apareciam por cima das da frente
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1)

    vertices, texcoords, faces = load_obj(os.path.join(PASTA, "unoTest.obj"))
    vertices = normalize_vertices(vertices)
    texture = load_texture(os.path.join(PASTA, "unodelado.png"))

    clock = pygame.time.Clock()
    angulo = 0.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return

        angulo = (angulo + 1) % 360
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)
        glRotatef(angulo, 3, 1, 1)
        draw_obj(vertices, texcoords, faces, texture)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
