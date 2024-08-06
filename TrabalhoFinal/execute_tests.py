import subprocess
import os
import glob
import concurrent.futures
import traceback

def execute_script(script, input_file, log_dir):
    log_file = os.path.join(log_dir, f"{os.path.splitext(os.path.basename(script))[0]}_{os.path.splitext(os.path.basename(input_file))[0]}.txt")
    
    try:
        # Verifica se o arquivo de script e de input existem
        if not os.path.isfile(script):
            raise FileNotFoundError(f"Script file not found: {script}")
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Abre o arquivo de input para leitura
        with open(input_file, 'r') as infile:
            input_data = infile.read()
            
        print(f"Executando script {script} com input {input_file}...")
        # Executa o script com o input fornecido
        process = subprocess.Popen(['python', script, '--path', log_file.replace('.txt', '.png')],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Define um timeout de 30 minutos (1800 segundos)
        try:
            stdout, stderr = process.communicate(input=input_data, timeout=1980)
        except subprocess.TimeoutExpired:
            process.kill()  # Termina o processo se exceder o timeout
            stdout, stderr = process.communicate()  # Obtém o que foi produzido até o momento
            print(f"O processo para o script {script} com o input {input_file} excedeu o limite de tempo de 30 minutos.")
        
        # Verifica se o diretório de logs existe
        if not os.path.exists(log_dir):
            raise OSError(f"Falha ao criar o diretório de logs: {log_dir}")
        
        # Escreve a saída e erros no arquivo de log
        with open(log_file, 'w') as log:
            log.write(f"{stdout}\n")
            if stderr:
                log.write(f"Erros:\n{stderr}\n")
            log.write("-"*80 + "\n")
    
    except Exception as e:
        # Em caso de erro, grava o erro no log
        with open(f"{log_file.replace('logs/', 'logs/error_')}", 'w') as log:
            log.write(f"Erro ao executar o script: {script}\n")
            log.write(f"Erro: {str(e)}\n")
            log.write("\n" + "-"*80 + "\n\n")
        print(f"Erro ao executar o script {script}. Veja o log em {log_file} para mais detalhes.")
        print("Detalhes do erro:\n", traceback.format_exc())
            


if __name__ == '__main__':
    # Lista de arquivos de scripts a serem executados
    script_files = [
        './VRP_CUTS.py',
        './VRP_MTZ.py',
    ]
    # Lista de arquivos de input correspondentes aos scripts
    tests_dir = 'tests/'
    input_files = glob.glob(os.path.join(tests_dir, '*'))
    # Diretório onde os arquivos de log serão armazenados
    log_dir = 'logs/'
    os.makedirs(log_dir, exist_ok=True)

    # Executa os scripts em paralelo
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(execute_script, script, input_file, log_dir) for input_file in input_files for script in script_files]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Captura exceções se ocorrerem
            except Exception as e:
                print(f"Erro ao executar uma das tarefas em paralelo: {e}")