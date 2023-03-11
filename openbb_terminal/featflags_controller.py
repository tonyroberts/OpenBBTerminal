"""Feature Flags Controller Module"""
__docformat__ = "numpy"

# IMPORTATION STANDARD
import argparse
import logging
from typing import List, Optional

from pydantic import ValidationError

# IMPORTATION INTERNAL
from openbb_terminal.core.models.preferences_model import PreferencesModel

# IMPORTATION THIRDPARTY
from openbb_terminal.core.session.current_user import get_current_user
from openbb_terminal.core.session.preferences_handler import set_preference
from openbb_terminal.custom_prompt_toolkit import NestedCompleter
from openbb_terminal.decorators import log_start_end
from openbb_terminal.menu import session
from openbb_terminal.parent_classes import BaseController
from openbb_terminal.rich_config import MenuText, console

# pylint: disable=too-many-lines,no-member,too-many-public-methods,C0302
# pylint:disable=import-outside-toplevel

logger = logging.getLogger(__name__)


class FeatureFlagsController(BaseController):
    """Feature Flags Controller class."""

    CHOICES_COMMANDS: List[str] = [c for c in PreferencesModel.__annotations__.keys()]
    CHOICES_COMMANDS.append("set")

    PATH = "/featflags/"

    def __init__(self, queue: Optional[List[str]] = None):
        """Constructor."""
        super().__init__(queue)

        if session and get_current_user().preferences.USE_PROMPT_TOOLKIT:
            choices: dict = {c: {} for c in self.controller_choices}
            self.completer = NestedCompleter.from_nested_dict(choices)

    def print_help(self):
        """Print help."""
        current_user = get_current_user()

        mt = MenuText("featflags/")
        mt.add_info("_info_")
        mt.add_raw("\n")

        for (
            pref_name,
            pref_field,
        ) in current_user.preferences.__dataclass_fields__.items():
            help_message = pref_field.metadata.get("help")
            pref_value = getattr(current_user.preferences, pref_name)
            mt.add_raw(
                f"[cmds]{pref_name}[/cmds]: [yellow]{pref_value}[/yellow] {help_message}\n"
            )

            mt.add_raw("\n")

        mt.add_raw("\n")
        mt.add_raw(
            "    [cmds]featflags/set[/cmds] [cmds]preference[/cmds] [cmds]value[/cmds]\n"
        )

        console.print(text=mt.menu_text, menu="Settings")

    # @log_start_end(logger)
    def call_set(self, other_args: List[str]):
        """Process set command."""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="set",
            description="Set a preference",
        )
        parser.add_argument(
            "preference",
            choices=self.CHOICES_COMMANDS,
            help="The preference to set",
        )
        parser.add_argument(
            "value",
            help="The value to set the preference to",
        )

        if not other_args or "-h" in other_args:
            help_txt = parser.format_help()
            console.print(f"[help]{help_txt}[/help]")
            return

        elif other_args[0] not in self.CHOICES_COMMANDS:
            console.print(
                f"""[red]"{other_args[0]}" is not a valid preference[/red]."""
            )
            return

        ns_parser = self.parse_simple_args(parser, other_args)

        if ns_parser:
            try:
                default_value_type = type(
                    getattr(get_current_user().preferences, other_args[0])
                )
                default_value_type(ns_parser.value)
            except (ValueError, ValidationError):
                console.print(
                    f"""[red]Value "{ns_parser.value}" is not valid.[/red]""",
                    f"""[red]It should be of type {default_value_type}[/red]""",
                )
            else:
                set_preference(
                    f"OPENBB_{ns_parser.preference}",
                    ns_parser.value,
                )

                console.print(
                    f"[green] {ns_parser.preference} set to {ns_parser.value}[/green]"
                )
