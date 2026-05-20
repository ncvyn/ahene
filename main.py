import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_LOOP_ITERATIONS
from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Ahene")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(MAX_LOOP_ITERATIONS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")
            break

    print(f"Maximum iterations ({MAX_LOOP_ITERATIONS}) reached")
    sys.exit(1)


def generate_content(
    client: genai.Client,
    messages: list[types.Content],
    verbose: bool,
) -> str | None:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("usage metadata not found")

    if verbose:
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")
        print("Response:")

    if not response.function_calls:
        return response.text

    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")

        messages.append(result)

    return None


if __name__ == "__main__":
    main()
