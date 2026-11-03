
import networkx as nx
import os



building = nx.Graph()


locations = [
    "Ground Floor Library Entrance",
    "Ground Floor Study Hall 2 Entrance",
    "Ground Floor Library Hall 2 Entrance",
    "Ground Floor Staircase Entrance",
    "Ground Floor Study Hall Centre",
    "Ground Floor Library Hall 2 Centre",

    "First Floor Staircase Landing",
    "First Floor Computer Centre Entrance",
    "First Floor Computer Lab 2",
    "First Floor Corridor Outside Lab 2",
    "First Floor Ojah Ma'am's Cabin"
]

building.add_nodes_from(locations)




building.add_weighted_edges_from([

   
    (
        "Ground Floor Library Entrance",
        "Ground Floor Study Hall 2 Entrance",
        5
    ),

    (
        "Ground Floor Library Entrance",
        "Ground Floor Library Hall 2 Entrance",
        5
    ),

    (
        "Ground Floor Library Entrance",
        "Ground Floor Staircase Entrance",
        10
    ),

    (
        "Ground Floor Study Hall 2 Entrance",
        "Ground Floor Study Hall Centre",
        4
    ),

    (
        "Ground Floor Library Hall 2 Entrance",
        "Ground Floor Library Hall 2 Centre",
        4
    ),

   
    (
        "Ground Floor Staircase Entrance",
        "First Floor Staircase Landing",
        8
    ),

    
    (
        "First Floor Staircase Landing",
        "First Floor Computer Centre Entrance",
        4
    ),

    (
        "First Floor Computer Centre Entrance",
        "First Floor Corridor Outside Lab 2",
        5
    ),

    (
        "First Floor Corridor Outside Lab 2",
        "First Floor Ojah Ma'am's Cabin",
        7
    ),

   
    (
        "First Floor Corridor Outside Lab 2",
        "First Floor Computer Lab 2",
        4
    )
])




def find_shortest_route(start, destination):

    if start not in building:
        return None, None

    if destination not in building:
        return None, None

    try:

        route = nx.shortest_path(
            building,
            source=start,
            target=destination,
            weight="weight",
            method="dijkstra"
        )

        distance = nx.shortest_path_length(
            building,
            source=start,
            target=destination,
            weight="weight",
            method="dijkstra"
        )

        return route, distance

    except nx.NetworkXNoPath:

        return None, None




def get_maps_for_route(route):

    maps_to_display = []

    if not route:
        return maps_to_display

    ground_floor_map = "maps/ground_floor_map.png"
    first_floor_map = "maps/first_floor_map.png"

    if any(location.startswith("Ground Floor") for location in route):
        maps_to_display.append(ground_floor_map)

    if any(location.startswith("First Floor") for location in route):
        maps_to_display.append(first_floor_map)

    return maps_to_display




def display_navigation(start, destination):

    route, distance = find_shortest_route(
        start,
        destination
    )

    print("\n================================")
    print("       INDOOR NAVIGATION")
    print("================================")

    print("Starting location:", start)
    print("Destination:", destination)

    if route:

        print("\nRecommended route:")

        for i, location in enumerate(route, start=1):
            print(f"{i}. {location}")

        print("\nApproximate route distance:", distance, "metres")

        maps = get_maps_for_route(route)

        print("\nMaps required:")

        for map_file in maps:

            if os.path.exists(map_file):
                print("Available:", map_file)

            else:
                print("Map not found:", map_file)

        return route, distance, maps

    else:

        print("\nNo route available between these locations.")

        return None, None, []




if __name__ == "__main__":

    start = "Ground Floor Library Entrance"

    destination = "First Floor Ojah Ma'am's Cabin"

    display_navigation(start, destination)

