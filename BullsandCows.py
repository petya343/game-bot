import random

BullsandCows = [num for num in range(1000, 10000) if len(set(str(num))) == 4]

def check_number(bulls: int, cows: int, number: str) -> bool:
    global prev_guess
    new_bulls = 0
    new_cows = 0
    for i, j in zip(number, str(prev_guess)):
        if i == j:
            new_bulls += 1
        elif i in str(prev_guess):
            new_cows += 1
    return new_bulls == bulls and new_cows == cows

prev_guess = 0

def bot_guess_BullsandCows(user_response: str = "") -> int:
    global prev_guess
    global BullsandCows

    if prev_guess == 0:
        prev_guess = random.choice(BullsandCows)
        print(prev_guess)
        return prev_guess
    
    l = []
    bulls = 0
    cows = 0
    for i in user_response:
       if i.isdigit():
           l.append(i)

    if len(l) != 2: 
        return -1
    
    bulls, cows = int(l[0]), int(l[1])
    print(f"{bulls} bulls {cows} cows")
    BullsandCows = [num for num in BullsandCows if check_number(bulls, cows, str(num))]

    if not BullsandCows:
        return -1;

    prev_guess = random.choice(BullsandCows)
    print(prev_guess)
    return prev_guess

def get_BullsandCows(user_input: list, bot_number: str) -> str: 

    bot_bulls = 0
    bot_cows = 0
    for i,j in zip(str(user_input[1]), str(bot_number)):
        if i == j:
            bot_bulls += 1
        elif i in str(bot_number):
            bot_cows += 1

    if bot_bulls == 4:
        end_game()
        return "YOU WON! Congrats, you guessed my number 😊!"
    
    guess = bot_guess_BullsandCows(user_input[0])

    if not BullsandCows:
        end_game()
        return "liar... ;)"
    
    if guess == -1:
        return "invalid bulls and cows"
    
    print(f"{bot_bulls} bulls {bot_cows} cows, {guess}")
    return f"{bot_bulls} bulls {bot_cows} cows, {guess}"

def get_response_BullsandCows(user_input: str, bot_number: str):

    if user_input == "bulls and cows":
        return "Please use the following format: /number/ bulls /number/ cows, /your guess number/. The first move contains only a guess for the number. Good luck!:)"

    if user_input.lower().strip() == "end":
        end_game()
        return "The game ended"
    
    if user_input == "You won":
        end_game()
        return "Yohooo"

    user_input = list(map(lambda x: x.replace(" ",""), user_input.split(",")))
    
    try: 
        if len(user_input) == 1:
            guess = user_input[0]
            user_input = ["", guess]

        user_input[1] = int(user_input[1])
    except ValueError: 
        return "Invalid message format. Please try again."
    
    if int(user_input[1]) not in [num for num in range(1000, 10000) if len(set(str(num))) == 4]:
        return "Not a valid number"
    else:
        print(user_input)
        return get_BullsandCows(user_input, bot_number)
    
def end_game():

    global prev_guess
    global BullsandCows

    prev_guess = 0
    BullsandCows = [num for num in range(1000, 10000) if len(set(str(num))) == 4]
