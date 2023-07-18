from pathlib import Path
from openbb_core.app.model.system_settings import SystemSettings
from openbb_core.app.model.user_settings import UserSettings
from openbb_core.logs.utils.utils import get_app_id


# pylint: disable=too-many-instance-attributes
class ChartingSettings:
    def __init__(self, user_settings: UserSettings, system_settings: SystemSettings):
        has_hub = user_settings.profile.hub_session is not None

        user_data_directory = (
            str(Path.home() / "OpenBBUserData")
            if not user_settings.preferences
            else user_settings.preferences.data_directory
        )

        # System
        self.log_collect: bool = system_settings.log_collect
        self.version = system_settings.version
        self.python_version = system_settings.python_version
        self.test_mode = system_settings.test_mode
        self.app_id: str = get_app_id(user_data_directory)
        # User
        self.plot_pywry_width = user_settings.preferences.plot_pywry_width
        self.plot_pywry_height = user_settings.preferences.plot_pywry_height
        self.plot_open_export = user_settings.preferences.plot_open_export
        self.user_email = user_settings.profile.hub_session.email if has_hub else None
        self.user_uuid = (
            user_settings.profile.hub_session.user_uuid if has_hub else None
        )
        self.user_exports_directory = user_settings.preferences.export_directory
        # Theme
        self.chart_style = user_settings.preferences.chart_style
        self.rich_style = user_settings.preferences.rich_style
