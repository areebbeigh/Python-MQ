# Author: Areeb Beigh <areebbeigh@gmail.com>

"""
Python MQ (Maths Quiz) - A simple Maths Quiz program
"""

import random
from src.managedb import ManageDB

db = ManageDB()

TOTAL_QUESTIONS = 15  # Edit this to change the total number of questions


def main():
    print("Welcome to Python Maths Quiz\n")
    print("    1. Play")
    print("    2. View Records")
    print()
    choice = int(input("Enter your choice: "))
    if choice == 1:
        play()
    else:
        db.view_records()


def play():
    modes = ("Easy", "Medium", "Hard")
    print("\nChoose a level")
    print("    1. Easy")
    print("    2. Medium")
    print("    3. Hard")
    print("    4. Back")
    print()
    choice = int(input("Enter your choice: "))
    if choice > 4 or choice < 1:
        print("Invalid input")
        play()
    if choice == 4:
        main()
    else:
        difficulty = modes[choice - 1]
        start_game(difficulty)


def generate_expression(difficulty):
    """ Generates a mathematical expression based on the given difficulty """

    signs = ["+", "-"]  # Signs for easy difficulty
    numbers = []

    if difficulty != "Easy":
        for i in range(0, 3):
            numbers.append(random.randrange(100, 300))

    if difficulty == "Easy":
        # Sample expression:  207 - 264 + 202 - 155
        for i in range(0, 4):
            numbers.append(random.randrange(100, 300))
        expression = "{0} {1} {2} {3} {4} {5} {6}".format(
            numbers[0],
            random.choice(signs),
            numbers[1],
            random.choice(signs),
            numbers[2],
            random.choice(signs),
            numbers[3]
        )
    elif difficulty == "Medium":
        # Sample expression: 127 + 112 * 25 - 210
        multiple = random.choice([i for i in range(10, 30) if i % 5 == 0])
        expression = "{0} {1} {2} {3} {4} {5} {6}".format(
            numbers[0],
            random.choice(signs),
            numbers[1],
            "*",
            multiple,
            random.choice(signs),
            numbers[2]
        )
    elif difficulty == "Hard":
        # Sample expression:  293 + 148 * 10 - 148 / 25
        multiple = random.choice([i for i in range(10, 30) if i % 5 == 0])
        dividend = random.choice([i for i in range(10, 30) if i % 5 == 0])
        expression = "{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(
            numbers[0],
            random.choice(signs),
            numbers[1],
            "*",
            multiple,
            random.choice(signs),
            numbers[1],
            "/",
            dividend
        )

    return expression


def end_game(correct, incorrect, questions, difficulty):
    """
    Generates a result based on the given data, prints it, saves it to the database
    and displays the HTML records in a browser
    """

    result = {
        "correct": correct,
        "incorrect": incorrect,
        "accuracy": (correct / questions) * 100,
        "difficulty": difficulty
    }

    db.save_data(result)
    db.view_records()

    print("""Results:
    Correct: {0}
    Incorrect: {1}
    Accuracy: {2}""".format(correct, incorrect, result["accuracy"]))
    input()


def start_game(difficulty):
    """ Starts the game, with the given difficulty (level) """

    level_guide = {
        "Easy": "This round will contain simple addition and subtraction expressions.",
        "Medium": "This round will contain addition, subtraction and multiplication expressions.",
        "Hard": "This round will contain addition, subtraction, multiplication and division expressions."
    }

    print("""
    Quick guide:
        You'll have to answer a total of {0} question. After answering all of them your
        result will be computed, saved in the database and then displayed to you.

        {1}
    """.format(
        TOTAL_QUESTIONS,
        level_guide[difficulty]
    ))

    correct = 0
    incorrect = 0
    questions = 1

    while questions <= TOTAL_QUESTIONS:
        expression = generate_expression(difficulty)
        print()
        print("Q" + str(questions) + ":")
        print(expression)
        answer = round(eval(expression), 2)
        while True:
            try:
                given_answer = float(input("Ans: "))
                break
            except ValueError:
                print("Invalid input")
        if answer == given_answer:
            correct += 1
        else:
            incorrect += 1
            print("Oops! Wrong answer. (Answer: {0})".format(answer))
        if questions == TOTAL_QUESTIONS:
            break
        questions += 1

    end_game(correct, incorrect, questions, difficulty)


main()
