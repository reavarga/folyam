import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
import seaborn as sns
import random
import os

def create_structured_numeric_puzzle_logic():
    G = nx.DiGraph()
    # Part 1: Flow
    correct_path = [('S', 'G', 4), ('G', 'A', 7), ('A', 'F', 4), ('F', 'C', 8), ('C', 'T', 7)]
    extra_edges = [('S', 'B', 9), ('B', 'D', 1), ('G', 'E', 5), ('E', 'T', 2),
                    ('A', 'B', 3), ('F', 'H', 6), ('H', 'T', 2), ('S', 'D', 2), ('D', 'F', 5)]
    G.add_weighted_edges_from(correct_path + extra_edges)

    # Part 2: Dijkstra
    dijkstra_main = ['T', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,'Z']
    for i in range(len(dijkstra_main)-1):
        G.add_edge(dijkstra_main[i], dijkstra_main[i+1], weight=random.choice([3, 5, 6]))

    # Traps
    G.add_weighted_edges_from([(10, 31, 1), (31, 13, 20), (15, 32, 2), (32, 18, 15), 
                               (20, 33, 3), (33, 34, 2), (34, 'Z', 25),(22,34, 60),
                               (22, 'Z',20), (24,34,10),(21,34,22), (34,20,15),
                                (14,20,34), (13, 33, 44),(12,13,8) ,(13,14,6),('T',10,3),
                                (19,20,4),(10,33,55),(17,18,4),(24,25,7)])
    return G

def show_interactive_graph():
    st.set_page_config(layout="wide")
    st.title("Interactive Puzzle: Labels Inside Nodes")
    
    st.markdown("---") # Adds a nice horizontal divider
    user_guess = st.text_input("Enter the shortest path:")
    
    if st.button("Submit Answer"):
        if user_guess == "S-A-T": # Just an example condition
            st.success("Correct!")
        else:
            st.error("Try again!")

    G = create_structured_numeric_puzzle_logic()
    # Adjusted height here to match your requested window size logic
    net = Network(height="750px", width="100%", bgcolor="#ffffff", directed=True)
    
    # Generate Seaborn Palette
    palette = sns.color_palette("viridis", 12).as_hex()
    highlight_color = sns.color_palette("flare", 10).as_hex()[1]

    # Add Nodes manually to ensure labels are INSIDE
    for node in G.nodes():
        # Specific check for S, T, and Z
        if node in ['S', 'T', 'Z']:
            node_color = highlight_color
            node_size = 35 # Making them slightly larger too!
        else:
            # Regular logic: Letters vs Numbers
            node_color = palette[3] if isinstance(node, str) else palette[8]
            node_size = 25
        
        net.add_node(
            node, 
            label=str(node), 
            shape='circle',
            size=node_size, 
            color=node_color, 
            font={
                'size': 20, 
                'face': 'Arial', 
                'color': 'white'
            }
        )

    # Add Edges manually to ensure weights show up properly
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 0)
        net.add_edge(
            u, v, 
            label=str(weight), 
            width=3, 
            color='#34495e',
            arrowStrikethrough=False,
            font={
                'size': 22, 
                'color': '#e74c3c', 
                'strokeWidth': 5, 
                'strokeColor': '#ffffff'
            }
        )

    net.set_options("""
    {
      "physics": {
        "barnesHut": { "gravitationalConstant": -20000, "springLength": 150 },
        "stabilization": {"iterations": 50}
      },
      "edges": { "arrows": { "to": { "enabled": true, "scaleFactor": 1.2 } } }
    }
    """)

    path = "temp_graph.html"
    net.save_graph(path)
    with open(path, 'r', encoding='utf-8') as f:
        html_string = f.read()
    
    # Streamlit component height (kept close to 800 to avoid excess scrolling)
    components.html(html_string, height=800)
    
    if os.path.exists(path):
        os.remove(path)

if __name__ == "__main__":
    show_interactive_graph()