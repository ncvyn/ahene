import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Ahente")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
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
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if args.verbose:
        usage_metadata = response.usage_metadata
        if usage_metadata is None:
            raise RuntimeError("usage metadata not found")
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")
        print("Response:")

    if response.function_calls is not None:
        for function in response.function_calls:
            print(f"Calling function: {function.name}({function.args})")
    print(response.text)


if __name__ == "__main__":
    main()
