import requests
import random

def get_categories():
    categories_url = "https://the-trivia-api.com/v2/categories"
    categories_data = requests.get(categories_url)
    categories_dict = categories_data.json()
    return categories_dict

url = "https://the-trivia-api.com/v2/questions"

difficulties = ["easy", "medium", "hard", "All"]
categories = [item[0] for item in get_categories().values()]+["All"]
types = ["Questions with open answers", "Questions with 4-option answers", "Both"]

category_index = 0
difficulty_index = 0
type_index = 0
count_index = 0

chosen_categories = []
chosen_difficulty = []
chosen_type = []
chosen_count = 0

questions = []
question_index = -1
question_type = ""
correct_answer = ""

correct_open_answers = 0
correct_closed_answers = 0

print_categories = [item[0] for item in get_categories().items()]
print_categories.append("All")

def pretty_print(question_characteristic) -> str:
    index = 0
    result = ""
    for i in question_characteristic:
        result += f"\n{index}. {i}"
        index += 1

    return result

def url_characteristics(question_characteristic: list, chosen_question_characteristic: list):
    
    s = set(chosen_question_characteristic)
    if  len(question_characteristic) - 1 in s:
        print("h")
        return "All"
    
    return list(s)

def get_response_Quiz(user_input: str) -> str:

    try:
        if user_input.lower() == "quiz":
            return f"Choose a category: {pretty_print(print_categories)} \nWrite the numbers of the categories you want to be included."
        if user_input.lower() == "end":
            end_game_Quiz()
            return "The game ended"
        
        global category_index
        global difficulty_index
        global type_index
        global count_index

        global chosen_categories
        global chosen_count
        global chosen_type
        global chosen_difficulty

        global questions
        global question_type  #add
        global correct_open_answers
        global correct_closed_answers

        if category_index == 0:
            chosen_categories = []
            if "10" in user_input:
                chosen_categories.append(9)
                user_input = [item for item in user_input if item != "10"]
            if "11" in user_input:
                chosen_categories.append(10)
                user_input = [item for item in user_input if item != "11"]
                
            for i in user_input:
                if i.isdigit() and i != '0':
                    chosen_categories.append(int(i) - 1)
            print(f"chosed cat2 = {chosen_categories}")

            if chosen_categories == []:
                return "There's no such category"
            
            category_index = 1
            return f"Choose difficulty: {pretty_print(difficulties)}\n Write the numbers: "
        
        elif difficulty_index == 0:
            chosen_difficulty = []
            for i in user_input:
                if i.isdigit() and i in ["1", "2", "3", "4"]:
                    chosen_difficulty.append(int(i) - 1)

            if chosen_difficulty == []:
                return "There's no such difficulty"
            
            difficulty_index = 1
            return f"Choose type of questions: {pretty_print(types)}\n Write the numbers: "

        elif type_index == 0:
            chosen_type = []
            for i in user_input:
                if i.isdigit() and i in ["1", "2", "3"]:
                    chosen_type.append(int(i) - 1)

            if chosen_type == []:
                return "There's no such type"
            
            type_index = 1
            return "Choose the count of questions - choose a number from 1 to 20:"
        
        elif count_index == 0:
            chosen_count = int(user_input)
            if chosen_count not in range(1,21):
                return "Invalid count"
            
            count_index = 1
            questions = get_questions()
            return f"Let's begin the quiz! If there are options for the answer - write the letter of the answer you choose. Good luck! \n{ask_question()}"

        else:
            guess = False
            if question_type == "closed":

                if user_input.upper().strip() == correct_answer.upper():
                    guess = True
                    correct_closed_answers += 1
                else: 
                    guess = False

            else:
                if user_input.lower() == get_correct_answer().lower():
                    guess = True
                    correct_open_answers += 1
                else:
                    guess = False

            if url_characteristics(types, chosen_type) == "All": #add
                question_type = "both"
            
            if question_index + 1 == chosen_count: #add
                print("I am here...")
                if guess:
                    return f"Correct 😊! You guessed {correct_closed_answers + correct_open_answers} out of {chosen_count}" #put c
                else:
                    return f"Wrong 😞 You guessed {correct_closed_answers + correct_open_answers} out of {chosen_count}"  #put c

            if guess:
                return f"Correct😊! \n{ask_question()}"
            return f"Wrong 😞 \n{ask_question()}"
    except ValueError:
        return "Invalid input"

def build_url() -> str:

    global question_type
    link = f"?limit={chosen_count}"

    c = url_characteristics(categories, chosen_categories)
    if c != "All":
        print(c)
        link += "&categories="
        for i in c:
            link += categories[i] + ","
        link = link[:-1]

    d = url_characteristics(difficulties, chosen_difficulty)
    if d != "All":
        link += "&difficulty="
        for i in d:
             link += difficulties[i] + ","
        link = link[:-1]

    if url_characteristics(types, chosen_type) == "All":
        question_type = "both"
    elif 0 in chosen_type:
        question_type = "open"
    else:
        question_type = "closed"
    
    return url + link

def get_questions():

    questions_url = build_url()
    questions_data = requests.get(questions_url)
    questions_list = questions_data.json()
    return questions_list

def ask_question() -> str:
    global question_index
    global question_type
    global correct_answer

    if question_type == "both":
        question_type = random.choice(["open", "closed"]) #add choice

    question_index += 1
    q = questions[question_index]["question"]["text"]
    print(f"q = {q}")
    
    print(f"correct answer = {get_correct_answer()}")
    print(f"answers = {get_answers()}")
    if question_type == "closed":
        for i,j in zip(get_answers(),["A", "B", "C", "D"]):
            if i == get_correct_answer():
                correct_answer = j
                print(f"c.a = {correct_answer}")
            q += f"\n{j}. {i}"

    print(f"question_index = {question_index}")
    print(f"chosen_count = {chosen_count}")
    return q

def get_correct_answer():
    return questions[question_index]["correctAnswer"]

def get_answers():
    answers = questions[question_index]["incorrectAnswers"] + [get_correct_answer()]
    random.shuffle(answers)   #add
    return answers

def get_correct_answers_points():
    return correct_closed_answers + correct_open_answers*2

def end_game_Quiz():

    global category_index
    global difficulty_index
    global type_index
    global count_index

    global chosen_categories
    global chosen_count
    global chosen_type
    global chosen_difficulty

    global questions
    global question_index
    global question_type
    global correct_answer

    global correct_open_answers
    global correct_closed_answers
    
    category_index = 0
    difficulty_index = 0
    type_index = 0
    count_index = 0

    chosen_categories = []
    chosen_difficulty = []
    chosen_type = []
    chosen_count = 0

    questions = []
    question_index = 0
    question_type = ""
    correct_answer = ""

    correct_open_answers = 0
    correct_closed_answers = 0