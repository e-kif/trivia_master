import wikipedia
import json

FILENAME = "storage/questions.json"

# Define category_map globally
category_map = {
    "a": "movies",
    "b": "food",
    "c": "books",
    "d": "places",
    "e": "trivia",
    "f": "animals"
}


def load_json(file_path):
    """
    Load data from the json file as long as it can be found
    param: filename
    return: Data loaded from file or empty dict if not found.
    """
    try:
        with open(file_path, "r") as fileobj:
            data = json.load(fileobj)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")
        return {}


def get_category_title(data, category_input):
    """
    Collect the list of titles from a given category in the json data.
    param: data: dictionary containing category data.
    param: category_input: user input saying which category to access.
    return: List of titles for the selected category, or None if the category is invalid.
    """
    category = category_map.get(category_input)
    if category and category in data:
        return data[category]
    else:
        print("Invalid input. Please choose a valid category.")
        return None


def create_dictionary_from_list_of_titles(list_items):
    """
    creates a dictionary of wikipedia article summaries from a list of titles.

    param: list of wiki article titles
    return: dictionary key = (str)title name: value = (str)summary
    """
    category_dictionary = {}
    for item in list_items:
        try:
            wiki_page = wikipedia.page(item, auto_suggest=False)
            summary = wiki_page.summary
            category_dictionary[item] = summary
        except wikipedia.exceptions.PageError:
            print(f"Page not found for: {item}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation error for: {item}. Options: {e.options}")
        except Exception as e:
            print(f"Error accessing {item}: {e}")
    return category_dictionary


def wiki_call(category):
    data = load_json(FILENAME)
    titles = get_category_title(data, category)
    if titles is None:
        return
    # Use category_map to get the correct category name
    title_dict = create_dictionary_from_list_of_titles(titles)

    return title_dict
