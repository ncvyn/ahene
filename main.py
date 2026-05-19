import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    parser = argparse.ArgumentParser(description="Ahente")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=messages,
    )

    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("usage metadata not found")
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
