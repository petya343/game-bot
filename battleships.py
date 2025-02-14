import random

player_ships_length = [2, 3, 4, 5, 6]
player_ships_positions = []
game_started = False
positions = [(x,y) for x in range(10) for y in range(10)]
player_guesses = []
prev_guess = (-1,-1)
guess_orientation = ""
left_and_right = 0
up_and_down = 0
hit_pos = (-1,-1)

def get_board():

    return [["🌫️" for i in range(10)] for i in range(10)]

bot_field = get_board()
player_field = get_board()
player_field_solution = get_board()

def generate_bot_ships(ships_length: list, ships_positions: list):
    print(ships_length)
    print(ships_positions)
    indicator = 0
    orientation = random.choice(["x","y"])
    ship = random.choice(ships_length)

    if not ships_length:
        return

    if orientation == "x":
        x = random.choice(list(range(10)))
        y1 = random.choice(list(range(10)))
        print(ship)
        
        y2 = y1 + ship - 1 if y1 + ship - 1 < 10 and y1 + ship - 1 >= 0 else y1 - ship + 1

        new_ship_positions = [(x, y) for y in range(min(y1,y2), max(y1,y2) + 1)]

    else:
        y = random.choice(list(range(10)))
        x1 = random.choice(list(range(10)))
        print(ship)
        
        x2 = x1 + ship - 1 if x1 + ship - 1 < 10 and x1 + ship - 1 >= 0 else x1 - ship + 1

        new_ship_positions = [(x, y) for x in range(min(x1,x2),max(x1,x2) + 1)]

    if any(pos in ships_positions for pos in new_ship_positions):
        return generate_bot_ships(ships_length, ships_positions)
    
    ships_positions.extend(new_ship_positions)
    ships_length.remove(ship)
    return ships_positions

def start_game_Battleships(user_message: str, ships_positions: list) -> str:
    global game_started

    if user_message.lower().strip() == "end":
        end_game()
        return "The game ended"

    if game_started == True:
        return get_response_Battleships(user_message, ships_positions)

    if user_message.lower() == "battleships":
        return "You have 5 ships with lengths: 2, 3, 4, 5, 6. Choose where you want to put them using the following format: (start_point_coordinate_x, start_point_coordinate_y) (end_point_coordinate_x, end_point_coordinate_y), where the coordinates are a number from 0 to 9."

    try:
        points = []
        for i in user_message:
            if i.isdigit():
                points.append(i)
        
        start_point, end_point = (int(points[0]), int(points[1])), (int(points[2]), int(points[3]))
        print(f"start = {start_point}, end = {end_point}")

    except ValueError:
        return "Invalid input"
    
    if start_point[0] not in range(10) or start_point[1] not in range(10) or end_point[0] not in range(10) or end_point[1] not in range(10):
        return "Invalid coordinates"
    
    if start_point[0] != end_point[0] and start_point[1] != end_point[1]:
        return "Invalid coordinates"
    
    global player_ships_positions
    global player_ships_length
    global player_field_solution

    positions_taken = player_ships_positions.copy()
    field = player_field_solution.copy()
    if start_point[0] == end_point[0]:

        ship = abs(start_point[1] - end_point[1]) + 1
        if ship not in player_ships_length:
            return f"You've already put a ship with size {ship}"

        for i in range(min(start_point[1], end_point[1]), max(start_point[1], end_point[1]) + 1):
            if (start_point[0], i) in player_ships_positions:
                player_ships_positions = positions_taken
                player_field_solution = field
                return "You are crossing another ship"

            player_ships_positions.append((start_point[0], i))
            player_field_solution[start_point[0]][i] = "🚢"

        player_ships_length.remove(ship)
        
    else:

        ship = abs(start_point[0] - end_point[0]) + 1
        if ship not in player_ships_length:
            return f"You've already put a ship with size {ship}"
        
        for i in range(min(start_point[0], end_point[0]), max(start_point[0], end_point[0]) + 1):
            if (i, start_point[1]) in player_ships_positions:
                player_ships_positions = positions_taken
                player_field_solution = field
                return "You are crossing another ship"
            
            player_ships_positions.append((i, start_point[1]))
            player_field_solution[i][start_point[1]] = "🚢"

        player_ships_length.remove(ship)
    
    field = str('\n'.join(' '.join(row) for row in player_field_solution))+"\n"
    if player_ships_length:    
        print(field)
        return f"You placed the ship with size {ship}, left sizes: {player_ships_length} \n{field}"
    else:
        game_started = True
        player_ships_length = [2, 3, 4, 5, 6]
        return f"You placed all ships :). Now it's time to guess. Good luck! \n{field}"
    
