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

DEBUG = True

ACT_ZOOM = "zoom"
ACT_MOVE = "move"
ACT_SET_MARKERS = "set_marker"
ACT_CLR_MARKERS = "clr_marker"

# 用dataclass定义位置信息
DEFAULT_CENTER = (24.2629,120.6283)
@dataclasses.dataclass(frozen=True)    
class Location:
    name : str = ""
    latitude : float = 0.0
    longitude : float = 0.0
    
    def create_marker(self):
        return ipyleaflet.Marker(
                location=[self.latitude, self.longitude], 
                draggable=False,
                opacity=0.8,
                name=self.name,            
        )
        
    @staticmethod
    def center(ps) :
        if len(ps) > 0:
            lat = [ p.latitude for p in ps]
            lon = [ p.longitude for p in ps]
            return sum(lat)/len(lat), sum(lon)/len(lon)
        else:
            return DEFAULT_CENTER
        
# state and reducer
@dataclasses.dataclass(frozen=True)
class MapState:
    zoom : int = 13
    # center : Tuple[float, float] = (24.2629,120.6283) # lat, lon
    # locations : List[Location]  = dataclasses.field(default_factory=list_of_locs)
    # locations : pd.DataFrame = dataclasses.field(default_factory=create_df)
    locations : List[Location] = dataclasses.field(default_factory=list)
    
    # def __init__(self, **kwargs) :
    #     if "locations" in kwargs and len(kwargs["locations"]) > 0:
    #         kwargs["center"] = Location.center(kwargs["locations"])
    #     super().__init__(**kwargs)
        
def map_reducer(state: MapState, action):
    action_type, payload = action
    if DEBUG :
        print("reducer", state, action_type, payload)    
    if action_type == ACT_ZOOM:
        return dataclasses.replace(state, zoom=payload)
    elif action_type == ACT_MOVE:
        return dataclasses.replace(state, center=payload)
    elif action_type == ACT_SET_MARKERS:
        return dataclasses.replace(state, locations=payload)
    elif action_type == ACT_CLR_MARKERS:
        return dataclasses.replace(state, locations=payload)
    else:
        print("invalidation action")
        return state

#%%
class LocationMapper(leafmap.Map):
    
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
        
        if len(self.marker_locations) > 0:
            lat, lon = Location.center(self.marker_locations)
        #     self.center=(lon, lat)
            self.set_center(lon, lat)
           
    @traitlets.observe("marker_locations")
    def on_marker_locations_changed(self, change):
        self.plot_markers()
        
    def clear_markers(self):
        for m in self.markers_of_my___:  
            self.remove_layer(m)  
        self.markers_of_my___ = []
       

@solara.component
def LocationMapperWidget( locations :List[Location] = [] ):  
    init_map_state = MapState(
        locations=locations
    )
    map_state, dispatch = solara.use_reducer(map_reducer, init_map_state)
    
    with solara.Row(justify="center") as m:
        with solara.Column(style={"min-width": "600px"}) as main:
            LocationMapper.element(  # type: ignore
                marker_locations = locations,
                zoom=map_state.zoom,
                on_zoom=lambda v: dispatch((ACT_ZOOM, v)),
                # center=center,
                # on_center=lambda v: dispatch((ACT_MOVE, v)),
                scroll_wheel_zoom=True,
                toolbar_ctrl=False,
                data_ctrl=False,
                attribution_control=False,
            )
            solara.Text(f"Zoom: {map_state.zoom}")
            # solara.Text(f"Center: {map_state.center}")
            
    return m


# %%
# 测试数据
EXAMPLE_LOCATIONS_EMPTY = []

from tname.alias import AliasTarget
as_list_init = [
{"language": "chs", "alias_id": "cc7ceffa-432f-11ee-8f7a-00155dc4f249", "alias": "志航雷达站", "name": "志航雷达站", "target_id": "cc7ceee2-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.404119832450892, 120.58161709312168], "target_type": "军营"},
{"language": "chs", "alias_id": "cc7cf194-432f-11ee-8f7a-00155dc4f249", "alias": "林田山雷达", "name": "林田山雷达", "target_id": "cc7cf16c-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.129186874986946, 121.08013062435067], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cf248-432f-11ee-8f7a-00155dc4f249", "alias": "美仑山雷", "name": "美仑山雷", "target_id": "cc7cf22a-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.664779158344224, 120.60514845546976], "target_type": "机场"},
{"language": "chs", "alias_id": "cc7cf2f2-432f-11ee-8f7a-00155dc4f249", "alias": "东澳岭", "name": "东澳岭", "target_id": "cc7cf2d4-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.09174090430521, 120.55425007263351], "target_type": "防空阵地"},
{"language": "chs", "alias_id": "cc7cf392-432f-11ee-8f7a-00155dc4f249", "alias": "鹅銮", "name": "鹅銮", "target_id": "cc7cf374-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.026637740397973, 120.63380502308954], "target_type": "港口"}    ,
]
as_list_obj = [AliasTarget.from_dict(j) for j in as_list_init]

def create_location(a : AliasTarget):
    return Location(name=a.name, latitude=a.location[0], longitude=a.location[1])

@solara.component 
def TestLocation():
    # 查询条件
    query, set_query = solara.use_state("") 
    locs, set_locs = solara.use_state(EXAMPLE_LOCATIONS_EMPTY)
    alias, set_alias = solara.use_state(as_list_obj)
    with solara.Card() as main :
        with solara.Row(justify="center") :            
            LocationMapperWidget(
                locations = locs
                )        
            with solara.Column() :
                solara.InputText(label="输入查询条件", value=query) 
                for a in alias :
                    def move_to(aa, als):
                        def m():
                            set_locs( [create_location(aa) ] )
                        return m
                        
                    solara.Button(
                        f"{a.name}:{a.alias}", on_click=move_to(a, alias), text=True)
                    
                solara.Button("Markers Clear", 
                                on_click=lambda : set_locs(EXAMPLE_LOCATIONS_EMPTY), text=True)

    return main