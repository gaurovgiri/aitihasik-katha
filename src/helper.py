import time
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from config import CHAT_MODEL

clock_time = None

def clock():
    global clock_time
    clock_time = time.time()

def is_stop_word(word):
    stop_words = [
        ".", ",", "!", "?", ";", "and", "or", "but", "so", "because", "although", "however", "therefore", "nevertheless", "moreover", "furthermore", "meanwhile", "consequently", "nonetheless", "thus", "hence", "accordingly", "otherwise", "instead", "henceforth", "likewise", "subsequently", "similarly", "indeed", "hence", "thus", "therefore", "consequently", "accordingly"
    ]
    for stop_word in stop_words:
        if stop_word in word:
            return True
    return False

def split_sentences(sentences):
    llm = ChatOllama(model=CHAT_MODEL)
    prompt_template = """
    You are an expert in text-to-speech optimization. Your task is to split a given story into short text groups with at most 5 words, ensuring that the flow remains natural when read aloud.  

    Guidelines:
        - Avoid splitting into single words unless necessary.
        - Each text group should STRICTLY contain at most 5 words.  
        - Splits should occur at points that maintain natural speech rhythm.  
        - Avoid breaking phrases or names awkwardly.  
        - Preserve the original sentence order.  
        - The response should contain only the split text groups, with each group on a new line. No explanations, comments, or additional information should be included.  

    Here is the story text:  
    
    {sentences}  

    Return only the split text groups, with each group on a new line.
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    response = llm.invoke(prompt.format(sentences=sentences)).content.strip()
    text_groups = [group for group in response.split('\n') if group.strip()]
    return text_groups

if __name__ == "__main__":
    print(split_sentences("""
    At the helm of the administration stood Jung Bahadur, a man whose strength lay not in his position, but in the loyalty of those who supported him. His three old regiments and brothers' troops were his bulwark against any potential threat, and he was willing to go to great lengths to protect them. On the other side, Queen Rajendra Bikram Shah's authority was waning, and she sought revenge against her arch-nemesis.
    """))
