
import solara 
from solara.components.applayout import AppBar, AppBarTitle, ElementPortal, Sidebar
import reacton.ipyvuetify as v
import solara.components.title as t

should_use_embed = solara.create_context(False)

sidebar_portal = ElementPortal()
appbar_portal = ElementPortal()
apptitle_portal = ElementPortal()

@solara.component
def AppIcon(open=False, on_click=None, **kwargs):
    def click(*ignore):
        on_click()

    icon = v.AppBarNavIcon(**kwargs)
    v.use_event(icon, "click", click)
    return icon

@solara.component
def Layout(
    children=[],
    sidebar_open=True,
    title=None,
    navigation=True,
    toolbar_dark=True,
):
    """The default layout for Solara apps. It consists of an toolbar bar, a sidebar and a main content area.

     * The title of the app is set using the [Title](/api/title) component.
     * The sidebar content is set using the [Sidebar](/api/sidebar) component.
     * The content is set by the `Page` component provided by the user.

    This component is usually not used directly, but rather through via the [Layout system](/docs/howto/layout).

    The sidebar is only added when the AppLayout has more than one child.

    ```python
    with AppLayout(title="My App"):
        with v.Card():
            ...  # sidebar content
        with v.Card():
            ...  # main content
    ```

    # Arguments

     * `children`: The children of the AppLayout. The first child is used as the sidebar content, the rest as the main content.
     * `sidebar_open`: Whether the sidebar is open or not.
     * `title`: The title of the app shown in the app bar, can also be set using the [Title](/api/title) component.
     * `toolbar_dark`: Whether the toolbar should be dark or not.
     * `navigation`: Whether the navigation tabs based on routing should be shown.

    """
    route, routes = solara.use_route()
    paths = [solara.resolve_path(r, level=0) for r in routes]
    location = solara.use_context(solara.routing._location_context)
    embedded_mode = solara.use_context(should_use_embed)
    fullscreen, set_fullscreen = solara.use_state(False)
    # we cannot nest AppLayouts, so we can use the context to set the embedded mode
    should_use_embed.provide(True)
    index = routes.index(route) if route else None

    sidebar_open, set_sidebar_open = solara.use_state_or_update(sidebar_open)
    # remove the appbar from the children
    children_without_portal_sources = [c for c in children if c.component != AppBar]
    use_drawer = len(children_without_portal_sources) > 1
    children_content = children
    children_sidebar = []
    if use_drawer:
        child_sidebar = children_without_portal_sources.pop(0)
        children_sidebar = [child_sidebar]
        children_content = [c for c in children if c is not child_sidebar]
    children_sidebar = children_sidebar + sidebar_portal.use_portal()
    children_appbar = appbar_portal.use_portal()
    if children_sidebar:
        use_drawer = True
    title = t.use_title_get() or title
    children_appbartitle = apptitle_portal.use_portal()
    show_app_bar = (title and (len(routes) > 1 and navigation)) or children_appbar or use_drawer or children_appbartitle
    if not show_app_bar and not children_sidebar and len(children) == 1:
        return children[0]

    def set_path(index):
        path = paths[index]
        location.pathname = path

    v_slots = []

    tabs = None
    for child_appbar in children_appbar.copy():
        if child_appbar.component == solara.lab.Tabs:
            if tabs is not None:
                raise ValueError("Only one Tabs component is allowed in the AppBar")
            tabs = child_appbar
            children_appbar.remove(tabs)

    if (tabs is None) and routes and navigation and (len(routes) > 1):
        with solara.lab.Tabs(value=index, on_value=set_path, align="center") as tabs:
            for route in routes:
                name = route.path if route.path != "/" else "Home"
                solara.lab.Tab(name)
        # with v.Tabs(v_model=index, on_v_model=set_path, centered=True) as tabs:
        #     for route in routes:
        #         name = route.path if route.path != "/" else "Home"
        #         v.Tab(children=[name])
    if tabs is not None:
        v_slots = [{"name": "extension", "children": tabs}]
    if embedded_mode and not fullscreen:
        # this version doesn't need to run fullscreen
        # also ideal in jupyter notebooks
        with v.Html(tag="div") as main:
            if show_app_bar or use_drawer:
                with v.AppBar(color="primary" if toolbar_dark else None, dark=toolbar_dark, v_slots=v_slots):
                    if use_drawer:
                        icon = AppIcon(sidebar_open, on_click=lambda: set_sidebar_open(not sidebar_open), v_on="x.on")
                        with v.Menu(
                            offset_y=True,
                            nudge_left="50px",
                            left=True,
                            v_slots=[{"name": "activator", "variable": "x", "children": [icon]}],
                            close_on_content_click=False,
                        ):
                            pass
                            v.Html(tag="div", children=children_sidebar, style_="background-color: white; padding: 12px; min-width: 400px")
                    if title or children_appbartitle:
                        v.ToolbarTitle(children=children_appbartitle or [title])
                    v.Spacer()
                    for child in children_appbar:
                        solara.display(child)
                    solara.Button(icon_name="mdi-fullscreen", on_click=lambda: set_fullscreen(True), icon=True, dark=False)
            with v.Row(no_gutters=False, class_="solara-content-main"):
                v.Col(cols=12, children=children_content)
    else:
        # this limits the height of the app to the height of the screen
        # and further down we use overflow: auto to add scrollbars to the main content
        # the navigation drawer adds it own scrollbars
        # NOTE: while developing this we added overflow: hidden, but this does not seem
        # to be necessary anymore
        with v.Html(tag="div", style_="height: 100vh") as main:
            # with solara.HBox():
            #     if use_drawer:
            #         with v.NavigationDrawer(
            #             width="min-content",
            #             v_model=sidebar_open,
            #             on_v_model=set_sidebar_open,
            #             style_="min-width: 400px; max-width: 600px",
            #             clipped=True,
            #             app=True,
            #             # disable_resize_watcher=True,
            #             disable_route_watcher=True,
            #             mobile_break_point="960",
            #             class_="solara-content-main",
            #         ):
            #             if not show_app_bar:
            #                 AppIcon(sidebar_open, on_click=lambda: set_sidebar_open(not sidebar_open))
            #             v.Html(tag="div", children=children_sidebar, style_="padding: 12px;").meta(ref="sidebar-content")
            #     else:
            #         AppIcon(sidebar_open, on_click=lambda: set_sidebar_open(not sidebar_open), style_="position: absolute; z-index: 2")
            if show_app_bar:
                # if hide_on_scroll is True, and we have a little bit of scrolling, vuetify seems to act strangely
                # when scrolling (on @mariobuikhuizen/vuetify v2.2.26-rc.0
                with v.AppBar(color="primary", dark=True, app=True, clipped_left=True, hide_on_scroll=False, v_slots=v_slots):
                    if use_drawer:
                        AppIcon(sidebar_open, on_click=lambda: set_sidebar_open(not sidebar_open))
                    if title or children_appbartitle:
                        v.ToolbarTitle(children=children_appbartitle or [title])
                    v.Spacer()
                    for child in children_appbar:
                        solara.display(child)
                    if fullscreen:
                        solara.Button(icon_name="mdi-fullscreen-exit", on_click=lambda: set_fullscreen(False), icon=True, dark=False)

            with v.Content(class_="solara-content-main", style_="height: 100%;"):
                # make sure the scrollbar does no go under the appbar by adding overflow: auto
                # to a child of content, because content has padding-top: 64px (set by vuetify)
                # the padding: 12px is needed for backward compatibility with the previously used
                # v.Col which has this by default. If we do not use this, a solara.Column will
                # use a margin: -12px which will make a horizontal scrollbar appear
                solara.Div(style_="height: 100%; overflow: auto; padding: 12px;", children=children_content)
        if fullscreen:
            with v.Dialog(v_model=True, children=[], fullscreen=True, hide_overlay=True, persistent=True, no_click_animation=True) as dialog:
                v.Sheet(class_="overflow-y-auto overflow-x-auto", children=[main])
                pass
            return dialog
    return main
