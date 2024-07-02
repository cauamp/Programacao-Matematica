from pyomo.environ import Var, ConcreteModel, Objective, ConstraintList, SolverFactory, Binary, NonNegativeReals, minimize
import networkx as nx
import matplotlib.pyplot as plt

def print_steiner_tree(modelo):
    # Criando o grafo
    G = nx.Graph()

    # Adicionando arestas do grafo baseadas nas variáveis x
    for (i, j) in modelo.x:
        if modelo.x[i, j].value == 1:
            G.add_edge(i, j, weight=d[(i, j)])

    # Posicionando os vértices
    pos = nx.spring_layout(G)

    # Desenhando os vértices e as arestas
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Exibindo o grafo
    plt.title('Árvore de Steiner')
    plt.show()
    
# Leitura da entrada
n, m = map(int, input().split())  # Número de vértices e número de arestas

# Dados de entrada
V = set(range(1, n + 1))  # Conjunto de vértices
E = set()  # Conjunto de arestas
d = {}  # Distâncias das arestas

# Leitura das arestas
for _ in range(m):
    v, u, w = map(int, input().split())
    E.add((v, u))  # Adiciona aresta ao conjunto E
    d[(v, u)] = w  # Define a distância da aresta
    E.add((u, v))  # Adiciona a aresta reversa
    d[(u, v)] = w  # Define a distância da aresta

# Leitura do número de nós terminais
t = int(input())

# Conjunto de nós terminais
T = set(int(input()) for _ in range(t))

print('------------ Leitura completa ------------')

# Criando o modelo
modelo = ConcreteModel()

# Variáveis binárias x
modelo.x = Var(E, within=Binary)

# Variáveis de fluxo f para cada nó terminal em T
modelo.f = Var(E, T - {1}, within=NonNegativeReals)

# Função objetivo: minimizar a soma das distâncias das arestas em x
modelo.objetivo = Objective(expr=sum(d[i, j] * modelo.x[i, j] for i, j in E), sense=minimize)

# Restrições de fluxo para cada mercadoria k ∈ T \ {1}
modelo.restricao_fluxo_mercadoria = ConstraintList()

raiz = list(T)[0]  # Nó raiz
T_r = T - {raiz}  # Conjunto de nós terminais sem a raiz

for k in T_r:
    for i in V:
        if i == k:
            modelo.restricao_fluxo_mercadoria.add(
                sum(modelo.f[j, i, k] for j in V if (j, i) in E) - sum(modelo.f[i, j, k] for j in V if (i, j) in E) == 1
            )
        elif i == raiz:
            modelo.restricao_fluxo_mercadoria.add(
                sum(modelo.f[j, i, k] for j in V if (j, i) in E) - sum(modelo.f[i, j, k] for j in V if (i, j) in E) == -1
            )
        else:
            modelo.restricao_fluxo_mercadoria.add(
                sum(modelo.f[j, i, k] for j in V if (j, i) in E) - sum(modelo.f[i, j, k] for j in V if (i, j) in E) == 0
            )

# Restrições de capacidade de fluxo para cada mercadoria k ∈ T \ {1}
modelo.restricao_capacidade = ConstraintList()
for (i, j) in E:
    for k in T_r:
        modelo.restricao_capacidade.add(modelo.f[i, j, k] <= modelo.x[i, j])

# Restrições de binaridade
modelo.restricao_binaridade = ConstraintList()
for (i, j) in E:
    modelo.restricao_binaridade.add(modelo.x[i, j] <= 1)

# Resolver o modelo
solver = SolverFactory('glpk')
solver.options['tmlim'] = 30 * 60
resultado = solver.solve(modelo, tee=True)

# Imprimir a solução
print("\nSolucao Otima Encontrada")

# Extraindo informações do resultado
LB = resultado.problem.lower_bound
UB = resultado.problem.upper_bound
relaxacao = modelo.objetivo()
gap_relaxacao = ((UB - LB) / UB) * 100 if UB != 0 else float('inf')

# Imprimir as informações solicitadas
print("\nResumo da Execucao:")
print(f"Valor da funcao objetivo: {modelo.objetivo()}")
print(f"Melhor Limite Inferior (LB): {LB}")
print(f"Melhor  Limite Superior (UB): {UB}")
print(f"Relaxacao (LBR): {relaxacao}")
print(f"Gap de Relaxacao (%): {gap_relaxacao}")
print(f'--------------------------------------\n{resultado}')
