import os
import random
import streamlit as st
from rapidfuzz.fuzz import ratio


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

# ✅ Input field
keyword = st.text_input("Enter a word or sentence to search:", "")

# ✅ Safe mode checkbox
safe_mode = st.checkbox("Lag Mode (view less than 20)", value=True)

# ✅ Center the button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
search_button = st.button("Search")
st.markdown("</div>", unsafe_allow_html=True)

# ✅ Music toggle checkbox
music_enabled = st.checkbox("Enable Music", value=False)

# ✅ Music folder path
music_folder = "music"  # Set your music folder path here

# ✅ Get a list of audio files in the folder
audio_files = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav', '.ogg'))]

# Music Player Logic
if music_enabled and audio_files:
    # Store the playlist if not done yet
    if 'playlist' not in st.session_state:
        st.session_state.playlist = random.sample(audio_files, len(audio_files))

    # Play next song if playlist is not empty
    if 'current_index' not in st.session_state or st.session_state.current_index >= len(st.session_state.playlist):
        st.session_state.current_index = 0
        st.session_state.playlist = random.sample(audio_files, len(audio_files))  # Shuffle playlist again

    # Display the currently playing song
    current_song = st.session_state.playlist[st.session_state.current_index]
    st.write(f"Currently Playing: {current_song}")

    # Play the song
    audio_file_path = os.path.join(music_folder, current_song)
    st.audio(audio_file_path, format="audio/mp3")

    # Increment to the next song after it finishes
    st.session_state.current_index += 1

# Functions for searching subtitles and text processing
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
