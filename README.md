# Battleship Game

Battleship (also known as Battleships or Sea Battle) is a strategy-type guessing game for two players. It is played on ruled grids (paper or board) on which each player's fleet of warships is marked. The locations of the fleets are concealed from the other player. Players alternate turns calling "shots" at the other player's ships, and the game's objective is to destroy the opposing player's fleet.

# Game Rules

The game is played on four grids of squares, each grid being 10x10 in size, with two grids for each player.

Players secretly arrange their ships on their hidden grid. Each ship occupies consecutive squares on the grid, either horizontally or vertically, without overlapping with other ships.

The types and numbers of ships are the same for each player. The ship types and their sizes are as follows:

      Carrier (5 squares)
      
      Battleship (4 squares)

      Destroyer (3 squares)

      Submarine (3 squares)

      Patrol Boat (2 squares)

Players take turns calling shots by announcing a target square in the opponent's grid to shoot.

The game informs whether the shot hits or misses a ship, and marks the hit or miss on the grid.

When all squares of a ship are hit, the game announces the sinking of that ship.

The game continues until one player's fleet is completely sunk, and the opposing player wins.

If all ships of both players are sunk by the end of the round, the game is a draw.

# How to Run the Game

Make sure you have Python installed on your computer.

Save the provided code in a file named battleship.py.

Open a command prompt or terminal and navigate to the directory where the battleship.py file is located.

Run the game by executing the following command: python battleship.py player1_input.txt player2_input.txt player1.in player2.in

Note: Replace player1_input.txt and player2_input.txt with the paths to the input files for each player. The input files should contain the coordinates of the shots to be made in each round, separated by semicolons (;).

The game will be played automatically based on the input files. The game boards and results will be displayed in the console.

# Output

The game will display the game boards for each player, showing their hidden ships and the shots made by the opponent. After each round, the game will indicate whether a shot hit or missed a ship. If a ship is sunk, it will be announced. Finally, the game will print the winner of the game.

# Notes

The code provided assumes that the input files are properly formatted and contain valid coordinates for the shots. Make sure the input files are correct to avoid any errors.

The game code uses the ASCII characters for column letters, so the column letters should be uppercase letters from A to J.

The code includes error handling for missing input files. If any of the input files are not found, an error message will be displayed.

[BBM103_A4.pdf](https://github.com/SerhatAkbulut1/Assignment-3/files/11971634/BBM103_A4.pdf)
