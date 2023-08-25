"""_summary_

Returns:
    _type_: _description_
    
    #1 internal state in components
    #2 state
        s = solara.reactive("some")
        value, set_value = solara.use_state("s")
        s = solara.use_reactive("s")
"""


import solara 
import plotly.express as px
df = px.data.iris()
columns = list(df.columns)

# click_data = solara.reactive(None)
# x_axis = solara.reactive("sepal_length")
# y_axis = solara.reactive("sepal_width")

def find_nearest_neighbours(df, xcol, ycol, x, y, n=10):
    df = df.copy()
    df["distance"] = ((df[xcol] - x)**2 + (df[ycol] - y)**2)**0.5
    return df.sort_values('distance')[1:n+1]


@solara.component
def Refresh():    

    # declare state
    click_data_, set_click_data_ = solara.use_state(None)    
    x_axis = solara.use_reactive("sepal_length")
    y_axis = solara.use_reactive("sepal_width")  
    
    # compose ui with data
    fig = px.scatter(df, x_axis.value, y_axis.value, color="species", custom_data=[df.index])
  
    card_style = "min-width: 800px"
    with solara.Column(align="center") as main:
        
        with solara.Card(style=card_style):
            if click_data_ is not None:
                x = click_data_["points"]["xs"][0]
                y = click_data_["points"]["ys"][0]

                # add an indicator 
                fig.add_trace(px.scatter(x=[x], y=[y], text=["⭐️"]).data[0])
                df_nearest = find_nearest_neighbours(df, x_axis.value, y_axis.value, x, y, n=3)
            else:
                df_nearest = None

            solara.Select(label="X-axis", value=x_axis, values=columns)
            solara.Select(label="Y-axis", value=y_axis, values=columns)
                
    # set callback with ui change
        with solara.Card(style=card_style):
            solara.FigurePlotly(fig, on_click=set_click_data_)
            
        with solara.Card(style=card_style):
            if df_nearest is not None:
                solara.Markdown("## Nearest 3 neighbours")
                solara.DataFrame(df_nearest)
            else:
                solara.Info("Click to select a point")
            
        
    return main