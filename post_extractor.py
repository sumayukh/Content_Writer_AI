import os
import uuid
import pandas as pd
from chains import reading_chain

from chroma_config import connect_chroma

from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
client = connect_chroma()

def extract_post(filename):
    filepath = os.path.join('assets', filename)

    if not os.path.exists(filepath):
        print(f"Error-\t{filename} not found\n")
        return False
    try:
        content_df = pd.read_csv(filepath)
        content_list = content_df.to_dict(orient='records')
        processed_content_list = []
        for post in content_list:
            metadata = reading_chain(post['text'], api_key)
            processed_content_list.append(post | metadata)
        store_posts(processed_content_list)
        return processed_content_list
    except Exception as e:
        print(f"Error Type-\t{type(e)}\nError-\t{e}\n")
        return False



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
        "$or": [{"tags": {"$in": metadata["tags"]}}, {"language": {"$in": metadata["language"]}}]
    }
    try:
        query_results = pc.query(
            query_texts='', n_results=n_results, where=where_clause, include=['documents']
        )
        return query_results['documents']
    except Exception as e:
        print(f"Error Type-\t{type(e)}\nError-\t{e}\n")
        return False