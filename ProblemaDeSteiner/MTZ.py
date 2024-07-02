from pyomo.environ import Var, ConcreteModel, Objective, ConstraintList, SolverFactory, Boolean, NonNegativeIntegers, minimize

    
# Dados de entrada
V = set()  # Conjunto de vértices
E = set()  # Conjunto de arestas
T = set()  # Conjunto de nós terminais
d = {}  # Distâncias das arestas

# Leitura da entrada
n, m = map(int, input().split())  # Número de vértices e número de arestas

# Leitura das arestas e distâncias
for _ in range(m):
    v, u, w = map(int, input().split())
    E.add((v, u))  # Adiciona aresta ao conjunto E
    d[(v, u)] = w  # Define a distância da aresta
    E.add((u, v))  # Adiciona a aresta reversa (caso seja não direcionado)
    d[(u, v)] = w  # Define a distância da aresta reversa

# Leitura do número de nós terminais
t = int(input())

# Leitura dos nós terminais
for _ in range(t):
    terminal = int(input())
    T.add(terminal)

print('------------ Leitura completa ------------')

# Criando o modelo
modelo = ConcreteModel()

# Conjunto de vértices
V = set(range(1, n + 1))

# Variáveis binárias x
modelo.x = Var(E, within=Boolean)

# Variáveis u para desigualdades de Miller-Tucker-Zemlin
modelo.u = Var(V, within=NonNegativeIntegers, bounds=(0, len(V)-1))

# Função objetivo: minimizar a soma das distâncias das arestas em x
modelo.objetivo = Objective(expr=sum(d[i, j] * modelo.x[i, j] for i, j in E), sense=minimize)

# Lista de restrições
modelo.restricoes = ConstraintList()

raiz = list(T)[0]  # Nó raiz
T_r = T - {raiz}  # Conjunto de nós terminais sem a raiz

# Adiciona restrições para garantir que cada nó terminal está conectado
for k in T_r:
    modelo.restricoes.add(sum(modelo.x[i, k] for i in V if (i, k) in E) >= 1)

# Adiciona restrição para garantir que a raiz está conectada
modelo.restricoes.add(sum(modelo.x[raiz, i] for i in V if (raiz, i) in E) >= 1)

# Restrições de grau para garantir conectividade
for i in V:
    if i not in T:
        modelo.restricoes.add(sum(modelo.x[i, j] for j in V if (i, j) in E) <= t * sum(modelo.x[j, i] for j in V if (j, i) in E))

# Define a restrição para a variável de ordem do nó raiz

modelo.restricoes.add(modelo.u[raiz] == 0)

# Restrições de Miller-Tucker-Zemlin para eliminar subcircuitos
for j in V:
    if j == raiz:
        continue
    for i in V:
        if (i, j) in E:
            modelo.restricoes.add(modelo.u[j] >= modelo.u[i] + (n - 1) * modelo.x[i, j] + (n - 3) * modelo.x[j, i] - (n - 2))
            
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
