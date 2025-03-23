from vector_store import vector_store
from langchain_ollama import ChatOllama
from config import CHAT_MODEL
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import random

def format_docs(docs):
    return "\n\n---\n\n".join([doc.page_content for doc in docs])

def is_story(story):
    llm = ChatOllama(model=CHAT_MODEL)
    prompt_template = """
    Given the following paragraphs, determine if it is a narrative story with a clear sequence of events, characters, and a plot. Respond strictly with 'Yes' or 'No' only. A narrative story typically includes a beginning, middle, and end, with events unfolding over time. If the passage is primarily an analysis, historical account, or structured informational text without a flowing storyline, respond with 'No'.

    ## Paragraphs:
    {story}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    vote = []
    for i in range(5):
        response = llm.invoke(prompt.format(story=story)).content.strip()
        if "Yes" in response or "yes" in response:
            vote.append(True)
        elif "No" in response or "no" in response:
            vote.append(False)
    return sum(vote) >= 3


    
        

def generate_story():
    llm = ChatOllama(model=CHAT_MODEL)
    print(CHAT_MODEL)
    while True:
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

        if is_story(story):
            break
        print("Not a story. Generating again...")
        
    return story

if __name__ == "__main__":
    story = generate_story()
    print(story)