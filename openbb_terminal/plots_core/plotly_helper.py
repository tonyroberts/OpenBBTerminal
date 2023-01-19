import json
import os
from pathlib import Path
from typing import Any, Dict, List, Union

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

from openbb_terminal.base_helpers import strtobool
from openbb_terminal.plots_core.backend import get_backend

# Reads the template from a file
with open(
    str(Path(__file__).parent.resolve() / "config/openbb.json"), encoding="utf-8"
) as f:
    OPENNBB_THEME = json.load(f)

# Register the template and set it as the default
pio.templates["openbb"] = go.layout.Template(OPENNBB_THEME)
pio.templates.default = "plotly_dark+openbb"


# pylint: disable=R0913
class OpenBBFigure(go.Figure):
    """Custom Figure class for OpenBB Terminal

    Parameters
    ----------
    fig : `go.Figure`, optional
        Figure to copy, by default None
    is_subplots : `bool`, optional
        Whether the figure is a subplots figure, by default False
    **kwargs
        Keyword arguments to pass to `go.Figure.update_layout`

    Class Methods
    -------------
    create_subplots(rows: `int`, cols: `int`, **kwargs) -> `OpenBBFigure`
        Creates a subplots figure

    Methods
    -------
    add_hline_legend(y: `float`, name: `str`, line: `dict`, legendrank: `int`, **kwargs)
        Adds a horizontal line with a legend label
    add_vline_legend(x: `float`, name: `str`, line: `dict`, legendrank: `int`, **kwargs)
        Adds a vertical line with a legend label
    add_legend_label(trace: `str`, label: `str`, mode: `str`, marker: `dict`, **kwargs)
        Adds a legend label

    """

    def __init__(self, fig: go.Figure = None, is_subplots: bool = False, **kwargs):
        super().__init__()
        if fig:
            self.__dict__ = fig.__dict__

        self._is_subplots = is_subplots
        self._has_secondary_y = kwargs.pop("has_secondary_y", False)

        if xaxis := kwargs.pop("xaxis", None):
            self.update_xaxes(xaxis)
        if yaxis := kwargs.pop("yaxis", None):
            self.update_yaxes(yaxis)

        if get_backend().isatty:
            self.update_layout(
                margin=dict(l=0, r=0, t=0, b=0, pad=0, autoexpand=True),
                height=762,
                width=1400,
                **kwargs,
            )

    @property
    def is_subplots(self):
        return self._is_subplots

    @is_subplots.setter
    def is_subplots(self, value):
        self._is_subplots = value

    @classmethod
    def create_subplots(
        cls,
        rows: int = 1,
        cols: int = 1,
        shared_xaxes: bool = True,
        vertical_spacing: float = None,
        horizontal_spacing: float = None,
        subplot_titles: Union[List[str], tuple] = None,
        row_width: List[Union[float, int]] = None,
        specs: List[List[Dict[Any, Any]]] = None,
        **kwargs,
    ) -> "OpenBBFigure":
        """Create a new Plotly figure with subplots

        Parameters
        ----------
        rows : `int`, optional
            Number of rows, by default 1
        cols : `int`, optional
            Number of columns, by default 1
        shared_xaxes : `bool`, optional
            Whether to share x axes, by default True
        vertical_spacing : `float`, optional
            Vertical spacing between subplots, by default None
        horizontal_spacing : `float`, optional
            Horizontal spacing between subplots, by default None
        subplot_titles : `Union[List[str], tuple]`, optional
            Titles for each subplot, by default None
        row_width : `List[Union[float, int]]`, optional
            Width of each row, by default [1]
        specs : `List[List[dict]]`, optional
            Subplot specs, by default `[[{}] * cols] * rows` (all subplots are the same size)
        """

        fig = make_subplots(
            rows=rows,
            cols=cols,
            shared_xaxes=shared_xaxes,
            vertical_spacing=vertical_spacing,
            horizontal_spacing=horizontal_spacing,
            subplot_titles=subplot_titles,
            row_width=row_width or [1] * rows,
            specs=specs or [[{}] * cols] * rows,
            **kwargs,
        )
        kwargs = {}
        if specs and any(
            spec.get("secondary_y", False) for row in specs for spec in row
        ):
            kwargs["has_secondary_y"] = True

        return cls(fig, is_subplots=True, **kwargs)

    def _set_openbb_overlays(self):
        """Sets the overlays for Command Location and OpenBB Terminal"""
        # pylint: disable=C0415
        from openbb_terminal.helper_funcs import command_location

        if command_location:
            yaxis = self.layout.yaxis
            yaxis2 = self.layout.yaxis2 if hasattr(self.layout, "yaxis2") else None
            xshift = -60 if yaxis.side == "right" else -80

            if yaxis2 and yaxis2.overlaying == "y":
                xshift = -110 if not yaxis2.title.text else -130

            self.add_annotation(
                x=-0.015,
                y=0.5,
                yref="paper",
                xref="paper",
                text=command_location,
                textangle=-90,
                font_size=24,
                font_color="gray",
                opacity=0.5,
                yanchor="middle",
                xanchor="left",
                xshift=xshift,
                showarrow=False,
            )

        self.add_annotation(
            yref="y domain" if not self.is_subplots else "paper",
            xref="x domain",
            x=1,
            y=0,
            text="OpenBB Terminal",
            font_size=17,
            font_color="gray",
            opacity=0.5,
            xanchor="right",
            yanchor="bottom",
            showarrow=False,
            yshift=-80,
            xshift=40,
        )

    def set_title(self, title: str, **kwargs):
        """Set the title of the figure"""
        self.update_layout(title=title, **kwargs)

    def add_hline_legend(
        self,
        y: float,
        name: str,
        line: dict,
        legendrank: int = None,
        **kwargs,
    ):
        """Add a horizontal line with a legend label

        Parameters
        ----------
        y : `float`
            y value of the line
        name : `str`
            Name of the to display in the legend
        line : `dict`
            Line style
        legendrank : `int`, optional
            Legend rank, by default None (e.g. 1 is above 2)
        """
        self.add_hline(
            y,
            line=line,
        )
        self.add_legend_label(
            label=name,
            mode="lines",
            line_dash=line["dash"],
            marker=dict(color=line["color"]),
            legendrank=legendrank,
            **kwargs,
        )

    def add_vline_legend(
        self,
        x: float,
        name: str,
        line: dict,
        legendrank: int = None,
        **kwargs,
    ):
        """Add a vertical line with a legend label

        Parameters
        ----------
        x : `float`
            x value of the line
        name : `str`
            Name of the to display in the legend
        line : `dict`
            Line style
        legendrank : `int`, optional
            Legend rank, by default None (e.g. 1 is above 2)
        """
        self.add_vline(
            x,
            line=line,
        )
        self.add_legend_label(
            label=name,
            mode="lines",
            line_dash=line["dash"],
            marker=dict(color=line["color"]),
            legendrank=legendrank,
            **kwargs,
        )

    def add_legend_label(
        self,
        trace: str = None,
        label: str = None,
        mode: str = None,
        marker: dict = None,
        line_dash: str = None,
        legendrank: int = None,
        **kwargs,
    ):
        """Adds a legend label

        Parameters
        ----------
        trace : `str`, optional
            The name of the trace to use as a template, by default None
        label : `str`, optional
            The label to use, by default None (uses the trace name if trace is specified)
            If trace is not specified, label must be specified
        mode : `str`, optional
            The mode to use, by default "lines" (uses the trace mode if trace is specified)
        marker : `dict`, optional
            The marker to use, by default dict() (uses the trace marker if trace is specified)
        line_dash : `str`, optional
            The line dash to use, by default "solid" (uses the trace line dash if trace is specified)
        legendrank : `int`, optional
            The legend rank, by default None (e.g. 1 is above 2)

        Raises
        ------
        ValueError
            If trace is not found
        ValueError
            If label is not specified and trace is not specified
        """

        if trace:
            for trace_ in self.data:
                if trace_.name == trace:
                    for arg, default in zip(
                        [label, mode, marker, line_dash],
                        [trace, trace_.mode, trace_.marker, trace_.line_dash],
                    ):
                        if not arg and default:
                            arg = default

                    kwargs.update(dict(yaxis=trace_.yaxis))
                    break
            else:
                raise ValueError(f"Trace '{trace}' not found")

        if not label:
            raise ValueError("Label must be specified")

        self.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode=mode or "lines",
                name=label,
                marker=marker or dict(),
                line_dash=line_dash or "solid",
                legendrank=legendrank,
                **kwargs,
            )
        )

    def show(self, *args, **kwargs):
        """Show the figure"""
        self._set_openbb_overlays()
        margin_add = (
            [90, 100, 80, 40, 10] if not self._has_secondary_y else [90, 40, 80, 40, 10]
        )

        # We adjust margins
        if get_backend().isatty:
            for margin, add in zip(
                ["l", "r", "b", "t", "pad"],
                margin_add,
            ):
                if (
                    margin in self.layout.margin
                    and self.layout.margin[margin] is not None
                ):
                    self.layout.margin[margin] += add
                else:
                    self.layout.margin[margin] = add

        if not get_backend().isatty:
            self.layout.margin = dict(l=40, r=40, b=50, t=50, pad=10)

        # Set legend position
        height = 600 if not self.layout.height else self.layout.height
        self.update_layout(
            legend=dict(
                tracegroupgap=height / 4.5,
            )
        )

        # Set modebar style
        if self.layout.template.layout.mapbox.style == "dark":  # type: ignore
            self.update_layout(  # type: ignore
                newshape_line_color="gold",
                modebar=dict(
                    orientation="v",
                    bgcolor="#2A2A2A",
                    color="#FFFFFF",
                    activecolor="#d1030d",
                ),
            )

        # We check if in Terminal Pro to return the JSON
        if strtobool(os.environ.get("TERMINAL_PRO", "False")):
            return self.to_json()

        kwargs.update(config=dict(scrollZoom=True, displaylogo=False))
        return super().show(*args, **kwargs)

    def to_subplot(
        self,
        subplot: go.Figure,
        row: int,
        col: int,
        secondary_y: bool = False,
        **kwargs,
    ):
        """Return the figure as a subplot of another figure

        Parameters
        ----------
        subplot : `plotly.graph_objects.Figure`
            The subplot
        row : `int`
            Row number
        col : `int`
            Column number
        secondary_y : `bool`, optional
            Whether to use the secondary y axis, by default False

        Returns
        -------
        `plotly.graph_objects.Figure`
            The subplot with the figure added
        """
        for trace in self.data:
            trace.legendgroup = f"{row}"
            subplot.add_trace(
                trace, row=row, col=col, secondary_y=secondary_y, **kwargs
            )

        fig_dict = self.to_dict()
        if "layout" in fig_dict:
            if f"xaxis{col}" in fig_dict["layout"]:
                subplot.layout[f"xaxis{col}"] = fig_dict["layout"][f"xaxis{col}"]
            if f"yaxis{row}" in fig_dict["layout"]:
                subplot.layout[f"yaxis{row}"] = fig_dict["layout"][f"yaxis{row}"]

        if not get_backend().isatty:
            subplot.update_layout(
                margin=dict(l=30, r=30, b=50, t=50, pad=0),
            )

        return subplot