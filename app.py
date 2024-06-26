import streamlit as st


st.title("Structured Audio Output")
st.info("Extract structured output from spoken audio files.")


uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])
output_fields: list[str] = st.text_input("Output fields (comma separated)", "Goal, Next Steps").split(", ")


if uploaded_file is not None and output_fields:
    st.audio(uploaded_file, format="audio/wav")
    st.write("**Output fields:**")
    st.write(output_fields)

    with st.spinner("Transcribing..."):
        st.write("# Transcription")

    st.write("Sample transcription output.")

    with st.spinner("Analyzing..."):
        st.write("# Structured Output")
        structured_output: dict[str, str] = {
            "Goal": "Sample goal",
            "Next Steps": "Sample next steps"
        }
        
    md_string = ""
    for field, value in structured_output.items():
        md_string += f"### {field}\n {value}\n\n"

    st.markdown(md_string)
    st.code(md_string, language="markdown")
