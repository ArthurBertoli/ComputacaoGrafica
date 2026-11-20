# Trabalho Final — Esferas 3D controladas pelo rosto

> Projeto da disciplina **Computação Gráfica** — Ciência da Computação, UDESC.

## Sobre

Simulação 3D interativa em que a posição do rosto do usuário, captada pela webcam, controla uma esfera em uma cena OpenGL. Essa esfera empurra outras esferas que estão sujeitas a uma física simples (gravidade, atrito, limites do cenário e colisões).

## Funcionalidades

- Captura da webcam com OpenCV e detecção de rosto com MediaPipe (`face_detection`).
- O centro da caixa delimitadora do rosto define as coordenadas X e Y da esfera "cabeça"; o tamanho da caixa (proximidade da câmera) define a profundidade Z. O movimento é suavizado.
- 12 esferas laranja criadas em posições aleatórias, com gravidade, atrito e rebote com perda de energia nas bordas do mundo.
- Colisão entre esferas: correção de sobreposição e aplicação de impulso (cabeça × esferas e esferas × esferas).
- Esferas desenhadas manualmente com `GL_TRIANGLE_STRIP` e normais, iluminação com `GL_LIGHT0`, teste de profundidade e projeção em perspectiva.

## Tecnologias

Python, PyOpenGL (GL/GLU), Pygame, OpenCV, MediaPipe, NumPy.

## Estrutura

| Arquivo | Descrição |
|---|---|
| `CGR.py` | Código da simulação (desenho da esfera, física, colisões, OpenGL e laço principal). |
| `SlidesCGR.pdf` | Slides da apresentação do trabalho. |
| `WordCGR.docx` | Documento com a explicação de cada parte do código. |

## Como executar

É necessário ter uma webcam conectada.

```bash
pip install pygame PyOpenGL numpy opencv-python mediapipe
python CGR.py
```

O código usa a API clássica `mp.solutions.face_detection`, portanto é preciso uma versão do MediaPipe que ainda a inclua. Para sair, feche a janela.

## Autores

- Arthur Bertoli
- Andressa Budziak
