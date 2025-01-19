import os
import streamlit as st
from chains import writing_chain
from dotenv import load_dotenv
from post_extractor import get_posts_from_collection, extract_post

def app():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    #recent_posts = extract_post('assets/blogs.csv')

    #print(f"\nRecent Posts\n{recent_posts}")

    st.set_page_config(page_icon=":lightning", page_title='MagicPen AI', layout='wide')

    st.header('MagicPen AI', anchor=False)
    st.subheader("You pick, I'll write!", anchor=False)

    topic = st.selectbox(
        'Pick one', options=['Select', 'Music', 'Technology and AI', 'Movies', 'Books']
    )
    if topic and topic != 'Select':
        response = writing_chain(topic, api_key).content
        st.chat_message(name='ai', avatar=':material/history_edu:').write(response)
        topic = 'Select'

def app_two():
    load_dotenv()
    #api_key = os.getenv("GROQ_API_KEY")

    recent_posts = extract_post('assets/blogs.csv')

    if len(recent_posts) > 0:
        metadata = {}
        metadata['tags'] = ['Poem', 'Book', 'Phantoms']
        metadata['language'] = 'English'
        match_results = get_posts_from_collection(metadata, 2)

        print(f'matches\n{match_results}\n')

if __name__ == '__main__':
    app()
    #app_two()