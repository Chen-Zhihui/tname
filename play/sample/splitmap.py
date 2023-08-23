import leafmap.leafmap as  leafmap
import solara
import pathlib
from leafmap.toolbar import change_basemap

tiff_path = str(pathlib.Path(__file__).parent / "data" / "srtm90.tif")

basemap = "OpenTopoMap"

zoom = solara.reactive(8)
center = solara.reactive((20, 0))

s = solara.reactive("var")

class Map(leafmap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        for k in kwargs:
            print(f"{k}:{kwargs[k]}")
       
        self.add_basemap(basemap)
        # change_basemap(self)
        self.add_raster(tiff_path, cmap="terrain", layer_name="Local COG")
        self.split_map("Local COG", basemap)
        # self.add_colormap(vmin=0, vmax=4000, cmap='terrain', label='Elevation (m)')
        

@solara.component
def SplitMap():
    with solara.Row(justify="center", ) as m:
    # if 1:
        with solara.Column(
            style={
            "min-width": "800px",
            "max-width": "960px"
            },
            # align = "center"
        ) as mm:
            # solara components support reactive variables
            with solara.Card() :
                solara.SliderInt(label="Zoom level", value=zoom, min=1, max=20)
            with solara.Card() :
                Map.element(
                    zoom=zoom.value,
                    on_zoom=zoom.set,
                    center=center.value,
                    on_center=center.set,
                    scroll_wheel_zoom=True,
                    toolbar_ctrl=True,
                    data_ctrl=True,
                    attribution_control=True,
                    var = s
                    )
            with solara.Card():
                solara.Markdown(f"Zoom: {zoom.value}")
                solara.Markdown(f"Center: {center.value}")

    return m
    