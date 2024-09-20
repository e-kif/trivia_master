# Who wants to become a Trivia Master?

### Working with AI models for questions and answers creation

First you should create your own API keys:
- [Gemini](https://ai.google.dev/gemini-api/docs/api-key)
- [OpenAI (aka chatGPT)](https://platform.openai.com/signup?launch)

Then create file `.env` and put there your API keys:

`GPT_KEY={your key here}`

`GEMINI_KEY={your key here}`

Default AI engine is *Gemini*. If you want to switch to *chatGPT*, pass correspoinding parameter in Question object creation:

`questions = Questions(summaries, engine='gpt')`

### More of READMY is coming in foreseeable future

Just be a little bit patient, brave one!