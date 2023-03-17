import openai
import os

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

# Read transcript file
with open("transcript.txt", "r") as f:
    transcript = f.read()

# Split transcript into chunks of 1300 tokens
chunks = split_text(transcript)

# Initialize OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Summarize each chunk using OpenAI GPT 3.5 Turbo API
summary_list = []
for i, chunk in enumerate(chunks):
    prompt = [
        {"role": "system", "content": "Act as a meeting note taker, and summarize this meeting transcript. Highlight to-do lists and important keypoints from each speaker as highly precisely as possible. Make sure not to give any numbering to anything but add a new line after every keypoint. Additionally, add curly brackets around each speaker name."},
        {"role": "user", "content": chunk},
        {"role": "assistant", "content": "Keypoints:"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=300,
        temperature=0.6,
        n=1,
        stop=None
    )
    summary = response.choices[0].message['content'].strip()
    summary_list.append(summary)

# Join all summaries into one string
summary = '\n'.join(summary_list)

# Save the results in a text file named 'summary.txt'
with open("results/summary.txt", "w") as f:
    f.write(summary)

# Print final summary
print(summary)
