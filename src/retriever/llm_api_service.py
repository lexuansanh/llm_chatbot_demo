import os
import sys

import requests

# Add 'src' folder to sys.path
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_path)
from src.config import DEFAULT_SYSTEM_PROMPT, configsetting


def get_answer(user_query: str):
    """
    Function to get the answer from the API based on user query.
    Args:
        user_query (str): The user's question.
    Returns:
        str: Text of API response.
    """
    try:
        # Request body
        data = {
            "system_instruction": DEFAULT_SYSTEM_PROMPT,
            "contents": [{"role": "user", "parts": [{"text": user_query}]}],
        }

        headers = {"Content-Type": "application/json"}
        params = {"key": configsetting.LLM_KEY}

        # Make POST request
        response = requests.post(
            configsetting.LLM_API, headers=headers, params=params, json=data
        )
        print(response)
        # Return response
        if response.status_code == 200:
            response = response.json()
            return response["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "No answer"
    except Exception as e:
        print(e)
        return "No answer"
