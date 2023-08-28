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
from . import alias_search

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
init_center = (24.2629,120.6283)
@dataclasses.dataclass(frozen=True)
class MapState:
    zoom : int = 13
    center : Tuple[float, float] = init_center # lat, lon
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
            self.set_center(lon, lat)
           
    @traitlets.observe("marker_locations")
    def on_marker_locations_changed(self, change):
        self.plot_markers()
        
    def clear_markers(self):
        for m in self.markers_of_my___:  
            self.remove_layer(m)  
        self.markers_of_my___ = []
       

@solara.component
def LocationMapperWidget( locations :List[Location] = []):  
    # init_map_state = MapState(
    #     locations=locations,
    #     center=Location.center(locations)
    # )
    # map_state, dispatch = solara.use_reducer(map_reducer, init_map_state)
    
    with solara.Row(justify="center") as m:
        with solara.Column(style={"min-width": "600px"}) as main:
            LocationMapper.element(  # type: ignore
                marker_locations = locations,
                zoom=13,
                # on_zoom=lambda v: dispatch((ACT_ZOOM, v)),
                # center=init_center,
                # on_center=lambda v: dispatch((ACT_MOVE, v)),
                scroll_wheel_zoom=True,
                toolbar_ctrl=False,
                data_ctrl=False,
                attribution_control=False,
            )
            # solara.Text(f"Zoom: {map_state.zoom}")
            # solara.Text(f"Center: {map_state.center}")
            
    return m


# %%
# 测试数据
EXAMPLE_LOCATIONS_EMPTY = [Location(name="",latitude=24.2629,longitude=120.6283)]

from tname.alias import AliasTarget
import pandas as pd
from typing import Any, Dict, Optional, cast

