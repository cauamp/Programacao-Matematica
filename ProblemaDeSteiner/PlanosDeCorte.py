from pyomo.environ import (
    Var,
    Objective,
    ConstraintList,
    SolverFactory,
    Boolean,
    ConcreteModel,
    minimize,
    value,
)

# Leitura da entrada
n, m = map(int, input().split())  # Número de vértices e número de arestas

# Dados de entrada
V = set(range(0, n))  # Conjunto de vértices
E = set()  # Conjunto de arestas
d = {}  # Distâncias das arestas

# Leitura das arestas
for _ in range(m):
    v, u, w = map(int, input().split())
    v, u = v - 1, u - 1
    E.add((v, u))  # Adiciona aresta ao conjunto E
    d[(v, u)] = w  # Define a distância da aresta
    E.add((u, v))  # Adiciona a aresta reversa
    d[(u, v)] = w  # Define a distância da aresta

# Leitura do número de nós terminais
t = int(input())

# Conjunto de nós terminais
T = list(int(input()) - 1 for _ in range(t))

print("------------ Leitura completa ------------")

raiz = T[0]  # Nó raiz
T_r = T[1:]  # Conjunto de nós terminais sem a raiz

# Definir o modeloo Pyomo
modelo = ConcreteModel()

# Variáveis binárias para indicar se uma aresta (i, j) está no conjunto da árvore de Steiner
modelo.x = Var(E, within=Boolean)

# Função objetivo: minimizar o custo total das arestas na árvore de Steiner
modelo.objetivo = Objective(
    expr=sum(modelo.x[i, j] * d[i, j] for (i, j) in E), sense=minimize
)


# Lista de restrições
modelo.restricoes = ConstraintList()

# Restrições de grau para nós terminais
for k in T_r:
    modelo.restricoes.add(sum(modelo.x[i, k] for i in V if (i, k) in E) == 1)


# Função para busca em largura (BFS) para verificar conectividade
def bfs(src):
    eps = 0.0001  # Pequeno valor para comparação de float
    queue = [src]  # Inicializa a fila com o nó fonte

    visitados = [False for i in V]
    visitados[src] = True

    while len(queue):
        v = queue.pop(0)
        for u in V:
            if (
                ((v, u) in E)
                and (not visitados[u])
                and (
                    (abs(1 - value(modelo.x[v, u])) < eps)
                    or (abs(1 - value(modelo.x[u, v])) < eps)
                )
            ):
                visitados[u] = True
                queue.append(u)

    return visitados


# Resolver o modelo
solver = SolverFactory("glpk")
solver.options["tmlim"] = 1800
solver.options["nopresol"] = ""  # Desativa o pré-processamento


# Conjunto inicial de cortes
L = []
tempo_total = 0
count = 1

while True:
    solver.options["tmlim"] = 1800
    results = solver.solve(modelo, tee=True)
    tempo_iteracao = results.solver.time
    tempo_total += tempo_iteracao
    print(f"Tempo na iteracao {count}: {tempo_iteracao}, Tempo total acumulado: {tempo_total}")

    L_mudou = False
    vistos  = [False] * n

    for i in V:
        if not vistos [i]:
            S = bfs(i)
            vistos  = [(vistos [i] or S[i]) for i in V]

            tem_raiz = S[raiz]
            tem_terminal = any(S[k] for k in T_r)

            if not tem_raiz and tem_terminal:
                conjunto_complementar  = [not S[i] for i in V]
                L.append(conjunto_complementar )
                L_mudou = True

    if not L_mudou or tempo_total >= 1800:
        break

    for S in L:
        modelo.restricoes.add(
            sum(
                modelo.x[i, j]
                for i in V
                for j in V
                if (S[i]) and (not S[j]) and (i, j) in E
            )
            >= 1
        )
    count += 1

# Imprimir as informações solicitadas
print("\nResumo da Execucao:")
print(f"Valor da funcao objetivo: {modelo.objetivo()}")
print(f"Numero de Cortes: {len(L)}")
print(f"Iteracoes: {count}")
print(f"Total Time: {tempo_total}")
