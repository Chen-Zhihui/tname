import solara

routes = [
    # route level == 0
    solara.Route(path="/"),  # matches empty path ''
    solara.Route(
        # route level == 1
        path="docs",  # matches '/docs'
        children=[
            # route level == 2
            solara.Route(path="basics", children=[  # matches '/docs/basics'
                # route level == 3
                solara.Route(path="react"),      # matches '/docs/basics/react'
                solara.Route(path="ipywidgets"), # matches '/docs/basics/ipywidgets'
                solara.Route(path="solara"),     # matches '/docs/basics/solara'
            ]),
            solara.Route(path="advanced")  # matches '/docs/advanced'
        ],
    ),
    solara.Route(
        path="blog",
        # route level == 1
        children=[
            solara.Route(path="/"),   # matches '/blog'
            solara.Route(path="foo"), # matches '/blog/foo'
            solara.Route(path="bar"), # matches '/blog/bar'
        ],
    ),
    solara.Route(path="contact")  # matches '/contact'
]

# Lets assume our pathname is `/docs/basics/react`,
@solara.component
def Page():
    level = solara.use_route_level()  # returns 0
    route_current, routes_current_level = solara.use_routes()
    # route_current is routes[1], i.e. solara.Route(path="docs", children=[...])
    # routes_current_level is [routes[0], routes[1], routes[2], routes[3]], i.e.:
    #    [solara.Route(path="/"), solara.Route(path="docs", children=[...]),
    #     solara.Route(path="blog", children=[...]), solara.Route(path="contact")]
    if route_current is None: # no matching route
        return solara.Error("oops, page not found")
    else:
        # we could render some top level navigation here based on route_current_level and route_current
        return solara.Button(label="TEXT")