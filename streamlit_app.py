import os
import re
import streamlit as st
from rapidfuzz.fuzz import ratio
from collections import Counter

# ✅ Set page config FIRST before anything else!
st.set_page_config(page_title="SML Finder", page_icon="https://i.imgur.com/pWQOKtC.png")

# ✅ Hide Streamlit's menu, footer, and deploy button
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none !important;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# ✅ Navigation bar
st.markdown("""
    <style>
        .topnav {
            overflow: hidden;
            background-color: #333;
            display: flex;
            justify-content: space-around;
            padding: 10px;
        }
        .topnav a {
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
            font-size: 17px;
        }
        .topnav a:hover {
            background-color: #ddd;
            color: black;
        }
    </style>
    <div class='topnav'>
        <a href='/?page=search'>Search</a>
        <a href='/?page=top15'>Top 15 Searches</a>
        <a href='https://www.google.com' target='_blank'>Discord</a>
    </div>
""", unsafe_allow_html=True)

# Track search analytics
SEARCH_HISTORY_FILE = "search_history.txt"

def save_search(keyword):
    with open(SEARCH_HISTORY_FILE, "a") as f:
        f.write(keyword + "\n")

def get_top_searches():
    if not os.path.exists(SEARCH_HISTORY_FILE):
        return []
    with open(SEARCH_HISTORY_FILE, "r") as f:
        searches = f.readlines()
    counter = Counter(search.strip() for search in searches)
    return counter.most_common(15)

# ✅ Page Routing
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["search"])[0]

if page == "search":
    # ✅ Search Page
    st.markdown("""
        <h1 style='text-align: center;'>
            <img src='https://i.imgur.com/pWQOKtC.png' width='40' height='40' style='vertical-align: middle;' />
            Cuz why not?
        </h1>
    """, unsafe_allow_html=True)

    keyword = st.text_input("Enter a word or sentence to search:", "")
    safe_mode = st.checkbox("Lag Mode (view less than 20)", value=True)
    search_button = st.button("Search")

    def normalize_text(text):
        return re.sub(r"\s+", " ", text.lower().replace("'", ""))

    def is_similar(a, b, threshold=80):
        return ratio(a, b) >= threshold

    def search_subtitles(keyword, directory="subtitles", threshold=80):
        keyword_norm = normalize_text(keyword)
        matching_videos = []
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                video_id = filename[:-4]
                with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                    content = f.read()
                    content_norm = normalize_text(content)
                    if keyword_norm in content_norm:
                        matching_videos.append(video_id)
                    else:
                        for sentence in re.split(r'[.!?]', content):
                            if is_similar(keyword, sentence.strip(), threshold):
                                matching_videos.append(video_id)
                                break
        return matching_videos

    if search_button and keyword:
        save_search(keyword)  # Save the search term
        results = search_subtitles(keyword)
        if len(results) > 20 and safe_mode:
            st.markdown("<p style='color: red; font-weight: bold;'>Not able to continue due to more than 20 videos!</p>", unsafe_allow_html=True)
        elif results:
            st.write(f"Found {len(results)} videos.")
            col1, col2 = st.columns(2)
            for i, video_id in enumerate(results):
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                if i % 2 == 0:
                    with col1:
                        st.markdown(f'<a href="{video_url}" target="_blank"><img src="{thumbnail_url}" style="width: 100%; height: auto;" /></a>', unsafe_allow_html=True)
                else:
                    with col2:
                        st.markdown(f'<a href="{video_url}" target="_blank"><img src="{thumbnail_url}" style="width: 100%; height: auto;" /></a>', unsafe_allow_html=True)
        else:
            st.write("No matches found.")

elif page == "top15":
    # ✅ Top 15 Searches Page
    st.markdown("<h2>Top 15 Searches</h2>", unsafe_allow_html=True)
    top_searches = get_top_searches()
    if top_searches:
        for i, (term, count) in enumerate(top_searches, start=1):
            st.write(f"{i}. '{term}' ({count} times)")
    else:
        st.write("No searches recorded yet.")
