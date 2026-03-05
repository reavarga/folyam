import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import random

sns.set_theme(style="white")
node_colors = sns.color_palette("viridis", 12)

def create_structured_numeric_puzzle():
    G = nx.DiGraph()

    # --- 1. RÉSZ: FOLYAM (S -> T) ---
    correct_path_1 = [
        ('S', 'G', 4), ('G', 'A', 7), ('A', 'F', 4), ('F', 'C', 8), ('C', 'T', 7)
    ]
    extra_edges_1 = [
        ('S', 'B', 9), ('B', 'D', 1), ('G', 'E', 5), ('E', 'T', 2),
        ('A', 'B', 3), ('F', 'H', 6), ('H', 'T', 2), ('S', 'D', 2), ('D', 'F', 5)
    ]
    G.add_weighted_edges_from(correct_path_1 + extra_edges_1)

    # --- 2. RÉSZ: SZÁMOS DIJKSTRA (T -> Z) ---
    dijkstra_main = ['T', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 'Z']
    custom_weights = {5: 3, 8: 8, 13: 4, 21: 5}

    for i in range(len(dijkstra_main)-1):
        u, v = dijkstra_main[i], dijkstra_main[i+1]
        idx = i + 5
        w = custom_weights.get(idx, random.choice([3, 5, 6]))
        G.add_edge(u, v, weight=w)

    # Csapdák - Fontos, hogy a csúcsnevek (31, 32...) egyezzenek a pozíciókkal!
    G.add_weighted_edges_from([(10, 31, 1), (31, 13, 20), (15, 32, 2), (32, 18, 15), 
                               (20, 33, 3), (33, 34, 2), (34, 'Z', 25)])

    # --- 3. A RENDEZÉS ---
    pos = {
        'S': [0, 2], 'G': [1, 3], 'B': [1, 1], 'A': [2, 3], 'D': [2, 1],
        'F': [3, 3], 'E': [3, 1], 'C': [4, 3], 'H': [4, 1], 'T': [5, 2]
    }

    # Főút elrendezése
    for i, node in enumerate(dijkstra_main[1:-1]): 
        col = (i // 3)*1.5 + 6   
        row = (i % 3)*1.2 + 1    
        pos[node] = [col, row]

    # CSAPDÁK ÉS Z FIXÁLÁSA (Ha ezek nincsenek benne, repülnek a 0,0-ba!)
    pos[31] = [6.5, 4]
    pos[32] = [8.5, 0]
    pos[33] = [10.5, 4]
    pos[34] = [11.5, 0]
    pos['Z'] = [14, 2] # Kicsit messzebb tettem a Z-t

    plt.figure(figsize=(30, 120))
    
    # Élek rajzolása
    nx.draw_networkx_edges(G, pos, edge_color="#000000", width=1.5, arrowsize=30, 
                           connectionstyle="arc3,rad=0.1", alpha=0.7)
    
    # Csomópontok
    nodes = list(G.nodes())
    node_colors_list = [node_colors[4] if isinstance(n, str) and n != 'Z' else node_colors[9] for n in nodes]
    
    nx.draw_networkx_nodes(G, pos, node_size=1100, node_color=node_colors_list, )
    nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold', font_size=10)
    
    # Súlyok - A label_pos=0.3 segít, hogy ne fedjék egymást
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, 
                                 font_color='#bf360c', font_weight='bold', 
                                 label_pos=0.3, rotate=False, bbox=dict(alpha=0))

    plt.axis('off')
    plt.show()

create_structured_numeric_puzzle()