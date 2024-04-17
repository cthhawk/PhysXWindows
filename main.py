from pyphysx import *
from pyphysx_utils.rate import Rate
from pyphysx_render.pyrender import PyPhysxViewer
import numpy as np
import numpy.random

scene = Scene()
scene.add_actor(RigidStatic.create_plane(material=Material(static_friction=0.0, dynamic_friction=0.0, restitution=0.5)))

wall_length = 6.
unit = .2

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


actors = []
number_actors = 6
for item in range(number_actors):
    actor = RigidDynamic()
    actor.attach_shape(Shape.create_box([0.2] * 3, Material(restitution=1.)))
    actor.set_global_pose(
        [np.random.uniform( -1 * int(wall_length/2), int(wall_length/2) ), 
         np.random.uniform( -1 * int(wall_length/2), int(wall_length/2) ), 
         0])
    actor.set_linear_velocity([np.random.random(),np.random.random(),0])
    actor.set_mass(1.)
    actors.append(actor)

for actor in actors:
    scene.add_actor(actor)



render = PyPhysxViewer(video_filename='videos/01_free_fall.gif')
render.add_physx_scene(scene)

rate = Rate(20)
while render.is_active:
    scene.simulate(rate.period())
    render.update()
    rate.sleep()
