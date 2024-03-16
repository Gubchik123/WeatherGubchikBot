import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

from constants import TEXT


def get_generated_temp_graph_image_path(
    max_temps: list[int], min_temps: list[int]
) -> str:
    """Returns the path to the image with the generated temperature graph."""
    figure = plt.figure()
    ax = figure.add_subplot(1, 1, 1)

    x_new = np.linspace(0, len(max_temps) - 1, 300)

    plot_smooth_line(ax, x_new, max_temps, "blue", TEXT().night_label())
    plot_points(ax, max_temps, "blue")
    annotate_points(ax, max_temps)

    plot_smooth_line(ax, x_new, min_temps, "red", TEXT().day_label())
    plot_points(ax, min_temps, "red")
    annotate_points(ax, min_temps)

    remove_axes(ax)
    remove_border_lines(ax)

    ax.legend()
    image_path = "weather_temperature_graph.png"
    plt.savefig(image_path, bbox_inches="tight")
    return image_path


def plot_smooth_line(
    ax: plt.Axes, x_new, temps: list[int], color: str, label: str
) -> None:
    """Plots a smooth line on the graph."""
    spl: BSpline = make_interp_spline(range(len(temps)), temps, k=3)
    power_smooth = spl(x_new)
    ax.plot(x_new, power_smooth, "-", color=color, label=label)


def plot_points(ax: plt.Axes, temps: list[int], color: str) -> None:
    """Plots points on the graph."""
    ax.plot(range(len(temps)), temps, "o", color=color)


def annotate_points(ax: plt.Axes, temps: list[int]) -> None:
    """Annotates points on the graph."""
    for i, txt in enumerate(temps):
        ax.annotate(
            txt,
            (range(len(temps))[i], temps[i]),
            xytext=(3, 3),
            textcoords="offset points",
        )


def remove_axes(ax: plt.Axes) -> None:
    """Removes axes from the graph."""
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


def remove_border_lines(ax: plt.Axes) -> None:
    """Removes border lines from the graph."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
