import openai
import os
import time
import json
import threading
from dotenv import load_dotenv
import glob
import re

# Load .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY")

def split_text(text, word_limit=1300):
    """
    Splits a given text into chunks of a specific size.

    Parameters:
    text (str): The text to be split.
    word_limit (int): The maximum size of each chunk.

    Returns:
    list: The list of chunks.
    """
    words = text.split()
    num_parts = len(words) // word_limit + 1
    return [' '.join(words[i * word_limit: (i + 1) * word_limit]) for i in range(num_parts)]

def print_period():
    """
    Prints a period character to the console every second. 
    Uses a global timer object to schedule itself to run every second.
    """
    global period_timer
    print(".", end="", flush=True)
    period_timer = threading.Timer(1.0, print_period)
    period_timer.start()

def load_prompt(filename="prompt.json"):
    """
    Loads a prompt from a JSON file.

    Parameters:
    filename (str): The name of the JSON file.

    Returns:
    list: The loaded prompt.
    """
    with open(filename, "r") as f:
        return json.load(f)

def preprocess_text(text):
    lines = text.split('\n')
    processed_lines = [line for line in lines if not line.strip().startswith(tuple('0123456789')) and line.strip() != '']
    return '\n'.join(processed_lines)

def create_summary(file_path, prompt):
    """
    Creates a summary for a given file using the OpenAI GPT 3.5 Turbo API.

    Parameters:
    file_path (str): The path of the file.
    prompt (list): The prompt to use for the OpenAI API.

    Returns:
    str: The summary.
    """
    with open(file_path, "r") as f:
        print(f"Reading {os.path.basename(file_path)}")
        transcript = f.read()

    # Preprocess the transcript
    transcript = preprocess_text(transcript)

    chunks = split_text(transcript)
    summary_list = []
    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks, start=1):
        prompt[-2]["content"] = chunk
        retries = 0
        while retries < 5:
            try:
                print(f"Making summarization request {i}/{total_chunks} to OpenAI API for {os.path.basename(file_path)}", end="")
                print_period()

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=prompt,
                    max_tokens=300,
                    temperature=0.6,
                    n=1,
                    stop=None
                )
                period_timer.cancel()
                print("")
                summary = response.choices[0].message['content'].strip()
                summary_list.append(summary)
                break
            except openai.error.RateLimitError:
                print("\nReceived rate limit error, waiting for 60 seconds before retrying...")
                period_timer.cancel()
                time.sleep(60)
                retries += 1
            except Exception as e:
                print("\nQuitting due to unexpected error: {}".format(e))
                period_timer.cancel()
                return None
        if retries >= 5:
            print("\nExceeded maximum number of retries. Giving up on current chunk.")
    return '\n'.join(summary_list)

def save_summary(file_path, summary):
    """
    Saves a summary to a file.

    Parameters:
    file_path (str): The path of the file.
    summary (str): The summary to save.
    """
    with open(file_path, "w") as f:
        print(f"Creating {os.path.basename(file_path)} in results directory")
        f.write(summary)


def process_files(input_files, prompt):
    """
    Processes a list of files.

    Parameters:
    input_files (list): The list of input files.
    prompt (list): The prompt to use for the OpenAI API.
    """
    for file_path in input_files:
        output_file = os.path.join("results", os.path.basename(file_path).replace(".txt", "-summary.txt"))
        if os.path.exists(output_file):
            print(f"Output file {os.path.basename(output_file)} already exists, skipping.")
            continue
        summary = create_summary(file_path, prompt)
        if summary is not None:
            try:
                save_summary(output_file, summary)
            except PermissionError:
                print(f"No permission to write file: {output_file}")
            except FileExistsError:
                print(f"File already exists: {output_file}")
            except Exception as e:
                print(f"An error occurred while writing the file: {output_file}. Error: {e}")

# Define the timer object as global so we can access it everywhere
period_timer = None

# Load the prompt
prompt = load_prompt()

# Get a list of all .txt files in the ./input directory
input_files = glob.glob('./input/*.txt')

if not input_files:
    print("No text files found in the input directory.")
else:
    process_files(input_files, prompt)
