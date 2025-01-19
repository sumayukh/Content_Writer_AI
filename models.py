from langchain_groq import ChatGroq

def model_init(model, temperature, api_key):
    return ChatGroq(model=model, temperature=temperature, api_key=api_key, max_retries=2)