"""Feature Flags Controller Module"""
__docformat__ = "numpy"

# IMPORTATION STANDARD
import logging
from typing import List, Optional

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
    """Feature Flags Controller class"""

    CHOICES_COMMANDS: List[str] = [c for c in PreferencesModel.__annotations__.keys()]

    PATH = "/featflags/"

    def __init__(self, queue: Optional[List[str]] = None):
        """Constructor"""
        super().__init__(queue)

        if session and get_current_user().preferences.USE_PROMPT_TOOLKIT:
            choices: dict = {c: {} for c in self.controller_choices}
            self.completer = NestedCompleter.from_nested_dict(choices)

    def print_help(self):
        """Print help"""
        current_user = get_current_user()

        mt = MenuText("featflags/")
        mt.add_info("_info_")
        mt.add_raw("\n")

        # automatically add the settings  by looping over the CHOICES_COMMANDS and the preferences model
        for (
            pref_name,
            pref_field,
        ) in current_user.preferences.__dataclass_fields__.items():
            help = pref_field.metadata.get("help")
            pref_value = getattr(current_user.preferences, pref_name)
            mt.add_raw(f"{pref_name}: {pref_value} {help}\n")

        console.print(text=mt.menu_text, menu="Feature Flags")

    def call_overwrite(self, _):
        """Process overwrite command"""
        set_preference(
            "OPENBB_FILE_OVERWITE", not get_current_user().preferences.FILE_OVERWRITE
        )
