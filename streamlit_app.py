import os
import re
import streamlit as st
from rapidfuzz.fuzz import ratio
from collections import Counter

# Set page config
st.set_page_config(page_title="SML Finder", page_icon="https://i.imgur.com/pWQOKtC.png")

# Hide Streamlit UI elements
st.markdown("""
    <style>
        #MainMenu, footer, header, [data-testid="stToolbar"] {visibility: hidden;}
        .stDeployButton {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Search", "Top 15 Searches", "Discord"])

# Search history storage (session state)
if "search_history" not in st.session_state:
    st.session_state.search_history = Counter()

def normalize_text(text):
    text_no_apostrophe = text.lower().replace("'", "")
    text_original = text.lower()
    text_no_spaces = re.sub(r"\s+", " ", text_no_apostrophe)
    return text_no_spaces, text_original

def is_similar(a, b, threshold=80):
    return ratio(a, b) >= threshold

def search_subtitles(keyword, directory="subtitles", threshold=80):
    keyword_no_apostrophe, keyword_original = normalize_text(keyword)
    matching_videos = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            video_id = filename[:-4]
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                content = f.read()
                cleaned_no_apostrophe, cleaned_original = normalize_text(content)
                
                if keyword_no_apostrophe in cleaned_no_apostrophe or keyword_original in cleaned_original:
                    matching_videos.append(video_id)
                else:
                    sentences = re.split(r'[.!?]', cleaned_original)
                    for sentence in sentences:
                        if is_similar(keyword_original, sentence.strip(), threshold):
                            matching_videos.append(video_id)
                            break
    return matching_videos

if page == "Search":
    st.title("SML Finder")
    keyword = st.text_input("Enter a word or sentence to search:", "")
    safe_mode = st.checkbox("Lag Mode (view less than 20)", value=True)
    search_button = st.button("Search")

    if search_button and keyword:
        st.session_state.search_history[keyword] += 1
        results = search_subtitles(keyword)
        
        if len(results) > 20 and safe_mode:
            st.markdown("<p style='color: red; font-weight: bold;'>Too many results! Enable safe mode.</p>", unsafe_allow_html=True)
        elif results:
            st.write(f"Found {len(results)} videos.")
            col1, col2 = st.columns(2)
            for i, video_id in enumerate(results):
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                column = col1 if i % 2 == 0 else col2
                with column:
                    st.markdown(f'<a href="{video_url}" target="_blank"><img src="{thumbnail_url}" style="width: 100%;" /></a>', unsafe_allow_html=True)
        else:
            st.write("No matches found.")

elif page == "Top 15 Searches":
    st.title("Top 15 Searches")
    top_searches = st.session_state.search_history.most_common(15)
    for i, (term, count) in enumerate(top_searches, 1):
        st.write(f"{i}. {term} ({count} times)")

elif page == "Discord":
    st.markdown("[Go to Google](https://www.google.com)")
