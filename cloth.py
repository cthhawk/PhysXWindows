import numpy as np
import pyphysx as px

# Initialize the PhysX simulation environment

# Create a simulation scene
scene = px.Scene()
scene.add_actor(px.RigidStatic.create_plane(material=px.Material(static_friction=0.0, dynamic_friction=0.0, restitution=0.5)))

# Define cloth material properties
cloth_material = px.ClothMaterial(
    stretch_stiffness=1.0,
    bend_stiffness=1.0,
    shear_stiffness=1.0
)

# Define cloth geometry and initial position
cloth_width = 2.0
cloth_height = 2.0
resolution = 20
particle_distance = cloth_width / (resolution - 1)

# Generate particle grid
particles = np.zeros((resolution, resolution), dtype=px.ClothParticle)
for i in range(resolution):
    for j in range(resolution):
        fixed = i == 0  # Fix one edge of the cloth
        particles[i, j] = px.ClothParticle(
            pos=[i * particle_distance, j * particle_distance, 2],
            inv_weight=0 if fixed else 1,
            velocity=[0, 0, 0]
        )

# Create cloth object
cloth = px.Cloth(
    particles=particles.ravel(),
    triangles=px.utils.generate_triangles_cloth(resolution, resolution),
    material=cloth_material
)

# Add cloth to the scene
scene.add_actor(cloth)


render = PyPhysxViewer(video_filename='videos/cloth.gif')
render.add_physx_scene(scene)

#Simulate scene
rate = Rate(20)
while render.is_active:
    scene.simulate(rate.period())
    render.update()
    rate.sleep()


# Clean up
px.cleanup()