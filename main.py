import os
import streamlit as st
from chains import writing_chain
from dotenv import load_dotenv
from post_extractor import extract_post, get_posts_from_collection

def app():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    st.set_page_config(page_icon=":material/history_edu:", page_title='MagicPen AI', layout='wide')

    @st.cache_resource
    def get_resources(filename):
        recent_posts = extract_post(filename)
        if not recent_posts:
            return False
        metadata = {}
        all_tags = ','.join([','.join(post['tags']) for post in recent_posts])
        unique_tags = set()
        unique_tags.update(all_tags.split(','))
        unique_languages = {post['language'] for post in recent_posts}
        metadata['tags'] = list(unique_tags)
        metadata['language'] = list(unique_languages)
        return metadata

    st.header('MagicPen AI', anchor=False)
    st.subheader("You pick, I'll write!", anchor=False)

    metadata = get_resources('blogs.csv')
    sample_post_list = False

    if metadata:
        sample_post_list = get_posts_from_collection(metadata, 2)[0]
    if sample_post_list:
        topic_col, language_col, word_limit_col = st.columns(3, vertical_alignment='top')
        topic = topic_col.selectbox('Select topic', options=['Select'] + metadata['tags'])
        language = language_col.selectbox(
            'Select language', options=['Select'] + metadata['language']
        )
        word_limit = word_limit_col.selectbox(
            'Select word limit', options=['Select', 200, 400, 600, 800, 1000]
        )
        write_button = st.button(
            'Write',
            type='secondary',
            icon=":material/history_edu:",
            disabled='Select' in (topic, language, word_limit),
        )
        if write_button:
            container = st.container()
            magic_pen = container.chat_message(name='ai', avatar=":material/history_edu:")
            with magic_pen:
                placeholder = st.empty()
                with st.spinner('Writing...'):
                    new_post = writing_chain(
                        topic, language, sample_post_list, word_limit, api_key
                    )['post']
                placeholder.markdown(new_post)



if __name__ == '__main__':
    app()