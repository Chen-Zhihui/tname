from solara import layout 
import solara
from solara.website.pages.examples.utilities import calculator

@solara.component
def Home():
    solara.Markdown("Home")


@solara.component
def About():
    solara.Markdown("About")
    
@solara.component 
def Page() :
    left = solara.Text("Left")
    right = solara.Text("right")
    title = solara.Title("title")
    with layout.LayoutApp(
        left=left,
        right=right,
        open_left=True,
        open_right=True,
        title=title,
        ) as main:
        # calculator()
        Home()
        
    return main 
