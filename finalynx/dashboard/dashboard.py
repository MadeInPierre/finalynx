"""
```{tip}
TODO Dummy class for now, check back later or help us by contributing!
```
"""
import datetime
import json
from typing import Dict

from nicegui import ui
from rich.tree import Tree

from ..portfolio.portfolio import Portfolio


class Dashboard:
    """
    Main class for hosting an interactive web-based dashboard.

    It will soon show your portfolio and simulation results in all its glory!

    This module has not started development yet. Check back soon!
    """

    _url_logo = (
        "https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/logo_assistant_transparent.png"
    )

    def __init__(self) -> None:
        """Empty initialization for now."""
        pass

    def run(self, portfolio: Portfolio) -> None:
        """Dummy output for now, will host a local web server in the future."""

        with ui.header(elevated=True).style("background-color: #3874c8").classes("items-center justify-between"):
            ui.label(f"Finalynx Dashboard - {self._get_today_str()}")
            ui.button("Export PDF", on_click=lambda: ui.notify("Coming soon!")).props("icon=file_download disabled")
            # ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')

        with ui.left_drawer(top_corner=True, bottom_corner=True).style("background-color: #d7e3f4"):
            ui.image(self._url_logo)
            with ui.card_section():
                ui.label("Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...")

        # with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        #     ui.label('RIGHT DRAWER')

        # with ui.footer().style('background-color: #3874c8'):
        #     ui.label('FOOTER')

        with ui.row():
            with ui.card().tight():
                print(json.dumps(self._convert_rich_tree_to_nicegui(portfolio.rich_tree()), indent=4))
                with ui.card_section():
                    ui.tree(
                        [self._convert_rich_tree_to_nicegui(portfolio.rich_tree())],
                        node_key="label",
                        on_expand=self._on_tree_expand,
                    ).props("default-expand-all tick-strategy=leaf")

        ui.run(title="Finalynx Dashboard", favicon=self._url_logo, reload=False)

    def _on_tree_expand(self, sender, client, value):
        print(sender, client, value)

    def _convert_rich_tree_to_nicegui(self, rich_tree: Tree) -> Dict:
        name = str(rich_tree.label)
        result = {"label": name, "icon": "dollar", "expanded": "true"}
        if rich_tree.children:
            result["children"] = [self._convert_rich_tree_to_nicegui(c) for c in rich_tree.children]
        return result

    def _get_today_str(self) -> str:
        today = datetime.date.today()
        return today.strftime("%B %d") + (
            "th" if 11 <= today.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(today.day % 10, "th")
        )
