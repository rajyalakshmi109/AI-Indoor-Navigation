import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import textwrap


# ==================================================
# COMMON MAP FUNCTIONS
# ==================================================

def add_location_marker(ax, name, position, route):
    """Display location markers with START and DESTINATION labels."""

    x, y = position

    if route and name == route[0]:
        color = "green"
        marker = "o"
        label = "START"

    elif route and name == route[-1]:
        color = "red"
        marker = "*"
        label = "DESTINATION"

    elif name in route:
        color = "orange"
        marker = "o"
        label = None

    else:
        color = "#2563eb"
        marker = "o"
        label = None

    ax.scatter(
        x,
        y,
        s=190 if label else 110,
        color=color,
        marker=marker,
        edgecolors="white",
        linewidths=1.5,
        zorder=8
    )

    if label:
        ax.annotate(
            label,
            (x, y),
            xytext=(0, 20),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            fontweight="bold",
            color=color,
            zorder=10
        )


def draw_route(ax, points):
    """Highlight the selected route with direction arrows."""

    if len(points) < 2:
        return

    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    ax.plot(
        x_values,
        y_values,
        color="#ef4444",
        linewidth=5,
        solid_capstyle="round",
        label="Selected Route",
        zorder=6
    )

    for start, end in zip(points, points[1:]):
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={
                "arrowstyle": "->",
                "color": "#7f1d1d",
                "linewidth": 2,
                "mutation_scale": 18
            },
            zorder=7
        )


def style_map(ax, title, xlim, ylim):
    """Apply common styling to both floor maps."""

    ax.set_title(
        title,
        fontsize=18,
        fontweight="bold",
        pad=20
    )

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_facecolor("#f8fafc")

    ax.grid(
        True,
        linestyle="--",
        alpha=0.2
    )

    ax.set_xlabel("Building Layout - Schematic View")
    ax.set_ylabel("")


def add_location_labels(ax, locations, floor_name):
    """Display readable location names."""

    for name, (x, y) in locations.items():

        short_name = name.replace(
            floor_name,
            ""
        )

        ax.text(
            x,
            y + 0.25,
            "\n".join(textwrap.wrap(short_name, 22)),
            ha="center",
            fontsize=8,
            fontweight="medium",
            zorder=9
        )


# ==================================================
# GROUND FLOOR MAP
# ==================================================

