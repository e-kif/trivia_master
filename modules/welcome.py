import colorama
from colorama import Fore

colorama.init(autoreset=True)


def greet_player():
    print(f"{Fore.CYAN}Hello stranger.\nI welcome you to a game of {Fore.YELLOW}'Who Wants to Be a Trivia Master?'.")
    print(Fore.CYAN + "I invite you to test your knowledge.\n"
                      "If you dare.")


def get_player_name():
    while True:
        try:
            player_name = input(Fore.YELLOW + "What would you like to be called, brave one?\n>>> ").strip()

            if player_name == "":
                print(Fore.CYAN + "Okay, we shall call you Blank then.")
                return "Blank"

            return player_name

        except KeyboardInterrupt:
            print(Fore.RED + "\nInput was interrupted by the user. Please enter a name again. ")
            continue


def explain_rules():
    print(Fore.CYAN + """
    The rules are simple. You get to choose one category. 
    You will be presented questions about said category. 
    Only one of the given 4 answers is correct, so choose wisely!
    You have 60 seconds to answer each question. If your time is up, you loose.
    If you enter a wrong answer, you loose. 
    You have the opportunity of using one of 3 lifelines. 
    So take your chances!
    If you answer all questions correctly, you can call yourself the true trivia master
    and mention this in your podcast. Hooray!
    """)


def get_category():
    while True:
        try:
            choose_category = input(f"""
{Fore.CYAN}Please choose one of the following categories:
{Fore.CYAN}Enter{Fore.YELLOW} "A" {Fore.CYAN}for{Fore.YELLOW} 'Very good movies.'
{Fore.CYAN}Enter{Fore.YELLOW} "B" {Fore.CYAN}for{Fore.YELLOW} 'Super tasty international food.'
{Fore.CYAN}Enter{Fore.YELLOW} "C" {Fore.CYAN}for{Fore.YELLOW} 'Pretty awesome books.'
{Fore.CYAN}Enter{Fore.YELLOW} "D" {Fore.CYAN}for{Fore.YELLOW} 'You can’t go there. Seriously.'
{Fore.CYAN}Enter{Fore.YELLOW} "E" {Fore.CYAN}for{Fore.YELLOW} 'Can’t decide? Pick random trivia!'
{Fore.CYAN}Enter{Fore.YELLOW} "F" {Fore.CYAN}for{Fore.YELLOW} 'You can’t touch this. At least you shouldn’t.'
""").strip().lower()

            if choose_category not in ["a", "b", "c", "d", "e", "f"]:
                if choose_category == "":
                    print(Fore.CYAN + "Just pick a category. It's not that hard. ")
                else:
                    print(Fore.CYAN + "Sorry what? Please enter a letter from A to B. ")
                continue

            return choose_category

        except KeyboardInterrupt:
            print(Fore.RED + "\nInput was interrupted by the user. Please enter a letter for category again. ")
            continue


def welcome_player():
    greet_player()

    name = get_player_name()

    print(f"Greetings {name}! Shall we proceed!?")

    explain_rules()

    category = get_category()

    return name, category
