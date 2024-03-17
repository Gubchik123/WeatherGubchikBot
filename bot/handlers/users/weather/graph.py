from typing import Dict, List

import numpy as np
import matplotlib.pyplot as plt

from constants import TEXT


def get_generated_temp_graph_image_path(
    max_temps: Dict[str, int], min_temps: Dict[str, int]
) -> str:
    """Returns the path to the image with the generated temperature graph."""
    figure = plt.figure()
    ax = figure.add_subplot(1, 1, 1)

    plot_lines_with_points(
        ax, max_temps.values(), "blue", TEXT().night_label()
    )
    annotate_points(ax, list(max_temps.values()))

    plot_lines_with_points(ax, min_temps.values(), "red", TEXT().day_label())
    annotate_points(ax, list(min_temps.values()))

    ax.get_yaxis().set_visible(False)
    plt.xticks(
        np.arange(len(max_temps)),
        max_temps.keys(),
        rotation=45 if len(max_temps) == 7 else 90,
    )
    remove_border_lines(ax)

    ax.legend()
    image_path = "weather_temperature_graph.png"
    plt.savefig(image_path, bbox_inches="tight")
    return image_path


def plot_lines_with_points(
    ax: plt.Axes, temps: List[int], color: str, label: str
) -> None:
    """Plots lines with points on the graph."""
    ax.plot(temps, "-o", color=color, label=label)


def annotate_points(ax: plt.Axes, temps: List[int]) -> None:
    """Annotates points on the graph."""
    for index, num in enumerate(temps):
        symbol = "+" if num > 0 else ""
        ax.annotate(
            f"{symbol}{num}°",
            (range(len(temps))[index], temps[index]),
            xytext=(3, 3),
            textcoords="offset points",
        )


def remove_border_lines(ax: plt.Axes) -> None:
    """Removes border lines from the graph."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
