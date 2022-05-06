"""
HeatmapLayer
===========

Location of livestock raised in New Mexico in the United States in 2006,
via the United Nations and FAOSTAT, with the source data viewable here: http://www.fao.org/faostat/en/

Locations for poultry are viewable in blue and cattle are in orange.

Overlaid with the satellite imagery from Mapbox to highlight the how terrain affects agriculture.
"""

import pandas as pd
import pydeck as pdk
DATA="data/graph_medellin_all_data.json"

HEADER = ["origin", "harassmentRisk"]
data=pd.read_json(DATA)

print(data)
print(data["node"])

view = pdk.ViewState(latitude=6.2564059689324, longitude= -75.5983559112375, pitch=20, zoom=15)
layer1 = pdk.Layer(
    "HeatmapLayer",
    data=data,
    opacity=0.9,
    get_position="node",
    threshold=1,
    get_weight="harassmentRisk",
    pickable=True,
)


r = pdk.Deck(layers=[layer1], initial_view_state=view)

r.to_html("heatmap_layer.html")