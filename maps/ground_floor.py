import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots(figsize=(12, 8))

# Location coordinates
locations = {
    "Library Entrance": (5, 4),
    "Library Hall 2 Entrance": (2, 4),
    "Library Hall 2 Centre": (2, 5.5),
    "Study Hall 2 Entrance": (8, 4),
    "Study Hall 2 Centre": (8, 5.5),
    "Staircase": (5, 0.5)
}

# Draw room boundaries
ax.add_patch(Rectangle((0.5, 4.5), 3, 2, fill=False, linewidth=2))
ax.add_patch(Rectangle((6.5, 4.5), 3, 2, fill=False, linewidth=2))

# Draw corridor connections
ax.plot([2, 5, 8], [4, 4, 4], linewidth=4, alpha=0.25)
ax.plot([5, 5], [4, 0.5], linewidth=4, alpha=0.25)

# Connections to room centres
ax.plot([2, 2], [4, 5.5], linestyle="--")
ax.plot([8, 8], [4, 5.5], linestyle="--")

# Highlight recommended route
ax.plot(
    [5, 5],
    [4, 0.5],
    color="red",
    linewidth=5,
    marker="o",
    markersize=9,
    label="Recommended Route",
    zorder=5
)

# Plot location markers
for name, (x, y) in locations.items():
    ax.scatter(x, y, s=100, zorder=6)
    ax.text(x, y + 0.25, name, ha="center", fontsize=9)

# Room labels
ax.text(2, 6.8, "LIBRARY HALL 2", ha="center", fontsize=11)
ax.text(8, 6.8, "STUDY HALL 2", ha="center", fontsize=11)
ax.text(5, 3.5, "LIBRARY JUNCTION", ha="center", fontsize=9)

# Map settings
ax.set_title("Ground Floor - Indoor Navigation Map")
ax.set_xlabel("Schematic X Position")
ax.set_ylabel("Schematic Y Position")
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.set_aspect("equal")
ax.grid(True, alpha=0.2)
ax.legend()

plt.tight_layout()
plt.savefig("maps/ground_floor_map.png", dpi=300)
plt.show()