def get_response_Battleships(user_message: str, ships_positions: list) -> str:

    global player_ships_length
    global player_guesses
    global bot_field

    coord = []

    for i in user_message:
        if i.isdigit():
            coord.append(i)

    if len(coord)!= 2:
        return "Invalid input"
    
    x,y = int(coord[0]), int(coord[1])
    if x < 0 or x >= 10 or y < 0 or y >= 10:
        return "Invalid coordinates"
    
    if (x,y) not in player_guesses:
        player_guesses.append((x,y))
    else:
        return "You've already hit this spot"

    if (x,y) in ships_positions:
        bot_field[x][y] = "💥"
        field = '\n'.join(' '.join(row) for row in bot_field)

        if all(ship in player_guesses for ship in ships_positions):
            end_game()
            return "Congrats, YOU WON! You found all my ships 😊"

        return f"Good job! My field:\n{field} \nYour turn again!"
    
    else:
        bot_field[x][y] = "❌"
        field = '\n'.join(' '.join(row) for row in bot_field)

        return f"My field:\n{field} \nYou've missed😞 {bot_guess()}\n"
    
def valid_up_and_down():
    up_down = {"up":(prev_guess[0] - 1, prev_guess[1]),
                "down":(prev_guess[0] + 1, prev_guess[1])}
    return dict(filter(lambda item: item[1][0] >= 0 and item[1][0] < 10 and item[1][1] >= 0 and item[1][1] < 10 and item[1] in positions, 
                              up_down.items()))
def valid_left_and_right():
    left_right = {"left":(prev_guess[0], prev_guess[1] - 1),
                "right":(prev_guess[0], prev_guess[1] + 1)}
    return dict(filter(lambda item: item[1][0] >= 0 and item[1][0] < 10 and item[1][1] >= 0 and item[1][1] < 10 and item[1] in positions, 
                              left_right.items()))
