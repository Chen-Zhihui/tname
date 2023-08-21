import solara 
from .scatter import Scatter
from .pokemom import Pokemom
from .fruit import Fruit
from .lmap import LMap
from .splitmap import SplitMap
from solara.layout import LayoutApp, AppIcon
# from . import layout 
from solara.alias import rv, rvue

# Layout = layout.Layout


# @solara.component
# def Layout(children=[]):
#     # Note that children being passed here for this example will be a Page() element.
#     route_current, routes_all = solara.use_route()
#     with solara.Column():
#         # put all buttons in a single row
#         with solara.Row():
#             for route in routes_all:
#                 with solara.Link(route):
#                     solara.Button(route.path, color="red" if route_current == route else None)
#         # under the navigation buttons, we add our children (the single Page())
#         solara.Column(children=children)

     
# @solara.component
# def Layout(children=[]):
#     print("I get called before the Page component gets rendered")
#     with solara.AppLayout(children=children) as main:
        
#         route_current, routes_all = solara.use_route()
        
#         with solara.Sidebar() as s:
#             with solara.Column():
#                 for route in routes_all:
#                     with solara.Link(route):
#                         solara.Button(route.path, color="red" if route_current == route else None)
                
#     return main

# @solara.component
# def Layout(children=[]):
#     print("I get called before the Page component gets rendered")
#     return solara.AppLayout(children=children)

# @solara.component
# def Layout(children=[]):
#     # Note that children being passed here for this example will be a Page() element.
#     route_current, routes_all = solara.use_route()
#     with solara.Column():
#         # put all buttons in a single row
#         with solara.Column():
#             for route in routes_all:
#                 with solara.Link(route):
#                     solara.Button(route.path, color="red" if route_current == route else None)
#         # under the navigation buttons, we add our children (the single Page())
#         solara.Column(children=children)
     
      
# subpages = ["", "foo", "bar", "solara", "react-ipywidgets"]

# routes = [
#     # level 0
#     solara.Route(path="/", label="Map", component=LMap),
    
#     # level 1
#     solara.Route(path="fruit", label="水果", component=Fruit),
#     solara.Route(path="scatter", component=Scatter, label="Scatter"),
#     solara.Route(path="poke", label="Poke", component=Pokemom),
# ]



# title = "Home"

# route_order = ["/", "showcase", "docs", "api", "examples", "apps"]

# @solara.component
# def Layout(children=[]):
#     # router = solara.use_router()
#     # route_current, all_routes = solara.use_route()
#     # route_sidebar_current, all_routes_sidebar = solara.use_route(1)

#     # show_left_menu, set_show_left_menu = solara.use_state(False)
#     # show_right_menu, set_show_right_menu = solara.use_state(False)

#     # target, set_target = solara.use_state(0)

#     # if route_current and route_current.path == "apps":
#     #     return children[0]
#     pass

applet = {
    "map" : LMap,
    "poke" : Pokemom,
    "Fruit" : Fruit,
    "ScATTer" : Scatter,
    "split" : SplitMap
}

app_current = solara.reactive("map")
app_all = [ k for k in applet.keys() ]

@solara.component 
def ModSelector(mods, c):
    def on_click(m):
        def c() :
            app_current.set(m)
        return c
    with solara.Row(style="color: blue;") as main:
        for m in mods :
            solara.Button(m, on_click=on_click(m) , outlined=True, color="blue",
                          style="min-width: 100px; max-width: 100px; min-height: 60px; max-height: 60px;"
                          )
    return main

@solara.component
def Page():
    with solara.AppBarTitle() :
        solara.Title("Applet")
        ModSelector(app_all, app_current)
        
    # with solara.Row():          
    # with solara.Sidebar(style="min-width: 80px; max-width: 80px;",) as bar:
        # solara.ToggleButtonsSingle(app_current, values=app_all)
    
    mod = applet[app_current.value]
    mod()

    
    
    

