import json
import sys


class TextAdventureGame:
    def __init__(self, map_filename):
        self.load_map(map_filename)
        self.current_room = 0
        self.player_inventory = []

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
            print("Items:", ", ".join(items))
            print("\n")

    def display_exits(self, room):
        exits = room.get("exits", {})
        if exits:
            print("Exits:", " ".join(exits.keys()))
        print("\n")

    def display_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")

    def process_input(self, command):
        verb, *args = command.split()
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
            print("Invalid command. Type 'help' for a list of valid commands.")

    def go(self, args):
        direction = " ".join(args).lower()
        room = self.game_map[self.current_room]
        exits = room.get("exits", {})
        if not direction:
            print("Sorry, you need to 'go' somewhere.")
        elif direction in exits:
            destination = exits[direction]
            self.current_room = destination
            print(f"You go {direction}.")
            self.display_room()
        else:
            print(f"There's no way to go {direction}.")

    def get(self, args):
        room = self.game_map[self.current_room]
        item_name = " ".join(args).lower()
        items = room.get("items", [])
        if not item_name:
            print("Sorry, you need to 'get' something.")
        elif item_name in items:
            items.remove(item_name)
            self.player_inventory.append(item_name)
            print(f"You pick up the {item_name}.")
        else:
            print(f"There's no {item_name} anywhere.")

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
            print("Use 'quit' to exit.")
        except KeyboardInterrupt:
            game.quit_game()


if __name__ == "__main__":
    main()
