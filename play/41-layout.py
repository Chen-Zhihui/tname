from solara import layout 
import solara
from solara.website.pages.examples.utilities import calculator

@solara.component
def Home():
    solara.Markdown("Home")


@solara.component
def About():
    with solara.Column(style="min-width:100px") as main :
        solara.Markdown("About")
        solara.Markdown("ppppppppppppppppppppppp")
    return main
@solara.component 
def Page() :
    left = solara.Text("Left")
    right = solara.Text("right")
    title = solara.Title("title")
    with layout.LayoutApp(
        left=left,
        right=right,
        open_left=False,
        open_right=False,
        title=title,
        ) as main:
        # calculator()
        Home()
        
    return main 
