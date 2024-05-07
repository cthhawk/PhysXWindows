import pyphysx as ppx
from pyphysx_utils.rate import Rate
from pyphysx_render.pyrender import PyPhysxViewer
import numpy as np
import numpy.random
import pandas as pd
import matplotlib.pyplot as plt
import trimesh
import quaternion as quat
import itertools as it
import pygad as pygad

actors = []
number_actors = 3
wall_length = 6.
unit = .2
scene = ppx.Scene()

def set_boundaries(number_actors):
    
    scene.add_actor(ppx.RigidStatic.create_plane(material=ppx.Material(static_friction=0.0, dynamic_friction=0.0, restitution=0.5)))

    ## Set parameters
    

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


def set_items(number_actors):
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
        #actor.set_linear_velocity([np.random.uniform(-1, 1),np.random.uniform(-1, 1),0])
        for i, s in enumerate(actor.get_atached_shapes()):
            s.set_user_data(dict(color='tab:blue'))
        actors.append(actor)
        print("success")
    for actor in actors:
        scene.add_actor(actor)
        
def get_distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return np.sqrt(dx**2 + dy**2 + dz**2)

num_generations = 5
sol_per_pop = 10
num_genes = number_actors 
num_parents_mating = 2

'''
def fitness_func(ga_instance, solution, solution_idx):
    actors = solution
    actor_pairs = it.combinations(actors, 2)
    fitness = 0
    for pair in actor_pairs:
        print("happy happy day: ", pair[0])
        pos1, quat1 = pair[0].get_global_pose()
        pos2, quat2 = pair[1].get_global_pose()
        fitness += get_distance(pos1, pos2)
    return(-1 * fitness)

'''

def fitness_func(solution, solution_idx, ga_instance):
    # Decode the solution array into a matrix (num_objects, 3)
    
    set = []
    for i in solution:
        set.append(i)
    set = np.array(set)
    x = np.abs(set)
    fitness = np.sum(set)
    # Calculate the total distance between all pairs of objects
    
    # Negative distance for minimization
    return -fitness


def mutation_function(offspring, mutation_percent_genes):
    random_mutation_min_val = -0.01  # Small mutation range
    random_mutation_max_val = 0.01   # Small mutation range
    for i, child in enumerate(offspring):
        if (i+1 % 3) != 0:
            random_mutation_values = np.random.uniform(low=random_mutation_min_val, 
                                                   high=random_mutation_max_val, 
                                                   size=2)
            random_mutation_values.append(0)
            child += random_mutation_values
    return offspring

def run_ga(actors):
    initial_positions = []
    for actor in actors:
        pos, quat = actor.get_global_pose()
        initial_positions.append(pos[0])
    initial_positions = np.array(initial_positions).flatten()
    initial_positions = np.vstack((initial_positions, initial_positions))
    ga_instance = pygad.GA(num_generations=num_generations,
                        fitness_func=fitness_func,
                        sol_per_pop=sol_per_pop, 
                        num_genes=num_genes,
                        num_parents_mating = num_parents_mating,
                        mutation_type = mutation_function,
                        initial_population = initial_positions)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    for index, position in enumerate(solution):
        actors[index].set_global_pos(position)


def create_render():
    #Initialize scene
    render = PyPhysxViewer(video_filename='videos/15_test.gif')
    render.add_physx_scene(scene)

    rate = Rate(20)


    #while render.is_active:
    for i in range(10):
        scene.simulate(rate.period())
        run_ga(actors)
        render.update()
        rate.sleep()
    
    print("complete")


set_boundaries(number_actors)
set_items(number_actors)
create_render()