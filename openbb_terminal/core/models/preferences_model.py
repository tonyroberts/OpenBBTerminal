import os
from dataclasses import field
from typing import Optional

from pydantic import NonNegativeInt, PositiveFloat, PositiveInt
from pydantic.dataclasses import dataclass

from openbb_terminal.core.config.paths import (
    HOME_DIRECTORY,
    USER_DATA_SOURCES_DEFAULT_FILE,
)

# pylint: disable=too-many-instance-attributes


@dataclass(config=dict(validate_assignment=True, frozen=True))
class PreferencesModel:
    """Data model for preferences."""

    # PLOT
    # Plot backend
    # Examples:
    # "tkAgg" - This uses the tkinter library.  If unsure, set to this
    # "module://backend_interagg" - This is what pycharm defaults to in Scientific Mode
    # "MacOSX" - Mac default.  Does not work with backtesting
    # "Qt5Agg" - This requires the PyQt5 package is installed
    # See more: https://matplotlib.org/stable/tutorials/introductory/usage.html#the-builtin-backends
    PLOT_BACKEND: Optional[str] = field(
        default=None,
        metadata={"help": "plotting backend (None, tkAgg, MacOSX, Qt5Agg)"},
    )
    PLOT_DPI: PositiveInt = field(default=100, metadata={"help": "plot dpi"})
    PLOT_HEIGHT: PositiveInt = field(
        default=500, metadata={"help": "select plot height"}
    )
    PLOT_WIDTH: PositiveInt = field(default=800, metadata={"help": "select plot width"})
    PLOT_HEIGHT_PERCENTAGE: PositiveFloat = field(
        default=50.0, metadata={"help": "plot height percentage"}
    )
    PLOT_WIDTH_PERCENTAGE: PositiveFloat = field(
        default=70.0, metadata={"help": "plot width percentage"}
    )

    # FEATURE FLAGS
    SYNC_ENABLED: bool = field(default=True, metadata={"help": "sync enabled"})
    FILE_OVERWRITE: bool = field(
        default=False, metadata={"help": "featflags/overwrite"}
    )
    RETRY_WITH_LOAD: bool = field(
        default=False, metadata={"help": "retry misspelled commands with load first"}
    )
    USE_TABULATE_DF: bool = field(
        default=True, metadata={"help": "use tabulate to print dataframes"}
    )
    USE_CLEAR_AFTER_CMD: bool = field(
        default=False, metadata={"help": "clear console after command"}
    )
    USE_COLOR: bool = field(default=True, metadata={"help": "use coloring features"})
    USE_DATETIME: bool = field(
        default=True, metadata={"help": "add or remove datetime from flair"}
    )
    # Enable interactive matplotlib mode: change variable name to be more descriptive and delete comment
    USE_ION: bool = field(
        default=True, metadata={"help": "interactive matplotlib mode"}
    )
    USE_WATERMARK: bool = field(default=True, metadata={"help": "watermark in figures"})
    # Enable command and source in the figures: change variable name to be more descriptive and delete comment
    USE_CMD_LOCATION_FIGURE: bool = field(
        default=True, metadata={"help": "command and source in figures"}
    )
    USE_PROMPT_TOOLKIT: bool = field(
        default=True,
        metadata={"help": "enable prompt toolkit (autocomplete and history)"},
    )
    USE_PLOT_AUTOSCALING: bool = field(
        default=False, metadata={"help": "plot autoscaling"}
    )
    ENABLE_THOUGHTS_DAY: bool = field(
        default=False, metadata={"help": "enable thoughts of the day"}
    )
    ENABLE_QUICK_EXIT: bool = field(
        default=False, metadata={"help": "enable quick exit"}
    )
    OPEN_REPORT_AS_HTML: bool = field(
        default=True, metadata={"help": "open report as HTML otherwise notebook"}
    )
    ENABLE_EXIT_AUTO_HELP: bool = field(
        default=True, metadata={"help": "automatically print help when quitting menu"}
    )
    REMEMBER_CONTEXTS: bool = field(
        default=True,
        metadata={"help": "remember contexts loaded params during session"},
    )
    ENABLE_RICH: bool = field(default=True, metadata={"help": "colorful rich terminal"})
    ENABLE_RICH_PANEL: bool = field(
        default=True, metadata={"help": "colorful rich terminal panel"}
    )
    ENABLE_CHECK_API: bool = field(
        default=True, metadata={"help": "check api before running command"}
    )
    LOG_COLLECTION: bool = field(
        default=False, metadata={"help": "enable log collection"}
    )
    TOOLBAR_HINT: bool = field(
        default=True, metadata={"help": "displays usage hints in the bottom toolbar"}
    )
    TOOLBAR_TWEET_NEWS: bool = field(
        default=False, metadata={"help": "displays tweets news in the bottom toolbar"}
    )

    # TOOLBAR
    TOOLBAR_TWEET_NEWS_SECONDS_BETWEEN_UPDATES: PositiveInt = field(
        default=300, metadata={"help": "seconds between updates"}
    )
    TOOLBAR_TWEET_NEWS_ACCOUNTS_TO_TRACK: str = field(
        default="WatcherGuru,unusual_whales,gurgavin,CBSNews",
        metadata={"help": "accounts to track"},
    )
    TOOLBAR_TWEET_NEWS_KEYWORDS: str = field(
        default="BREAKING,JUST IN", metadata={"help": "keywords to track"}
    )
    TOOLBAR_TWEET_NEWS_NUM_LAST_TWEETS_TO_READ: PositiveInt = field(
        default=3, metadata={"help": "number of last tweets to read"}
    )

    # GENERAL
    PREVIOUS_USE: bool = field(default=False, metadata={"help": "previous use"})
    TIMEZONE: str = field(default="America/New_York", metadata={"help": "set timezone"})
    FLAIR: str = field(default=":openbb", metadata={"help": "set flair"})
    USE_LANGUAGE: str = field(default="en", metadata={"help": "set terminal language"})
    REQUEST_TIMEOUT: PositiveInt = field(
        default=5, metadata={"help": "set request timeout"}
    )
    MONITOR: NonNegativeInt = field(
        default=0,
        metadata={"help": "which monitor to display on (primary 0, secondary 1, etc.)"},
    )

    # STYLE
    # Color for `view` command data.  All pyplot colors listed at:
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    VIEW_COLOR: str = field(default="tab:green", metadata={"help": "view color"})
    MPL_STYLE: str = field(default="dark", metadata={"help": "matplotlib style"})
    PMF_STYLE: str = field(default="dark", metadata={"help": "pmf style"})
    RICH_STYLE: str = field(default="dark", metadata={"help": "rich style"})

    # PATHS
    # PREFERRED_DATA_SOURCE_FILE: str = field(
    #     default=str(USER_DATA_SOURCES_DEFAULT_FILE),
    #     metadata={"help": "specify data source file"},
    # )
    # GUESS_EASTER_EGG_FILE: str = field(
    #     default=os.getcwd() + os.path.sep + "guess_game.json",
    #     metadata={"help": "easter egg file"},
    # )
    # USER_DATA_DIRECTORY = field(
    #     default=str(HOME_DIRECTORY / "OpenBBUserData"),
    #     metadata={"help": "set folder to store user data"},
    # )
    # USER_EXPORTS_DIRECTORY = field(
    #     # combine the default user data directory with the exports folder
    #     # the user data directory is the default value for USER_DATA_DIRECTORY
    #     default=str(USER_DATA_DIRECTORY) + os.path.sep + "exports",
    #     metadata={"help": "set folder to store user exports"},
    # )
    # USER_CUSTOM_IMPORTS_DIRECTORY = field(
    #     default=str(USER_DATA_DIRECTORY) + os.path.sep + "custom imports",
    #     metadata={"help": "set folder to store user custom imports"},
    # )
    # USER_PORTFOLIO_DATA_DIRECTORY = field(
    #     default=str(USER_DATA_DIRECTORY) + os.path.sep + "portfolio",
    #     metadata={"help": "set folder to store user portfolio data"},
    # )
    # USER_ROUTINES_DIRECTORY = field(
    #     default=str(USER_DATA_DIRECTORY) + os.path.sep + "routines",
    #     metadata={"help": "set folder to store user routines"},
    # )
    # USER_PRESETS_DIRECTORY = field(
    #     default=str(USER_DATA_DIRECTORY) + os.path.sep + "presets",
    #     metadata={"help": "set folder to store user presets"},
    # )
    # USER_REPORTS_DIRECTORY = field(
    #     default=str(USER_DATA_DIRECTORY) + os.path.sep + "reports",
    #     metadata={"help": "set folder to store user reports"},
    # )
    # USER_CUSTOM_REPORTS_DIRECTORY = field(
    #     default=str(USER_DATA_DIRECTORY)
    #     + os.path.sep
    #     + "reports"
    #     + os.path.sep
    #     + "custom reports",
    #     metadata={"help": "set folder to store user custom reports"},
    # )
    # USER_FORECAST_MODELS_DIRECTORY = field(
    #     default=str(USER_DATA_DIRECTORY)
    #     + os.path.sep
    #     + "exports"
    #     + os.path.sep
    #     + "forecast_models",
    #     metadata={"help": "set folder to store user forecast models"},
    # )
    # USER_FORECAST_WHISPER_DIRECTORY = field(
    #     default=str(USER_DATA_DIRECTORY)
    #     + os.path.sep
    #     + "exports"
    #     + os.path.sep
    #     + "whisper",
    #     metadata={"help": "set folder to store user forecast whispers"},
    # )

    # @validator("VIEW_COLOR")
    # def validate_view_color(cls, v):  # pylint: disable=no-self-argument
    #     if v not in {
    #         *mcolors.BASE_COLORS,
    #         *mcolors.TABLEAU_COLORS,
    #         *mcolors.CSS4_COLORS,
    #         *mcolors.XKCD_COLORS,
    #     }:
    #         raise ValueError("Color not supported")

    # PATHS
    PREFERRED_DATA_SOURCE_FILE: str = str(USER_DATA_SOURCES_DEFAULT_FILE)
    GUESS_EASTER_EGG_FILE: str = os.getcwd() + os.path.sep + "guess_game.json"
    USER_DATA_DIRECTORY = HOME_DIRECTORY / "OpenBBUserData"
    USER_EXPORTS_DIRECTORY = USER_DATA_DIRECTORY / "exports"
    USER_CUSTOM_IMPORTS_DIRECTORY = USER_DATA_DIRECTORY / "custom_imports"
    USER_PORTFOLIO_DATA_DIRECTORY = USER_DATA_DIRECTORY / "portfolio"
    USER_ROUTINES_DIRECTORY = USER_DATA_DIRECTORY / "routines"
    USER_PRESETS_DIRECTORY = USER_DATA_DIRECTORY / "presets"
    USER_REPORTS_DIRECTORY = USER_DATA_DIRECTORY / "reports"
    USER_CUSTOM_REPORTS_DIRECTORY = USER_DATA_DIRECTORY / "reports" / "custom reports"
    USER_FORECAST_MODELS_DIRECTORY = USER_DATA_DIRECTORY / "exports" / "forecast_models"
    USER_FORECAST_WHISPER_DIRECTORY = USER_DATA_DIRECTORY / "exports" / "whisper"
