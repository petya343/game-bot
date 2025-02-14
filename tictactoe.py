import random

possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
board = [[1,2,3],[4,5,6],[7,8,9]]
number_positions = {
    number: (i, j)
    for i, row in enumerate(board)
    for j, number in enumerate(row)
}
bot_sign = ""
player_sign = ""
num_emojis = {
    1: "1️⃣", 2: "2️⃣", 3: "3️⃣",
    4: "4️⃣", 5: "5️⃣", 6: "6️⃣",
    7: "7️⃣", 8: "8️⃣", 9: "9️⃣"
}

def print_board():
    board_string = "----+----+----\n"
    for row in board:
        board_string += " | ".join(num_emojis[i] if isinstance(i, int) else i for i in row) + "\n"
        board_string += "----+----+----\n"
    return board_string

def short_check() -> str:
    if checkwin(bot_sign):
        b = print_board()
        end_game()
        return f"You lost 😞. Better luck next time! \n{b}"
    return print_board()

def check_sign(sign: str) -> bool:
    return sign != bot_sign and sign != player_sign

def bot_guess(sign: str) -> bool:
    global possible_numbers
    global board
    
    for i in range(3):
        if board[i][0] == sign and board[i][1] == sign and check_sign(board[i][2]):
            board[i][2] = bot_sign
            possible_numbers.remove(3+3*i)
            return True
        if board[i][0] == sign and board[i][2] == sign and check_sign(board[i][1]):
            board[i][1] = bot_sign
            possible_numbers.remove(2+3*i)
            return True
        if board[i][1] == sign and board[i][2] == sign and check_sign(board[i][0]):
            board[i][0] = bot_sign
            possible_numbers.remove(1+3*i)
            return True
        if board[0][i] == sign and board[1][i] == sign and check_sign(board[2][i]):
            board[2][i] = bot_sign
            possible_numbers.remove(7+i)
            return True
        if board[0][i] == sign and board[2][i] == sign and check_sign(board[1][i]):
            board[1][i] = bot_sign
            possible_numbers.remove(4+i)
            return True
        if board[1][i] == sign and board[2][i] == sign and check_sign(board[0][i]):
            board[0][i] = bot_sign
            possible_numbers.remove(1+i)
            return True
    
    if board[0][0] == sign and board[1][1] == sign and check_sign(board[2][2]):
        board[2][2] = bot_sign
        possible_numbers.remove(9)
        return True
    elif board[0][0] == sign and board[2][2] == sign and check_sign(board[1][1]):
        board[1][1] = bot_sign
        possible_numbers.remove(5)
        return True
    elif board[2][2] == sign and board[1][1] == sign and check_sign(board[0][0]):
        board[0][0] = bot_sign
        possible_numbers.remove(1)
        return True

    elif board[0][2] == sign and board[1][1] == sign and check_sign(board[2][0]):
        board[2][0] = bot_sign
        possible_numbers.remove(7)
        return True
    elif board[2][0] == sign and board[1][1] == sign and check_sign(board[0][2]):
        board[0][2] = bot_sign
        possible_numbers.remove(3)
        return True
    elif board[0][2] == sign and board[2][0] == sign and check_sign(board[1][1]):
        board[1][1] = bot_sign
        possible_numbers.remove(5)
        return True

    return False

def bot_move():

    if bot_guess(bot_sign):
        return short_check()
    elif bot_guess(player_sign):
        return short_check()
    else:
        guess = random.choice(possible_numbers)
        possible_numbers.remove(guess)
        pos = number_positions[guess]
        board[pos[0]][pos[1]] = bot_sign

    return short_check()

def checkwin(sign: str) -> bool :

    for i in range(3):
        if board[i][0] == sign and board[i][1] == sign and board[i][2] == sign:
        
            return True
        if board[0][i] == sign and board[1][i] == sign and board[2][i] == sign:
            
            return True
    
    if board[0][0] == sign and board[1][1] == sign and board[2][2] == sign:
        
        return True
    
    if board[0][2] == sign and board[1][1] == sign and board[2][0] == sign:
       
        return True

    return False

def get_response_TicTacToe(user_input: str) -> str:

    if user_input.lower() == "tic tac toe":
        return "Choose a sign: X or O"
    
    if user_input.lower().strip() == "end":
        end_game()
        return "The game ended"
    
    global player_sign
    global bot_sign
    
    if user_input.upper().strip() == "X":
        bot_sign = "⭕"
        player_sign = "❌"
        return "Let's begin! Choose a position between 1 and 9 :)"
    
    if user_input.upper().strip() == "O":
        bot_sign = "❌"
        player_sign = "⭕"
        return "Let's begin! Choose a position between 1 and 9 :)"
    
    global board
    global possible_numbers
   
    try:
        player_move = int(user_input.strip())
        print(f"player move = {player_move}")

        pos = number_positions[player_move]
        print(f"pos = {pos}")
        print(f"board = {print_board()}")

        if not isinstance(board[pos[0]][pos[1]], int):
            return "This position is already taken"
        
        board[pos[0]][pos[1]] = player_sign
        print(f"board = {print_board()}")

        if checkwin(player_sign):
            b = print_board()
            end_game()
            return f"Congrats, YOU WON!😊 \n{b}"
        
        print(f"possible numbers = {possible_numbers}")
        possible_numbers.remove(player_move)
        print(f"possible numbers2 = {possible_numbers}")
        if not possible_numbers and not checkwin(player_sign) and not checkwin(bot_sign):
            end_game()
            return "It's a tie!"

        return bot_move()
    
    except ValueError:
        return "Invalid input"
    
def end_game():

    global possible_numbers
    global board
    global bot_sign
    global player_sign

    possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    board = [[1,2,3],[4,5,6],[7,8,9]]
    bot_sign = ""
    player_sign = ""