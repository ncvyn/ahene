import os

from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)
    object = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )

    usage_metadata = object.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("usage metadata not found")
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")
    print("Response:")
    print(object.text)


if __name__ == "__main__":
    main()
