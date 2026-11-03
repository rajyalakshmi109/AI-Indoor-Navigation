import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots(figsize=(12, 9))

# Locations based on your building layout
locations = {
    "First Floor Staircase Landing": (9, 1),
    "Computer Centre Entrance": (9, 7),
    "Computer Lab 2": (2, 7),
    "Ojah Ma'am's Cabin": (4, 3),
    "Corridor Outside Lab 2": (4, 5)
}

# Draw Computer Lab 2
ax.add_patch(
    Rectangle((0.8, 6), 2.8, 2,
              fill=False, linewidth=2)
)

# Draw Ojah Ma'am's Cabin
ax.add_patch(
    Rectangle((3.5, 2.3), 2, 1.8,
              fill=False, linewidth=2)
)

# Draw walking corridor
corridor_x = [9, 9, 7, 4, 4]
corridor_y = [1, 7, 7, 7, 5]

ax.plot(
    corridor_x, corridor_y,
    linewidth=5, alpha=0.25,
    label="Walking corridor"
)

# Corridor connection to cabin
ax.plot([4, 4], [5, 3.2],
        linewidth=3, alpha=0.25)

# Corridor connection to Computer Lab 2
ax.plot([4, 2.2], [7, 7],
        linestyle="--", linewidth=2)

# Highlight recommended route
route_x = [9, 9, 7, 4, 4]
route_y = [1, 7, 7, 7, 5]

ax.plot(
    route_x, route_y,
    color="red",
    linewidth=5,
    marker="o",
    markersize=9,
    label="Recommended Route",
    zorder=5
)

# Highlight final connection to cabin
ax.plot(
    [4, 4], [5, 3.2],
    color="red",
    linewidth=5,
    marker="o",
    markersize=8,
    zorder=5
)

# Plot location markers
for name, (x, y) in locations.items():
    ax.scatter(x, y, s=110, zorder=6)
    ax.text(x, y + 0.3, name,
            ha="center", fontsize=9)

# Room labels
ax.text(2.2, 8.2, "COMPUTER LAB 2",
        ha="center", fontsize=11)

ax.text(4.5, 2.7, "OJAH MA'AM'S CABIN",
        ha="center", fontsize=10)

# Map settings
ax.set_title("First Floor - Indoor Navigation Map")
ax.set_xlabel("Schematic X Position")
ax.set_ylabel("Schematic Y Position")
ax.set_xlim(0, 11)
ax.set_ylim(0, 9)
ax.set_aspect("equal")
ax.grid(True, alpha=0.2)
ax.legend()

plt.tight_layout()
plt.savefig("maps/first_floor_map.png", dpi=300)
plt.show()