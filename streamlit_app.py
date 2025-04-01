import os
import re
import streamlit as st
from rapidfuzz.fuzz import ratio
import streamlit.components.v1 as components

# ✅ Set page config FIRST before anything else!
st.set_page_config(page_title="SML Finder", page_icon="https://i.imgur.com/pWQOKtC.png")

# ✅ Hide Streamlit's menu, footer, and deploy button
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_streamlit_cloud_toolbar = """
    <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
"""
st.markdown(hide_streamlit_cloud_toolbar, unsafe_allow_html=True)

# ✅ Streamlit UI Title with Logo
st.markdown("<h1 style='text-align: center;'><img src='https://i.imgur.com/pWQOKtC.png' width='40' height='40' style='vertical-align: middle;' /> Cuz why not?</h1>", unsafe_allow_html=True)

# ✅ Custom CSS for checkbox styling and positioning
st.markdown("""
    <style>
        /* Move the checkbox to the top-left corner */
        .checkbox-container {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 9999;
            display: flex;
            align-items: center;
            font-size: 16px;
        }
        .stCheckbox label {
            font-weight: bold;
            font-size: 16px;
            color: #333;
            margin-left: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Music Icon/Button to toggle playlist
with st.container():
    st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
    music_enabled = st.checkbox("Enable Music 🎵", value=False)
    st.markdown('</div>', unsafe_allow_html=True)

# If the music checkbox is checked, embed the YouTube playlist
if music_enabled:
    playlist_url = "https://www.youtube.com/embed/?listType=playlist&list=PLJrbUAaaqQuzSL7NOO9ayHlbbi_lGhrOL&autoplay=1"  # Add autoplay=1
    # Set width and height to 1 to effectively hide the player but keep it playing in the background
    components.iframe(playlist_url, width=1, height=1)

# ✅ Input field
keyword = st.text_input("Enter a word or sentence to search:", "")

# ✅ Safe mode checkbox
safe_mode = st.checkbox("Lag Mode (view less than 20)", value=True)

# ✅ Center the button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
search_button = st.button("Search")
st.markdown("</div>", unsafe_allow_html=True)


def normalize_text(text):
    # Convert to lowercase and standardize apostrophes
    text_no_apostrophe = text.lower().replace("'", "")  # Remove apostrophes
    text_original = text.lower()
    text_no_spaces = re.sub(r"\s+", " ", text_no_apostrophe)  # Normalize spaces (keep single spaces)
    return text_no_spaces, text_original

def is_similar(a, b, threshold=80):  # RapidFuzz uses a 0-100 scale
    return ratio(a, b) >= threshold

def search_subtitles(keyword, directory="subtitles", threshold=80):
    keyword_no_apostrophe, keyword_original = normalize_text(keyword)
    matching_videos = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            video_id = filename[:-4]  # Remove .txt extension
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                content = f.read()
                cleaned_no_apostrophe, cleaned_original = normalize_text(content)
                
                # Check for exact match with and without apostrophes
                if keyword_no_apostrophe in cleaned_no_apostrophe or keyword_original in cleaned_original:
                    matching_videos.append(video_id)
                else:
                    # Check for approximate match in the entire text
                    sentences = re.split(r'[.!?]', cleaned_original)
                    for sentence in sentences:
                        if is_similar(keyword_original, sentence.strip(), threshold):
                            matching_videos.append(video_id)
                            break
    
    return matching_videos

if search_button and keyword:
    # Call the search function
    results = search_subtitles(keyword)
    
    if len(results) > 20 and safe_mode:
        # Display warning message in red if safe mode is enabled
        st.markdown("<p style='color: red; font-weight: bold;'>Not able to continue due to more than 20 videos!</p>", unsafe_allow_html=True)
    elif results:
        st.write("Found in these videos:")
        
        # Set up a grid for two videos per row
        col1, col2 = st.columns(2)
        
        for i, video_id in enumerate(results):
            # Generate the YouTube thumbnail URL
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Set the column based on index (0 for col1, 1 for col2)
            if i % 2 == 0:
                with col1:
                    st.markdown(f'<a href="{video_url}" target="_blank"><img src="{thumbnail_url}" style="width: 100%; height: auto;" /></a>', unsafe_allow_html=True)
            else:
                with col2:
                    st.markdown(f'<a href="{video_url}" target="_blank"><img src="{thumbnail_url}" style="width: 100%; height: auto;" /></a>', unsafe_allow_html=True)

            # Reset columns for next pair
            if i % 2 == 1 or i == len(results) - 1:
                col1, col2 = st.columns(2)

    else:
        st.write("No matches found.")