def bot_guess():

    global positions
    global prev_guess
    global up_and_down
    global left_and_right
    global hit_pos
    global player_field
    global guess_orientation

    print(f"valid lr = {valid_left_and_right()}")
    print(f"valid ud = {valid_up_and_down()}")
    valid_moves = {**valid_left_and_right(), **valid_up_and_down()}
    print(f"valid moves = {valid_moves}")
    print("and here...")
    print(f"prev_guess now = {prev_guess}")

    if prev_guess != (-1,-1) and guess_orientation == "":
        print("L")
        hit_pos = prev_guess
        move = random.choice(list(valid_moves.items()))
        print(f"move = {move}")
        guess_orientation = move[0]
        print(f"guess_orientation = {guess_orientation}")
        guess = move[1]
        print(f"guess = {guess}")

        if guess in player_ships_positions:
            prev_guess = guess
            if guess_orientation == "up" or guess_orientation == "down":
                up_and_down = len(valid_up_and_down()) + 1
                print(f"up and down = {up_and_down}")
            else:
                left_and_right = len(valid_left_and_right()) + 1
                print(f"left and right = {left_and_right}")
        else:
            guess_orientation = ""
        
    elif prev_guess != (-1,-1) and guess_orientation == "up":
        print("LL")
        if "up" in valid_moves:
            guess = valid_moves["up"]

            if guess in player_ships_positions:
                prev_guess = guess
            else:
                up_and_down -= 1
                if up_and_down == 0:
                    prev_guess = (-1,-1)
                    guess_orientation = ""
                else:
                    guess_orientation = "down"
                    prev_guess = hit_pos
        
        else:
            if up_and_down == 0:
                prev_guess =(-1,-1)
                guess_orientation = ""
                guess = random.choice(positions)
            
            else:
                prev_guess = hit_pos
                guess_orientation = "down"
                guess = (prev_guess[0] + 1, prev_guess[1])
    
    elif prev_guess != (-1,-1) and guess_orientation == "down":
        print("LLL")
        if "down" in valid_moves:
            guess = valid_moves["down"]

            if guess in player_ships_positions:
                prev_guess = guess
            else:
                up_and_down -= 1
                if up_and_down == 0:
                    prev_guess = (-1,-1)
                    guess_orientation = ""
                else:
                    guess_orientation = "up"
                    prev_guess = hit_pos
        
        else:
            if up_and_down == 0:
                prev_guess =(-1,-1)
                guess_orientation = ""
                guess = random.choice(positions)
            
            else:
                prev_guess = hit_pos
                guess_orientation = "up"
                guess = (prev_guess[0] - 1, prev_guess[1])
    
    elif prev_guess != (-1,-1) and guess_orientation == "left":
        print("LLLL")
        if "left" in valid_moves:
            guess = valid_moves["left"]

            if guess in player_ships_positions:
                prev_guess = guess
            else:
                left_and_right -= 1
                if left_and_right == 0:
                    prev_guess = (-1,-1)
                    guess_orientation = ""
                else:
                    guess_orientation = "right"
                    prev_guess = hit_pos
        else:
            if left_and_right == 0:
                prev_guess =(-1,-1)
                guess_orientation = ""
                guess = random.choice(positions)
            
            else:
                prev_guess = hit_pos
                guess_orientation = "right"
                guess = (prev_guess[0], prev_guess[1] + 1)

    elif prev_guess != (-1,-1) and guess_orientation == "right":
        print("LLLLL")
        if "right" in valid_moves:
            guess = valid_moves["right"]

            if guess in player_ships_positions:
                prev_guess = guess
            else:
                left_and_right -= 1
                if left_and_right == 0:
                    prev_guess = (-1,-1)
                    guess_orientation = ""
                else:
                    guess_orientation = "left"
                    prev_guess = hit_pos
        else:
            if left_and_right == 0:
                prev_guess =(-1,-1)
                guess_orientation = ""
                guess = random.choice(positions)
            
            else:
                prev_guess = hit_pos
                guess_orientation = "left"
                guess = (prev_guess[0], prev_guess[1] - 1)

    else:
        print("yayy")
        guess = random.choice(positions)

    print(f"guess = {guess}")

    positions.remove(guess)
    indicator = False
    if guess in player_ships_positions:
        if all(i not in positions for i in player_ships_positions):
            field_solution = str('\n'.join(' '.join(row) for row in player_field_solution))
            lost = f"You lost 😞. Better luck next time! \n{field_solution}"
            end_game()
            return lost
        indicator = True
        prev_guess = guess
        print(f"prev guess = {prev_guess}")
        player_field_solution[guess[0]][guess[1]] = "💥"
        bot_guess()
       
    else:
        player_field_solution[guess[0]][guess[1]] = "❌"
    field_solution = str('\n'.join(' '.join(row) for row in player_field_solution))
    
    if indicator:
        return f"I've guessed correctly. My guesses: \n{field_solution}. \nYour turn!"
    return f"I've missed 😢. My guess: \n{field_solution}  \nYour turn!"
   
def end_game():

    global player_ships_positions
    global player_ships_length
    global game_started
    global player_guesses
    global positions
    global prev_guess
    global up_and_down
    global left_and_right
    global hit_pos
    global player_field
    global guess_orientation

    player_ships_length = [2, 3, 4, 5, 6]
    player_ships_positions = []
    game_started = False
    positions = [(x,y) for x in range(10) for y in range(10)]
    player_guesses = []
    prev_guess = (-1,-1)
    guess_orientation = ""
    left_and_right = 0
    up_and_down = 0
    hit_pos = (-1,-1)
