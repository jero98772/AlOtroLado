from ipywidgets import HTML
import pydeck as pdk

text = HTML(value='Move the viewport')
layer = pdk.Layer(
    'ScatterplotLayer',
    df,
    pickable=True,
    get_position=['lng', 'lat'],
    get_fill_color=[255, 0, 0],
    get_radius=100
)
r = pdk.Deck(layer, initial_view_state=viewport)

def filter_by_bbox(row, west_lng, east_lng, north_lat, south_lat):
    return west_lng < row['lng'] < east_lng and south_lat < row['lat'] < north_lat

def filter_by_viewport(widget_instance, payload):
    try:
        west_lng, north_lat = payload['data']['nw']
        east_lng, south_lat = payload['data']['se']
        filtered_df = df[df.apply(lambda row: filter_by_bbox(row, west_lng, east_lng, north_lat, south_lat), axis=1)]
        text.value = 'Points in viewport: %s' % int(filtered_df.count()['lng'])
    except Exception as e:
        text.value = 'Error: %s' % e


r.deck_widget.on_click(filter_by_viewport)
display(text)
r.show()