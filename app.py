from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define a simple map of the game with rooms and items
game_map = {
    "living room": {
        "description": "You are in a cozy living room. There is a door to the north.",
        "items": ["key"],
        "directions": {"north": "kitchen"}
    },
    "kitchen": {
        "description": "You are in a small kitchen. There is a door to the south.",
        "items": [],
        "directions": {"south": "living room", "east": "garden"}
    },
    "garden": {
        "description": "You are in a beautiful garden. There is a door to the west.",
        "items": ["flower"],
        "directions": {"west": "kitchen"}
    }
}

# Initialize game state
game_state = {
    "location": "living room",
    "inventory": []
}

def move_player(direction):
    """Move player to a different room if possible."""
    current_location = game_state["location"]
    if direction in game_map[current_location]["directions"]:
        game_state["location"] = game_map[current_location]["directions"][direction]
        return f"You move to the {game_state['location']}."
    else:
        return "You can't go that way!"

def pick_item(item):
    """Pick up an item if it exists in the room."""
    current_location = game_state["location"]
    if item in game_map[current_location]["items"]:
        game_map[current_location]["items"].remove(item)
        game_state["inventory"].append(item)
        return f"You picked up a {item}."
    else:
        return f"There is no {item} here."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    user_input = request.json.get("command").lower()
    response = "Invalid command."

    if user_input.startswith("go "):
        direction = user_input.split(" ")[1]
        response = move_player(direction)
    elif user_input.startswith("pick up "):
        item = user_input.split("pick up ")[1]
        response = pick_item(item)
    elif user_input == "look":
        current_location = game_state["location"]
        response = game_map[current_location]["description"]
        if game_map[current_location]["items"]:
            response += f" You see: {', '.join(game_map[current_location]['items'])}."
    elif user_input == "inventory":
        if game_state["inventory"]:
            response = f"You have: {', '.join(game_state['inventory'])}."
        else:
            response = "Your inventory is empty."
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
