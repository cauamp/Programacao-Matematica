from pyomo.environ import ConcreteModel, Var, Objective, ConstraintList, SolverFactory, Binary, NonNegativeReals, minimize, Constraint

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

# Variáveis de fluxo f
modelo.f = Var(E, within=NonNegativeReals)

# Função objetivo: minimizar a soma das distâncias das arestas em x
modelo.objetivo = Objective(expr=sum(d[i, j] * modelo.x[i, j] for i, j in E), sense=minimize)

# Lista de restrições
modelo.restricoes = ConstraintList()

raiz = list(T)[0]  # Nó raiz
T_r = T - {raiz}  # Conjunto de nós terminais sem a raiz

# Restrições de fluxo para nós terminais
for i in T_r:
    modelo.restricoes.add(
        sum(modelo.f[j, i] for j in V if (j, i) in E) - sum(modelo.f[i, j] for j in V if (i, j) in E) == 1
    )

# Restrições de fluxo para nós não terminais
for i in V - T:
    modelo.restricoes.add(
        sum(modelo.f[j, i] for j in V if (j, i) in E) - sum(modelo.f[i, j] for j in V if (i, j) in E) == 0
    )

# Restrições de capacidade de fluxo
for (i, j) in E:
    modelo.restricoes.add(modelo.f[i, j] <= len(T_r) * modelo.x[i, j])

# Restrições de binaridade já estão definidas pelas variáveis binárias

# Restrições de não negatividade já estão definidas pelas variáveis de fluxo

# Resolver o modelo
solver = SolverFactory('glpk')
solver.options['tmlim'] = 1800
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
