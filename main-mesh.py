from pyphysx import *
from pyphysx_utils.rate import Rate
from pyphysx_render.pyrender import PyPhysxViewer
import numpy as np
import numpy.random
import pandas as pd
import matplotlib.pyplot as plt
import trimesh



scene = Scene()
scene.add_actor(RigidStatic.create_plane(material=Material(static_friction=0.0, dynamic_friction=0.0, restitution=0.5)))

## Set parameters
wall_length = 6.
unit = .2

## Set "boundaries"
north_wall = RigidStatic()
north_wall.attach_shape(Shape.create_box([unit, wall_length, unit], Material(restitution=1.)))
north_wall.set_global_pose([-1*wall_length/2, 0, unit/2])
scene.add_actor(north_wall)

east_wall = RigidStatic()
east_wall.attach_shape(Shape.create_box([wall_length, .2, .2], Material(restitution=1.)))
east_wall.set_global_pose([0, wall_length/2, unit/2])
scene.add_actor(east_wall)

south_wall = RigidStatic()
south_wall.attach_shape(Shape.create_box([.2,wall_length,.2], Material(restitution=1.)))
south_wall.set_global_pose([wall_length/2, 0, unit/2])
scene.add_actor(south_wall)

west_wall = RigidStatic()
west_wall.attach_shape(Shape.create_box([wall_length, .2, .2], Material(restitution=1.)))
west_wall.set_global_pose([0, -wall_length/2, unit/2])
scene.add_actor(west_wall)

#Set actors/cubes
actors = []
number_actors = 6
obj: trimesh.Scene = trimesh.load('sample_plan.obj', split_object=True, group_material=False)
obj.export('output_mesh.obj')

for item in range(number_actors):
    actor = RigidDynamic()
    mesh_mat = Material()
    for g in obj.geometry.values():
        actor.attach_shape(Shape.create_convex_mesh_from_points(g.vertices, mesh_mat, scale=1))
    actor.set_global_pose([0.5, 0.5, 1.0])
    actor.set_mass(1.)
    actor.set_global_pose(
        [np.random.uniform( -1 * int(wall_length/2), int(wall_length/2) ), 
         np.random.uniform( -1 * int(wall_length/2), int(wall_length/2) ), 
         0])
    for i, s in enumerate(actor.get_atached_shapes()):
        s.set_user_data(dict(color='tab:blue'))
    actor.set_linear_velocity([np.random.uniform(-1, 1),np.random.uniform(-1, 1),0])
    actor.set_mass(1.)
    actors.append(actor)

for actor in actors:
    scene.add_actor(actor)


#Initialize scene
render = PyPhysxViewer(video_filename='videos/03_free_fall.gif')
render.add_physx_scene(scene)



rate = Rate(20)
while render.is_active:
    scene.simulate(rate.period())
    render.update()
    rate.sleep()
