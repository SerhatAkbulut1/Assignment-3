import string
import sys

# Oyun sonucunu bir dosyaya yazmak için çıktıyı yönlendiriyoruz
temp = sys.stdout
sys.stdout = open('Battleship.out', 'w', encoding='utf-8')

# Gemi türlerinin toplam sayısı ve uzunlukları belirlendi
CARRIER_SIZE = 5
CARRIER_COUNT = 1
BATTLESHIP_SIZE = 4
BATTLESHIP_COUNT = 2
DESTROYER_SIZE = 3
DESTROYER_COUNT = 1
SUBMARINE_SIZE = 3
SUBMARINE_COUNT = 1
PATROL_BOAT_SIZE = 2
PATROL_BOAT_COUNT = 4
ALPHABET = string.ascii_uppercase
ROW_LEN = 10
COLUMN_LEN = 10
EMPTY_PIECE = "-"

# Gemi türleri bir sözlükte saklandı
shipDict = {
    'P': PATROL_BOAT_SIZE,
    'C': CARRIER_SIZE,
    'D': DESTROYER_SIZE,
    'S': SUBMARINE_SIZE,
    'B': BATTLESHIP_SIZE,
}

# Her bir oyuncu için gemi türlerinin sayısını tutacak ayrı bir sözlük oluşturuldu
shipCountDict_player1 = {
    'P': 0,
    'C': 0,
    'D': 0,
    'S': 0,
    'B': 0,
}
shipCountDict_player2 = {
    'P': 0,
    'C': 0,
    'D': 0,
    'S': 0,
    'B': 0,
}

# Dosyayı okumak için bir fonksiyon oluşturuldu
def dataReader(data):
    with open(data, "r") as file:
        return file.readlines()

# Gizli oyun tahtasını oluşturmak için bir fonksiyon
def create_secret_board(game_board):
    return [[EMPTY_PIECE for _ in range(COLUMN_LEN)] for _ in range(ROW_LEN)]

# Dosyadan alınan girişi düzgün hale getirmek için bir fonksiyon oluşturuldu
def transform_line(line: str):
    if len(line) == COLUMN_LEN:
        return line

    result = line.replace("P;", "P").replace("S;", "S").replace("D;", "D").replace("B;", "B").replace("C;", "C")

    if len(line) != COLUMN_LEN:
        result += ";"

    return result

# Seçilen koordinatta geminin olup olmadığını kontrol etmek için bir fonksiyon oluşturuldu
def is_ship(secret_game_board, game_board, shipType, direction, x, y):
    isShip = True
    shipLen = shipDict[shipType[0]]

    if direction == "right":
        try:
            for j in range(shipLen):
                if game_board[x][y + j] != shipType or secret_game_board[x][y + j] != "X":
                    isShip = False
        except IndexError:
            pass

    elif direction == "down":
        try:
            for i in range(shipLen):
                if game_board[x + i][y] != shipType or secret_game_board[x + i][y] != "X":
                    isShip = False
        except:
            isShip = False

    return isShip

# Gemilerin sayısını ayarlamak için bir fonksiyon oluşturuldu
def shipCount(game_board, secret_game_board, player_shipCountDict):
    for i in range(COLUMN_LEN):
        for j in range(ROW_LEN):
            if game_board[i][j] != EMPTY_PIECE:
                if secret_game_board[i][j] == "X":
                    if (j + shipDict[game_board[i][j]]) <= COLUMN_LEN:
                        if game_board[i][j + 1] == game_board[i][j]:
                            if is_ship(secret_game_board, game_board, game_board[i][j], "right", i, j):
                                player_shipCountDict[game_board[i][j]] += 1
                    if (i + shipDict[game_board[i][j]]) <= ROW_LEN:
                        if game_board[i + 1][j] == game_board[i][j]:
                            if is_ship(secret_game_board, game_board, game_board[i][j], "down", i, j):
                                player_shipCountDict[game_board[i][j]] += 1

# Koordinatları oyun tahtası değerlerine göre dönüştürmek için bir fonksiyon oluşturuldu
def convertCoordinates(coordinate):
    x_coordinate = int(coordinate.split(",")[0]) - 1
    y_coordinate = int(string.ascii_uppercase.index(coordinate.split(",")[1]))

    return x_coordinate, y_coordinate

# Y koordinatını bir harfe dönüştürmek için bir fonksiyon oluşturuldu
def convertLetter(x, y):
    x = x + 1
    y = string.ascii_uppercase[y]
    return f"{x},{y}"

# Dosyayı işlemek için bir fonksiyon oluşturuldu
def processInputFile(player_input_data):
    try:
        with open(player_input_data, "r") as player_input_file:
            player_input = player_input_file.readline().split(";")[:-1]
            player_input = list(map(convertCoordinates, player_input))
            return player_input
    except IOError:
        print(f"IOError: {player_input_data} file is not reachable.")
        sys.exit(1)

# Oyun tahtasını oluşturmak için bir fonksiyon
def create_game_board(filepath):
    try:
        with open(filepath, "r") as file:
            line = file.readline().replace("\n", "")
            line = transform_line(line).replace(";", EMPTY_PIECE)
            game_board = [[" " for _ in range(COLUMN_LEN)] for _ in range(ROW_LEN)]
            for rowIndex in range(ROW_LEN):
                letters = list(line)
                for columnIndex in range(COLUMN_LEN):
                    game_board[rowIndex][columnIndex] = letters[columnIndex]
                line = file.readline().replace("\n", "")
                line = transform_line(line).replace(";", EMPTY_PIECE)
            return game_board
    except IOError:
        print(f"IOError: {filepath} file is not reachable.")
        sys.exit(1)

