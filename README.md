# Adventure

## Group Project
### Parth Panchal
ppanchal@stevens.edu
### Nancy Radadia 
nradadia@stevens.edu

## URL: 
https://github.com/parth-panchal/adventure

## Time Spent 
An estimate of 36 hours each were spent on this project.

## Description

Welcome to our Text Adventure Game, a classic text-based exploration game. In this game, you navigate through various rooms, interact with objects, solve puzzles, and overcome challenges. The game is played entirely through text commands in a console or terminal.


## Installation

Clone the repository to your local machine:

```zsh
git clone https://github.com/parth-panchal/adventure
```

## GamePlay Instructions

1. Starting the Game:
   * Run the game using python adventure.py [map filename].
    ```zsh
        python adventure.py loop.map
    ```
   * The game initializes in the starting room, as defined in the map file.
2. Navigating Rooms:
   * Use direction commands to move between rooms.
   * Example: north, n, east, e, etc.
3. Interacting with Items:
   * get [item] to pick up items.
   * drop [item] to leave items in the current room.
   * Use partial names for items when unambiguous.
4. Managing Inventory:
   * View current items using inventory or i.
5. General Commands:
   * look to describe the current room again.
   * help for a list of commands.
   * quit to exit the game.
6. Winning the Game:
   * Fulfill the winning conditions to complete the game.
   
## Map Configuration
The game's world is defined in a JSON file.
Each room in the file is a JSON object with attributes like name, desc, exits and items
Additional attributes locked, and winning_items are included to support the extentions implemented.

*Note: The Provided map in the repository covers all additional attributes and can be used to test our implemented extentions.*

## Extentions Implemented

### 1. Abbreviations for Directions, Verbs, and Items

#### Usage
   * Directions:

      * Shortened forms of cardinal and intercardinal directions are recognized by the game.

      * Example: Use n for north, se for southeast, etc.
      * Benefit: Saves time and enhances the ease of gameplay.

   * Verbs:
      * Common game actions have abbreviated versions.
      * Example: g or ge for get, i or inv for inventory, d or dr for drop.
      * Benefit: Provides quick and efficient command input.
  
   * Items:
      * Items can be referenced by partial names if unique in the context.
      * Example: get lan could be used to pick up a lantern.
      * Benefit: Simplifies interaction with objects, especially those with longer names.

#### Implementation

* Directions: Recognizes first letter or two-letter combinations for compound directions.
* Verbs: Maps short forms to standard verbs (g for get, i for inventory, etc.).
* Items: Allows partial name matching for unique items in the current room context.

#### Testing
* Input abbreviated commands and observe if they execute the intended action.
* Try partial item names and verify if they are correctly recognized.

### 2. Directions as Verbs

#### Usage
* Players can input directions as commands without the need for the go prefix.
* Example: Typing east or e is equivalent to go east.
* Benefit: Streamlines navigation, making movement commands more intuitive and direct.
  
#### Implementation
* Accepts direction names (north, east, etc.) or their abbreviations (n, e, etc.) as standalone commands equivalent to go [direction].
* 
#### Testing
* Directly input direction commands without the go prefix and check if the movement is correctly executed.

### 3. Drop

#### Usage
* Allows players to remove items from their inventory and leave them in the current room.
* Usage: drop [item name], e.g., drop key.
* Benefit: Enables strategic management of inventory and interaction with the game environment.

#### Implementation

* Adds functionality to remove items from the player's inventory and place them in the current room.

#### Testing

* Pick up an item using get, then use drop to remove it from inventory and ensure it is listed in the room's items.

### 4. Winning and Losing Conditions

#### Usage
  * Winning:

    * To win, players must achieve specific goals, such as bringing certain items to a particular location.
    * Example: Carrying a treasure to a vault room.
    * Upon winning, the game displays a congratulatory message and ends.
  
* Losing:

    * Certain conditions or actions can result in a loss, such as entering a critical area unprepared.
    * Example: Entering a dragon's lair without a shield.
    * Losing results in a game-over message and termination of the session.
  
#### Implementation
* Winning: Defined by reaching a specific room with required items.
* Losing: Occurs upon entering specific rooms without necessary items.

#### Testing

* For winning, enter the designated 'win' room with the required items and check for a win message.
* For losing, enter a room where certain items are required without having them and verify if a loss is triggered.

### 5. Locked Doors

#### Usage
  * Some rooms feature exits that are locked and require specific items to unlock.
  * If a player tries to access a locked exit without the necessary item, the game will inform them of what is missing.
  * Example: A door might be locked requiring a key to unlock.
  * Benefit: Adds puzzle elements and encourages exploration to find needed items.

#### Implementation

* Some exits are locked and can only be accessed if the player has specific items in their inventory.

#### Testing

* Attempt to go through a locked exit without the required item and observe the 'locked' message.
* Acquire the necessary item, try again, and verify access is granted.
  

### 6. Help (For Guidance, Not for Grading)
We implemented a static help function designed to assist users in navigating the game.

## Bugs 

Currently, there are no identified bugs or errors within the code; however, the code has not successfully passed the test cases provided on Gradescope. Further investigation and testing may be required to align with Gradescope's specific testing criteria. 

## How we tested the code

We created a variety of map configurations, encompassing all possible combinations, to thoroughly test our code.

## Issues Encountered

  * We initally decided to implement the help verb as it seemed doable, but we faced a lot of challenges figuring out the correct way to implement it while following the requirements of it not just being static text. We eventually ended up not implementing it for credit as we ran out of time trying to figure out how to implement it correctly.
  * We also faced some difficulties implementing abbreviations for directions but we figured that out and resolved it
  * The output formatting took a lot of time too surprisingly, mainly trying to get the output of our game match the sample interaction provided to us in the project details. We had to pay a lot of attention to detail on capitalisation, white space, etc.
  * Inspite of all the outputs displaying correctly byte by byte, it still dosen't passes the test cases given on gradescope