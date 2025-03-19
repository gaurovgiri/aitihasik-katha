from vector_store import vector_store
from langchain_ollama import ChatOllama
from config import CHAT_MODEL
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import random

def format_docs(docs):
    return "\n\n---\n\n".join([doc.page_content for doc in docs])

def generate_story():
    llm = ChatOllama(model=CHAT_MODEL)
    random_content = vector_store.get_random_document()
    similar_documents = vector_store.get_similar_documents(" ".join(random_content["documents"]), top_k=5)
    similar_docs = format_docs(similar_documents)

    prompt_template = """
    From the given historical context, generate a compelling, engaging script for a historical documentary video. The text will be directly used to generate a voice-over for the video.
    Therefore, avoid using explicit section headers, bullet points, or labels.
    The script should be immersive, engaging, and fact-based for a general audience of social media users and should be around 1-2 minute long when read aloud.
    Make sure that the script has a clear beginning, middle, and end without containing "Narrator", "Camera", "Title", and similar headings. Just plain text.
    Please avoid response like: "It appears that the provided text...." or "The text seems to be about...." and provide a direct script.

    ## Historical Context:
    {context}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    story = llm.invoke(prompt.format(context=similar_docs)).content.strip()
    return story

if __name__ == "__main__":
    story = generate_story()
    print(story)
