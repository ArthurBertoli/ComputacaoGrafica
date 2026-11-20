# Modelagem 3D com Primitivas — PyVista

> Projeto da disciplina **Computação Gráfica** — Ciência da Computação, UDESC.

## Sobre

Três cenas 3D montadas a partir de primitivas geométricas (esferas, cilindros, cones, cubos e caixas) e exibidas em uma janela interativa do PyVista.

## Funcionalidades

- **Boneco de neve** (`boneco_neve.py`): três esferas empilhadas, olhos, nariz de cenoura em cone, chapéu com dois cilindros e braços.
- **Castelo** (`castelo.py`): piso, quatro torres com telhado cônico, muralhas e janelas. A abertura do portão na muralha frontal é feita por diferença booleana entre malhas; se a operação falhar, a muralha é montada com três caixas (as duas laterais do portão e o trecho acima dele).
- **Robô** (`robo.py`): tronco em cubo, cabeça esférica, braços e pernas em cilindros, juntas em esferas e espinhos nos ombros. Usa uma função auxiliar que cria um cilindro entre dois pontos.

## Tecnologias

Python, PyVista, NumPy.

## Estrutura

| Arquivo | Descrição |
|---|---|
| `boneco_neve.py` | Cena do boneco de neve. |
| `castelo.py` | Cena do castelo. |
| `robo.py` | Cena do robô. |

## Como executar

```bash
pip install pyvista numpy
python boneco_neve.py
python castelo.py
python robo.py
```

## Autores

Arthur Bertoli
