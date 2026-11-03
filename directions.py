def generate_instructions(route):

    if not route:
        return []

    if len(route) == 1:
        return ["You are already at your destination!"]

    directions = []

    # Starting point
    directions.append(f"Start at {route[0]}.")

    # Instructions for each route connection
    movement_instructions = {

        # Ground Floor
        (
            "Ground Floor Library Entrance",
            "Ground Floor Study Hall 2 Entrance"
        ): "Follow the Ground Floor corridor towards Study Hall 2.",

        (
            "Ground Floor Study Hall 2 Entrance",
            "Ground Floor Library Entrance"
        ): "Follow the corridor back towards the Library Entrance.",

        (
            "Ground Floor Library Entrance",
            "Ground Floor Library Hall 2 Entrance"
        ): "Follow the corridor towards Library Hall 2.",

        (
            "Ground Floor Library Hall 2 Entrance",
            "Ground Floor Library Entrance"
        ): "Follow the corridor back towards the Library Entrance.",

        (
            "Ground Floor Library Entrance",
            "Ground Floor Staircase Entrance"
        ): "Walk from the Library Entrance towards the Ground Floor staircase.",

        (
            "Ground Floor Staircase Entrance",
            "Ground Floor Library Entrance"
        ): "Walk from the staircase towards the Library Entrance.",

        (
            "Ground Floor Study Hall 2 Entrance",
            "Ground Floor Study Hall Centre"
        ): "Enter Study Hall 2 and proceed towards its centre.",

        (
            "Ground Floor Study Hall Centre",
            "Ground Floor Study Hall 2 Entrance"
        ): "Walk from the centre towards the Study Hall 2 entrance.",

        (
            "Ground Floor Library Hall 2 Entrance",
            "Ground Floor Library Hall 2 Centre"
        ): "Enter Library Hall 2 and proceed towards its centre.",

        (
            "Ground Floor Library Hall 2 Centre",
            "Ground Floor Library Hall 2 Entrance"
        ): "Walk from the centre towards the Library Hall 2 entrance.",

        # Staircase between floors
        (
            "Ground Floor Staircase Entrance",
            "First Floor Staircase Landing"
        ): "Take the stairs up to the First Floor Staircase Landing.",

        (
            "First Floor Staircase Landing",
            "Ground Floor Staircase Entrance"
        ): "Take the stairs down to the Ground Floor Staircase Entrance.",

        # First Floor
        (
            "First Floor Staircase Landing",
            "First Floor Computer Centre Entrance"
        ): "Follow the First Floor corridor towards the Computer Centre Entrance.",

        (
            "First Floor Computer Centre Entrance",
            "First Floor Staircase Landing"
        ): "Follow the corridor towards the First Floor staircase.",

        (
            "First Floor Computer Centre Entrance",
            "First Floor Corridor Outside Lab 2"
        ): "Follow the corridor towards the area outside Computer Lab 2.",

        (
            "First Floor Corridor Outside Lab 2",
            "First Floor Computer Centre Entrance"
        ): "Follow the corridor towards the Computer Centre Entrance.",

        (
            "First Floor Corridor Outside Lab 2",
            "First Floor Computer Lab 2"
        ): "Continue along the corridor and reach Computer Lab 2.",

        (
            "First Floor Computer Lab 2",
            "First Floor Corridor Outside Lab 2"
        ): "Exit Computer Lab 2 and follow the corridor towards its outside passage.",

        (
            "First Floor Corridor Outside Lab 2",
            "First Floor Ojah Ma'am's Cabin"
        ): "Follow the passage towards Ojah Ma'am's Cabin.",

        (
            "First Floor Ojah Ma'am's Cabin",
            "First Floor Corridor Outside Lab 2"
        ): "Exit Ojah Ma'am's Cabin and return to the corridor."
    }

    # Generate instructions from the calculated route
    for current, next_location in zip(route, route[1:]):

        instruction = movement_instructions.get(
            (current, next_location),
            f"Continue from {current} towards {next_location}."
        )

        directions.append(instruction)

    # Destination reached
    directions.append(
        f"You have reached your destination: {route[-1]}!"
    )

    return directions