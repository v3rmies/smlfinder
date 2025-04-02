import streamlit as st

st.sidebar.title("Sidebar Test")
page = st.sidebar.radio("Navigation", ["Option 1", "Option 2", "Option 3"])

st.write(f"You selected: {page}")
