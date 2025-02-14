from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from BullsandCows import get_BullsandCows, get_response_BullsandCows
import random
from battleships import get_board, generate_bot_ships, start_game_Battleships
from tictactoe import get_response_TicTacToe
from quiz import get_response_Quiz, get_correct_answers_points, end_game_Quiz
from database import add_user, won_Battleships, won_BullsandCows, won_TicTacToe, good_quiz

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents = intents)

indicator_game = ""

bot_number = 0

ships_length = [2, 3, 4, 5, 6]
ships_positions = []

def end_game_BullsandCows() -> None:

    global indicator_game
    global bot_number
    bot_number = 0
    indicator_game = ""

def end_game_Battleships() -> None:

    global ships_length
    global ships_positions
    global indicator_game

    ships_length = [2, 3, 4, 5, 6]
    ships_positions = []
    indicator_game = ""

def get_username(message: Message):
    return message.author

async def send_message_BullsandCows(message: Message, user_message: str) -> None:
    try:
        response: str = get_response_BullsandCows(user_message, bot_number)
        await message.author.send(response)

    except discord.errors.Forbidden: 
        print("Couldn't response")

        if response == "liar... ;)" or response == "Yohooo" or response == "The game ended":
            end_game_BullsandCows()
        if response == "YOU WON! Congrats, you guessed my number 😊!":
            end_game_BullsandCows()
            print("IIII")
            rank_up = won_BullsandCows(get_username(message))
            if rank_up != "":
                await message.author.send(rank_up)

async def send_message_Battleships(message: Message, user_message: str) -> None:
    try:
        response: str = start_game_Battleships(user_message, ships_positions)
        await message.author.send(response)

    except discord.errors.Forbidden as e: 
        print(e)

        if response.startswith("You") or response == "The game ended":
            end_game_Battleships()
        if response == "Congrats, YOU WON! You found all my ships 😊":
            end_game_Battleships()
            rank_up = won_Battleships(get_username(message))
            if rank_up != "":
                await message.author.send(rank_up)
    

async def send_message_TicTacToe(message: Message, user_message: str) -> None:
    global indicator_game
    try:
        response: str = get_response_TicTacToe(user_message)
        await message.author.send(response)
    except discord.errors.Forbidden as e: 
        print(e)
        if response == "The game ended" or response.startswith("You") or response == "It's a tie!":
            indicator_game = ""
        if response.startswith("Congrats,"):
            indicator_game = ""
            rank_up = won_TicTacToe(get_username(message))
            if rank_up != "":
                await message.author.send(rank_up)
        
async def send_games(message: Message, user_message: str) -> None:
    try:
        response: str = "Games: \nBulls and cows \nTic Tac Toe \nBattleships \nquiz \nChoose a game and let's play 😊"
        await message.author.send(response)
    except discord.errors.Forbidden as e: 
        print(e)

async def send_message_Quiz(message: Message, user_message: str) -> None:
    global indicator_game
    try:
        response: str = get_response_Quiz(user_message)
        await message.author.send(response)
    except discord.errors.Forbidden as e: 
        print(e)

    if response.startswith("Correct 😊! You guessed") or response.startswith("Wrong 😞 You guessed"):
        indicator_game = ""
        rank_up = good_quiz(get_username(message), get_correct_answers_points())   
        end_game_Quiz()      #!!!!!
        if rank_up != "":
            await message.author.send(rank_up)

async def send_message_Error(message: Message, user_message: str) -> None:
    try:
        response: str = "Invalid input"
        await message.author.send(response)
    except discord.errors.Forbidden as e: 
        print(e)


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)
    user_id: int = message.author.id

    add_user(username)

    print(f'[{channel}] {username}: "{user_message}"')

    user_message = user_message.lower()
    global indicator_game

    if user_message == "games" and indicator_game == "":
        await send_games(message, user_message)
        return

    if user_message == "bulls and cows" and indicator_game == "":
        global bot_number
        bot_number = random.choice([num for num in range(1000, 10000) if len(set(str(num))) == 4])
        print(f"bot_number = {bot_number}")
        indicator_game = "bulls and cows"
        await send_message_BullsandCows(message, user_message)
        return

    if user_message == "battleships" and indicator_game == "":

        indicator_game = "battleships"
        global ships_positions
        global ships_length

        for i in range(5):
            ship_positions = generate_bot_ships(ships_length, ships_positions)

        print(ships_positions)
        await send_message_Battleships(message, user_message)
        return
    
    if user_message == "tic tac toe" and indicator_game == "":
         indicator_game = "tic tac toe"
         await send_message_TicTacToe(message, user_message)
         return
    
    if user_message == "quiz" and indicator_game == "":
        indicator_game = "quiz"
        await send_message_Quiz(message, user_message)
        return
    
    if indicator_game == "":
        await send_message_Error(message, user_message)
        return


    match indicator_game:
        case "bulls and cows":
            await send_message_BullsandCows(message, user_message)
        case "battleships":
            await send_message_Battleships(message, user_message)
        case "tic tac toe":
            await send_message_TicTacToe(message, user_message)
        case "quiz":
            await send_message_Quiz(message, user_message)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()


