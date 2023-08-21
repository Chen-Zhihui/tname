import leafmap.leafmap as  leafmap
import solara
import pathlib
from leafmap.toolbar import change_basemap

tiff_path = str(pathlib.Path(__file__).parent / "data" / "srtm90.tif")

basemap = "OpenTopoMap"

print(tiff_path)

zoom = solara.reactive(2)
center = solara.reactive((20, 0))

class Map(leafmap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
       
        self.add_basemap(basemap)
        # change_basemap(self)
        self.add_raster(tiff_path, cmap="terrain", layer_name="Local COG")
        self.split_map("Local COG", basemap)
        # self.add_colormap(vmin=0, vmax=4000, cmap='terrain', label='Elevation (m)')
        

@solara.component
def SplitMap():
    with solara.Column(style={"min-width": "300px"}) as main:
        # solara components support reactive variables
        solara.SliderInt(label="Zoom level", value=zoom, min=1, max=20)
        Map.element(
            zoom=zoom.value,
            on_zoom=zoom.set,
            center=center.value,
            on_center=center.set,
            scroll_wheel_zoom=True,
            toolbar_ctrl=True,
            data_ctrl=True,
            attribution_control=True,
        )
        solara.Text(f"Zoom: {zoom.value}")
        solara.Text(f"Center: {center.value}")
        # m.add_basemap("TERRAIN")
        # change_basemap(m)
        # m.add_raster(tiff_path, cmap="terrain", layer_name="Local COG")
        # m.add_colormap(vmin=0, vmax=4000, cmap='terrain', label='Elevation (m)')
        # m.split_map("Local COG", "TERRAIN")
    return main
    