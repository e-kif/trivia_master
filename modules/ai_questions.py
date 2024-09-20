import requests
import dotenv
import json
import re


class Questions:
    """Class for interacting with Artificial Intelligence models OpenAI (aka chatGPT) and Gemini"""

    GPT_KEY = dotenv.get_key('.env', 'GPT_KEY')
    GEMINI_KEY = dotenv.get_key('.env', 'GEMINI_KEY')

    urls = {'gpt': 'https://api.openai.com/v1/chat/completions',
            'gemini': 'https://generativelanguage.googleapis.com/v1beta/models/'
                      'gemini-1.5-flash-latest:generateContent'}
    headers = {'gpt': {"Content-Type": "application/json",
                       "Authorization": f"Bearer {GPT_KEY}"},
               'gemini': {"Content-Type": "application/json",
                          "x-goog-api-key": GEMINI_KEY}}
    prompt_string_start = ('generate json with question, answers and a hint:'
                           'where answers are shorter than 40 symbols:'
                           '{"question":"{}","right_answer":"{}","wrong_answers":["{}","{}","{}"],'
                           '"funny_answer": {}, "hint": "{}"}from this summary:')
    prompt_list_start = ('generate list of jsons with question, answers and a hint:'
                         'where answers are shorter than 40 symbols:'
                         '{"question":"{}","right_answer":"{}","wrong_answers":["{}","{}","{}"],'
                         '"funny_answer": {}, "hint": "{}"}from this summaries:')

    def __init__(self, category, summaries, use_ai, engine='gemini'):
        """Initializes an object instance of Questions class"""
        if isinstance(summaries, dict):
            summaries = list(summaries.values())
        self._summaries = summaries
        self._category = category
        self._engine = engine
        self._use_ai = use_ai
        self._prompt = '\n'.join([self.get_prompt_start(), str(summaries)])

    @property
    def use_ai(self):
        """Returns bool whether AI should be used"""
        if not self._use_ai:
            return False
        elif self._engine == 'gpt' and not self.GPT_KEY:
            return False
        elif self._engine == 'gemini' and not self.GEMINI_KEY:
            return False
        return True

    def get_prompt_start(self):
        """Returns right prompt start string depending on a type of instance's variable summaries (str or list)"""
        return self.prompt_list_start if isinstance(self._summaries, list) else self.prompt_string_start

    def get_questions(self):
        """Forms and sends post request to the instance's AI engine, returns useful text of the response
        if api_key is present. otherwise returns static questions read from a json file"""
        if not self.use_ai:
            with open(f'storage/no_api_key_questions/{self._category}.json', 'r') as handle:
                questions_list = json.loads(handle.read())
            return questions_list
        datas = {'gpt': {"model": "gpt-4o-mini-2024-07-18",
                         "messages": [
                             {"role": "system", "content": "You are a helpful assistant."},
                             {"role": "user", "content": self._prompt}]},
                 'gemini': {"contents": [{"role": "user", "parts": [{"text": self._prompt}]}]}
                 }
        response = requests.post(self.urls[self._engine],
                                 headers=self.headers[self._engine],
                                 json=datas[self._engine])
        return self.extract_questions_from_response(response)

    def extract_questions_from_response(self, response):
        """Turns request response into python dictionary, returns the dictionary"""
        question_response = ""
        if response.status_code == 200 and self._engine == 'gpt':
            question_response = response.json()['choices'][0]['message']['content']
        elif response.status_code == 200 and self._engine == 'gemini':
            question_response = response.json()['candidates'][0]['content']['parts'][0]['text']
        if question_response:
            question_json = re.search("(\{|\[)\s*(.*\n)*(\}|\])", question_response).group(0)
            question_dict = json.loads(question_json)
            return question_dict
