import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate


from models import model_init
load_dotenv()
model = os.getenv('LLM')

def chain_init(template, api_key, schema=None):
    llm = model_init(model=model, temperature=0.8, api_key=api_key)
    prompt = PromptTemplate(template=template)
    if schema:
        return prompt | llm.with_structured_output(schema)
    return prompt | llm


def writing_chain(topic, language, content, word_limit, api_key):

    schema = {
        "title": "social media post",
        "type": "string",
    }

    template = '''
    Study the following list of social media sample posts below:
     {content}
    You need to write a social media post similar to these and it should be around {word_limit} words long.
    You should mimic the exact style of writing as the sample, but write
    about {topic} in {language}. It should also be meaningful and engaging to read.
    You're free to do as much content research as you need
    on {topic} for factual accuracy. But write the post strictly in {language} only.
    Avoid any grammatical or spelling errors in {language}.
    Include appropriate hashtags at the end of your post to make it rank better on social media.
    Remember, you only need to provide your written work. No Preamble.
    '''
    chain = chain_init(template, api_key, schema)
    return chain.invoke(
        input={'topic': topic, "language": language, 'content': content, 'word_limit': word_limit}
    )



def reading_chain(text, api_key):

    schema = {
        "title": "metadata",
        "description": "structured object to store metadata of a given post",
        "type": "object",
        "properties": {
            "language": {
                "type": "string",
                "description": "This denotes the language of the post.",
            },
            "tags": {
                "type": "array",
                "description": "This denotes a list of multiple hashtags which are relevant to the post",
                "items": {"type": "string"},
                "maxItems": 5,
            },
            "line_count": {
                "type": "integer",
                "description": "This denotes how many the number of lines are present in the post",
            },
            "required": ["language", "tags", "line_count"],
    },}

    template = '''
    I'll give you a social media post that contains textual content like articles, blogs, stories and poems:
    {text}
    Your job is to detect and extract metadata like language, tags and line_count from the post in the form of a structured json object.
    Remember, you only need to provide the json object. No Preamble
    '''
    chain = chain_init(template, api_key, schema)
    return chain.invoke(input={"text": text})