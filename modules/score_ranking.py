import os
import json
import colorama
from colorama import Fore

colorama.init(autoreset=True)


def initiate_ranking_dict(questions_length=10):
    ranking_dict = {}
    for number in range(questions_length):
        ranking_dict[number + 1] = []
    return ranking_dict


def get_storage_ranking_info(filename='storage/ranking_storage.json'):
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, 'w', encoding='utf8') as handle:
            handle.write(json.dumps(initiate_ranking_dict()))
    with open(filename, 'r', encoding='utf8') as handle:
        current_ranks = json.loads(handle.read())
    return current_ranks


def write_new_rankings(ranking_dict, filename='ranking_storage.json'):
    with open(filename, 'w', encoding='utf8') as handle:
        handle.write(json.dumps(ranking_dict))


def print_scoreboard_greetings(width=41):
    title = Fore.YELLOW + "Our best of the best!"
    print()
    print('*' * width)
    print(f'*{" " * (width - 2)}*')
    print('*{0}{1}{0}*'.format(" " * int((width - len(title) + 3)/2), title + Fore.RESET))
    print(f'*{" " * (width - 2)}*')
    print('*' * width)
    print()


def add_user_score(username, question_number, total_score):
    scoreboard = get_storage_ranking_info()
    user_dict = {"user": username, "score": total_score}

    scoreboard[str(question_number)].append(user_dict)
    write_new_rankings(scoreboard)
    print(f'{Fore.GREEN}{username}{Fore.CYAN}, your score is {Fore.GREEN}{int(total_score)} '
          f'{Fore.CYAN}with {question_number} questions answered!')
    users_list = sorted(scoreboard[str(question_number)], key=lambda item: item['score'], reverse=True)
    position = users_list.index(user_dict) + 1
    print(f'{Fore.CYAN}You took an honorable place {Fore.YELLOW}#{position}{Fore.CYAN} '
          f'among all braves with {question_number} right answers!')


def display_top_players(amount=5, scoreboard=""):
    if not scoreboard:
        scoreboard = get_storage_ranking_info()
    ranks = sorted(scoreboard.items(), key=lambda item: int(item[0]), reverse=True)
    for answers_info in ranks:
        users_list = sorted(answers_info[1], key=lambda user_info: user_info['score'], reverse=True)
        if not users_list:
            continue
        top_amount = min(amount, len(users_list))
        print(f'{Fore.CYAN}Top {top_amount} users with {answers_info[0]} right answers:')
        for i in range(len(users_list[:top_amount])):
            print(f'\t{Fore.YELLOW}{i + 1}.{Fore.RESET} Score {Fore.GREEN}'
                  f'{int(users_list[i]["score"])} - {users_list[i]["user"]}')
        print()


def show_scoreboard(username, questions_answered_right, total_score, top_number):
    if questions_answered_right > 0:
        add_user_score(username, questions_answered_right, total_score)
    print_scoreboard_greetings()
    display_top_players(top_number)
