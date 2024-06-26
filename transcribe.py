import assemblyai as aai
import anthropic

import os


aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
config = aai.TranscriptionConfig(
    disfluencies=True, 
    filter_profanity=False,
    word_boost=["Prerit", "Das", "Prerit Das"]
)
transcriber = aai.Transcriber(config=config)

anthrophic_client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
)


REFINE_PROMPT = """You are designed to take raw voice transcriptions and refine them into more readable text.
You do this by removing filler words, correcting obvious spelling/homonym errors, and altering punctuation where necessary.
You must also ensure that the refined transcription is still faithful to the original message. Keep the content and tone intact.
If the original transcription is already perfect, respond with the exact same transcription.
Make the structure more readable by splitting into paragraphs.
Most people will read the refined transcription on a phone, so be liberal with paragraph splits to improve readability.

You always respond only with the refined transcription. The beginning of your response is always the beginning of the refined transcription.
"""


def transcribe_audio(audio_bytes: bytes) -> str:
    response = transcriber.transcribe(audio_bytes)
    transcription = response.text

    return transcription

def refine_transcription(transcription: str) -> str:
    if not transcription.strip():
        return "*Empty Transcription*"

    message = anthrophic_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        temperature=0,
        system=REFINE_PROMPT,
        messages=[
            {"role": "user", "content": f"Original Transcription:\n\n{transcription}\n\nRefined Transcription:\n\n"}
        ]
    )

    if len(message.content) > 1:
        raise ValueError("Error, lots of text blocks. Fix me!")

    response = message.content[0].text
    return response
