import solara
from solara.website.pages.examples.utilities import calculator


@solara.component
def Home():
    solara.Markdown("Home")


@solara.component
def About():
    solara.Markdown("About")


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
    
    # bunch of buttons which navigate to our dynamic route
    with solara.Sidebar():
        with solara.Column():
            for subpage in subpages:
                with solara.Link(solara.resolve_path(subpage)):
                    solara.Markdown(f"{solara.resolve_path(subpage)}")
                    solara.Text(f"Go to: {subpage}")


routes = [
    solara.Route(path="/", component=Home, label="Home3"),
    solara.Route(path="fruit", label="Fruit", component=Fruit),
    # the calculator module should have a Page component
    solara.Route(path="calculator", module=calculator, label="Calculator"),
    solara.Route(path="about", component=About, label="About")
]

