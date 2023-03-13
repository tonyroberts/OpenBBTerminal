"""Feature Flags Controller Module"""
__docformat__ = "numpy"

import argparse
import logging

# IMPORTATION STANDARD
import os
from typing import List, Optional

from pydantic import ValidationError

from openbb_terminal import config_terminal as cfg

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

    CHOICES_COMMANDS: List[str] = list(PreferencesModel.__annotations__.keys())
    CHOICES_COMMANDS.append("set")

    PATH = "/featflags/"

    languages_available = [
        lang.strip(".yml")
        for lang in os.listdir(cfg.i18n_dict_location)
        if lang.endswith(".yml")
    ]

    def __init__(self, queue: Optional[List[str]] = None):
        """Constructor."""
        super().__init__(queue)

        if session and get_current_user().preferences.USE_PROMPT_TOOLKIT:
            choices: dict = {"set": {}}
            choices["set"] = {c: {} for c in self.CHOICES_COMMANDS[:-1]}

            self.completer = NestedCompleter.from_nested_dict(choices)

    def print_help(self):
        """Print help."""
        current_user = get_current_user()

        mt = MenuText("featflags/")
        mt.add_info("_info_")
        mt.add_raw("\n")

        available_preferences = current_user.preferences.__dataclass_fields__.items()
        available_preferences = sorted(available_preferences)
        for (
            pref_name,
            pref_field,
        ) in available_preferences:
            help_message = pref_field.metadata.get("help")
            pref_value = getattr(current_user.preferences, pref_name)
            mt.add_raw(
                f"[cmds]    {pref_name}[/cmds]: {help_message} [yellow]{pref_value}[/yellow]"
            )

            mt.add_raw("\n")

        mt.add_raw("\n")
        mt.add_cmd("set")

        console.print(text=mt.menu_text, menu="Settings")

    @log_start_end(log=logger)
    def call_set(self, other_args: List[str]):
        """Process set command."""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="set",
            description="Set a preference",
        )
        parser.add_argument(
            "--name",
            "-n",
            dest="name",
            choices=self.CHOICES_COMMANDS[:-1],
            help="The name of preference to set",
            required="-h" not in other_args and "--help" not in other_args,
        )
        parser.add_argument(
            "--value",
            "-v",
            dest="value",
            help="The value to set the preference to",
            required="-h" not in other_args and "--help" not in other_args,
        )

        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-n")
        ns_parser = self.parse_simple_args(parser, other_args)

        if ns_parser:
            try:
                set_preference(
                    f"OPENBB_{ns_parser.name}",
                    ns_parser.value,
                )
                console.print(
                    f"[green]{ns_parser.name} set to {ns_parser.value}[/green]"
                )

            except ValidationError as error:
                err = error.errors()[0]
                msg = err.get("msg", "").capitalize()
                console.print(
                    f"""[red]{msg}.[/red]""",
                )
