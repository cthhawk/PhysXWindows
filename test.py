import pyphysx as ppx
from pyphysx_utils.rate import Rate
from pyphysx_render.pyrender import PyPhysxViewer
import numpy as np
import numpy.random
import pandas as pd
import matplotlib.pyplot as plt
import trimesh
import quaternion as quat


scene = ppx.Scene()
#scene.add_actor(RigidStatic.create_plane(material=Material(static_friction=0.0, dynamic_friction=0.0, restitution=0.5)))

## Set parameters
wall_length = 6.
unit = .2

## Set "boundaries"
north_wall = ppx.RigidStatic()
north_wall.attach_shape(ppx.Shape.create_box([unit, wall_length, unit], ppx.Material(restitution=1.)))
north_wall.set_global_pose([-1*wall_length/2, 0, unit/2])
scene.add_actor(north_wall)

east_wall = ppx.RigidStatic()
east_wall.attach_shape(ppx.Shape.create_box([wall_length, .2, .2], ppx.Material(restitution=1.)))
east_wall.set_global_pose([0, wall_length/2, unit/2])
scene.add_actor(east_wall)

south_wall = ppx.RigidStatic()
south_wall.attach_shape(ppx.Shape.create_box([.2,wall_length,.2], ppx.Material(restitution=1.)))
south_wall.set_global_pose([wall_length/2, 0, unit/2])
scene.add_actor(south_wall)

west_wall = ppx.RigidStatic()
west_wall.attach_shape(ppx.Shape.create_box([wall_length, .2, .2], ppx.Material(restitution=1.)))
west_wall.set_global_pose([0, -wall_length/2, unit/2])
scene.add_actor(west_wall)

obj: trimesh.Scene = trimesh.load('simple-topo.obj', split_object=True, group_material=False)

#Set actors/cubes
actors = []
number_actors = 1
topo_obj: trimesh.Scene = trimesh.load('simple-topo.obj', split_object=True, group_material=False)

topo = ppx.RigidStatic()
mesh_mat = ppx.Material()
topo.attach_shape(ppx.Shape.create_convex_mesh_from_points(topo_obj.vertices, mesh_mat, scale=1))
actors.append(topo)

for item in range(number_actors):
    actor = ppx.RigidDynamic()
    mesh_mat = ppx.Material()
    actor.attach_shape(ppx.Shape.create_box([0.2] * 3, ppx.Material(restitution=1.)))
    actor.set_global_pose([0.5, 0.5, 1.0])
    actor.set_mass(1.)
    actor.set_global_pose(
        [np.random.uniform( -1 * int(wall_length/2), int(wall_length/2) ), 
         np.random.uniform( -1 * int(wall_length/2), int(wall_length/2) ), 
         0])
    for i, s in enumerate(actor.get_atached_shapes()):
        s.set_user_data(dict(color='tab:blue'))
    #rotate 30 degrees
    pose, q = actor.get_global_pose()
    transform = ppx.cast_transformation([0,0,0,.87, 0, 0, .5])
    actor.set_global_pose(transform)


    actors.append(actor)

for actor in actors:
    scene.add_actor(actor)


#Initialize scene
render = PyPhysxViewer(video_filename='videos/12_test.gif')
render.add_physx_scene(scene)

rate = Rate(20)
while render.is_active:
    scene.simulate(rate.period())
    render.update()
    rate.sleep()



#show actors
for actor in actors:
    pose, q = actor.get_global_pose()
    print(q)
    euler_angles = quat.as_rotation_vector(q)

# Extract roll, pitch, and yaw
    roll = euler_angles[0]
    pitch = euler_angles[1]
    yaw = euler_angles[2]

    print("Roll:", round(roll))
    print("Pitch:", round(pitch))
    print("Yaw:", round(yaw))
