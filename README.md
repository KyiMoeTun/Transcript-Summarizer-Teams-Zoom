Team Zoom Meeting Transcripts Summarizer
========================================

This is a python script that uses the OpenAI GPT-3.5-turbo API to summarize a meeting transcript and present insights by each speaker. It splits the transcript file into small chunks of 1300 tokens, summarizes each chunk and aggregates them all into one summary.

Getting Started
---------------

These instructions will help you to run the software code smoothly. Clone or download the repository in your desired location on your system.

### Prerequisites

Before running the software code, install the following packages:  
python>=3.8.6  
openai>=0.10.2

You can install them using pip:

```bash
pip install python>=3.8.6
pip install openai>=0.10.2
```

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

Aditional Notes
---------------

The output will be printed on the console for debugging purposes, but also will be saved in a `summary.text` file placed in the same directory.

Please make sure that the transcript is in the correct format and spellings of speaker names match with those you have used in prompts.

Thanks for using my code! I am going to add improvements along the way. Please don't forget to reward me with 'Stars' at the right corner of the repository.
