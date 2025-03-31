import os
import re
import streamlit as st

def search_subtitles(keyword, directory="subtitles"):
    keyword = re.sub(r"\s+", "", keyword.lower())  # Remove spaces and lowercase
    matching_videos = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            video_id = filename[:-4]  # Remove .txt extension
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                content = f.read()
                cleaned_content = re.sub(r"\s+", "", content.lower())  # Remove spaces and lowercase
                
                if keyword in cleaned_content:
                    matching_videos.append(video_id)
    
    return matching_videos

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>Subtitle Search App</h1>", unsafe_allow_html=True)

# Input field with placeholder text
keyword = st.text_input("Enter a word or sentence to search:", "")

# Center the button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
search_button = st.button("Search")
st.markdown("</div>", unsafe_allow_html=True)

if search_button and keyword:
    # Call the search function
    results = search_subtitles(keyword)
    
    if results:
        st.write("Found in these videos:")
        for video_id in results:
            st.markdown(f"[Watch Video](https://www.youtube.com/watch?v={video_id})")
    else:
        st.write("No matches found.")