def draw_ground_floor(route):

    fig, ax = plt.subplots(figsize=(12, 8))

    # ----------------------------------------------
    # LOCATION COORDINATES
    # ----------------------------------------------

    locations = {

        "Ground Floor Library Entrance": (5, 4),

        "Ground Floor Library Hall 2 Entrance": (2, 4),

        "Ground Floor Library Hall 2 Centre": (2, 5.5),

        "Ground Floor Study Hall 2 Entrance": (8, 4),

        "Ground Floor Study Hall Centre": (8, 5.5),

        "Ground Floor Staircase Entrance": (5, 0.5)
    }

    # ----------------------------------------------
    # DRAW LIBRARY HALL
    # ----------------------------------------------

    ax.add_patch(
        Rectangle(
            (0.5, 4.5),
            3,
            2,
            facecolor="#dbeafe",
            edgecolor="#2563eb",
            linewidth=2,
            alpha=0.65
        )
    )

    # ----------------------------------------------
    # DRAW STUDY HALL
    # ----------------------------------------------

    ax.add_patch(
        Rectangle(
            (6.5, 4.5),
            3,
            2,
            facecolor="#dcfce7",
            edgecolor="#16a34a",
            linewidth=2,
            alpha=0.65
        )
    )

    # ROOM LABELS

    ax.text(
        2,
        6.8,
        "LIBRARY HALL 2",
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

    ax.text(
        8,
        6.8,
        "STUDY HALL 2",
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

    # ----------------------------------------------
    # DRAW WALKING CORRIDORS
    # ----------------------------------------------

    corridor_style = {
        "color": "#94a3b8",
        "linewidth": 9,
        "alpha": 0.5,
        "solid_capstyle": "round",
        "zorder": 1
    }

    # Main corridor

    ax.plot(
        [2, 5, 8],
        [4, 4, 4],
        label="Walking Corridor",
        **corridor_style
    )

    # Staircase corridor

    ax.plot(
        [5, 5],
        [4, 0.5],
        **corridor_style
    )

    # Library internal connection

    ax.plot(
        [2, 2],
        [4, 5.5],
        color="#94a3b8",
        linewidth=4,
        linestyle="--",
        zorder=2
    )

    # Study hall internal connection

    ax.plot(
        [8, 8],
        [4, 5.5],
        color="#94a3b8",
        linewidth=4,
        linestyle="--",
        zorder=2
    )

    ax.text(
        5,
        3.5,
        "LIBRARY JUNCTION",
        ha="center",
        fontsize=9,
        fontweight="bold"
    )

    # ----------------------------------------------
    # SELECTED ROUTE
    # ----------------------------------------------

    floor_route = [
        name for name in route
        if name in locations
    ]

    points = [
        locations[name]
        for name in floor_route
    ]

    draw_route(ax, points)

    # ----------------------------------------------
    # LOCATION MARKERS
    # ----------------------------------------------

    for name, position in locations.items():

        add_location_marker(
            ax,
            name,
            position,
            route
        )

    add_location_labels(
        ax,
        locations,
        "Ground Floor "
    )

    # ----------------------------------------------
    # STAIRCASE
    # ----------------------------------------------

    ax.text(
        5,
        0.05,
        "STAIRCASE",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

    # ----------------------------------------------
    # MAP SETTINGS
    # ----------------------------------------------

    style_map(
        ax,
        "GROUND FLOOR - INDOOR NAVIGATION",
        (0, 10),
        (0, 8)
    )

    ax.legend(
        loc="upper right",
        framealpha=0.95
    )

    fig.tight_layout()

    return fig


# ==================================================
# FIRST FLOOR MAP
# ==================================================

def draw_first_floor(route):

    fig, ax = plt.subplots(figsize=(12, 8))

    # ----------------------------------------------
    # LOCATION COORDINATES
    # ----------------------------------------------

    locations = {

        "First Floor Staircase Landing": (9, 1),

        "First Floor Computer Centre Entrance": (9, 7),

        "First Floor Computer Lab 2": (2, 7),

        "First Floor Corridor Outside Lab 2": (4, 5),

        "First Floor Ojah Ma'am's Cabin": (4, 3)
    }

    # ----------------------------------------------
    # COMPUTER LAB 2
    # ----------------------------------------------

    ax.add_patch(
        Rectangle(
            (0.8, 6),
            2.8,
            2,
            facecolor="#dbeafe",
            edgecolor="#2563eb",
            linewidth=2,
            alpha=0.65
        )
    )

    # ----------------------------------------------
    # OJAH MA'AM'S CABIN
    # ----------------------------------------------

    ax.add_patch(
        Rectangle(
            (3.5, 2.3),
            2,
            1.8,
            facecolor="#fef3c7",
            edgecolor="#d97706",
            linewidth=2,
            alpha=0.65
        )
    )

    # ROOM LABELS

    ax.text(
        2.2,
        8.2,
        "COMPUTER LAB 2",
        ha="center",
        fontsize=11,
        fontweight="bold"
    )

    ax.text(
        4.5,
        2.7,
        "OJAH MA'AM'S CABIN",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

    # ----------------------------------------------
    # WALKING CORRIDORS
    # ----------------------------------------------

    corridor_style = {
        "color": "#94a3b8",
        "linewidth": 9,
        "alpha": 0.5,
        "solid_capstyle": "round",
        "zorder": 1
    }

    ax.plot(
        [9, 9, 7, 4, 4],
        [1, 7, 7, 7, 5],
        label="Walking Corridor",
        **corridor_style
    )

    # Cabin corridor

    ax.plot(
        [4, 4],
        [5, 3.2],
        **corridor_style
    )

    # Lab corridor connection

    ax.plot(
        [4, 2.2],
        [7, 7],
        color="#94a3b8",
        linewidth=4,
        linestyle="--",
        zorder=2
    )

    # ----------------------------------------------
    # ROUTE CONNECTIONS
    # ----------------------------------------------

    corridor_paths = {

        (
            "First Floor Computer Lab 2",
            "First Floor Corridor Outside Lab 2"
        ): [
            (2, 7),
            (4, 7),
            (4, 5)
        ],

        (
            "First Floor Corridor Outside Lab 2",
            "First Floor Computer Lab 2"
        ): [
            (4, 5),
            (4, 7),
            (2, 7)
        ],

        (
            "First Floor Corridor Outside Lab 2",
            "First Floor Computer Centre Entrance"
        ): [
            (4, 5),
            (4, 7),
            (9, 7)
        ],

        (
            "First Floor Computer Centre Entrance",
            "First Floor Corridor Outside Lab 2"
        ): [
            (9, 7),
            (4, 7),
            (4, 5)
        ],

        (
            "First Floor Corridor Outside Lab 2",
            "First Floor Ojah Ma'am's Cabin"
        ): [
            (4, 5),
            (4, 3)
        ],

        (
            "First Floor Ojah Ma'am's Cabin",
            "First Floor Corridor Outside Lab 2"
        ): [
            (4, 3),
            (4, 5)
        ]
    }

    # ----------------------------------------------
    # BUILD SELECTED ROUTE
    # ----------------------------------------------

    floor_route = [
        name for name in route
        if name in locations
    ]

    points = []

    if floor_route:

        points.append(
            locations[floor_route[0]]
        )

        for current, next_location in zip(
            floor_route,
            floor_route[1:]
        ):

            segment = corridor_paths.get(
                (current, next_location),
                [
                    locations[current],
                    locations[next_location]
                ]
            )

            points.extend(segment[1:])

    draw_route(ax, points)

    # ----------------------------------------------
    # LOCATION MARKERS
    # ----------------------------------------------

    for name, position in locations.items():

        add_location_marker(
            ax,
            name,
            position,
            route
        )

    add_location_labels(
        ax,
        locations,
        "First Floor "
    )

    # ----------------------------------------------
    # STAIRCASE
    # ----------------------------------------------

    ax.text(
        9,
        0.35,
        "STAIRCASE",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

    # ----------------------------------------------
    # MAP SETTINGS
    # ----------------------------------------------

    style_map(
        ax,
        "FIRST FLOOR - INDOOR NAVIGATION",
        (0, 11),
        (0, 9)
    )

    ax.legend(
        loc="upper right",
        framealpha=0.95
    )

    fig.tight_layout()

    return fig