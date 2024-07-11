import subprocess
import os

def execute_scripts(script_files, input_files, log_dir):

    for input_file in input_files:
        for script in script_files:
            print(f"Modelo: {script} Input {input_file}")
            # Cria um nome de arquivo de log baseado no nome do script e do input
            log_file = os.path.join(log_dir, f"{os.path.splitext(os.path.basename(script))[0]}_{os.path.splitext(os.path.basename(input_file))[0]}.txt")
                
            try:
                # Verifica se o arquivo de script e de input existem
                if not os.path.isfile(script):
                    raise FileNotFoundError(f"Script file not found: {script}")
                if not os.path.isfile(input_file):
                    raise FileNotFoundError(f"Input file not found: {input_file}")
                if  os.path.isfile(log_file):
                    print("JA PRONTO")
                    continue
                
                # Abre o arquivo de input para leitura
                with open(input_file, 'r') as infile:
                    input_data = infile.read()
                
                # Executa o script com o input fornecido
                process = subprocess.Popen(['python', script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(input=input_data)
                
                print(stdout, stderr)
                # Verifica se o arquivo de log está sendo criado
                if not os.path.exists(log_dir):
                    raise OSError(f"Falha ao criar o diretório de logs: {log_dir}")
                
                # Escreve a saída e erros no arquivo de log
                with open(log_file, 'w') as log:
                    log.write(f"{stdout}\n")
                    if stderr:
                        log.write(f"Erros:\n{stderr}\n")
                    log.write("\n" + "-"*80 + "\n\n")
            
            except Exception as e:
                # Em caso de erro, grava o erro no log
                with open(f"{log_file.replace('logs/', 'logs/error_')}", 'w') as log:
                    log.write(f"Erro ao executar o script: {script}\n")
                    log.write(f"Erro: {str(e)}\n")
                    log.write("\n" + "-"*80 + "\n\n")
                print(f"Erro ao executar o script {script}. Veja o log em {log_file} para mais detalhes.")

            


# Lista de arquivos de scripts a serem executados
script_files = [
    './MultiplaMercadoria.py',
    './UnicaMercadoria.py',
    './MTZ.py',
    './PlanosDeCorte.py'
]

# Lista de arquivos de input correspondentes aos scripts
input_files = [
    './tests/1.txt',
    './tests/2.txt',
    './tests/3.txt',
    './tests/4.txt',
    './tests/5.txt',
    './tests/6.txt',
    './tests/7.txt',
    './tests/8.txt',
    './tests/9.txt',
    './tests/10.txt',
    './tests/11.txt',
    './tests/12.txt',
    './tests/13.txt',
    './tests/14.txt',
    './tests/15.txt',
    './tests/16.txt',
    './tests/17.txt',
    './tests/18.txt'
]

# Diretório onde os arquivos de log serão armazenados
log_dir = 'logs/'

# Executa os scripts com os inputs fornecidos e registra os logs
execute_scripts(script_files, input_files, log_dir)
