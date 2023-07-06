import string
import sys
temp = sys.stdout
sys.stdout = open('Battleship.out', 'w', encoding='utf-8')   # The result of the game was written into a file.
# The total number of ships and the length of ship types were determined.
CARRIER_SIZE = 5
CARRIER_COUNT = 1
BATTLESHIP_SIZE = 4
BATTLESHIP_COUNT = 2
DESTROYER_SIZE = 3
DESTROYER_COUNT = 1
SUBMERINE_SIZE = 3
SUBMERINE_COUNT = 1
PATROL_BOAT_SIZE = 2
PATROL_BOAT_COUNT = 4
ALPHABET = string.ascii_uppercase # This code was written for the column naming.
ROW_LEN = 10              # row number
COLUMN_LEN = 10           # column number
EMPTY_PIECE = "-" # These signs were placed where the ships were not placed.

# Cruise tours were kept in a dict.
shipDict = {
    'P' : PATROL_BOAT_SIZE,
    'C' : CARRIER_SIZE,
    'D' : DESTROYER_SIZE,
    'S' : SUBMERINE_SIZE,
    'B' : BATTLESHIP_SIZE,
}

# According to the number of ship types, it was kept in a separate dict for each player.
shipCountDict_player1 = {
    'P' : 0,
    'C' : 0,
    'D' : 0,
    'S' : 0,
    'B' : 0,
}
shipCountDict_player2 = {
    'P' : 0,
    'C' : 0,
    'D' : 0,
    'S' : 0,
    'B' : 0,
}
# A function was written to read the file.
def dataReader(data):
    file = open(data , "r")
    data = file.readlines()
    return data

# A function was written to create a secret game board (appears while playing).
def create_secret_board(game_board):
    return [[EMPTY_PIECE for j in range(COLUMN_LEN)] for i in range(ROW_LEN)]

# A function was created to make the input given in the file smooth.
def transform_line(line: str):
       # Created a code to equalize the row if it is equal to the number of columns.
    if len(line) == COLUMN_LEN:
        return line

    # A code was created to change the letters that designate ship types.
    result = line.replace("P;" , "P").replace("S;" , "S").replace("D;" , "D").replace("B;" , "B").replace("C;" , "C")

    # If there is a missing input at the end of the given input, a code has been created to complete it.
    if len(line) != COLUMN_LEN:
        result +=";"

    return result


# A function has been created to check that the ship is at the selected coordinate.
def is_ship(secret_game_board,game_board, shipType, direction , x ,y):
    isShip = True
    shipLen = shipDict[shipType[0]]

    # A code has been created to check that ships are to the right.
    if direction == "right":
        # The code checks for ship length, if true it equalizes true.
        try:
            for j in range(shipLen):
                if game_board[x][y + j] != shipType or secret_game_board[x][y+j] != "X":
                    isShip = False
        except IndexError:
            pass

    # A code was created to check that the ships were down.
    elif direction == "down":

        try:
            for i in range(shipLen):
                if game_board[x + i][y] != shipType or secret_game_board[x+i][y] != "X":
                    isShip = False
        except:
            isShip = False

    return isShip

# A function has been created to set the number of ships.
def shipCount(game_board, secret_game_board,player_shipCountDict):
    for i in range(COLUMN_LEN): 
        for j in range(ROW_LEN):
            if game_board[i][j] != EMPTY_PIECE:                        # The code was written to understand that the point whose coordinates were given was hit. If hit, the if is entered.
                if secret_game_board[i][j] == "X":                     # It was understood that if the sign of the point whose coordinates were given was "X", it was hit. Entered into an if loop.
                    if ((j + shipDict[game_board[i][j]]) <= COLUMN_LEN ):  #  In order not to get an index error, if the sum of j and ship length is more than the number of columns, it is not included in if.
                        if game_board[i][j + 1] == game_board[i][j]:    # Checked if the ship's direction is right. If right, the if is entered.
                            if is_ship(secret_game_board,game_board, game_board[i][j], "right", i, j):  # It was checked whether the entire ship was hit. If hit, the if is entered.
                                player_shipCountDict[game_board[i][j]] += 1 # Added to the dict what type of ship was hit by the players to indicate that the entire ship was hit.
                    if ((i + shipDict[game_board[i][j]]) <= ROW_LEN):# In order not to get an index error, if the sum of i and ship length is more than the number of columns, it is not included in if.
                        if game_board[i + 1][j] == game_board[i][j]: # Checked if the direction of the ship is down. If right, the if is entered.
                            if is_ship(secret_game_board,game_board, game_board[i][j], "down", i, j):# It was checked whether the entire ship was hit. If hit, the if is entered.
                                player_shipCountDict[game_board[i][j]] += 1 # It was checked whether the entire ship was hit. If hit, the if is entered.


