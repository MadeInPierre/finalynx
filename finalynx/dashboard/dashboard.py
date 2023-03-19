"""
```{tip}
TODO Dummy class for now, check back later or help us by contributing!
```
"""
import datetime
from typing import Any
from typing import Dict
from typing import Set

from nicegui import ui
from rich.tree import Tree

from ..console import console
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

    _logo_colors = ["000000", "E0AE80", "885540", "EEDFBC", "6F988D"]
    _attempts = ["F8333C", "7D8491"]
    _greys = [
        "FFFFFF",
        "F4F5F6",
        "DDE0E3",
        "C7CCD1",
        "B0B8BF",
        "9AA4AC",
        "84909A",
        "6E7C87",
        "5C6770",
        "49525A",
        "373E43",
        "25292D",
        "121416",
        "000000",
    ]

    def __init__(self) -> None:
        """Empty initialization for now."""
        pass

    def run(self, portfolio: Portfolio) -> None:
        """Dummy output for now, will host a local web server in the future."""

        ui.colors(primary="#2E3440", secondary="#F5A623", accent="#F8333C")

        with ui.header(elevated=True).classes("items-center justify-between"):
            with ui.row().classes("items-center"):
                ui.button(on_click=lambda: left_drawer.toggle()).props("flat color=white icon=menu")
                ui.label("Finalynx Dashboard").classes("text-bold").style("font-size: 20px")
            ui.label(self._get_today_str()).style("font-size: 18px")
            ui.button("Export", on_click=lambda: ui.notify("Coming soon!")).props("icon=file_download color=accent")

        with ui.left_drawer(bottom_corner=True, elevated=True).style("background-color: #ECEFF4") as left_drawer:
            ui.image(self._url_logo)
            ui.markdown("#### Welcome to Finalynx!").classes("text-center")
            ui.label("Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...")
            # ui.badge("Hello", color="accent").props("rounded")
            ui.button(
                "Dense",
                on_click=lambda: tree.props("dense")
                if "dense" not in tree._props.keys()
                else tree.props(remove="dense"),
            ).props("color=secondary")

        # with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        #     ui.label('RIGHT DRAWER')
        # with ui.footer(value=True).style('background-color: #3874c8'):
        #     ui.label('FOOTER')

        with ui.row():
            with ui.card().tight():
                portfolio_dict = self._convert_rich_tree_to_nicegui(portfolio.tree(format="name"))
                max_id = self._add_ids_to_tree(portfolio_dict)

                with ui.card_section().style("padding: 20px 40px"):
                    ui.markdown(f"#### **{portfolio_dict['label']}**").classes("text-center").style(
                        "padding: 0 0 10px 0"
                    )
                    tree = ui.tree(
                        portfolio_dict["children"],
                        on_expand=self._on_expand,
                        on_select=self._on_select,
                        on_tick=self._on_tick,
                    ).props("selected-color=accent")
                    tree._props["expanded"] = list(range(max_id))

            with ui.card():
                self.hey = ui.label("Hello")

        ui.run(title="Finalynx Dashboard", favicon=self._url_logo, reload=True, show=False)

    def _on_expand(self, event: Any) -> None:
        console.log(event)

    def _on_select(self, event: Any) -> None:
        console.log(event)
        self.hey.set_text(f"Selected node: {event.value}")

    def _on_tick(self, event: Any) -> None:
        console.log(event)

    def _convert_rich_tree_to_nicegui(self, rich_tree: Tree) -> Dict[str, Any]:
        name = str(rich_tree.label)
        result = {"label": name, "icon": "trending_up", "classes": "text-weight-bold text-primary"}
        if rich_tree.children:
            result["children"] = [self._convert_rich_tree_to_nicegui(c) for c in rich_tree.children]  # type: ignore
        return result

    def _add_ids_to_tree(self, node: Dict[str, Any], used_ids: Set[int] = set(), id_counter: int = 1) -> int:
        while id_counter in used_ids:
            id_counter += 1
        node["id"] = id_counter
        used_ids.add(id_counter)
        if "children" in node:
            for child in node["children"]:
                id_counter = self._add_ids_to_tree(child, used_ids, id_counter + 1)
        return id_counter

    def _get_today_str(self) -> str:
        today = datetime.date.today()
        letter = "th" if 11 <= today.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(today.day % 10, "th")
        return today.strftime(f"%B %d{letter}, %Y")
