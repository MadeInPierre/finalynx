"""
```{warning}
This is a barebones file (with a temporary ugly structure), please check back later!
```
"""
import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Set

from finalynx.analyzer.asset_class import AnalyzeAssetClasses
from finalynx.portfolio.folder import Folder
from finalynx.portfolio.node import Node
from nicegui import ui

from ..console import console
from ..portfolio.portfolio import Portfolio

# TODO UGLY CODE FOR NOW, TO BE REFACTORED!!!


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

    def run(self, portfolio: Portfolio) -> None:
        """Simple structure for now, to be improved!"""
        self.color_map = "finalynx"
        self.selected_node: Node = portfolio

        def _on_select_color_map(data: Any) -> None:
            self.color_map = "finalynx" if data.value == 1 else "finary"
            self._update_chart()

        ui.colors(primary="#2E3440", secondary="#F5A623", accent="#F8333C")

        with ui.header(elevated=True).classes("items-center justify-between"):
            with ui.row().classes("items-center"):
                ui.button(on_click=lambda: left_drawer.toggle()).props("flat color=white icon=menu")
                ui.label("Finalynx Dashboard").classes("text-bold").style("font-size: 20px")
            ui.label(self._get_today_str()).style("font-size: 18px")
            ui.button("Export", on_click=lambda: ui.notify("Coming soon!")).props("icon=file_download color=accent")

        with ui.left_drawer(value=False, bottom_corner=True, elevated=True).style(
            "background-color: #ECEFF4"
        ) as left_drawer:
            ui.image(self._url_logo)
            ui.markdown("#### Welcome to Finalynx!").classes("text-center")
            ui.label("Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...")
            # ui.badge("Hello", color="accent").props("rounded")

            with ui.column():
                ui.button(
                    "Dense",
                    on_click=lambda: tree.props("dense")
                    if "dense" not in tree._props.keys()
                    else tree.props(remove="dense"),
                ).props("color=secondary")

                with ui.row():
                    ui.label("Color map: ")
                    ui.toggle({1: "Finalynx", 2: "Finary"}, value=1, on_change=_on_select_color_map)

        # with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        #     ui.label('RIGHT DRAWER')
        # with ui.footer(value=True).style('background-color: #3874c8'):
        #     ui.label('FOOTER')

        with ui.splitter(value=40).classes("w-full") as splitter:
            with splitter.before:
                self.portfolio_dict = self._convert_rich_tree_to_nicegui(portfolio)
                max_id = self._add_ids_to_tree(self.portfolio_dict)

                # with ui.card_section().style("padding: 20px 40px"):
                #     ui.markdown(f"#### {self.portfolio_dict['label']}").classes("text-center").style(
                #         "padding: 0 0 10px 0"
                #     )
                #     tree = ui.tree(
                #         self.portfolio_dict["children"],
                #         on_expand=self._on_tree_expand,
                #         on_select=self._on_tree_select,
                #         on_tick=self._on_tree_tick,
                #     ).props("selected-color=secondary")
                #     tree._props["expanded"] = list(range(max_id))

                ui.markdown(f"#### {portfolio.render('[dashboard_tree]')}").classes("text-center").style(
                    "padding: 0 0 10px 0"
                )

                with ui.tree(
                    self.portfolio_dict["children"],
                    on_select=self._on_tree_select,
                ).classes("w-full") as tree:
                    tree._props["expanded"] = list(range(max_id))

                    tree.add_slot(
                        "default-header",
                        """
                            <q-icon v-if="props.node.icon !== 'menu'" v-bind="{ name: props.node.icon, color: props.node.color }" size="20px"/>
                            <span :props="props">
                            <strong>
                                <span :style="{ color: props.node.color }">&nbsp;{{ props.node.amount }} €</span>
                            </strong>
                            <strong v-if="props.node.is_folder">
                                <span style="color: #455A64">&nbsp;{{ props.node.name }}</span>
                            </strong>
                            <span v-else style="color: black">&nbsp;{{ props.node.name }}</span>
                            </span>
                        """,
                    )

                    # tree.add_slot(
                    #     "default-body",
                    #     """
                    #     <span :props="props">{{ props.node.hint }}</span>
                    # """,
                    # )

                # dashboard_console = Console(record=True)
                # dashboard_console.print(portfolio.tree(output_format="[dashboard_console]", hide_root=True))
                # ui.html(dashboard_console.export_html())

            with splitter.after:
                self.chart = ui.chart(AnalyzeAssetClasses(self.selected_node).chart(self.color_map))
                # self.hey = ui.label(f"Selected node: {portfolio.render(output_format='[dashboard]')}")

        ui.run(title="Finalynx Dashboard", favicon=self._url_logo, reload=True, show=True, host="0.0.0.0")

    def _on_tree_expand(self, event: Any) -> None:
        console.log(event)

    def _on_tree_select(self, event: Any) -> None:
        node_id = event.value if event.value else 1
        node = self._get_node_from_id(node_id, self.portfolio_dict)
        assert node is not None
        self.selected_node = node
        self._update_chart()

    def _update_chart(self) -> None:
        # Show which node is currently selected
        # self.hey.set_text(f"Selected node: {self.selected_node.render(output_format='[dashboard]')}")

        # Update chart with the selected node's info
        new_config = AnalyzeAssetClasses(self.selected_node).chart(self.color_map)
        self.chart.options["title"]["text"] = new_config["title"]["text"]
        self.chart.options["series"][0]["data"][:] = new_config["series"][0]["data"]
        self.chart.update()

    def _on_tree_tick(self, event: Any) -> None:
        console.log(event)

    def _convert_rich_tree_to_nicegui(self, node: Node) -> Dict[str, Any]:
        dict_icons = {
            "NOK": ("close", "red"),
            "OK": ("done", "green"),
            "Tolerated": ("warning", "yellow"),
            "Invest": ("keyboard_double_arrow_up", "red"),
            "Devest": ("keyboard_double_arrow_down", "purple"),
            "Start": ("bolt", "blue"),
            "No target": ("menu", "black"),
        }

        check_result = node.target.check()["name"]

        result = {
            "label": node.render(output_format="[dashboard_tree]"),
            "amount": node.get_amount(),
            "name": node.name,
            "hint": node.target.hint(),
            "icon": dict_icons[check_result][0],
            "color": dict_icons[check_result][1],
            "is_folder": isinstance(node, Folder),
            "instance": node,
        }

        if isinstance(node, Folder) and node.children:
            result["children"] = [self._convert_rich_tree_to_nicegui(c) for c in node.children]  # type: ignore
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

    def _get_node_from_id(self, node_id: int, nicegui_tree: Dict[str, Any]) -> Optional[Node]:
        # Return this node's object if the id corresponds
        if nicegui_tree["id"] == node_id:
            node: Node = nicegui_tree["instance"]
            return node

        # Otherwise, search for the node in the children
        if "children" in nicegui_tree.keys():
            for child in nicegui_tree["children"]:
                result = self._get_node_from_id(node_id, child)
                if result:
                    return result
        return None

    def _get_today_str(self) -> str:
        today = datetime.date.today()
        letter = "th" if 11 <= today.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(today.day % 10, "th")
        return today.strftime(f"%B %d{letter}, %Y")
