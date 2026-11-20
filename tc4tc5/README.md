# Carregador de OBJ com Textura

> Projeto da disciplina **Computação Gráfica** — Ciência da Computação, UDESC.

## Sobre

Programa que lê um modelo 3D no formato Wavefront OBJ (exportado do Blender), aplica uma textura e o exibe girando continuamente em uma janela Pygame com OpenGL.

## Funcionalidades

- Leitor de OBJ próprio: lê vértices (`v`), coordenadas de textura (`vt`) e faces (`f`).
- Carregamento da textura `unodelado.png` com Pygame e envio ao OpenGL.
- Renderização do modelo `unoTest.obj` com textura, em perspectiva, girando a cada quadro (30 FPS).

## Tecnologias

Python, PyOpenGL (GL/GLU), Pygame, Blender (modelagem).

## Estrutura

| Arquivo | Descrição |
|---|---|
| `main.py` | Leitor de OBJ, carregamento de textura e laço de renderização. |
| `unoTest.obj` / `unoTest.mtl` | Modelo exibido pelo programa. |
| `unodelado.png` | Textura aplicada ao modelo. |
| `dado.blend` / `dado.obj` / `dado.mtl` | Modelo de um dado feito no Blender. Não é carregado pelo `main.py`; o `dado.mtl` aponta a textura para um caminho absoluto de outro computador. |

## Como executar

```bash
pip install pygame PyOpenGL
python main.py
```

Execute de dentro desta pasta, pois os arquivos são carregados por caminho relativo.

## Observações

- O leitor desenha as faces com `GL_TRIANGLES`, mas os modelos foram exportados com faces de quatro vértices; para uma exibição correta, exporte o modelo triangulado no Blender.

## Autores

Arthur Bertoli
