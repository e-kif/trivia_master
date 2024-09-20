import colorama
from colorama import Fore
from modules import welcome, wiki
from modules.ai_questions import Questions
from modules.game import play_the_game
import storage.graphics as graphics
from modules.score_ranking import show_scoreboard

colorama.init(autoreset=True)


def main():
    ai_engine = 'gemini'  # either 'gpt' or 'gemini'
    is_fun_answer = True
    use_ai = True

    temp_ai_object = Questions('', '', use_ai, ai_engine)

    # Welcome player and get username + category
    graphics.print_game_intro()
    username, category = welcome.welcome_player()

    # create async task for category title rendering
    graphics.print_category_title(graphics.titles[category], 1, 8)

    # Fetch summaries from Wikipedia based on the selected category
    if temp_ai_object.use_ai:
        summaries = wiki.wiki_call(category)
        if not summaries:
            print(Fore.RED + "No summaries available for this category. Exiting the game.")
            return
    else:
        summaries = ""

    # Generate questions based on the category
    question_generator = Questions(category, summaries, use_ai, ai_engine)
    questions_list = question_generator.get_questions()

    if not questions_list:
        print(Fore.RED + "Could not generate questions. Exiting the game.")
        return
    
    # Initialize lifeline usage (each lifeline can only be used once)
    lifelines = {
        'fifty_fifty': [True, "50/50 Joker (removes two wrong answers)"],
        'skip': [True, "Skip Question"],
        'hint': [True, "Get AI-Generated Hint"]
    }

    # Start the game loop and play the game with generated questions and lifelines
    right_answers, total_score = play_the_game(questions_list, lifelines, is_fun_answer)

    # Add user score to the scoreboard, show up to 5 best players
    show_scoreboard(username, right_answers, total_score, 5)

    print(f"\nThank you for playing, {username}!")


if __name__ == "__main__":
    main()
