# Fumaça com Partículas

> Projeto da disciplina **Computação Gráfica** — Ciência da Computação, UDESC.

## Sobre

Sistema de partículas em OpenGL/GLUT que simula fumaça subindo a partir da base da cena.

## Funcionalidades

- 500 partículas que nascem na base com posição, velocidade, tamanho e tempo de vida aleatórios.
- Cada partícula sobe devagar e se espalha para os lados; ao fim do tempo de vida, é reiniciada na base.
- A cor e a transparência diminuem conforme a partícula envelhece (*fade*), usando *blending* alfa.
- Partículas desenhadas como pequenos quadrados (`GL_QUADS`) em projeção em perspectiva.

## Tecnologias

Python, PyOpenGL (GL/GLU/GLUT).

## Estrutura

- `particulas.py` — classe `SmokeParticle`, desenho e laço do GLUT.

## Como executar

```bash
pip install PyOpenGL
python particulas.py
```

É necessário ter o GLUT (por exemplo, FreeGLUT) disponível no sistema.

## Autores

Arthur Bertoli
