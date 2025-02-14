async def send_message_Battleships(message: Message, user_message: str) -> None:
    try:
        response: str = start_game_Battleships(user_message, ships_positions)
        if response == "You lost :(. Better luck next time!" or response == "Congrats, YOU WON! You found all my ships :)" or response == "End":
            end_game_Battleships()
        await message.author.send(response)
    except Exception: #create exception
        print("No")