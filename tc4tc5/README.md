# Carregador de OBJ com Textura

> Projeto da disciplina **Computação Gráfica** — Ciência da Computação, UDESC.

## Sobre

Programa que lê um modelo 3D no formato Wavefront OBJ (exportado do Blender), aplica uma textura e o exibe girando continuamente em uma janela Pygame com OpenGL.

## Funcionalidades

- Leitor de OBJ próprio: lê vértices (`v`), coordenadas de textura (`vt`) e faces (`f`), aceitando índices negativos.
- Faces com 4 ou mais vértices (como as que o Blender exporta) são trianguladas em leque ao carregar, então o modelo é desenhado corretamente com `GL_TRIANGLES` sem precisar reexportar.
- O modelo é centralizado e redimensionado automaticamente para caber na tela.
- Carregamento da textura `unodelado.png` com Pygame e envio ao OpenGL.
- Renderização do modelo `unoTest.obj` com textura, em perspectiva e com teste de profundidade, girando a cada quadro (30 FPS).

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

Os arquivos do modelo e da textura são procurados na pasta do `main.py`, então o programa pode ser executado de qualquer diretório. Para sair, feche a janela ou pressione `Esc`.

## Autores

Arthur Bertoli
