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
    vertices = []
    
    # Gerar vértices
    for i in range(num_vertices):
        x = random.randint(-10000, 10000)
        y = random.randint(-10000, 10000)
        vertices.append((x, y))
    
    # Calcular a distância média entre os vértices
    avg_distance = calculate_average_distance(vertices)
    
    def create_instance(num_vertices, num_vehicles, difficulty_factor):
        instance = []
        
        # Adicionar número de vértices e veículos à instância
        instance.append(f"{num_vertices} {num_vehicles}")
        
        # Adicionar vértices à instância
        for x, y in vertices:
            instance.append(f"{x} {y}")
        
        # Gerar parâmetros dos veículos
        for i in range(num_vehicles):
            speed = random.uniform(5, 15) * difficulty_factor
            battery = (avg_distance / speed) / (num_vehicles - 1) * difficulty_factor
            instance.append(f"{battery:.2f} {speed:.2f}")
        
        return instance

    # Instância fácil
    easy_instance = create_instance(num_vertices, num_vehicles, difficulty_factor=1.0)
    
    # Instância difícil (menos veículos e/ou menor bateria/velocidade)
    difficult_instance = create_instance(num_vertices, max(2, num_vehicles - 1), difficulty_factor=0.5)
    
    return easy_instance, difficult_instance

def write_instance_to_file(filename, instance):
    with open(filename, 'w') as f:
        for line in instance:
            f.write(line + "\n")

num_instances = 20
max_vertices = 15

# Criar diretório .tests se não existir
os.makedirs('./tests', exist_ok=True)

for idx in range(num_instances):
    num_vertices = random.randint(3, max_vertices)  # Número de vértices 
    num_vehicles = random.randint(2, min(num_vertices-1, 5))  # Número de veículos
    instance0, instance1 = generate_vrp_instance(num_vertices, num_vehicles)
    filename = f'./tests/{idx + 1}_1.txt'
    write_instance_to_file(filename, instance0)
    filename = f'./tests/{idx + 1}_2.txt'
    write_instance_to_file(filename, instance1)