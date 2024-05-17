# Step 1: Import the necessary libraries
import os
from openai import OpenAI

# Step 2: Initialize the OpenAI client with your API key
# client = OpenAI(api_key=os.environ.get("sk-proj-OEuHVXKn7Tn6Yz9HfFAZT3BlbkFJbEskcF10ZCcovZ4M1gJR"))
client = OpenAI(
  api_key='sk-proj-OEuHVXKn7Tn6Yz9HfFAZT3BlbkFJbEskcF10ZCcovZ4M1gJR',
  organization='org-q42mtcBEsqRkhDTVJcXVVjnh',
  project='proj_jaUKGLAcgNEBtYI6t7MZnBFs',
)

# Step 3: Define the prompt for generating the test code
prompt = """
{
    "role": "user",
    "content": "Please say hello world."
}
"""

# Step 4: Use the chat model to generate the test code
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[prompt]
)

# Step 5: Extract the generated test code from the response
test_code = response['choices'][0]['message']['content']

# Step 6: Print the generated test code
print(test_code)
