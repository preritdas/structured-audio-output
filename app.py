import streamlit as st

from dotenv import load_dotenv; load_dotenv()

from transcribe import transcribe_audio, refine_transcription
from parse import structured_output


st.title("Structured Audio Output")
st.info("Extract structured output from spoken audio files.")


uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])
output_fields: list[str] = st.text_input("Output fields (comma separated)", "Goal, Next Steps").split(", ")


if uploaded_file is not None and output_fields:
    st.audio(uploaded_file, format="audio/wav")
    st.write("**Output fields:**")
    st.write(output_fields)

    st.write("# Transcription")
    transcription_box = st.empty()

    with st.spinner("Transcribing..."):
        raw_transcript: str = transcribe_audio(uploaded_file.getvalue())
        transcription_box.write(raw_transcript)
        refined_transcript: str = refine_transcription(raw_transcript)
        transcription_box.write(refined_transcript)

    st.write("# Structured Output")

    with st.spinner("Analyzing..."):
        output: dict[str, str] = structured_output(output_fields, refined_transcript)
        
    md_string = ""
    for field, value in output.items():
        md_string += f"### {field}\n {value}\n\n"

    st.markdown(md_string)
    st.code(md_string, language="markdown")
