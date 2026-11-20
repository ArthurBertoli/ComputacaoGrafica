# Trabalho Final — Esferas 3D controladas pelo rosto

> Projeto da disciplina **Computação Gráfica** — Ciência da Computação, UDESC.

## Sobre

Simulação 3D interativa em que a posição do rosto do usuário, captada pela webcam, controla uma esfera em uma cena OpenGL. Essa esfera empurra outras esferas que estão sujeitas a uma física simples (gravidade, atrito, limites do cenário e colisões).

## Funcionalidades

- Captura da webcam com OpenCV e detecção de rosto com MediaPipe (`face_detection`).
- O centro da caixa delimitadora do rosto define as coordenadas X e Y da esfera "cabeça"; o tamanho da caixa (proximidade da câmera) define a profundidade Z. O movimento é suavizado.
- 12 esferas laranja criadas em posições aleatórias, com gravidade, atrito e rebote com perda de energia nas bordas do mundo.
- Colisão entre esferas: correção de sobreposição e aplicação de impulso (cabeça × esferas e esferas × esferas).
- Esferas desenhadas manualmente com `GL_TRIANGLE_STRIP` e normais, iluminação com `GL_LIGHT0`, teste de profundidade e projeção em perspectiva (na matriz de projeção, separada da modelview).
- Procura a webcam nos índices 0, 1 e 2. Sem webcam (ou se a leitura falhar), a simulação continua rodando e a esfera da cabeça apenas fica parada.

## Tecnologias

Python, PyOpenGL (GL/GLU), Pygame, OpenCV, MediaPipe, NumPy.

## Estrutura

| Arquivo | Descrição |
|---|---|
| `CGR.py` | Código da simulação (desenho da esfera, física, colisões, OpenGL e laço principal). |
| `requirements.txt` | Dependências com versões fixas (MediaPipe com `mp.solutions`). |
| `SlidesCGR.pdf` | Slides da apresentação do trabalho. |
| `WordCGR.docx` | Documento com a explicação de cada parte do código. |

## Como executar

Use Python 3.11 ou 3.12. Para controlar a esfera com o rosto é preciso uma webcam.

```bash
pip install -r requirements.txt
python CGR.py
```

O código usa a API clássica `mp.solutions.face_detection`, que foi removida das versões mais novas do MediaPipe; por isso o `requirements.txt` fixa o `mediapipe==0.10.21`, que ainda a inclui. O MediaPipe já instala o `opencv-contrib-python`; não instale também o `opencv-python`. Para sair, feche a janela ou pressione `Esc`.

## Autores

- Arthur Bertoli
- Andressa Budziak
