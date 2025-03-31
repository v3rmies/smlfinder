import streamlit as st

# Title of the app
st.title("Text Search App")

# Text input field with placeholder text
input_text = st.text_input("Sentence / word", "")

# Button to trigger the action
if st.button("Search"):
    # Print the text from the input field
    st.write(f"Search text: {input_text}")
