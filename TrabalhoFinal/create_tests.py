import random
import os
import math

def calculate_average_distance(vertices):
    total_distance = 0
    num_pairs = 0
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[j]
            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            total_distance += distance
            num_pairs += 1
    return total_distance / num_pairs if num_pairs > 0 else 0

def generate_vrp_instance(num_vertices, num_vehicles):
    instance = []
    vertices = []
    
    # Add number of vertices and vehicles to the instance
    instance.append(f"{num_vertices} {num_vehicles}")
    
    # Generate vertices
    for i in range(num_vertices):
        x = random.randint(-10000, 10000)
        y = random.randint(-10000, 10000)
        vertices.append((x, y))
        instance.append(f"{x} {y}")
    
    # Calculate average distance between vertices
    avg_distance = calculate_average_distance(vertices)
    
    # Generate vehicle parameters
    for i in range(num_vehicles):
        # To ensure that the coverage capacity is close to the average distance,
        # we adjust battery and speed such that battery * speed is close to avg_distance.
        speed = random.uniform(5, 15)
        battery = (avg_distance / speed)/num_vehicles-1
        instance.append(f"{battery:.2f} {speed:.2f}")
    
    return instance

def write_instance_to_file(filename, instance):
    with open(filename, 'w') as f:
        for line in instance:
            f.write(line + "\n")

num_instances = 10
max_vertices = 20

# Criar diretório .tests se não existir
os.makedirs('./tests', exist_ok=True)

for idx in range(num_instances):
    num_vertices = random.randint(2, max_vertices)  # Número de vértices entre 2 e 20
    num_vehicles = random.randint(1, 5)  # Número de veículos entre 1 e 5
    instance = generate_vrp_instance(num_vertices, num_vehicles)
    filename = f'./tests/{idx + 1}.txt'
    write_instance_to_file(filename, instance)
