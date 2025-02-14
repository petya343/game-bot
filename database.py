import pymysql
from typing import Final
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME: Final[str] = os.getenv('DATABASE_USER')
PASSWORD: Final[str] = os.getenv('DATABASE_PASSWORD')
NAME: Final[str] = os.getenv('DATABASE_NAME')
conn = pymysql.connect(host = "sql7.freesqldatabase.com", user = USERNAME, password = PASSWORD, database = NAME)

def add_user(username: str):

    cursor = conn.cursor()

    select_query: str = f"SELECT * FROM leaderboard WHERE name = '{username}'"
    cursor.execute(select_query)
    user = cursor.fetchone()
    print(f"user = {user}")
    
    if user is None:
        
        insert_query: str = f"INSERT INTO leaderboard (name, tic_tac_toe, battleships, bulls_and_cows, quiz, all_points, rank, achievements) VALUES ('{username}', 0, 0, 0, 0, 0, 'Unranked', 0)"
        cursor.execute(insert_query)
        conn.commit()
        print(f"User {username} added to the database.")

    else:
        print(f"User {username} already exists.")
    
    cursor.close()

rank_system = {0:"bronze",
               200:"silver",
               500:"gold",
               1000:"diamond"}

def won_TicTacToe(username: str):

    cursor = conn.cursor()

    if get_rank(username) == get_new_rank(get_all_points(username), 5):

        update_query = f"""
        UPDATE leaderboard
        SET tic_tac_toe = tic_tac_toe + 5,
        all_points = all_points + 5
        WHERE name = '{username}'
        """
    else:
        
        new_rank = get_new_rank(username, 5)
        update_query = f"""
        UPDATE leaderboard
        SET tic_tac_toe = tic_tac_toe + 5,
        all_points = all_points + 5
        rank = '{new_rank}
        WHERE name = '{username}'
        """
         
    cursor.execute(update_query)
    conn.commit()
    cursor.close() 
    if compare_ranks:
        return f"Congrats! You ranked up!!! Now your rank is {new_rank} 😊"
    return ""  

def won_Battleships(username: str):

    cursor = conn.cursor()

    if get_rank(username) == get_new_rank(get_all_points(username), 25):

        update_query = f"""
        UPDATE leaderboard
        SET battleships = battleships + 25,
        all_points = all_points + 25
        WHERE name = '{username}'
        """
    else:
        
        new_rank = get_new_rank(get_all_points(username), 25)
        update_query = f"""
        UPDATE leaderboard
        SET battleships = battleships + 25,
        all_points = all_points + 25
        rank = '{new_rank}
        WHERE name = '{username}'
        """
         
    cursor.execute(update_query)
    conn.commit()
    cursor.close()
    if compare_ranks:
        return f"Congrats! You ranked up!!! Now your rank is {new_rank} 😊"
    return ""

def won_BullsandCows(username: str):
    cursor = conn.cursor()

    if get_rank(username) == get_new_rank(get_all_points(username), 40):
        print("ouch")

        update_query = f"""
        UPDATE leaderboard
        SET bulls_and_cows = bulls_and_cows + 40,
        all_points = all_points + 40
        WHERE name = '{username}'
        """
    else:
        print("ouch22")
        new_rank = get_new_rank(get_all_points(username), 40)

        update_query = f"""
        UPDATE leaderboard
        SET bulls_and_cows = bulls_and_cows + 40,
        all_points = all_points + 40
        rank = '{new_rank}'
        WHERE name = '{username}'
        """
    
    print("ouchhhh")
    cursor.execute(update_query)
    print("ooo yeee")
    conn.commit()
    cursor.close()
    if compare_ranks:
        return f"Congrats! You ranked up!!! Now your rank is {new_rank} 😊"
    return ""

def good_quiz(username: str, points: int):
    cursor = conn.cursor()

    if get_rank(username) == get_new_rank(get_all_points(username), points):

        update_query = f"""
        UPDATE leaderboard
        SET quiz = quiz + {points},
        all_points = all_points + {points}
        WHERE name = '{username}'
        """
    else:
        new_rank = get_new_rank(get_all_points(username), points)
        update_query = f"""
        UPDATE leaderboard
        SET quiz = quiz + {points},
        all_points = all_points + {points}
        rank = '{new_rank}
        WHERE name = '{username}'
        """
         
    cursor.execute(update_query)
    conn.commit()
    cursor.close()
    if compare_ranks:
        return f"Congrats! You ranked up!!! Now your rank is {new_rank} 😊"
    return ""

def get_all_points(username: str):

    cursor = conn.cursor()
    select_query = f"SELECT all_points FROM leaderboard WHERE name = '{username}'"

    cursor.execute(select_query)
    result = cursor.fetchone()
    all_points = result[0]
    cursor.close()
    return all_points  

def get_rank(username: str):

    cursor = conn.cursor()
    select_query = f"SELECT rank FROM leaderboard WHERE name = '{username}'"

    cursor.execute(select_query)
    result = cursor.fetchone()
    rank = result[0]
    cursor.close()
    return rank 

def get_new_rank(all_points: int, add_points: int):
    all_points += add_points
    rank = ""
    for i in rank_system.keys():
        if i <= all_points:
            rank = rank_system[i]
    print(f"new_rank = {rank}")
    return rank

def compare_ranks(username:str, all_points: int, add_points: int):
    if get_rank(username) == get_new_rank(all_points, add_points):
        return False
    return True