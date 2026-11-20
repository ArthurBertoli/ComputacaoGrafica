# Bando de Pássaros — Boids

> Projeto da disciplina **Computação Gráfica** — Ciência da Computação, UDESC.

## Sobre

Simulação 2D de um bando de pássaros com o algoritmo de *Boids* (Reynolds), renderizada com OpenGL/GLUT sobre uma imagem de céu usada como textura de fundo.

## Funcionalidades

- 40 pássaros com posição e direção iniciais aleatórias.
- Comportamentos de bando: **separação**, **alinhamento** e **coesão**, com velocidade e força máximas limitadas.
- Os pássaros fogem do cursor do mouse quando ele está a menos de 150 pixels.
- Ao sair por uma borda da janela, o pássaro reaparece na borda oposta.
- Cada pássaro é desenhado com triângulos, rotacionado na direção do movimento, com uma oscilação simples das asas.
- Fundo texturizado com `ceu.jpg` (carregado com Pillow) e atualização a cerca de 60 quadros por segundo.

## Tecnologias

Python, PyOpenGL (GL/GLU/GLUT), Pillow.

## Estrutura

| Arquivo | Descrição |
|---|---|
| `tc3.py` | Classes `Vector2D` e `Bird`, desenho e laço do GLUT. |
| `ceu.jpg` | Imagem de céu usada como textura de fundo. |

## Como executar

```bash
pip install PyOpenGL Pillow
python tc3.py
```

Execute de dentro desta pasta, pois `ceu.jpg` é carregado por caminho relativo. É necessário ter o GLUT (por exemplo, FreeGLUT) disponível no sistema.

## Autores

Arthur Bertoli
