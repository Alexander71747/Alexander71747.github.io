import csv
import os
#OS allows us to access directory and Check if a file exists

import subprocess
#downloaded with the help of chatgpt
#module allows Python to run system commands as if they were executed in a terminal or command prompt
import platform
#this an extra process to check the system of the computer that the propgram is running on
#The platform module provides tools to identify the operating system and environment.

#Below is the module (suggested by Microsoft Co-Pilot) to import to encrypt 
# 1) Profile passwords
# 2) Quiz answers 
import bcrypt
#Below is suggested code snippet to encrypt a password inserted by the user
# Hashing a password: 
# password = "my_secure_password".encode('utf-8') 
# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
#this third party tool is used to: 1) hash and salt (basically encrypt) 
#account passwords so that only the user can access their account; 2) hash
# and salt quiz answer keys so that you can't cheat by opening the csv file
#to see the answers to the quizzes. If you are actually able to crack this, 
#you probably know all of the content in this course.
#Microsoft co-pilot was used as a search tool to find a way to hash this 
#information and to solve some debugging issues (helping me pin-point the issue)
#I fully understood how to use bcrypt thanks to the following video on Youtube:
#https://youtu.be/hNa05wr0DSA?si=yuMnijITv7I2h8u6


#To solve: 
# 1) Update csv levels
# 3) matplotlib for user performance
# 4) User interface function
# 5) Way to seamlessly open pdfs and matplot libs in-app
# 6) Clean code to make internal comments nicer

import matplotlib.pyplot as plt
#This will generate the resuts of the user after taking the quiz. Specifically, it will show a graphical represenation of the users score after taking the quiz.
'''


#encrypt the password

'''
# Constants for file paths
USER_DATA_FILE = "user_data.csv"
QUIZ_DATA_FILE = "quiz_data.csv"

# Function Definitions
def menu_1():
    """
    INPUT: Nothing is passed as an argument, but the user types in information
    OUTPUT: Returns a variable indicating the user's choice.
    USAGE: This function represents the first menu in the program flow chart.
    """
    user_menu_1 = """
    Please select one of these 3 options (Entries are case sensitive):
    > Login       = Log back into your profile to keep learning!
    > New Profile = Start your interactive Python educational journey!
    > Exit        = Exit the program
    """
    user_choice = input(user_menu_1)
    while user_choice not in ["Login", "New Profile", "Exit"]:
        user_choice = input("Option entered incorrectly; please retry: ")
    return user_choice


