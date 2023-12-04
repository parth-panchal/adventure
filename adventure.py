import json
import sys


class TextAdventureGame:
    def __init__(self, map_filename):
        self.load_map(map_filename)
        self.current_room = 0
        self.player_inventory = []
        self.awaiting_direction_decision = False
        self.valid_direction_choices = []
        self.ambiguous_direction_command = ""

    def load_map(self, map_filename):
        with open(map_filename, "r") as file:
            self.game_map = json.load(file)

    def display_room(self):
        room = self.game_map[self.current_room]
        print(f"> {room['name']}\n\n{room['desc']}\n")
        self.display_items(room)
        self.display_exits(room)

    def display_items(self, room):
        items = room.get("items", [])
        if items:
            print("Items:", ", ".join(items), "\n")

    def display_exits(self, room):
        exits = room.get("exits", {})
        if exits:
            # print("Exits:", " ".join(exits.keys()), "\n")
            exits_string = "Exits: " + " ".join(exits.keys())
            trimmed_exits_string = exits_string.strip()
            print(trimmed_exits_string, "\n")

    def display_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")

    def process_input(self, command):
        parts = command.split()
        verb = self.match_verb(parts[0])
        args = parts[1:]  # Arguments are the rest of the command
        if verb == "go":
            self.go(args)
        elif verb == "look":
            self.display_room()
        elif verb == "get":
            self.get(args)
        elif verb == "drop":
            self.drop(args)
        elif verb == "inventory":
            self.display_inventory()
        elif verb == "help":
            self.help()
        elif verb == "quit":
            self.quit_game()
        else:
            all_directions = self.get_all_directions()
            if verb in all_directions:
                self.go([verb])
            else:
                print("Use 'quit' to exit.")

    def go(self, args):
        if not args:
            print("Sorry, you need to 'go' somewhere.")
            return
        direction = " ".join(args).lower()
        if not direction and self.awaiting_direction_decision:
            direction = self.ambiguous_direction_command
        # Check if the direction (full or abbreviated) is valid and get its full form
        full_direction = self.match_direction(direction)
        if full_direction is None:
            return  # Wait for the next input
        elif not full_direction:
            print("Sorry, you need to 'go' somewhere.")
            return
        # Now check if the full direction is locked
        if self.is_exit_locked(full_direction):
            return  # Prevent moving if the exit is locked and the player lacks the required items
        self.move_to_direction(full_direction)

    def is_exit_locked(self, direction):
        """Check if an exit is locked and if the player has the required items to unlock it."""
        room = self.game_map[self.current_room]
        locked_exits = room.get("locked", {})
        if direction in locked_exits:
            required_items = locked_exits[direction]
            # Check if all required items are in the player's inventory
            for item in required_items:
                if item not in self.player_inventory:
                    print(f"You need {item} in your inventory to go {direction}.")
                    return True  # Exit is locked
        return False

    def match_direction(self, direction):
        room = self.game_map[self.current_room]
        exits = room.get("exits", {})
        if (
            direction in self.compound_directions()
            and self.compound_directions()[direction] in exits
        ):
            return self.compound_directions()[direction]
        if direction in exits:
            return direction
        matches = [exit for exit in exits if exit.startswith(direction)]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print(f"Did you want to go {' or '.join(matches)}?")
            return None
        print(f"There's no way to go {direction}.")
        return None

    def resolve_ambiguous_direction(self, direction):
        if direction in self.valid_direction_choices:
            self.move_to_direction(direction)
        else:
            print(
                f"Invalid direction. Please choose from {' or '.join(self.valid_direction_choices)}."
            )
        self.awaiting_direction_decision = False
        self.valid_direction_choices = []

    def move_to_direction(self, direction):
        room = self.game_map[self.current_room]
        exits = room.get("exits", {})
        if direction in exits:
            destination = exits[direction]
            self.current_room = destination
            print(f"You go {direction}.\n")
            self.display_room()
            # Check for win/lose condition in the new room
            self.check_win_condition(destination)
        else:
            print(f"There's no way to go {direction}.")

    def check_win_condition(self, room_id):
        room = self.game_map[room_id]
        if "winning_items" in room:
            if all(item in self.player_inventory for item in room["winning_items"]):
                print("Congratulations! You've won the game!")
                sys.exit(0)  # Exit the game on winning
            else:
                print(
                    "You've entered the boss room but lack the necessary items. You lose!"
                )
                sys.exit(0)

    def get(self, args):
        if not args:
            print("Sorry, you need to 'get' something.")
            return
        item_name_query = " ".join(args).lower()
        room = self.game_map[self.current_room]
        items = room.get("items", [])
        matches = [item for item in items if item_name_query in item.lower()]
        if len(matches) > 1:
            print(f"Did you want to get {' or '.join(matches)}?")
        elif len(matches) == 1:
            item_name = matches[0]
            items.remove(item_name)
            self.player_inventory.append(item_name)
            print(f"You pick up the {item_name}.")
        else:
            print(f"There's no {item_name_query} anywhere.")

    def get_all_directions(self):
        """Get all possible directions including abbreviations."""
        all_directions = set()
        for room in self.game_map:
            for exit in room.get("exits", {}):
                all_directions.add(exit)
                # Add abbreviation for each direction
                all_directions.update(self.get_direction_abbreviations(exit))
        return all_directions

    def get_direction_abbreviations(self, direction):
        abbreviations = {direction[0]}  # First letter for simple directions
        if direction in self.compound_directions():
            abbreviations.add(self.compound_directions()[direction])
        return abbreviations

    def drop(self, args):
        item_name = " ".join(args).lower()
        if not item_name:
            print("Sorry, you need to 'drop' something.")
        elif item_name in self.player_inventory:
            room = self.game_map[self.current_room]
            if "items" not in room:
                room["items"] = []
            items_in_room = room.get("items", [])
            items_in_room.append(item_name)
            self.player_inventory.remove(item_name)
            print(f"\nYou drop the {item_name}.\n")
            self.display_room()
        else:
            print(f"You're not carrying a {item_name}.")

    def display_inventory(self):
        if not self.player_inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.player_inventory:
                print(f"  {item}")

    def help(self):
        print("You can run the following commands:")
        print("  go ...")
        print("  get ...")
        print("  look")
        print("  inventory")
        print("  quit")
        print("  help")

    def quit_game(self):
        print("Goodbye!")
        sys.exit(0)

    def match_verb(self, verb):
        verb_abbreviations = {
            "get": ["ge", "g"],
            "drop": ["dr", "d"],
            "look": ["lo", "l"],
            "inventory": ["in", "i", "inv"],
            "help": ["he", "h"],
            "quit": ["qu", "q"],
            # Add more abbreviations as needed
        }
        for full_verb, abbreviations in verb_abbreviations.items():
            if verb == full_verb or verb in abbreviations:
                return full_verb
        # Return verb as is for directions and unrecognized commands
        return verb

    def match_direction(self, direction):
        room = self.game_map[self.current_room]
        exits = room.get("exits", {})
        # Handle standard abbreviations for compound directions
        compound_directions = self.compound_directions()
        if direction in compound_directions and compound_directions[direction] in exits:
            return compound_directions[direction]
        if direction in exits:
            return direction
        matches = [exit for exit in exits if exit.startswith(direction)]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print(f"Did you want to go {' or '.join(matches)}?")
            return None
        print(f"There's no way to go {direction}.")
        return None

    def match_item(self, item_name):
        room = self.game_map[self.current_room]
        items = room.get("items", [])
        matches = [item for item in items if item_name in item]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print(f"Did you want to get {' or '.join(matches)}?")
            return None
        return item_name

    @staticmethod
    def compound_directions():
        return {
            "nw": "northwest",
            "ne": "northeast",
            "sw": "southwest",
            "se": "southeast",
        }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)
    
    map_filename = sys.argv[1]
    game = TextAdventureGame(map_filename)
    game.display_room()
    
    while True:
        try:
            command = input("What would you like to do? ").lower()
            if command == "quit":
                game.quit_game()
            else:
                game.process_input(command)
        except EOFError:
            print("\nUse 'quit' to exit.")  # Handle Ctrl-D without exiting
        except KeyboardInterrupt:
            print("\n...")
            print("KeyboardInterrupt")
            sys.exit(0)


if __name__ == "__main__":
    main()
