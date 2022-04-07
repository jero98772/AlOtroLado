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
name="out2.json"
data=pd.read_json(name)
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
def vales2tuple(v):
    return tuple(v[1:-1].split(","))
#data["color"] = data["color"].apply(vales2tuple)#.apply(hex_to_rgb)

print(data)
#print(data["color"])
view = pdk.ViewState(latitude=6.256405968932449, longitude= -75.59835591123756, pitch=50, zoom=9)
layer = pdk.Layer(
    type="PathLayer",
    data=data,
    pickable=True,
    get_color=(0,155,0),
    width_scale=1,
    width_min_pixels=1,
    get_path="path",
    get_width=1,
)
r = pdk.Deck(layers=[layer], initial_view_state=view)
r.to_html('mapa_inutil_y_vende_humo.html')

"""
import pandas as pd
data=pd.read_csv(input())
print(data)
"""