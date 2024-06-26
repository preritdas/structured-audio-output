from openai import OpenAI

import os
import json


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


PROMPT = """Take the following voice transcription and format it into the following categories: {keys_desc}

You ONLY respond in JSON format with the following keys: {keys_str}

Retain the original text when inserting it into the JSON sections; do not rewrite it.

Transcription:

{transcription}"""


def create_prompt(keys: list[str], transcription: str) -> str:
    keys_str = str(keys)  # ex. '["What they do", "Problems solved", "Case study", "My initial take"]'
    return PROMPT.format(keys_str=keys_str, transcription=transcription, keys_desc=", ".join(keys))


def structured_output(keys: list[str], transcript: str) -> dict[str, str]:
    completion = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a transcript organizer who responds in only JSON and categorizes the following voice transcription into the following categories: What they do, Problems solved, Case study, and My initial take. You retain the original text when inserting it into the JSON sections; do not rewrite it."},
            {"role": "user", "content": create_prompt(keys, transcript)}
        ]
    )

    return json.loads(completion.choices[0].message.content)
