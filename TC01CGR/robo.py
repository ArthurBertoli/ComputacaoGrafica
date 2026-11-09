import pyvista as pv
import numpy as np

plotter = pv.Plotter()

def create_cylinder(start, end, radius=0.1):
    vector = np.array(end) - np.array(start)
    height = np.linalg.norm(vector)
    direction = vector / height
    cylinder = pv.Cylinder(center=(np.array(start)+np.array(end))/2,
                           direction=direction,
                           radius=radius,
                           height=height)
    return cylinder

def create_sphere(center, radius=0.15):
    return pv.Sphere(radius=radius, center=center)

joint_radius = 0.15  # mesmo valor da esfera

# Tronco
trunk = pv.Cube(center=(0,0,1), x_length=0.5, y_length=0.3, z_length=0.8)
plotter.add_mesh(trunk, color='#5B1E91')

# Cabeça
head = create_sphere(center=(0,0,1.6), radius=0.2)
plotter.add_mesh(head, color='#FFD700')

# Braços (corrigindo espaço)
left_arm = create_cylinder(start=(-0.45-joint_radius,0,1.4), end=(-0.9,0,1.0))
right_arm = create_cylinder(start=(0.45+joint_radius,0,1.4), end=(0.9,0,1.0))
plotter.add_mesh(left_arm, color='black')
plotter.add_mesh(right_arm, color='black')

# Pernas (corrigindo espaço)
left_leg = create_cylinder(start=(-0.15,0,0.8-joint_radius), end=(-0.15,0,0.0), radius=0.12)
right_leg = create_cylinder(start=(0.15,0,0.8-joint_radius), end=(0.15,0,0.0), radius=0.12)
plotter.add_mesh(left_leg, color='black')
plotter.add_mesh(right_leg, color='black')

# Juntas
plotter.add_mesh(create_sphere(center=(-0.45,0,1.4)), color='#39FF14')
plotter.add_mesh(create_sphere(center=(0.45,0,1.4)), color='#39FF14')
plotter.add_mesh(create_sphere(center=(-0.15,0,0.8)), color='#39FF14')
plotter.add_mesh(create_sphere(center=(0.15,0,0.8)), color='#39FF14')

# Espinhos dos ombros
spike_left = create_cylinder(start=(-0.45,0,1.4+joint_radius), end=(-0.45,0,2.2), radius=0.05)
spike_right = create_cylinder(start=(0.45,0,1.4+joint_radius), end=(0.45,0,2.2), radius=0.05)
plotter.add_mesh(spike_left, color='#39FF14')
plotter.add_mesh(spike_right, color='#39FF14')

plotter.show()
