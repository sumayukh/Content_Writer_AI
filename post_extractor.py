import os
import uuid
import pandas as pd
from chains import reading_chain

from chroma_config import connect_chroma

from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
client = connect_chroma()

def extract_post(filepath):
    content_df = pd.read_csv(filepath)
    content_list = content_df.to_dict(orient='records')
    processed_content_list = []
    for post in content_list:
        metadata = reading_chain(post['text'], api_key)
        processed_content_list.append(post | metadata)
    store_posts(processed_content_list)
    return processed_content_list



def store_posts(posts):
    pc = client.get_or_create_collection(name='post_collection')
    df = pd.DataFrame(posts).to_dict(orient='records')

    if not pc.count():
        for row in df:
            pc.add(
                documents=row['text'],
                metadatas={
                    'engagement': row['engagement'],
                    "language": row["language"],
                    'line_count': row['line_count'],
                    "tags": ','.join(row["tags"]),
                },
                ids=[str(uuid.uuid4())],
            )
    return pc



def get_posts_from_collection(metadata, n_results):
    pc = client.get_collection(name='post_collection')
    where_clause = {
        "$or": [{"tags": {"$in": metadata["tags"]}}, {"language": metadata["language"]}]
    }
    query_results = pc.query(
        query_texts='', n_results=n_results, where=where_clause, include=['documents']
    )

    print(query_results)
    return query_results['documents']