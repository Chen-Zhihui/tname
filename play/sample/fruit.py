import solara

subpages = ["", "foo", "bar", "solara", "react-ipywidgets"]
@solara.component
def Fruit(name: str = ""):
    
    level = solara.use_route_level()  # returns 0
    route_current, routes_current_level = solara.use_route()
    
    solara.Markdown(f"You are at: {name}")
    solara.Markdown(f"level: {level}")
    solara.Markdown(f"route_current: {route_current}")
    s = '\n'.join([ r.path for r in routes_current_level])
    solara.Markdown(f"routes_current_level: {s}")
    


