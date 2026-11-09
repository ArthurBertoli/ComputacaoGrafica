import pyvista as pv

def create_snowman():
    
    # Cria um plotter para visualizar as formas
    plotter = pv.Plotter()

    # Corpo do boneco de neve (esfera)
    # Esfera inferior
    esfera_inferior = pv.Sphere(radius=1.0, center=(0, 0, 1.0))
    plotter.add_mesh(esfera_inferior, color='#ADD8E6')

    # Esfera do meio
    esfera_meio = pv.Sphere(radius=0.7, center=(0, 0, 1.0 + 1.0 + 0.7))
    plotter.add_mesh(esfera_meio, color='#ADD8E6')

    # Esfera da cabeça
    esfera_cabeca = pv.Sphere(radius=0.5, center=(0, 0, 1.0 + 1.0 + 0.7 + 0.7 + 0.5))
    plotter.add_mesh(esfera_cabeca, color='#ADD8E6')

    # Olhos e nariz (esferas menores) 
    # Olho esquerdo
    olho_esquerdo = pv.Sphere(radius=0.08, center=(-0.25, 0.45, 1.0 + 1.0 + 0.7 + 0.7 + 0.5 + 0.2))
    plotter.add_mesh(olho_esquerdo, color='black')

    # Olho direito
    olho_direito = pv.Sphere(radius=0.08, center=(0.25, 0.45, 1.0 + 1.0 + 0.7 + 0.7 + 0.5 + 0.2))
    plotter.add_mesh(olho_direito, color='black')

    # Nariz (cenoura)
    nariz = pv.Cone(direction=(0, 1, 0), height=0.5, radius=0.1, center=(0, 0.5, 1.0 + 1.0 + 0.7 + 0.7 + 0.5 + 0.1))
    plotter.add_mesh(nariz, color='orange')
    
    # Chapéu (cilindro e disco) 
    # Base do chapéu
    chapeu_base = pv.Cylinder(radius=0.8, height=0.1, center=(0, 0, 1.0 + 1.0 + 0.7 + 0.7 + 0.5 + 0.5 - 0.05), direction=(0,0,1))
    plotter.add_mesh(chapeu_base, color='black')
    
    # Topo do chapéu
    chapeu_topo = pv.Cylinder(radius=0.6, height=1.0, center=(0, 0, 1.0 + 1.0 + 0.7 + 0.7 + 0.5 + 0.5 - 0.05 + 0.5), direction=(0,0,1))
    plotter.add_mesh(chapeu_topo, color='black')

    # Exibe a cena
    plotter.set_background('white')
    plotter.add_text("Boneco de Neve", position='upper_left', font_size=16)
    plotter.show()

# Chama a função para criar o boneco de neve
if __name__ == "__main__":
    create_snowman()