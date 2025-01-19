from langchain.prompts import PromptTemplate


from models import model_init


def chain_init(template, api_key, schema=None):
    llm = model_init(model='llama-3.3-70b-versatile', temperature=0.8, api_key=api_key)
    prompt = PromptTemplate(template=template)
    if schema:
        return prompt | llm.with_structured_output(schema)
    return prompt | llm



def writing_chain(topic, api_key):
    template = '''
    Use whatever you know and search wikipedia sites
    related to the topic and tell me
    what you know about {topic}
    '''
    chain = chain_init(template, api_key)
    return chain.invoke(input={'topic': topic})


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