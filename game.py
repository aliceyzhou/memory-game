from typing import List, Tuple
import random
import emoji


class Player:
    def __init__(self, name: str):
        """create basic player object"""
        self.name = name  # player name
        self.matches = 0  # number of pairs they've found
        self.found = []  # list of all the cards they've found

    def score(self) -> None:
        """update the score"""
        self.matches += 1


def get_emojis(file_name: str) -> List[str]:
    """read in all the emojis we will use from an external file"""
    try:
        file_pointer = open(file_name, "r")
    except FileNotFoundError:
        print("\nPlease import all the required files before running the program!")

    emojis = []
    for line in file_pointer:
        emojis.append(line.strip())
    return emojis


def get_size() -> int:
    """only accept 4, 6, 8, or 10 for game size"""
    size = 0
    valid = [4, 6, 8, 10]
    while size not in valid:
        size = int(input("Enter an even number for game size (between 4 - 10): "))
    return size


def get_players() -> int:
    """get the number of players (just has to be >= 0)"""
    inp = -5
    while type(inp) == str or inp < 0:
        inp = input("Enter the number of players: ")
        if inp.isdigit():
            inp = int(inp)
    return inp


def init_matrix(size: int) -> List[List[int]]:
    """thanks assignment 14 you're a real one"""
    matrix = []
    for row in range(size):
        matrix.append([])
        for column in range(size):
            matrix[row].append("🟩")
    return matrix


def generate_game(size: int, emoji_bank: List[str]) -> List[List[str]]:
    """Randomly generate a game of the specified size. The pairs of emojis will be scattered"""
    positions = []
    solution = init_matrix(size)
    for i in range(size*size):
        positions.append(i)

    random.shuffle(positions)  # the important part

    for i in range(0, len(positions), 2):
        n = random.randint(0, len(emoji_bank)-1)  # pick this emoji
        x1 = positions[i] // size
        y1 = positions[i] % size
        solution[x1][y1] = emoji_bank[n]  # first spot
        x2 = positions[i+1] // size
        y2 = positions[i+1] % size
        solution[x2][y2] = emoji_bank[n]  # second one
        del emoji_bank[n]  # no emoji reuse permitted

    # print(solution)
    return solution


def validate_guess(size: int, board: List[List[str]]) -> List[int]:
    """ user enters their 2 guesses, return the numbers split if valid coordinates """

    while True:
        guesses = input("Enter the coordinates for guess: ").split()
        if len(guesses) != 2:  # not enough or too many inputs = can't be right
            print("Incorrect formatting for guess. Please try again.")
            continue
        elif not guesses[0].isdigit() or int(guesses[0]) >= size or not guesses[1].isdigit() or int(guesses[1]) >= size:
            print("Invalid coordinate for guess. Please try again.")
            continue

        guesses[0] = int(guesses[0])  # cast
        guesses[1] = int(guesses[1])

        if (board[guesses[0]][guesses[1]]) != "🟩":
            print("Position has already been guessed. Please try again.")
            continue

        return guesses


def pretty_print(game: List[List[str]]) -> None:
    """nicely formats the game board with indices"""
    nums = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    print("   ", end="")
    for i in range(len(game)):
        print(nums[i], end=" ")  # the top line of indices

    for i in range(len(game)):
        print("\n" + nums[i] + " " , end="")  # number at front of every row
        for j in range(len(game[i])):
            print(game[i][j], sep=" ", end= " ")  # the board value
    print()


def introduction() -> None:
    """print the rules/introduction"""
    print("\n\nWelcome to Alice's memory game!")
    print("HOW TO PLAY: ")
    print("1. Enter the size of the game you want. The program will generate a square of that size. I recommend "
          "starting with 4 or 6.")
    print("2. Enter the number of players. Then, enter each player's name.")
    print("3. The game will rotate between the players. On your turn, enter two coordinates for a guess. The "
          "indices are provided along the sides. Enter the row first then the column. Please enter only"
          " two numbers on the line. You can not guess a space that has already been taken.")
    print("4. If you do not find a match, the game rotates to the next player. If you do, those two spaces are cleared,"
          "your score is updated, and you are permitted another turn.")
    print("5. The game ends when all matches have been found!\n")


def play_game(solution: List[List[str]], players: List[Player], size: int) -> None:
    """in charge of running all gameplay"""
    introduction()

    # comment out before playing for real, uncomment for debug/test
    # print("pst, secret solution: ")
    # pretty_print(solution)

    game_board = init_matrix(size)  # grid of all green squares

    counter = 0
    matches = 0
    maxMatches = 0
    while matches < size ** 2 / 2:
        print("\n" + players[counter].name + "'s Turn: ")
        pretty_print(game_board)

        coords1 = validate_guess(size, game_board)  # first guess
        g1 = solution[coords1[0]][coords1[1]]
        game_board[coords1[0]][coords1[1]] = g1

        coords2 = validate_guess(size, game_board)  # second guess
        g2 = solution[coords2[0]][coords2[1]]
        game_board[coords2[0]][coords2[1]] = g2

        print("\n" + players[counter].name + "'s Guesses: ")
        pretty_print(game_board)

        if g1 == g2:  # match found!
            matches += 1
            if not matches == size ** 2 / 2:
                print("Match found.", players[counter].name, "can go again.")
            players[counter].score()  # update score
            players[counter].found.append(g1)  # update found emojis list

            if players[counter].matches > maxMatches:
                maxMatches = players[counter].matches  # update the value of maximum score, so we can get winner later

            game_board[coords1[0]][coords1[1]] = "⬛"  # remove this spot from being guessed
            game_board[coords2[0]][coords2[1]] = "⬛"
        else:
            print("No match found.")
            game_board[coords1[0]][coords1[1]] = "🟩"
            game_board[coords2[0]][coords2[1]] = "🟩"
            counter += 1  # rotate to the next player

        counter %= len(players)  # for easier indexing

    print("\nAll cards have been found. ", end="")

    winnerList = []  # stores all the winners
    for player in players:
        if player.matches == maxMatches:
            winnerList.append(player)

    if len(winnerList) == 1:
        print(winnerList[0].name + " wins with " + str(maxMatches) + " pairs!")
        print(winnerList[0].name + " found " + str(winnerList[0].found))
    else:
        print(" and ".join(winnerList) + " tied with " + str(maxMatches) + " pairs each!")


def main():
    # set up stuff
    emoji_bank = get_emojis("emojis.txt")
    size = get_size()
    players = get_players()
    player_list = []
    print("Please enter the names for: ")
    for i in range(players):
        name = input("Player " + str(i+1) + ": ")
        player_list.append(Player(name))

    play_game(generate_game(size, emoji_bank), player_list, size)


if __name__ == "__main__":
    main()