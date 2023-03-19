from typing import Callable
from typing import Dict
from typing import Optional


class Render:
    """Abstract class used to transform a render format to the output."""

    MAX_ALIAS_DEPTH = 10
    """Maximum recursion depth when replacing aliases to prevent infinite loops."""

    def __init__(
        self, aliases: Optional[Dict[str, str]] = None, agents: Optional[Dict[str, Callable[[str], str]]] = None
    ) -> None:
        """Abstract class used by subclasses to render themselves as string with a customizable format.
        This class offers a `render` method which takes a format as input and outputs the corresponding string.
        See [formatting guidelines](https://finalynx.readthedocs.io/en/latest/tutorials/customization.html)
        for more information.
        :param aliases: A key:value dictionary, defaults to empty. Specified keywords will be recursively
        transformed into the value until all keywords don't appear in the text.
        :param agents: A key:value dictionary, defaults to empty. Keywords will be replaced by what the method
        given as value will output.
        """
        self._render_aliases: Dict[str, str] = aliases if aliases else {}
        self._render_agents: Dict[str, Callable[[str], str]] = agents if agents else {}

    def render(self, output_format: str = "console") -> str:
        """Render the instance as a string by following the output format. See
        [formatting guidelines](https://finalynx.readthedocs.io/en/latest/tutorials/customization.html)
        for more information.
        :returns: A string representation of the instance based on the output format.
        """

        # Recursively replace alias keywords by their correspoding values
        output_format = self._apply_aliases(output_format)

        # Call the corresponding methods called "agents" for each keyword
        rendered_str = output_format
        for keyword, renderer in self._render_agents.items():
            rendered_str = rendered_str.replace("{" + keyword + "}", renderer(rendered_str))

        return rendered_str

    def _apply_aliases(self, output_format: str) -> str:
        """Internal method that recursively replaces alias keywords into their values specified
        in `self._render_aliases`.
        :returns: A string of the output format with aliases replaced.
        """
        if not output_format:
            raise ValueError("Render format cannot be empty.")

        old_format, iterations = "", 0

        while old_format is not output_format and iterations < Render.MAX_ALIAS_DEPTH:
            old_format = output_format

            for alias, value in self._render_aliases.items():
                output_format = output_format.replace(alias, value)

            iterations += 1

        if iterations == Render.MAX_ALIAS_DEPTH:
            raise ValueError("Stopped infinite loop while applying render aliases.")

        return output_format
