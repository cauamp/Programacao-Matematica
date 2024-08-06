import os
import csv

# Função para extrair os dados dos arquivos de teste
def extract_test_data(test_path):
    with open(test_path, 'r') as file:
        lines = file.readlines()
        # Os primeiros números são o id, número de vértices e número de carros
        id = os.path.basename(test_path).split('.')[0]
        num_vertices, num_carros = map(int, lines[0].split())
        return id, num_vertices, num_carros

# Função para extrair o tempo de execução dos arquivos de log
def extract_time(log_path, method):
    if not os.path.exists(log_path):
        return None
    with open(log_path, 'r') as file:
        lines = file.readlines()
        if method == 'MTZ':
            for line in lines:
                if line.startswith('  Time:'):
                    return float(line.split()[1])
        elif method == 'CUTS':
            for line in lines:
                if line.startswith('Tempo total de execucao: '):
                    return float(line.split()[4])
    return None

# Caminhos dos diretórios
test_dir = './tests'
log_dir = './logs'
methods = ['MTZ', 'CUTS']

# Nome do arquivo CSV de saída
csv_file = 'test_results.csv'

# Lista para armazenar os dados
data = []

# Iterar sobre os arquivos de teste
for test_file in os.listdir(test_dir):
    if test_file.endswith('.txt'):
        test_path = os.path.join(test_dir, test_file)
        id, num_vertices, num_carros = extract_test_data(test_path)
        row = [id, num_vertices, num_carros]
        
        # Adicionar tempos de execução para cada método
        for method in methods:
            log_file = f'VRP_{method}_{id}.txt'
            log_path = os.path.join(log_dir, log_file)
            time = extract_time(log_path, method)
            row.append(time)
        
        data.append(row)

# Escrever os dados no arquivo CSV
header = ['ID', 'NumVertices', 'NumCarros', 'MTZ_Time', 'CUTS_Time']

with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)

print(f"CSV criado com sucesso: {csv_file}")
