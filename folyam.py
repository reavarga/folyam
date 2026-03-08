import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
import seaborn as sns
import random
import os
import hashlib

def create_structured_numeric_puzzle_logic():
    G = nx.DiGraph()
    correct_path = [('S', 'G', 4), ('G', 'A', 7), ('A', 'F', 4), ('F', 'C', 8), ('C', 'T', 7)]
    extra_edges = [('S', 'B', 9), ('B', 'D', 1), ('G', 'E', 5), ('E', 'T', 2),
                    ('A', 'B', 3), ('F', 'H', 6), ('H', 'T', 2), ('S', 'D', 2), ('D', 'F', 5)]
    G.add_weighted_edges_from(correct_path + extra_edges)

    dijkstra_main = ['T', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,'Z']
    for i in range(len(dijkstra_main)-1):
        G.add_edge(dijkstra_main[i], dijkstra_main[i+1], weight=random.choice([3, 5, 6]))

    G.add_weighted_edges_from([(10, 31, 1), (31, 13, 20), (15, 32, 2), (32, 18, 15), 
                               (20, 33, 3), (33, 34, 2), (34, 'Z', 25),(22,34, 60),
                               (22, 'Z',20), (24,34,10),(21,34,22), (34,20,15),
                                (14,20,34), (13, 33, 44),(12,13,8) ,(13,14,6),('T',10,3),
                                (19,20,4),(10,33,55),(17,18,4),(24,25,7)])
    return G

def show_interactive_graph():
    st.set_page_config(layout="wide")
    st.markdown('''
Az égben a legtöbb felhőt átvivő útvonalat keressük.         
A fűben a legrövidebbet a rovaroknak.  
Egy régi ösvény szélén vadrózsák nőnek.  
Ha megszámolod a bimbókat, először csak csupasz ágat látsz.  
Mellette hamarosan megjelenik egy.  
Aztán mintha a bokor emlékezne:  
minden új hajtás annyi bimbót hoz,  
amennyit az előző kettő együtt.  
''')


    st.markdown("---")
    user_guess = st.text_input("írd ide a megoldásod:")
    
    if st.button("Beküldés"):
        h = hashlib.sha256()
        h.update(user_guess.encode())
        hash_val = h.hexdigest()
        # Thought you could cheat mf?
        if hash_val == '5161dfe35b7c1b3d8ce387032836d5463a089fc767146e78bc51964fbc40459a' \
           or hash_val == 'd3b74d16a2fedca5370afecace8fe071e754b65a0406776cf3bb56e55451de56': 
            st.success("Helyes!")
        else:
            st.error("Próbáld újra")

    G = create_structured_numeric_puzzle_logic()
    net = Network(height="750px", width="100%", bgcolor="#ffffff", directed=True)
    
    palette = sns.color_palette("viridis", 12).as_hex()
    highlight_color = sns.color_palette("flare", 10).as_hex()[1]

    for node in G.nodes():
        if node in ['S', 'T', 'Z']:
            node_color = highlight_color
            node_size = 35 
        else:
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
    
    components.html(html_string, height=800)
    
    if os.path.exists(path):
        os.remove(path)
if "hint_used" not in st.session_state:
    st.session_state.hint_used = False

def reveal_hint():
    st.session_state.hint_used = True

st.button(
    "Need a hint?", 
    on_click=reveal_hint, 
    disabled=st.session_state.hint_used
)

if st.session_state.hint_used:
    st.info("Láss a dolgok mögé!")

if __name__ == "__main__":
    show_interactive_graph()