try:    
    import pandas as pd
except:
    print("please install pandas\npip install pandas")

try:
    import pydeck as pdk
except:
    print("please install pydeck\npip install pydeck")


#SOURCEURL="https://raw.githubusercontent.com/mauriciotoro/ST0245-Eafit/master/proyecto/Datasets/calles_de_medellin_con_acoso.csv"
#print(data.to_string())
#name="graph_medellin_data.json"
name="graph_medellin_no_private_data.json"

print("245")
data = pd.read_json(name)
print("24r")
#data=pd.read_json(name)
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
def vales2tuple(v):
    return tuple(v[1:-1].split(","))
#data["color"] = data["color"].apply(vales2tuple)#.apply(hex_to_rgb)

print(data)

#print(data["color"])
view = pdk.ViewState(latitude=6.256405968932449, longitude= -75.59835591123756, pitch=50, zoom=9)

layer2 = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=1,
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
    pickable=True,
    get_color=(0,155,0),
    width_scale=2,
    width_min_pixels=1,
    get_path="path",
    get_width=1,
)
r = pdk.Deck(layers=[layer1,layer2], initial_view_state=view)
r.to_html('mapa_inutil_y_vende_humo2.html')

"""
import pandas as pd
data=pd.read_csv(input())
print(data)
"""