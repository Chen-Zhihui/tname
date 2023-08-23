import solara
import reacton.ipyvuetify as rv

@solara.component
def Button():
    clicks, set_clicks = solara.use_state(0)
    def my_click_handler(*ignore_args):
        # trigger a new render with a new value for clicks
        set_clicks(clicks+1)
    button = rv.Btn(children=[f"Clicked {clicks} times"])
    rv.use_event(button, 'click', my_click_handler)
    return button



@solara.component
def Vue():
    return Button()