import inspect
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional


class Render:
    """Abstract class used to transform a render format to the output."""

    MAX_ALIAS_DEPTH = 10
    """Maximum recursion depth when replacing aliases to prevent infinite loops."""

    def __init__(
        self, aliases: Optional[Dict[str, str]] = None, agents: Optional[Dict[str, Callable[..., str]]] = None
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
        self._render_agents: Dict[str, Callable[..., str]] = agents if agents else {}

    def render(self, output_format: str = "[console]", **args: Dict[str, Any]) -> str:
        """Render the instance as a string by following the output format. See
        [formatting guidelines](https://finalynx.readthedocs.io/en/latest/tutorials/customization.html)
        for more information.
        :returns: A string representation of the instance based on the output format.
        """

        # TODO automatically add a space between components instead of hardcoding everywhere?

        # Utility method used below
        def safe_len(obj: Any) -> int:
            return len(obj) if obj else 0

        # Recursively replace alias keywords by their correspoding values
        output_format = self._apply_aliases(output_format)

        # Call the corresponding methods called "agents" for each keyword
        for keyword, agent in self._render_agents.items():
            # Filter the arguments to what this agent takes as input parameters
            argspec = inspect.getfullargspec(agent)
            kwargs = argspec.args[safe_len(argspec.args) - safe_len(argspec.defaults) :] if argspec else []  # noqa
            filtered_args = {k: v for k, v in args.items() if k in kwargs}

            # Call the method with the arguments provided by the user (filtered for this method above)
            output_format = output_format.replace(f"[{keyword}]", agent(**filtered_args))

        return output_format

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
            raise ValueError(f"Stopped infinite loop while applying render aliases, {output_format=}")

        return output_format
