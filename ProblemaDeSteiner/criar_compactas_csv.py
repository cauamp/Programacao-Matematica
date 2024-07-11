import re
import csv
import os


# Função para extrair informações do conteúdo do arquivo
def extract_info(content):
    # Regex para capturar LB e UB
    lb_pattern = re.compile(r'>=\s*(\d+\.\d+e[+-]\d{2})')
    ub_pattern = re.compile(r'Valor da funcao objetivo:\s*(-?\w+)')
    # Regex para capturar o tempo de execução
    time_pattern = re.compile(r'Time:\s+([\d\.]+)')
    # Regex para capturar o número de nós
    nodes_pattern = re.compile(r'% \(\d+;\s*(\d+)\)')
    # Regex para capturar o valor da relaxação linear
    lbr_pattern = re.compile(r'obj\s*=\s*([\d.]+e[\+\-]?\d+)\s*.*?', re.DOTALL)

    lb, ub, execution_time, nodes, lbr = None, None, None, None, None


    ub_match = ub_pattern.search(content)
    if ub_match:
        ub = ub_match.group(1)

    lb_match = lb_pattern.findall(content)
    if lb_match:
        match = lb_match[-1]
        if match == 'tree':
            lb = ub
        else:
            lb = float(match)

    time_match = time_pattern.search(content)
    if time_match:
        execution_time = time_match.group(1)

    nodes_match = nodes_pattern.findall(content)
    if nodes_match:
        nodes = nodes_match[-1]       

    lbr_match = lbr_pattern.findall(content)
    if lbr_match:
        print(lbr_match)
        lbr = lbr_match[-1]

    return lb, ub, execution_time, nodes, float(lbr)

# Função para calcular o gap de relaxação linear
def calculate_gap(ub, lbr):
    return (float(ub) - float(lbr)) / float(lbr) * 100


# Lista de arquivos de saída
log_dir = './logs/'
file_list = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]

# Nome do arquivo CSV de saída
output_csv = 'compacts.csv'

# Campos do CSV
fields = ['formulation', 'test', 'LB', 'UB', 'relaxation (LBR)', 'relaxation gap (%)', 'runtime (s)', 'number of nodes']

# Abrindo o arquivo CSV para escrita
with open(output_csv, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter = ';')
    writer.writerow(fields)  # Escrevendo o cabeçalho

    # Processando cada arquivo
    for file_name in file_list:
        if 'PlanosDeCorte' in file_name:
            continue
        with open(file_name, 'r') as file:
            print(file_name)
            content = file.read()
            lb, ub, execution_time, nodes, lbr = extract_info(content)
            gap = calculate_gap(ub, lbr)

            formulation, test = file_name.split('./logs/')[1].split('_')
            teste = test.split('.txt')[0]
            writer.writerow([formulation, test, lb, ub, lbr, f"{gap:.2f}%" if gap is not None else None, execution_time, nodes])

print(f"Informações extraídas e registradas em {output_csv}.")
