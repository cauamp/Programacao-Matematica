import matplotlib.pyplot as plt
import networkx as nx

def print_routes(model, V, N ,d):
    """Imprime a rota de cada veículo."""
    for k in V:
        route = [0]  # Começa do depósito
        current_location = 0
        while True:
            next_location = None
            for i in N:
                if i != current_location and model.x[current_location, i, k].value == 1:
                    next_location = i
                    break
            if next_location is None or next_location == 0:
                break
            route.append(next_location)
            current_location = next_location
        route.append(0)  # Volta ao depósito
        total_dist = sum(d[current_location, next_location] for current_location, next_location in zip(route, route[1:]))
        total_time = total_dist / V[k]['s']
        final_route= ' -> '.join(str(i) for i in route)
        print(f"Rota do veiculo {k}: {final_route} | Distancia percorrida: {total_dist/1000:.2f} km | Tempo de deslocamento: {total_time/ 60:.2f} minutos")

def plot_routes(model, V, N, d, save = False, path = None):
    """Plota a rota de cada veículo em um gráfico com cores diferentes."""
    # Criação do grafo
    G = nx.DiGraph()
    
    # Cores para os veículos
    colors = plt.cm.get_cmap('nipy_spectral', len(V))
    
    # Criação de um dicionário para as cores das arestas
    edge_colors = {}

    # Adicionar arestas e cores ao grafo
    for k_idx, k in enumerate(V):
        for i in N:
            for j in N:
                if i != j and model.x[i, j, k].value == 1:
                    dist = {round(d[i, j]/1000, 2)}
                    time = {round(d[i, j]/V[k]['s']/60, 2)}
                    G.add_edge(i, j, weight="{}km \n {}min".format(dist, time), color=(colors(k_idx)))
                    edge_colors[(i, j)] =(colors(k_idx)) # Mapeia a cor para a aresta

    # Configurações do grafo
    pos = {i: (N[i][0], N[i][1]) for i in N}
    labels = {i: f'{i}' for i in N}
    edge_color_list = [edge_colors.get((u, v), 'black') for u, v in G.edges()]  # Lista de cores para as arestas

    # Lista de cores para os nós, com a raiz (nó 0) em verde e os outros em azul claro
    node_color_list = ['green' if node == 0 else 'lightblue' for node in G.nodes()]

    # Desenho do grafo
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=700, node_color=node_color_list, font_size=10, font_weight='bold', edge_color=edge_color_list, width=2.0)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Rotas dos Veículos")
    if save:
        plt.savefig(path)
    else:
        plt.show()
