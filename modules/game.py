import sys
import random
from modules.score_keeping import get_score_time, get_current_time
import colorama
from colorama import Fore

colorama.init(autoreset=True)


def get_wrong_answers(question_data, fun):
    if fun:
        wrong_answers = question_data['wrong_answers'][:]
        wrong_answers.pop(random.randint(0, 2))
        wrong_answers.append(question_data['funny_answer'])
    else:
        wrong_answers = question_data['wrong_answers']
    return wrong_answers


def ask_questions(question_data, lifelines, fun):
    """Display the question, collect the user's answer, and offer lifeline options."""
    question = question_data['question']
    wrong_answers = get_wrong_answers(question_data, fun)
    answers = [question_data['right_answer']] + wrong_answers

    # Shuffle the answers to randomize the positions
    random.shuffle(answers)
    answers.append('Use a lifeline')

    options = ["A", "B", "C", "D"]
    while True:
        # 1. Display the question and possible answers
        print(f"\n{Fore.CYAN}Question: {question}")
        for i, answer in enumerate(answers):
            print(f"{Fore.YELLOW}{chr(i + 65)}) {Fore.RESET}{answer}")

        # 2. Get the user's answer
        display_options = options + ["E"]
        try:
            user_input = input(f"{Fore.YELLOW}Enter your answer ({', '.join(display_options)}): ").upper()
        except KeyboardInterrupt:
            print(f'{Fore.RED}\nLeaving so soon? Too sad. Schade. Tschüss!')
            sys.exit(0)

        if user_input not in display_options:
            print(Fore.RED + "Invalid input. Please try again.")
            continue

        if user_input == "E":  # lifeline logic
            if not any(value for value in lifelines.values()):
                print(Fore.RED + "There is no lifelines left.")
                continue
            lifeline_result = use_lifeline(lifelines, question_data, fun)
            if lifeline_result == "skip":
                return "skip"  # The user chose to skip the question
            elif lifeline_result == "hint":
                print(f"{Fore.MAGENTA}Hint: {question_data['hint']}")
            elif isinstance(lifeline_result, list):
                # If the 50/50 lifeline was used, update the displayed answers
                answers = lifeline_result
                options = options[:2]
            continue

        if user_input in "ABCD":
            selected_answer = answers[ord(user_input) - 65]  # Convert the input to an index
            return selected_answer == question_data['right_answer']


def apply_fifty_fifty(question_data, fun):
    """Applies the 50/50 lifeline to remove two wrong answers."""
    wrong_answers = get_wrong_answers(question_data, fun)

    # Randomly remove two wrong answers
    wrong_to_remove = random.sample(wrong_answers, 2)
    remaining_answers = [question_data['right_answer']] + [a for a in wrong_answers if a not in wrong_to_remove]
    random.shuffle(remaining_answers)
    return remaining_answers


def use_lifeline(lifelines, question_data, fun):
    """Handles the lifeline options for the user."""
    while True:
        print("\nChoose a lifeline:")
        
        choice_dict = {}
        number = 1
        for key, value in lifelines.items():
            if value:
                print(f'{Fore.YELLOW}{number}. {Fore.RESET}{value[1]}')
                choice_dict[str(number)] = key
                number += 1
        print(f'{Fore.YELLOW}{number}.{Fore.RESET} No lifeline')

        choice = input(Fore.YELLOW + "Enter the number of your choice: ")

        if choice == str(number):
            return None  # No lifeline chosen
        elif choice_dict[choice] == 'fifty_fifty':
            lifelines['fifty_fifty'] = False  # Disable the 50/50 lifeline after use
            return apply_fifty_fifty(question_data, fun)
        elif choice_dict[choice] == 'skip':
            lifelines['skip'] = False  # Disable the skip lifeline after use
            return "skip"
        elif choice_dict[choice] == 'hint':
            lifelines['hint'] = False  # Disable the hint lifeline after use
            return "hint"
        else:
            print(Fore.RED + "Invalid choice. Please try again.")


def play_the_game(questions_list, lifelines, fun=False):
    """Main game loop to manage the flow of questions and scoring."""
    print(Fore.CYAN + "Let's go!")

    # 1. Lifeline flags (already passed in the function call)
    lives = 3
    total_score = 0
    timer = 60  # Maximum time available for onr question (in seconds)
    question_count = 0  # Track the number of questions asked
    right_answers = 0  # Track the number of the right answers
    random.shuffle(questions_list)

    while ((lifelines['skip'] and question_count < len(questions_list) - 1)
            or (not lifelines['skip'] and question_count < len(questions_list))):
        # 2. Fetch the next question
        question_data = questions_list[question_count]
        print(f"{Fore.CYAN}\nQuestion {question_count + 1}")

        # 3. Record the time taken for the answer
        start_time = get_current_time()

        # Ask the user the current question, with lifelines offered
        result = ask_questions(question_data, lifelines, fun)

        end_time = get_current_time()

        # 4. Handle skipped questions (if a skip lifeline is used)
        if result == "skip":
            question_count += 1  # Move to the next question without penalizing the player
            continue

        # 5. Calculate score based on time and correctness
        if result:
            print(Fore.GREEN + "Correct!")
            # Function to calculate score based on the time taken (you need to define this in score_keeping)
            total_score += get_score_time(start_time, end_time, timer)
            right_answers += 1
        else:
            print(f"{Fore.RED}Wrong! {Fore.CYAN}The correct answer was: {Fore.GREEN}{question_data['right_answer']}.")
            if lives > 1:
                lives -= 1
                if lives == 1:
                    print(f"{Fore.CYAN}You lost one life for that wrong answer! Only "
                          f"{Fore.GREEN}{lives}{Fore.CYAN} life left.")
                else:
                    print(f"{Fore.CYAN}You lost one life for that wrong answer! "
                          f"Only {Fore.GREEN}{lives}{Fore.CYAN} lives left.")
            else:
                print(Fore.RED + "You lost! No more lives at stack!")
                break  # Break the loop if lives = 0
            
        # 6. Display the current total score
        print(f"{Fore.CYAN}Your current score: {Fore.GREEN}{int(total_score):}")
        question_count += 1  # Move to the next question

    # Game over
    return right_answers, total_score
