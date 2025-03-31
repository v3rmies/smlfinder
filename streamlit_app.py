import os
import re
import streamlit as st

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
