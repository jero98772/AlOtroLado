import networkx as nx
import pandas as pd
import pydeck as pdk


data = pd.read_json("data_json.json")#.head(10000)
Grafo = nx.Graph()

source=""
tarjet=""
print(data["edges"])
print(data["node"])
for i in range(len(data)):
    node=data["node"][i]
    weight=data["weights"][i]
    #weight=(data["length"][i]+data["harassmentRisk"][i]/100)

    Grafo.add_edge(str(data["edges"][i][0]),str(data["edges"][i][1]),weight=weight)
    Grafo.add_node(str(node))

#print(data.to_string())

#dijkstra funciona mal con wegiths pero no da error,dijkstra sin weigths funciona raro
#funcionando
o="Calle 10"
print(data.set_index(["name"]).loc[o])
d=""
nodes=nx.dijkstra_path(Grafo, "[-75.5728593, 6.2115169]", "[-75.5728593, 6.2115169]", weight=None)
#nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight='weight', method='dijkstra')
#nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight=None, method='dijkstra')
#nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight=None, method='bellman-ford')
#nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight='weight', method='bellman-ford')

#no funciona
#nodes=nx.dijkstra_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight='weight')

#no es lo mejor
#nodes=nx.astar_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5714665, 6.2450747]", weight=None)


#nodes=nx.floyd_warshall(Grafo)
#nodes=nx.bellman_ford_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight='weight')

#nodes=djNodes
"""
djPath=[]

tmp=list(Grafo.edges(odes,data=True))
for i in range(len(tmp)):
    djPath.append([tmp[i][0],tmp[i][1]])
"""

#print(tmp[i][0]+tmp[i][1])
#print(djNodes,djPath,len(djNodes),len(djPath))
#print(djPath,len(djNodes),len(djPath))
#,source,tarjet)

path=[]
for i in nodes:
    path.append(eval(i))
#print(djNodes)
#pathdj=pd.DataFrame({"path":path})
#print(data.head(5))
print(data)

pathdj=pd.DataFrame([{"name":"edges","edges":path}])
print(pathdj)
#data = pd.read_json("data/nodes_datas.json")

view = pdk.ViewState(latitude=6.2564059689324, longitude= -75.5983559112375, pitch=20, zoom=15)
layer4 = pdk.Layer(
    type="PathLayer",
    data=pathdj,
    pickable=False,
    get_color=(0,15,205),
    width_scale=5,
    width_min_pixels=5,
    get_path="edges",
    get_width=5,
)
#https://deckgl.readthedocs.io/en/latest/event_handling.html
layer3 =pdk.Layer(
    "TextLayer",
    data=data,
    get_position="node",
    get_size=16,
    get_color=[255, 255, 255],
    get_text="node",
    get_angle=0
)
layer5 = pdk.Layer(
    "TextLayer",
    data=data,
    pickable=True,
    get_position="node",
    get_text="node",
    get_size=16,
    get_color=[0, 0, 0],
    get_angle=0,

)

layer2 = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=3,
    radius_min_pixels=4,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position="node",
    get_radius=1,
    get_fill_color=[137, 36, 250],
    get_line_color=[0, 0, 0],
)

layer1 = pdk.Layer(
    type="PathLayer",
    data=data,
    pickable=False,
    get_color=(0,155,0),
    width_scale=2,
    width_min_pixels=1,
    get_path="edges",
    get_width=1,
)
r = pdk.Deck(layers=[layer1,layer4], initial_view_state=view)
r.to_html('tmp.html')
