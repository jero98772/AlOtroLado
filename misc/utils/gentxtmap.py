import pandas as pd
import pydeck as pdk
from ipywidgets import HTML
import json

data = pd.read_json("data/nodes_data.json")

view = pdk.ViewState(latitude=6.2564059689324, longitude= -75.5983559112375, pitch=20, zoom=15)

layer3 =pdk.Layer(
    "TextLayer",
    data=data,
    get_position="node",
    get_size=16,
    get_color=[255, 255, 255],
    get_text="name",
    get_angle=0
)
layer5 = pdk.Layer(
    "TextLayer",
    data=data,
    pickable=True,
    get_position="node",
    get_text="name2",
    get_size=20,
    get_color=[255, 255, 255],
    get_angle=0,

)

layer2 = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    radius_scale=3,
    radius_min_pixels=4,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position="node",
    get_radius=1,
    get_fill_color=[137, 36, 250],
    get_line_color=[0, 0, 0],
)
r = pdk.Deck(layers=[layer5,layer2], initial_view_state=view)
#r = pdk.Deck(layers=[layer2], initial_view_state=view)

r.deck_widget.on_click(filter_by_viewport)


display(text)
r.to_html('tmp.html')
