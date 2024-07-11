import re
import csv
import os


# Função para extrair informações do conteúdo do arquivo
def extract_info(content):
    # Padrões regex para extrair as informações desejadas
    iteracoes_pattern = re.compile(r"Iteracoes: (\d+)")
    cortes_pattern = re.compile(r"Numero de Cortes: (\d+)")
    tempo_pattern = re.compile(r"Total Time: ([\d.]+)")

    # Extraindo as informações usando regex
    iteracoes_match = iteracoes_pattern.search(content)
    cortes_match = cortes_pattern.search(content)
    tempo_match = tempo_pattern.search(content)

    # Verificando se as correspondências foram encontradas e extraindo os valores
    iteracoes = int(iteracoes_match.group(1)) if iteracoes_match else None
    cortes = int(cortes_match.group(1)) if cortes_match else None
    tempo_execucao = float(tempo_match.group(1)) if tempo_match else None

    return iteracoes, cortes, tempo_execucao



# Lista de arquivos de saída
log_dir = './logs/'
file_list = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]

# Nome do arquivo CSV de saída
output_csv = 'cuts.csv'

# Campos do CSV
fields = ['formulation', 'test', 'iterations', 'inserted cuts','runtime (s)', ]

# Abrindo o arquivo CSV para escrita
with open(output_csv, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter = ';')
    writer.writerow(fields)  # Escrevendo o cabeçalho

    # Processando cada arquivo
    for file_name in file_list:
        if 'PlanosDeCorte' not in file_name:
            continue
        with open(file_name, 'r') as file:
            content = file.read()
            iterations,  cuts, execution_time = extract_info(content)

            formulation, test = file_name.split('./logs/')[1].split('_')
            test = test.split('.txt')[0]
            writer.writerow([formulation, test, iterations, cuts, execution_time])

print(f"Informações extraídas e registradas em {output_csv}.")
