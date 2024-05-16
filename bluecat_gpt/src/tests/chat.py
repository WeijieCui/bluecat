import os
import openai
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# Function to interact with GPT-4
def ask_openai(prompt):
    # Call the OpenAI API with the desired parameters
    response = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        model="gpt-4o-2024-05-13",
    )
    return {
        'message': response.choices[0].message.content,
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
    }


# Example usage
if __name__ == "__main__":
    user_prompt = ("Yes, I am wonder if you can talk to my 4-years-old son, "
                   "how can you introduce yourself that he can understand better,"
                   "considering his age and cognitive level.")
    response = ask_openai(user_prompt)
    print("GPT-4 response:", response)
