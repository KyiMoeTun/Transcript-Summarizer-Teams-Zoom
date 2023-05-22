import openai
import os
import time
from dotenv import load_dotenv
import glob
import threading

# Load .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY")

# Define function to split text into chunks of 1300 tokens
def split_text(text):
    words = text.split()
    word_limit = 1300
    num_parts = len(words) // word_limit + 1
    parts = []
    for i in range(num_parts):
        start_index = i * word_limit
        end_index = (i + 1) * word_limit
        parts.append(' '.join(words[start_index:end_index]))
    return parts

# Define the timer object as global so we can access it everywhere
period_timer = None

def print_period():
    global period_timer
    print(".", end="", flush=True)
    period_timer = threading.Timer(1.0, print_period)
    period_timer.start()

# Get a list of all .txt files in the ./input directory
input_files = glob.glob('./input/*.txt')

if not input_files:
    print("No text files found in the input directory.")
    exit(1)

for file_path in input_files:
    try:
        # Read transcript file
        with open(file_path, "r") as f:
            print(f"Reading {os.path.basename(file_path)}")
            transcript = f.read()
    except PermissionError:
        print(f"No permission to read file: {file_path}")
        continue

    # Split transcript into chunks of 1300 tokens
    chunks = split_text(transcript)

    # Summarize each chunk using OpenAI GPT 3.5 Turbo API
    summary_list = []
    for i, chunk in enumerate(chunks):
        prompt = [
            {"role": "system", "content": "Act as a meeting note taker, and summarize this meeting transcript. Highlight to-do lists and important keypoints from each speaker as highly precisely as possible. Make sure not to give any numbering to anything but add a new line after every keypoint. Additionally, add curly brackets around each speaker name."},
            {"role": "user", "content": chunk},
            {"role": "assistant", "content": "Keypoints:"}
        ]
        retries = 0
        while retries < 5:
            try:
                print(f"Making summarization request to OpenAI API for {os.path.basename(file_path)}", end="")
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
            except openai.error.RateLimitError as e:
                print("\nReceived rate limit error, waiting for 60 seconds before retrying...")
                period_timer.cancel()
                time.sleep(60)
                retries += 1
            except Exception as e:
                print("\nQuitting due to unexpected error: {}".format(e))
                period_timer.cancel()
                exit(1)

        if retries >= 5:
            print("\nExceeded maximum number of retries. Giving up on current chunk.")
            continue

    # Join all summaries into one string
    summary = '\n'.join(summary_list)

    # Define output file path
    output_file = os.path.join("results", os.path.basename(file_path).replace(".txt", "-summary.txt"))

    # Save the results in a text file
    try:
        with open(output_file, "w") as f:
            print(f"Creating {os.path.basename(file_path)}-summary.txt in results directory")
            f.write(summary)
    except PermissionError:
        print(f"No permission to write file: {output_file}")
        continue
    except FileExistsError:
        print(f"File already exists: {output_file}")
        continue

    # Print final summary
    print("Final summary:\n", summary)
