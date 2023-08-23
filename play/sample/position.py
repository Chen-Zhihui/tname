"""_summary_
1 自定义状态，map-reducer
"""


import leafmap.leafmap as leafmap
import solara
from leafmap.toolbar import change_basemap
import dataclasses
from typing import Tuple

DEBUG = False

ACT_ZOOM = "zoom"
ACT_MOVE = "move"

@dataclasses.dataclass(frozen=True)
class MapState:
    zoom : int = 13
    center : Tuple[float, float] = (24.2629,120.6283) # lat, lon
    
    
def map_reducer(state: MapState, action):
    action_type, payload = action
    if DEBUG :
        print("reducer", state, action_type, payload)    
    if action_type == ACT_ZOOM:
        return dataclasses.replace(state, zoom=payload)
    elif action_type == ACT_MOVE:
        return dataclasses.replace(state, center=payload)
    else:
        print("invalidation action")
        return state


class Map(leafmap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add what you want below
        # self.add_basemap("OpenTopoMap")
        # change_basemap(self)
        # url = 'https://opendata.digitalglobe.com/events/california-fire-2020/pre-event/2018-02-16/pine-gulch-fire20/1030010076004E00.tif'
        # self.add_cog_layer(url, name="Fire (pre-event)")


@solara.component
def Position():
    
    init_map_state = MapState()
    map_state, dispatch = solara.use_reducer(map_reducer, init_map_state)
    
    with solara.Row(justify="center") as m:
        with solara.Column(style={"min-width": "800px"}) as main:
            # solara components support reactive variables
            # solara.SliderInt(label="Zoom level", value=zoom, min=1, max=20)
            # using 3rd party widget library require wiring up the events manually
            # using zoom.value and zoom.set
            Map.element(  # type: ignore
                zoom=map_state.zoom,
                on_zoom=lambda v: dispatch((ACT_ZOOM, v)),
                center=map_state.center,
                on_center=lambda v: dispatch((ACT_MOVE, v)),
                scroll_wheel_zoom=True,
                # toolbar_ctrl=True,
                # data_ctrl=True,
                # attribution_control=True,
            )
            solara.Text(f"Zoom: {map_state.zoom}")
            solara.Text(f"Center: {map_state.center}")
        
    return m
