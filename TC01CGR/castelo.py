import pyvista as pv

def create_castle_final():
    plotter = pv.Plotter()
    cor_castelo = '#C0C0C0'
    cor_telhado = '#8B4513'
    cor_janela = 'black'

    # --- função auxiliar para desenhar janelas (caixas finas pretas) ---
    def add_janela(xmin, xmax, ymin, ymax, zmin, zmax):
        janela = pv.Box(bounds=(xmin, xmax, ymin, ymax, zmin, zmax))
        plotter.add_mesh(janela, color=cor_janela)

    # piso
    piso = pv.Box(bounds=(-15, 15, -15, 15, -0.5, 0))
    plotter.add_mesh(piso, color=cor_castelo)

    # torres
    altura_torre = 10.0
    raio_torre = 3.0
    altura_telhado = 5.0

    def torre_com_casinha(x, y):
        torre = pv.Cylinder(radius=raio_torre, height=altura_torre,
                            center=(x, y, altura_torre/2), direction=(0,0,1))
        plotter.add_mesh(torre, color=cor_castelo)
        casinha = pv.Cylinder(radius=raio_torre*0.9, height=2.0,
                              center=(x, y, altura_torre+1), direction=(0,0,1))
        plotter.add_mesh(casinha, color=cor_castelo)
        telhado = pv.Cone(radius=raio_torre*1.2, height=altura_telhado,
                          center=(x, y, altura_torre+1+altura_telhado/2+1), direction=(0,0,1))
        plotter.add_mesh(telhado, color=cor_telhado)

        # janelinhas da torre (na frente e atrás)
        add_janela(x-0.5, x+0.5, y+raio_torre-0.1, y+raio_torre+0.1,
                   altura_torre*0.6, altura_torre*0.9)
        add_janela(x-0.5, x+0.5, y-raio_torre-0.1, y-raio_torre+0.1,
                   altura_torre*0.6, altura_torre*0.9)

    torre_com_casinha(-10, -10)
    torre_com_casinha(10, -10)
    torre_com_casinha(-10, 10)
    torre_com_casinha(10, 10)

    # muralhas
    altura_muralha = 6.0
    largura_muralha = 2.0

    muralha_frontal = pv.Box(bounds=(-10, 10,
                                     -10 - largura_muralha/2, -10 + largura_muralha/2,
                                     0, altura_muralha))
    abertura = pv.Box(bounds=(-2, 2,
                              -10 - largura_muralha/2 - 0.01, -10 + largura_muralha/2 + 0.01,
                              0, 4))

    muralha_frontal = muralha_frontal.triangulate().clean()
    abertura = abertura.triangulate().clean()

    try:
        muralha_com_buraco = muralha_frontal.boolean_difference(abertura, tolerance=1e-6)
        plotter.add_mesh(muralha_com_buraco, color=cor_castelo)
    except Exception as e:
        muralha_f_esq = pv.Box(bounds=(-10, -2,
                                       -10 - largura_muralha/2, -10 + largura_muralha/2,
                                       0, altura_muralha))
        muralha_f_dir = pv.Box(bounds=(2, 10,
                                       -10 - largura_muralha/2, -10 + largura_muralha/2,
                                       0, altura_muralha))
        # trecho da muralha acima do portão (a abertura vai só até z = 4)
        muralha_f_topo = pv.Box(bounds=(-2, 2,
                                        -10 - largura_muralha/2, -10 + largura_muralha/2,
                                        4, altura_muralha))
        plotter.add_mesh(muralha_f_esq, color=cor_castelo)
        plotter.add_mesh(muralha_f_dir, color=cor_castelo)
        plotter.add_mesh(muralha_f_topo, color=cor_castelo)

    # muralhas laterais e traseira
    muralha_e = pv.Box(bounds=(-10 - largura_muralha/2, -10 + largura_muralha/2, -10, 10, 0, altura_muralha))
    plotter.add_mesh(muralha_e, color=cor_castelo)
    muralha_t = pv.Box(bounds=(-10, 10, 10 - largura_muralha/2, 10 + largura_muralha/2, 0, altura_muralha))
    plotter.add_mesh(muralha_t, color=cor_castelo)
    muralha_d = pv.Box(bounds=(10 - largura_muralha/2, 10 + largura_muralha/2, -10, 10, 0, altura_muralha))
    plotter.add_mesh(muralha_d, color=cor_castelo)

    # --- janelas nas muralhas (2 em cada, menos a frontal) ---
    # muralha esquerda
    add_janela(-10-0.1, -10+0.1, -5, -3, 2, 4)
    add_janela(-10-0.1, -10+0.1, 3, 5, 2, 4)
    # muralha direita
    add_janela(10-0.1, 10+0.1, -5, -3, 2, 4)
    add_janela(10-0.1, 10+0.1, 3, 5, 2, 4)
    # muralha traseira
    add_janela(-5, -3, 10-0.1, 10+0.1, 2, 4)
    add_janela(3, 5, 10-0.1, 10+0.1, 2, 4)

    plotter.set_background('white')
    plotter.add_text("Castelo Final", position='upper_left', font_size=16)
    plotter.show()

if __name__ == "__main__":
    create_castle_final()
