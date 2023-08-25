#%%
from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl

watercolor = basemap_to_tiles(basemaps.Stamen.Watercolor)

m = Map(layers=(watercolor, ), center=(50, 354), zoom=5)

draw_control = DrawControl(
    
)
draw_control.polyline = {}
draw_control.polygon ={}
# draw_control.circlemarker ={}
draw_control.circle ={}
draw_control.rectangle ={}
draw_control.marker ={}
draw_control.edit = False
draw_control.remove = False

draw_control.circle = {
    "shapeOptions": {
        "fillColor": "#efed69",
        "color": "#efed69",
        "fillOpacity": 1.0
    }
}

def cb(control, action, geo_json) :
    print(f"control: {control}")
    print(f"action: {action}")
    print(f"geo_json: {geo_json}")

m.on_draw(cb)

m.add_control(draw_control)
m

# %%
m
# %%
