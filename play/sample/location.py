"""_summary_
1 自定义状态，map-reducer
"""

#%%
import leafmap.leafmap as leafmap
import ipyleaflet
import solara
from leafmap.toolbar import change_basemap
import dataclasses
from typing import Tuple, List
import os
import traitlets 
import pandas as pd

DEBUG = False

ACT_ZOOM = "zoom"
ACT_MOVE = "move"
ACT_SET_MARKERS = "set_marker"
ACT_CLR_MARKERS = "clr_marker"

# 
class Location(traitlets.HasTraits):
    name = traitlets.Unicode("")
    latitude = traitlets.Float(0)
    longitude = traitlets.Float(0)
    
    def create_marker(self):
        return ipyleaflet.Marker(
                location=[self.latitude, self.longitude], 
                draggable=False,
                opacity=0.8,
                name=self.name,            
        )
    
EXAMPLE_LOCATIONS = [
    Location(name="unname1", latitude=24.2629, longitude=120.6283),
    Location(name="unname2", latitude=24.2729, longitude=120.6383),
    ]
EXAMPLE_LOCATIONS_EMPTY = []

# EXAMPLE_LOCATIONS = pd.DataFrame([
#     ("unname", 24.2629, 120.6283),
#     ("unname", 24.2729, 120.6383),
#     ("unname", 24.2829, 120.6483),
#     ("unname", 24.2929, 120.6583),
#     ("unname", 24.3029, 120.6683),
#     ], columns=["name", "latitude", "longitude"])
# EXAMPLE_LOCATIONS_EMPTY = pd.DataFrame()

# state and reducer
@dataclasses.dataclass(frozen=True)
class MapState:
    zoom : int = 13
    center : Tuple[float, float] = (24.2629,120.6283) # lat, lon
    # locations : List[Location]  = dataclasses.field(default_factory=list_of_locs)
    # locations : pd.DataFrame = dataclasses.field(default_factory=create_df)
    locations : List[Location] = dataclasses.field(default_factory=list)
        
def map_reducer(state: MapState, action):
    action_type, payload = action
    if DEBUG :
        print("reducer", state, action_type, payload)    
    if action_type == ACT_ZOOM:
        return dataclasses.replace(state, zoom=payload)
    elif action_type == ACT_MOVE:
        return dataclasses.replace(state, center=payload)
    elif action_type == ACT_SET_MARKERS:
        li = EXAMPLE_LOCATIONS
        return dataclasses.replace(state, locations=li)
    elif action_type == ACT_CLR_MARKERS:
        return dataclasses.replace(state, locations=EXAMPLE_LOCATIONS_EMPTY)
    else:
        print("invalidation action")
        return state

#%%
class Map(leafmap.Map):
    
    marker_locations = traitlets.List([]) 
    markers_of_my___ = traitlets.List([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_minimap(zoom=8)
    
    def plot_markers(self):
        self.clear_markers()
        for r in self.marker_locations :
            m = r.create_marker()
            self.add_layer(m)
            self.markers_of_my___.append(m)      
           
    @traitlets.observe("marker_locations")
    def on_marker_locations_changed(self, change):
        self.plot_markers()
        
    def clear_markers(self):
        for m in self.markers_of_my___:  
            self.remove_layer(m)  
        self.markers_of_my___ = []
       

@solara.component
def Location():
    
    init_map_state = MapState()
    map_state, dispatch = solara.use_reducer(map_reducer, init_map_state)
    
    with solara.Row(justify="center") as m:
        with solara.Column(style={"min-width": "800px"}) as main:
            Map.element(  # type: ignore
                marker_locations = map_state.locations,
                zoom=map_state.zoom,
                on_zoom=lambda v: dispatch((ACT_ZOOM, v)),
                center=map_state.center,
                on_center=lambda v: dispatch((ACT_MOVE, v)),
                scroll_wheel_zoom=True,
                toolbar_ctrl=False,
                data_ctrl=False,
                attribution_control=False,
            )
            solara.SliderInt(
                label="Zoom level", 
                value=map_state.zoom, 
                on_value=lambda v: dispatch((ACT_ZOOM, v)), 
                min=1, 
                max=20
                )
            solara.Text(f"Zoom: {map_state.zoom}")
            solara.Text(f"Center: {map_state.center}")
            
            with solara.Row() :
                solara.Button("Markers Set", 
                              on_click=lambda : dispatch((ACT_SET_MARKERS, EXAMPLE_LOCATIONS)))
                solara.Button("Markers Clear", 
                              on_click=lambda : dispatch((ACT_CLR_MARKERS, None)))
        
    return m

# %%