def new_profile(csv_file):
    """
    INPUT: User information to be typed in and a csv file containing user data.
    OUTPUT: User information is added to a CSV file that stores all user data.
    USAGE: The function appends new user information to a CSV file.
    """
    user_instructions = """
    Create a new profile by inserting the following:
    > Username
    > Password
    If in the username field "BACK" is inserted (case sensitive), you will be redirected to the previous Menu.
    """
    print(user_instructions)
    username = input("Please insert your new username: ")

    if username == "BACK":
        return username

    # Check if username exists
    with open(csv_file, newline='', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        usernames = [row["Username"] for row in reader]

    while username in usernames:
        username = input("Username already taken. Please insert a different one: ")

    password = input("Please insert your password. It cannot be BACK: ")
    while password == "BACK":
        password = input("You have entered BACK. Please choose a different password: ")
    password = password.encode('utf-8')
    #default rounds for encryption is 12 
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Append to CSV
    with open(csv_file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #when changing the format from decode password to current, invalid salt occurs
        #before, the while used to always return false
        writer.writerow([username, password.decode('utf-8'), 1])

    print("Profile created successfully!")
    return username


def login(csv_file):
    """
    INPUT: User information is typed in (username and password).
    OUTPUT: user name (unique), is returned to menu_2
    USAGE: The function verifies a user's identity.
    """
    user_instructions = """
    Login to your profile by inserting:
    > Username
    > Password
    """
    print(user_instructions)
    username = input("Please insert your username (or type BACK to go back): ")

    # Fetch user data
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        users = {row["Username"]: row["Password"] for row in reader}

    while username not in users and username != "BACK":
        username = input("Username not found. Please retry (or type BACK to go to the menu): ")

    if username == "BACK":
        return username

    password = input("Please insert your password: ")
    if password == "BACK":
        return "BACK"
    #do this to convert in byte input in byte format
    password = password.encode('utf-8')
    hashed_password = users.get(username)
    #encode method is used to convert string from table into bytes
    hashed_password = hashed_password.encode('utf-8')
    while not bcrypt.checkpw(password, hashed_password):
        password = input("Incorrect password. Please retry (or type BACK to go to the menu): ")
        password = password.encode('utf-8')

    if password == "BACK":
        return "BACK"

    print(f"Login successful! Welcome, {username}.")
    return username


def menu_2(username):
    """
    INPUT: username is passed to manage user-specific options.
    OUTPUT: User choice from the secondary menu.
    USAGE: Provides options for lectures, quizzes, or exiting the program.
    """
    user_menu_2 = f"""
    Welcome, {username}!
    Please choose an option:
    > Lecture = Continue learning with lessons
    > Quiz    = Test your knowledge with a quiz
    > Back    = Go back to the main menu
    > Exit    = Exit the program
    """
    user_choice = input(user_menu_2)
    while user_choice not in ["Lecture", "Quiz", "Back", "Exit"]:
        user_choice = input("Invalid option. Please try again: ")
    return user_choice


#intergrated with the help of chat
def open_pdf(lesson_number):
    """
    INPUT: The lesson number (integer) corresponding to a PDF file. 
        The lesson number will be taken from the progress number in the csv later on
        
    OUTPUT: Opens the specified PDF file in the system's default viewer.
    
    USAGE: Displays the lesson for the user based on the given lesson number.
    warning: will have to return back to wing to continue the program
    """
    
    #this is where os accessess the system diretory and find the pdf file starting with "Lesson"
    pdf_path = f"Lesson {lesson_number}.pdf"
    if not os.path.exists(pdf_path):
        print(f"Lesson {lesson_number}.pdf not found. Ensure the file is in the directory.")
        return False

#this part for "try" is done by chatgpt
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", pdf_path])
        elif platform.system() == "Windows":  # Windows
            os.startfile(pdf_path)
        else:  # Linux and others
            subprocess.run(["xdg-open", pdf_path])
        print(f"Opened {pdf_path}.")
        
    except Exception as e:
        print(f"An error occurred while trying to open {pdf_path}: {e}")
        return False
    return True


def take_quiz(quiz_data_file, lesson_number):
    """
    INPUT: The CSV file for quizzes and the lesson number.
    OUTPUT: Provides a quiz, validates answers, and provides feedback.
    USAGE: Tests the user on content related to the lesson.
    """
    # Open quiz data
    with open(quiz_data_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        quiz_questions = [row for row in reader if row["Level"].startswith(f"{lesson_number}.")]

    if not quiz_questions:
        print(f"No quiz data available for Lesson {lesson_number}.")
        return False

    correct_count = 0
    for question in quiz_questions:
        print(f"Question: {question['Question']}")
       
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        answer = answer.encode('utf-8')
        raw_retrieval = question["Correct Answer"]
        #remove ""
        new_retrieval = raw_retrieval.strip("")
        #convert to bytestring, equating to simple variable
        final_retrieval = new_retrieval.encode('utf-8')
        #equate a boolean variable to the bcrypt function
        bool_variable = bcrypt.checkpw(answer, final_retrieval)
        if (bool_variable == True):
            print("Correct!")
            correct_count += 1
        else:
            print(f"Incorrect!")
                  

    print(f"You answered {correct_count}/{len(quiz_questions)} questions correctly.")
    return correct_count == len(quiz_questions)

def display_performance_graph(correct, total):
    """
    Displays a bar graph of the user's performance.
    """
    labels = ['Correct', 'Incorrect']
    values = [correct, total - correct]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Quiz Performance')
    plt.ylabel('Number of Questions')
    plt.xlabel('Performance')
    plt.show()


def main():
    """
    Main program loop that ties everything together.
    """
    print("Welcome to the Python Learning Program!")

    # Ensure user data file exists
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Username", "Password", "Progress"])

    while True:
        choice = menu_1()

        if choice == "Exit":
            print("Thank you for learning with us. Goodbye!")
            break

        elif choice == "New Profile":
            new_profile(USER_DATA_FILE)

        elif choice == "Login":
            username = login(USER_DATA_FILE)
            if username == "BACK":
                continue

            while True:
                action = menu_2(username)
                if action == "Back":
                    break
                elif action == "Exit":
                    print("Goodbye!")
                    return
                elif action == "Lecture":
                    #Here it asks lesson number once lesson is chosen 
                    progress = int(input("Insert lecture number to open (must be a whole number between 1 and 13):"))
                    #While loop to check input (all inputs must be converted to int)
                    numList = [1,2,3,4,5,6,7,8,9,10,11,12,13] 
                    while (progress not in numList):
                        #re-insert input
                        progress = int(input("Please insert a whole number between 1 and 13: ")) 
                    open_pdf(progress)
                elif action == "Quiz":
                    #Here it asks lesson number once lesson is chosen 
                    progress = int(input("Insert quiz number to open (must be a whole number between 1 and 13):"))
                    #While loop to check input
                    numList2 = [1,2,3,4,5,6,7,8,9,10,11,12,13] 
                    while (progress not in numList2):
                        #re-insert input
                        progress = int(input("Please insert a whole number between 1 and 13: "))
                    take_quiz(QUIZ_DATA_FILE, progress)


# Run the program
#calling the function that intergrates all the functions.
main()
