import solara 
# from .scatter import Scatter
# from .pokemom import Pokemom
# from .fruit import Fruit
# from .lmap import LMap
from .splitmap import SplitMap
from .vue import Vue
from .refresh import Refresh
from .position import Position
from solara.layout import LayoutApp, AppIcon
import solara.lab
from solara import layout 

applet = {
    # "map" : LMap,
    # "poke" : Pokemom,
    # "Fruit" : Fruit,
    # "ScATTer" : Scatter,
    "Vue" : Vue,
    "交互" : Refresh,
    "地图" : SplitMap,
    "位置" : Position,
}

app_all = [ k for k in applet.keys() ]
app_current = solara.reactive(app_all[-1])


@solara.component
def AppNavigator(apps):
    def on_value(v):
        k = app_all[v]
        app_current.set(k)
    with solara.Row(justify="center") as main :
        with solara.lab.Tabs(
            value=0,
            vertical=True,
            on_value=on_value
            ) :
            for k in apps.keys():           
                solara.lab.Tab(k)
    return main


@solara.component
def AppNavigator2(apps):
    def on_value(v):
        k = app_all[v]
        app_current.set(k)
    with solara.Row(justify="center") as main :
        with solara.lab.Tabs(
            value=0,
            vertical=False,
            on_value=on_value
            ) :
            for k in apps.keys():           
                solara.lab.Tab(k)
    return main
# routes = [
#     solara.Route("/", component=Vue),
#     solara.Route("split", component=SplitMap),
#     solara.Route("poke", component=Pokemom)
# ]

@solara.component
def Layout(children=[]):
    # print("I get called before the Page component gets rendered")
    return layout.LayoutApp(children=children,
                            left=AppNavigator(applet),
                            # title=AppNavigator2,
                            title=solara.ToggleButtonsSingle(app_current, values=app_all)
                            )

@solara.component
def Page():
    # with solara.AppBarTitle() :
        # with solara.Row() :
            # solara.Title("Applet")
            # AppNavigator(applet)
            # solara.ToggleButtonsSingle(app_current, values=app_all)
         
    # with solara.Sidebar() as bar:
        # solara.Text("Main")
    
    # mod = applet[app_current.value]
    # mod()    
    # with solara.TabNavigation(vertical=True) as main:
    #     Vue()
    #     Fruit()
    #     Scatter()
    # return main
    with solara.Column() as main:            
        mod = applet[app_current.value]
        mod()   
    
    return main

