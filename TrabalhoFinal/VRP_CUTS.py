import math
from utils.vrp_utils import print_routes, plot_routes
from pyomo.environ import ConcreteModel, Var, Objective, NonNegativeReals, Boolean, minimize, ConstraintList, SolverFactory, Binary
import numpy as np  
import networkx as nx
import time 
import argparse

# Configurar o Argument Parser
parser = argparse.ArgumentParser(description='Resolução do VRP e plotagem das rotas.')
parser.add_argument('--path', type=str, required=False, help='Caminho para salvar a imagem das rotas.')
args = parser.parse_args()

# Dados de entrada
V = {}  # Conjunto de pontos de visita
K = {}  # Conjunto de veículos
d = {}  # Distâncias das arestas

# Leitura da entrada
n, v = map(int, input("Digite o número de vértices e o número de veículos: ").split())  # Número de vértices e número de veículos

# Leitura das coordenadas dos vértices
for i in range(n):
    x, y = map(int, input(f"Digite as coordenadas do ponto {i + 1}: ").split())
    V[i] = (x, y)

# Leitura dos veículos
for i in range(v):
    b, s = map(float, input(f"Digite o tempo de bateria (m) e a velocidade do veículo {i + 1} (m/s) ").split())
    K[i] = {'b': b, 's': s, 'c': s*60*b}

# Cálculo das distâncias entre os pontos
for i in range(n):
    for j in range(n):
        if i != j:
            d[(i, j)] = math.sqrt((V[i][0] - V[j][0])**2 + (V[i][1] - V[j][1])**2)


# Criando o modelo
model = ConcreteModel()

# Variáveis binárias que determinam se o veículo k viaja do ponto i ao ponto j
model.x = Var(((i, j, k) for k in K for i in V for j in V if i != j), within=Boolean, initialize=0)

# Variáveis y determina se o ponto i é visitado pelo veículo k
model.y = Var(V.keys(), K, within=Binary, initialize=0)

# Variável auxiliar para o tempo máximo de viagem
model.max_time = Var(within=NonNegativeReals, initialize=0)

# Função objetivo: minimizar o tempo máximo de cobertura de todos os pontos
model.obj = Objective(expr=model.max_time, sense=minimize)

# Adicionando as restrições ao modelo
model.cnst = ConstraintList()

# Cada ponto deve ser visitado exatamente uma vez por algum veículo, exceto o depósito
for i in V:
    if i == 0:   
        # Cada veículo deve sair do depósito e retornar ao depósito
        model.cnst.add(sum(model.x[i, j, k] for j in V if i != j for k in K) == len(K))
        model.cnst.add(sum(model.x[j, i, k] for j in V if i != j for k in K) == len(K))
    else:
        #Se um veiculo chega no ponto i, ele deve sair do ponto i
        model.cnst.add(sum(model.x[i, j, k] for j in V if i != j for k in K) == 1)
        model.cnst.add(sum(model.x[j, i, k] for j in V if i != j for k in K) == 1)
    for k in K:
        # Se o veículo k visita o ponto i, então y[i, k] = 1
        model.cnst.add(sum(model.x[i, j, k] for j in V if i != j) == model.y[i, k])
        model.cnst.add(sum(model.x[j, i, k] for j in V if i != j) == model.y[i, k])


# Tempo de viagem não pode exceder a capacidade maxima do veículo e o tempo maximo 
for k in K:
    model.cnst.add(sum(d[i, j] * model.x[i, j, k] for i in V for j in V if i != j) <= K[k]['c'])
    model.cnst.add(sum(d[i, j] * model.x[i, j, k] / K[k]['s'] for i in V for j in V if i != j) <= model.max_time)
            

model.subtour_elimination = ConstraintList()
# Eliminação de subcircuito
def find_arcs(model, V, K):
    arcs = []
    for i in V:
        for j in V:
            if i != j:
                for k in K:
                    if np.isclose(model.x[i, j, k].value, 1):
                        arcs.append((i, j))
    return arcs

def find_subtours(arcs):
    G = nx.DiGraph(arcs)
    subtours = list(nx.strongly_connected_components(G))
    return subtours

def eliminate_subtours(model, subtours, V, K):
    proceed = False
    for S in subtours:
        if 0 not in S:
            proceed = True
            Sout = {i for i in V if i not in S}
            for h in S:
                for k in K:
                    model.subtour_elimination.add(
                      model.y[h, k] <= sum(model.x[i, j, k] for i in S for j in Sout)
                    )
    return proceed

def solve_step(model, solver, V, K):
    sol = solver.solve(model, tee=True)
    arcs = find_arcs(model, V, K)
    subtours = find_subtours(arcs)
    time.sleep(0.1)
    proceed = eliminate_subtours(model, subtours, V, K)
    return sol, proceed 

def solve(model, solver, V, K, tmlim=30*60):
    tm = 0
    cuts = 0
    proceed = True
    while proceed:
        sol, proceed = solve_step(model, solver, V, K)
        tm += sol.solver.time
        cuts +=1
        if tm >= tmlim:
            break
    
    print("\nResumo da Execucao:")
    print(f'{sol}\n--------------------------------------')
    print("Tempo total de execucao: ", tm)
    print("Numero de cortes: ", cuts)	
    return sol

# Resolver o modelo
solver = SolverFactory('glpk')
solver.options['tmlim'] = 30 * 60
results = solve(model, solver, V, K, tmlim=30*60)

if (results.solver.status == 'ok') :

    if(results.solver.termination_condition == 'optimal'):
        print("\nSolucao Otima Encontrada")
        print('-------------------------------------')
    # Extraindo informações do resultado
    print(f"Tempo para corbertura total: {model.obj():.2f} segundos")
    for i in range(v):
        print(f"Veiculo {i} Tempo Maximo de Voo {K[i]['b']/60:.2f} horas | Velocidade {K[i]['s']:.2f} m/s | Capacidade de corbetura {K[i]['c']/1000:.2f} km")
    print('-------------------------------------')

    # Imprimir as rotas de cada veículo
    print_routes(model, K, V, d)
    if args.path:
        plot_routes(model, K, V, d, save= True, path= args.path)
    else:
        plot_routes(model, K, V, d)
else:
    print("Nenhuma solução viável encontrada.")