as_list_init = [
{"language": "chs", "alias_id": "cc7ceffa-432f-11ee-8f7a-00155dc4f249", "alias": "志航雷达站", "name": "志航雷达站", "target_id": "cc7ceee2-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.404119832450892, 120.58161709312168], "target_type": "军营"},
{"language": "chs", "alias_id": "cc7cf0f4-432f-11ee-8f7a-00155dc4f249", "alias": "志航雷达", "name": "志航雷达站", "target_id": "cc7ceee2-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.404119832450892, 120.58161709312168], "target_type": "电厂"},
{"language": "chs", "alias_id": "cc7cf194-432f-11ee-8f7a-00155dc4f249", "alias": "林田山雷达", "name": "林田山雷达", "target_id": "cc7cf16c-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.129186874986946, 121.08013062435067], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cf1da-432f-11ee-8f7a-00155dc4f249", "alias": "田山雷达站站", "name": "林田山雷达", "target_id": "cc7cf16c-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.129186874986946, 121.08013062435067], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cf248-432f-11ee-8f7a-00155dc4f249", "alias": "美仑山雷", "name": "美仑山雷", "target_id": "cc7cf22a-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.664779158344224, 120.60514845546976], "target_type": "机场"},
{"language": "chs", "alias_id": "cc7cf28e-432f-11ee-8f7a-00155dc4f249", "alias": "仑山雷达站达站", "name": "美仑山雷", "target_id": "cc7cf22a-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.664779158344224, 120.60514845546976], "target_type": "防空阵地"},
{"language": "chs", "alias_id": "cc7cf2f2-432f-11ee-8f7a-00155dc4f249", "alias": "东澳岭", "name": "东澳岭", "target_id": "cc7cf2d4-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.09174090430521, 120.55425007263351], "target_type": "防空阵地"},
{"language": "chs", "alias_id": "cc7cf338-432f-11ee-8f7a-00155dc4f249", "alias": "澳岭雷达站雷达站", "name": "东澳岭", "target_id": "cc7cf2d4-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.09174090430521, 120.55425007263351], "target_type": "军营"},
{"language": "chs", "alias_id": "cc7cf392-432f-11ee-8f7a-00155dc4f249", "alias": "鹅銮", "name": "鹅銮", "target_id": "cc7cf374-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.026637740397973, 120.63380502308954], "target_type": "港口"}    ,
{"language": "chs", "alias_id": "cc7cf7b6-432f-11ee-8f7a-00155dc4f249", "alias": "佳山基地", "name": "佳山基地", "target_id": "cc7cf798-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [22.854510203446498, 120.58805659233533], "target_type": "电厂"},
{"language": "chs", "alias_id": "cc7cf806-432f-11ee-8f7a-00155dc4f249", "alias": "屏东基地", "name": "屏东基地", "target_id": "cc7cf7e8-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.02038125280086, 120.8465075670998], "target_type": "机场"},
{"language": "chs", "alias_id": "cc7cf860-432f-11ee-8f7a-00155dc4f249", "alias": "志航基地", "name": "志航基地", "target_id": "cc7cf842-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.96753944476481, 121.08079383081811], "target_type": "电厂"},
{"language": "chs", "alias_id": "cc7cf8b0-432f-11ee-8f7a-00155dc4f249", "alias": "清泉岗空军基地", "name": "清泉岗空军基地", "target_id": "cc7cf892-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [22.97836402801962, 120.43522647170747], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cf900-432f-11ee-8f7a-00155dc4f249", "alias": "花莲基地", "name": "花莲基地", "target_id": "cc7cf8e2-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.742281945581055, 120.88265722609137], "target_type": "军营"},
{"language": "chs", "alias_id": "cc7cf93c-432f-11ee-8f7a-00155dc4f249", "alias": "新竹空军基地", "name": "花莲基地", "target_id": "cc7cf8e2-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.742281945581055, 120.88265722609137], "target_type": "防空阵地"},
{"language": "chs", "alias_id": "cc7cf98c-432f-11ee-8f7a-00155dc4f249", "alias": "嘉义基地", "name": "嘉义基地", "target_id": "cc7cf96e-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.19845069322111, 120.51885790433697], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cf9e6-432f-11ee-8f7a-00155dc4f249", "alias": "清泉岗基", "name": "清泉岗基", "target_id": "cc7cf9c8-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [22.975432349378426, 120.63563388307942], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cfa18-432f-11ee-8f7a-00155dc4f249", "alias": "马公基地地", "name": "清泉岗基", "target_id": "cc7cf9c8-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [22.975432349378426, 120.63563388307942], "target_type": "军营"},
{"language": "chs", "alias_id": "cc7cfa68-432f-11ee-8f7a-00155dc4f249", "alias": "新竹基地", "name": "新竹基地", "target_id": "cc7cfa4a-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.60511758948916, 120.64672218820743], "target_type": "机场"},
{"language": "chs", "alias_id": "cc7cfac2-432f-11ee-8f7a-00155dc4f249", "alias": "台南基地", "name": "台南基地", "target_id": "cc7cfaa4-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.385214191171585, 121.07101213507748], "target_type": "防空阵地"},
{"language": "chs", "alias_id": "cc7cfb12-432f-11ee-8f7a-00155dc4f249", "alias": "马公空军基地", "name": "马公空军基地", "target_id": "cc7cfaf4-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.911338958377748, 120.69493801574475], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cfb80-432f-11ee-8f7a-00155dc4f249", "alias": "基隆军港", "name": "基隆军港", "target_id": "cc7cfb62-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [24.06738167884072, 120.66948838182344], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cfbd0-432f-11ee-8f7a-00155dc4f249", "alias": "左营军", "name": "左营军", "target_id": "cc7cfbbc-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.34923542123707, 120.57540682913685], "target_type": "机场"},
{"language": "chs", "alias_id": "cc7cfc02-432f-11ee-8f7a-00155dc4f249", "alias": "芦竹区草仔崎营区", "name": "左营军", "target_id": "cc7cfbbc-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.34923542123707, 120.57540682913685], "target_type": "军营"},
{"language": "chs", "alias_id": "cc7cfc34-432f-11ee-8f7a-00155dc4f249", "alias": "草仔崎营区港", "name": "左营军", "target_id": "cc7cfbbc-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.34923542123707, 120.57540682913685], "target_type": "机场"},
{"language": "chs", "alias_id": "cc7cfc84-432f-11ee-8f7a-00155dc4f249", "alias": "马公军港", "name": "马公军港", "target_id": "cc7cfc70-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.470751565429417, 120.98600814780684], "target_type": "电厂"},
{"language": "chs", "alias_id": "cc7cfcd4-432f-11ee-8f7a-00155dc4f249", "alias": "苏澳", "name": "苏澳", "target_id": "cc7cfcc0-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.925609802285813, 120.51782908731367], "target_type": "防空阵地"},
{"language": "chs", "alias_id": "cc7cfd06-432f-11ee-8f7a-00155dc4f249", "alias": "竹南公义里营区", "name": "苏澳", "target_id": "cc7cfcc0-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.925609802285813, 120.51782908731367], "target_type": "军营"},
{"language": "chs", "alias_id": "cc7cfd38-432f-11ee-8f7a-00155dc4f249", "alias": "公义里营区军港", "name": "苏澳", "target_id": "cc7cfcc0-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.925609802285813, 120.51782908731367], "target_type": "电厂"},
{"language": "chs", "alias_id": "cc7cfd88-432f-11ee-8f7a-00155dc4f249", "alias": "桃园市芦竹区草仔崎营", "name": "桃园市芦竹区草仔崎营", "target_id": "cc7cfd74-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.434343024686306, 120.66166793261381], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cfdba-432f-11ee-8f7a-00155dc4f249", "alias": "泰山区明志路神箭营区", "name": "桃园市芦竹区草仔崎营", "target_id": "cc7cfd74-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.434343024686306, 120.66166793261381], "target_type": "电厂"},
{"language": "chs", "alias_id": "cc7cfdec-432f-11ee-8f7a-00155dc4f249", "alias": "明志路神箭营区", "name": "桃园市芦竹区草仔崎营", "target_id": "cc7cfd74-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.434343024686306, 120.66166793261381], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cfe1e-432f-11ee-8f7a-00155dc4f249", "alias": "神箭营区区", "name": "桃园市芦竹区草仔崎营", "target_id": "cc7cfd74-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.434343024686306, 120.66166793261381], "target_type": "港口"},
{"language": "chs", "alias_id": "cc7cfe6e-432f-11ee-8f7a-00155dc4f249", "alias": "苗栗县竹南公义里营", "name": "苗栗县竹南公义里营", "target_id": "cc7cfe50-432f-11ee-8f7a-00155dc4f249", "country": "tw", "location": [23.17367681096938, 121.08272734607576], "target_type": "机场"},

]


as_list_obj = [AliasTarget.from_dict(j) for j in as_list_init]
as_df = pd.DataFrame(as_list_init)

def create_location(a : AliasTarget):
    return Location(name=a.name, latitude=a.location[0], longitude=a.location[1])

@solara.component 
def TestLocation2():
    # 查询条件
    
    query, set_query = solara.use_state("") 
    locs, set_locs = solara.use_state(EXAMPLE_LOCATIONS_EMPTY)
    df, set_df = solara.use_state(pd.DataFrame(None, columns=["alias", "name", "location"]))
    with solara.Row(justify="center") as r:
        with solara.Card() as main :
            with solara.Row(justify="center") :            
                LocationMapperWidget(
                    locations = locs
                    )        
                with solara.Card(title="查询") :
                    with solara.Row() :
                        def on_query(v) :
                            if v == "" :
                                set_df(pd.DataFrame())
                                set_locs([])
                            else:
                                res = alias_search.query_by_alias(v)
                                set_df(pd.DataFrame(res))
                                set_locs( [create_location(AliasTarget.from_dict(item)) for item in df.iterrows()] )
                        solara.InputText(label="输入查询条件", value=query, on_value=on_query) 
                    column, set_column = solara.use_state(cast(Optional[str], None))
                    cell, set_cell = solara.use_state(cast(Dict[str, Any], {}))
                    def on_action_column(column):
                        set_column(column)
                    def on_action_cell(column, row_index):
                        set_cell(dict(column=column, row_index=row_index))
                        item = df.iloc[row_index, :]
                        set_locs( [create_location(AliasTarget.from_dict(item))] )
                    column_actions = [solara.ColumnAction(icon="mdi-sunglasses", name="User column action", on_click=on_action_column)]
                    cell_actions = [solara.CellAction(icon="mdi-white-balance-sunny", name="显示", on_click=on_action_cell)]                    
                    solara.DataFrame(df, items_per_page=10, column_actions=column_actions, cell_actions=cell_actions)
    return r
# %%