# Oyun tahtalarını yazdırmak için bir fonksiyon
def print_boards(player1_game_board, player2_game_board):
    print("Player1's Hidden Board        Player2's Hidden Board")
    print("  ", *string.ascii_uppercase[:COLUMN_LEN], "       ", *string.ascii_uppercase[:COLUMN_LEN])
    for rowIndex in range(ROW_LEN):
        print(f"{rowIndex + 1:^2}", end=" ")
        print(*player1_game_board[rowIndex], sep=" ", end="      ")
        print(f"{rowIndex + 1:^2}", end=" ")
        print(*player2_game_board[rowIndex], sep=" ")

# Vuruş işlemini gerçekleştirmek için bir fonksiyon
def bombing(coordinates_x, coordinates_y, enemy_game_board, enemy_secret_game_board):
    if enemy_game_board[coordinates_x][coordinates_y] == EMPTY_PIECE and enemy_secret_game_board[coordinates_x][coordinates_y] == EMPTY_PIECE:
        enemy_secret_game_board[coordinates_x][coordinates_y] = "O"
        return True
    else:
        enemy_secret_game_board[coordinates_x][coordinates_y] = "X"
        return False

# Oyunun ana işleyişini sağlamak için bir fonksiyon
def main():
    try:
        player1_game_board = create_game_board(sys.argv[1])
        player2_game_board = create_game_board(sys.argv[2])
        player1_secret_game_board = create_secret_board(player1_game_board)
        player2_secret_game_board = create_secret_board(player2_game_board)
        player1_input = processInputFile(sys.argv[3])
        player2_input = processInputFile(sys.argv[4])

        print("Battle of Ships Game")
        print_boards(player1_secret_game_board, player2_secret_game_board)
    except IndexError:
        print("There should be 4 inputs")
        sys.exit(1)
    except Exception:
        print("kaBOOM: run for your life! ")
        sys.exit(1)

    lap = 0
    order = 1
    total_ship_count = BATTLESHIP_COUNT + CARRIER_COUNT + PATROL_BOAT_COUNT + SUBMARINE_COUNT + DESTROYER_COUNT
    while True:
        if order == 1:
            print("Player1's Move")
            print(f"\nRound : {lap + 1}\t\t\t\t\tGrid size: 10x10")

            success = bombing(*player1_input[lap], player2_game_board, player2_secret_game_board)
            print()
            print_boards(player1_secret_game_board, player2_secret_game_board)
            order = 2
            shipCount(player2_game_board, player2_secret_game_board, shipCountDict_player2)
            total_ship_count_player2 = total_ship_count - sum(shipCountDict_player2.values())

            print_ship_counts(shipCountDict_player1, shipCountDict_player2)

            print(f"\nEnter your move: {convertLetter(*player1_input[lap])}")
            print()

            if total_ship_count_player2 == 0:
                break
            else:
                reset_ship_counts(playerCountDict_player2)

        if order == 2:
            print("Player2's Move")
            print(f"\nRound : {lap + 1}\t\t\t\t\tGrid size: 10x10")

            success = bombing(*player2_input[lap], player1_game_board, player1_secret_game_board)
            print_boards(player1_secret_game_board, player2_secret_game_board)
            order = 1
            shipCount(player1_game_board, player1_secret_game_board, shipCountDict_player1)
            total_ship_count_player1 = total_ship_count - sum(shipCountDict_player1.values())

            print_ship_counts(shipCountDict_player1, shipCountDict_player2)

            print(f"\nEnter your move: {convertLetter(*player2_input[lap])}")
            print()

            if total_ship_count_player1 == 0:
                break
            else:
                reset_ship_counts(playerCountDict_player1)

        lap += 1

    print(f"\nPlayer {order} win")

# Gemi sayılarını sıfırlamak için bir fonksiyon
def reset_ship_counts(shipCountDict):
    shipCountDict['P'] = 0
    shipCountDict['B'] = 0
    shipCountDict['S'] = 0
    shipCountDict['C'] = 0
    shipCountDict['D'] = 0

# Gemi sayılarını yazdırmak için bir fonksiyon
def print_ship_counts(shipCountDict_player1, shipCountDict_player2):
    print("Carrier : \t" + "X" * shipCountDict_player1["C"] + "-" * (1 - shipCountDict_player1["C"]), end="\t\t")
    print("Carrier : \t" + "X" * shipCountDict_player2["C"] + "-" * (1 - shipCountDict_player2["C"]))
    print("Battleship: \t" + "X" * shipCountDict_player1["B"] + "-" * (2 - shipCountDict_player1["B"]), end="\t\t")
    print("Battleship: \t" + "X" * shipCountDict_player2["B"] + "-" * (2 - shipCountDict_player2["B"]))
    print("Destroyer : \t" + "X" * shipCountDict_player1["D"] + "-" * (1 - shipCountDict_player1["D"]), end="\t\t")
    print("Destroyer : \t" + "X" * shipCountDict_player2["D"] + "-" * (1 - shipCountDict_player2["D"]))
    print("Submarine : \t" + "X" * shipCountDict_player1["S"] + "-" * (1 - shipCountDict_player1["S"]), end="\t\t")
    print("Submarine : \t" + "X" * shipCountDict_player2["S"] + "-" * (1 - shipCountDict_player2["S"]))
    print("Patrol Boat : \t" + "X" * shipCountDict_player1["P"] + "-" * (4 - shipCountDict_player1["P"]), end="\t\t")
    print("Patrol Boat : \t" + "X" * shipCountDict_player2["P"] + "-" * (4 - shipCountDict_player2["P"]))

if __name__ == "__main__":
    main()

# Çıktıyı orijinal çıktıya geri yönlendiriyoruz
sys.stdout = temp

# Dosyadaki çıktıyı yazdırıyoruz
with open('Battleship.out', 'r') as file:
    print(*file.readlines())
