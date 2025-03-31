import streamlit as st

# Center the title
st.markdown("<h1 style='text-align: center;'>Text Search App</h1>", unsafe_allow_html=True)

# Center the text input and button using markdown
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

# Text input field with placeholder text
input_text = st.text_input("Sentence / word", "")

# Button to trigger the action
if st.button("Search"):
    # Print the text from the input field
    st.write(f"Search text: {input_text}")

# Close the centered div
st.markdown("</div>", unsafe_allow_html=True)
