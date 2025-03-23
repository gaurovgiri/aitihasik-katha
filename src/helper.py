import time
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from config import CHAT_MODEL
import os

clock_time = None

def clear():
    audio_files = os.listdir("data/audio")
    image_files = os.listdir("data/images")
    video_files = os.listdir("data/videos")
    output_files = os.listdir("data/output")
    for file in audio_files:
        os.remove(f"data/audio/{file}")
    for file in image_files:
        os.remove(f"data/images/{file}")
    for file in video_files:
        os.remove(f"data/videos/{file}")
    for file in output_files:
        os.remove(f"data/output/{file}")
    print("Cleared all files")

def clock():
    global clock_time
    clock_time = time.time()

def is_stop_word(word):
    stop_words = [
       "but", "so", "because", "although", "however", "therefore", "nevertheless", "moreover", "furthermore", "meanwhile", "consequently", "nonetheless", "thus", "hence", "accordingly", "otherwise", "instead", "henceforth", "likewise", "subsequently", "similarly", "indeed", "hence", "thus", "therefore", "consequently", "accordingly"
    ]
    if word[-1] in ['.', ',', '!', '?', ';'] or word.lower() in stop_words:
        return True
    return False

def split_sentences(sentences):
    sentences = sentences.strip()
    groups = []
    count = 0
    chunks = []
    for word in sentences.split():
        chunks.append(word)
        count += 1

        if count == 8 or is_stop_word(word):
            groups.append(" ".join(chunks))
            count = 0
            chunks = []

    if chunks:
        groups.append(" ".join(chunks))

    return groups

if __name__ == "__main__":
#     print(split_sentences("""
#     In the heart of India, a fascinating tale unfolds, a story that challenges our preconceived notions and reveals the extraordinary lives of British women who found themselves in the land of their exile.

#    In Upper Bengal, far from being houses of bondage, homes were filled with warmth and camaraderie between Englishwomen and their native servants. Contrary to popular beliefs, these ladies cherished fond memories of their Indian life, a stark contrast to the stereotypes painted by some.

#    Yet, in regions dominated by Muhammadan rule, education was scarce, making social interaction limited due to this lack of shared knowledge and understanding. However, even amidst these challenges, the kindness and assistance offered by native scholars was invaluable, enriching the lives of those who sought it.

#    Scholars like ourselves, with an open mind and no preconceived 'ideas', could accept this help without causing bitterness or reproach. The generosity shown to us is evident in the MSS, books, and copies of inscriptions we've received since our return.

#    As we delved deeper into Indian culture, we were struck by the superior manners exhibited by the younger members of the higher castes and nationalities. Contrary to some popular writers and talkers, there is no such thing as 'the Indian people', for India is a tapestry woven with countless threads, each representing a unique culture and identity.

#    Our experiences in India serve as a foundation, a beginning for our scholarly work. We hope to one day return, supplementing the material we've obtained with fresh insights, forever enriched by the knowledge and warmth of this extraordinary land.
#     """))
    clear()
    # print(is_stop_word("therefore"))