# A function was created to adapt the coordinates according to the values of the game board.
def convertCoordinates(coordinate):
    x_coordinate = int(coordinate.split(",")[0]) - 1                         # A code has been generated for the coordinate of the row number.
    y_coordinate = int(string.ascii_uppercase.index(coordinate.split(",")[1])) # Generated a code for the coordinate of the column number.

    return x_coordinate,y_coordinate

# A function has been created to convert the y coordinate to a letter.
def convertLetter(x, y):
    x = x + 1
    y = string.ascii_uppercase[y] # A code was written to convert the number to letter.
    return f"{x},{y}"

# A function has been created to extract files.
def processInputFile1(player1_input_data):
    player1_input_file = open(player1_input_data , "r")            # The file for player 1 has been opened.
    player1_input = player1_input_file.readline().split(";")[:-1]  # The file for player 1 has been extracted.
    player1_input = list(map(convertCoordinates , player1_input))  # A code was created to pass information into the convertcoordinates function.
   
    return player1_input

def processInputFile2(player2_input_data):
    player2_input_file = open(player2_input_data , "r")            # The file for player 2 has been opened.
    player2_input = player2_input_file.readline().split(";")[:-1]  # The file for player 2 has been extracted.
    player2_input = list(map(convertCoordinates , player2_input))  # A code was created to pass information into the convertcoordinates function.
   
    return player2_input



# A code was created to pass information into the convertcoordinates function.
def create_game_board(filepath):
    file = open(filepath, "r")                                               # The input for the game board is opened..
    line = file.readline().replace("\n", "")                                 # The input for the game board has been extracted.
    line = transform_line(line).replace(";", EMPTY_PIECE)                    # The input for the game board has been extracted.
    game_board = [[" " for j in range(COLUMN_LEN)] for i in range(ROW_LEN)]  # The game board was created in a list.
    for rowIndex in range(ROW_LEN):                                          # The for loop was entered to create the rows of the game board.
        letters = list(line)
        for columnIndex in range(COLUMN_LEN):                                # The for loop was entered to create the columns of the game board.
            game_board[rowIndex][columnIndex] = letters[columnIndex]
        line = file.readline().replace("\n", "")
        line = transform_line(line).replace(";", EMPTY_PIECE)

    return game_board


# A function has been created to print game boards.
def print_boards(player1_game_board, player2_game_board):
    print("Player1's Hidden Board        Player2's Hidden Board")                                      # the title of the player board was determined on behalf of each player.
    print("  ", *string.ascii_uppercase[:COLUMN_LEN], "       ", *string.ascii_uppercase[:COLUMN_LEN]) # row and column numbers are written.
    for rowIndex in range(ROW_LEN):                                                                    # Necessary arrangements were made for the row and column numbers to be in a proper order.
        print(f"{rowIndex + 1:^2}", end=" ")
        print(*player1_game_board[rowIndex], sep=" ", end="      ")
        print(f"{rowIndex + 1:^2}", end=" ")
        print(*player2_game_board[rowIndex], sep=" ")

# created a function to perform the hit action.
def bombing(coordinates_x , coordinates_y , enemy_game_board, enemy_secret_game_board):
    if enemy_game_board[coordinates_x][coordinates_y] == EMPTY_PIECE and enemy_secret_game_board[coordinates_x][coordinates_y] == EMPTY_PIECE: 
        enemy_secret_game_board[coordinates_x][coordinates_y] = "O"     # If the hit did not hit, it was indicated with an "O" sign.
        return True
    else:
        enemy_secret_game_board[coordinates_x][coordinates_y] = "X"      # If the hit was accurate, it was indicated with an "X".
        return False

