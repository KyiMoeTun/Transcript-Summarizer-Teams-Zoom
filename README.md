Team Zoom Meeting Transcripts Summarizer
========================================

This is a python script that uses the OpenAI GPT-3.5-turbo API to summarize a meeting transcript and present insights by each speaker. It splits the transcript file into small chunks of 1300 tokens, summarizes each chunk and aggregates them all into one summary. This script works on Zoom, Microsoft Teams, or any other time stamped transcripts with the speaker names.

Getting Started
---------------

These instructions will help you to run the software code smoothly. Clone or download the repository in your desired location on your system.

### Prerequisites

To run this project, you need to have Python version 3.8 or above installed in your system. You can download Python from the official website:

*   [Download Python](https://www.python.org/downloads/)

After installing Python, use pip to install OpenAI module at least 0.10.2 or above:

```bash
pip install openai
```

If you encounter any issues during installation or while running the project, feel free to raise an issue on this repository.

### Installing

*   Download/clone the repository at your preferred location.
*   Get an OpenAI API key to use the gpt-3.5-turbo API. You'll also need to setup your OpenAI API key to run the code. You can sign up for an API key and find more about the official python package at the official [OpenAI API documentation](https://beta.openai.com/docs/api-reference/authentication). Add your API key here:

```python
openai.api_key = "YOUR_OPENAI_API_KEY"
```

*   Place the 'transcript.txt' file in the same directory as the script. The contents of this file should be the transcript of the Zoom meeting.

### Running

To run the script, execute the following command:

```bash
python3 summary.py
```

Sample Output 
--------------
This is the summary insights from the transcript. The lines are chronological and each speaker is highlighted by curly bracekts. 

<img src="https://i.imgur.com/wsdmqvi.png" width="700">


Aditional Notes
---------------

The output will be printed on the console for debugging purposes, but also will be saved in a `summary.text` file placed in the same directory.

Please make sure that the transcript is in the correct format and spellings of speaker names match with those you have used in prompts.

Thanks for using my code! I am going to add improvements along the way. Please don't forget to reward me with 'Stars' at the right corner of the repository.