#  A function called "main" has been created for the game to run.
def main():
    BULUNMAYAN_DOSYA = []   
    try:                #Try-except block is used to prevent errors that will occur while receiving input. Incorrect entries have been added to the list of missing files.
        finish = False  # the finish is set to "False" for the game to continue.
        try:                                                    
            player1_game_board = create_game_board(sys.argv[1])               # The create_game_board function is called to open player1's file.
        except IOError:
            BULUNMAYAN_DOSYA.append(sys.argv[1])
        try:    
            player2_game_board = create_game_board(sys.argv[2])               # The create_game_board function is called to open player2's file
        except IOError:
            BULUNMAYAN_DOSYA.append(sys.argv[2])
        player1_secret_game_board = create_secret_board(player1_game_board) 
        player2_secret_game_board = create_secret_board(player2_game_board) 
        try:
            player1_input = processInputFile1(sys.argv[3]) # The input values given for the players to make the hit moves are called with the process Input File function.
        except IOError:
            BULUNMAYAN_DOSYA.append(sys.argv[3])
        try:
            player2_input = processInputFile2(sys.argv[4]) # The input values given for the players to make the hit moves are called with the process Input File function.
        except IOError:
            BULUNMAYAN_DOSYA.append(sys.argv[4])
        finally:
            if BULUNMAYAN_DOSYA != []:            # Possible IO Errors are kept in a list.
                file_names = " ".join(BULUNMAYAN_DOSYA)
                print("IOError: {} file(s) is/are not reachable.".format(file_names)) #Occurring IO Errors were printed to the file.
                quit()
        print("Battle of Ships Game")
        print_boards(player1_secret_game_board, player2_secret_game_board)
    except IndexError:
        print("There should be at 4 input")
    except Exception:
        print( "kaBOOM: run for your life! ")

    # The turn of the game and the number of rounds are assigned a value, the finish is created in the bombing function, when the number of ships is finished, the finish is true.
    lap = 0
    order = 1
    total_ship_count = BATTLESHIP_COUNT + CARRIER_COUNT +PATROL_BOAT_COUNT+SUBMERINE_COUNT + DESTROYER_COUNT # The count variable is set to be the total number of ships.
    while not finish:          # It is enclosed in a while loop to keep the game going.
        if order == 1:         # Code was written for player 1's moves.
            print("Player1's Move")
            
            print("\nRound : {}\t\t\t\t\tGrid size: 10x10".format(lap+1))                                     
            success = bombing(*player1_input[lap], player2_game_board, player2_secret_game_board)  # The bombing function has been called for player 1 
            print()
            print_boards(player1_secret_game_board, player2_secret_game_board)                     # The game boards were called as a result of player 1's toss.
            order = 2                                                                              # It's player 2's turn to play.
            shipCount(player2_game_board, player2_secret_game_board, shipCountDict_player2)        # It was checked with the shipCount() function whether there was an exploding ship.
            total_ship_count_player2 = total_ship_count - sum(shipCountDict_player2.values())      # Checked how many ships player 2 has left.
           # Prints are written below the output so that the number of exploded ships for each player is printed.
            print("Carrier : \t"+ "X" * shipCountDict_player1["C"]+"-" * (1-shipCountDict_player1["C"]), end=" \t\t" )
            print("Carrier : \t"+ "X" * shipCountDict_player2["C"]+"-" * (1-shipCountDict_player2["C"]))
            print("Battleship: \t"+ "X" * shipCountDict_player1["B"]+"-" * (2-shipCountDict_player1["B"]), end=" \t\t" )
            print("Battleship: \t"+ "X" * shipCountDict_player2["B"]+"-" * (2-shipCountDict_player2["B"]) )
            print("Destroyer : \t"+ "X" * shipCountDict_player1["D"]+"-" * (1-shipCountDict_player1["D"]), end=" \t\t" )
            print("Destroyer : \t"+ "X" * shipCountDict_player2["D"]+"-" * (1-shipCountDict_player2["D"]) )
            print("Submarine : \t"+ "X" * shipCountDict_player1["S"]+"-" * (1-shipCountDict_player1["S"]), end=" \t\t" )
            print("Submarine : \t"+ "X" * shipCountDict_player2["S"]+"-" * (1-shipCountDict_player2["S"]) )
            print("Patrol Boat : \t"+ "X" * shipCountDict_player1["P"]+"-" * (4-shipCountDict_player1["P"]), end=" \t\t" )
            print("Patrol Boat : \t"+ "X" * shipCountDict_player2["P"]+"-" * (4-shipCountDict_player2["P"]) )
           
            print("\nEnter your move: ", convertLetter(*player1_input[lap])) # The move coordinate entered by the player is printed on the table.
            print()
            if total_ship_count_player2 == 0:                                                     # If player 2 has no solid ships left, the game is over.
                finish = True
            else:
                shipCountDict_player2['P'] = 0
                shipCountDict_player2['B'] = 0
                shipCountDict_player2['S'] = 0
                shipCountDict_player2['C'] = 0
                shipCountDict_player2['D'] = 0
        if order == 2:      # Coded for player 2's moves.                                                                    
            print("Player2's Move")
            
            print("\nRound : {}\t\t\t\t\tGrid size: 10x10".format(lap+1))
            success = bombing(*player2_input[lap], player1_game_board, player1_secret_game_board)  # The bombing function has been called for player 2
            print_boards(player1_secret_game_board, player2_secret_game_board)                     # The game boards were called as a result of player 2's throw.
            order = 1                                                                              # It's player 1's turn to play
            shipCount(player1_game_board, player1_secret_game_board, shipCountDict_player1)        # It was checked with the shipCount() function whether there was an exploding ship.
            total_ship_count_player1 = total_ship_count - sum(shipCountDict_player1.values())      # Checked how many ships player 2 has left.
            # Prints are written below the output so that the number of exploded ships for each player is printed.
            print("Carrier : \t"+ "X" * shipCountDict_player1["C"]+"-" * (1-shipCountDict_player1["C"]), end=" \t\t" )
            print("Carrier : \t"+ "X" * shipCountDict_player2["C"]+"-" * (1-shipCountDict_player2["C"]))
            print("Battleship: \t"+ "X" * shipCountDict_player1["B"]+"-" * (2-shipCountDict_player1["B"]), end=" \t\t" )
            print("Battleship: \t"+ "X" * shipCountDict_player2["B"]+"-" * (2-shipCountDict_player2["B"]) )
            print("Destroyer : \t"+ "X" * shipCountDict_player1["D"]+"-" * (1-shipCountDict_player1["D"]), end=" \t\t" )
            print("Destroyer : \t"+ "X" * shipCountDict_player2["D"]+"-" * (1-shipCountDict_player2["D"]) )
            print("Submarine : \t"+ "X" * shipCountDict_player1["S"]+"-" * (1-shipCountDict_player1["S"]), end=" \t\t" )
            print("Submarine : \t"+ "X" * shipCountDict_player2["S"]+"-" * (1-shipCountDict_player2["S"]) )
            print("Patrol Boat : \t"+ "X" * shipCountDict_player1["P"]+"-" * (4-shipCountDict_player1["P"]), end=" \t\t" )
            print("Patrol Boat : \t"+ "X" * shipCountDict_player2["P"]+"-" * (4-shipCountDict_player2["P"]) )
            
            
            print("\nEnter your move: ", convertLetter(*player2_input[lap])) # The move coordinate entered by the player is printed on the table.
            print()
            if total_ship_count_player1 == 0:                                                    # If player 2 has no solid ships left, the game is over.
                finish = True
            else:
                shipCountDict_player1['P'] = 0
                shipCountDict_player1['B'] = 0
                shipCountDict_player1['S'] = 0
                shipCountDict_player1['C'] = 0
                shipCountDict_player1['D'] = 0
        lap += 1        # The number of laps is increased by 1 after the lap is over to know which lap we are in.                                                                                                
    print("\nPlayer {} win".format(order))
main()

sys.stdout = temp
with open('Battleship.out', 'r') as file:
    print(*file.readlines())