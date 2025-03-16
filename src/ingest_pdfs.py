from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
from config import TESS_NEP_CONFIG
from vector_store import vector_store
from translate import translate_text
import asyncio

class Document:
    """
    A class to represent a document with metadata and page content.
    Attributes:
    ----------
    metadata : dict
        A dictionary containing metadata information about the document.
    page_content : str
        The content of the document's pages.
    Methods:
    -------
    __call__():
        Returns a dictionary representation of the document.
    __str__():
        Returns a string representation of the document.
    """
    def __init__(self, metadata, page_content):
        self.metadata = metadata
        self.page_content = page_content
    
    def __call__(self):
        return {
            "metadata": self.metadata,
            "page_content": self.page_content
        }
    
    def __str__(self):
        return f"Document(metadata={self.metadata}, page_content={self.page_content})"


def load_pdf(doc_path, language="en"):
    if doc_path:
        if language == "en":
            loader = UnstructuredPDFLoader(doc_path)
            data = loader.load()
            return data

        elif language == "ne":
            data = Document(metadata={"source": doc_path}, page_content="")
            images = convert_from_path(doc_path)
            for image in images[38:39]:
                text = image_to_string(image, config=TESS_NEP_CONFIG).strip()
                print(text)
                translated_text = asyncio.run(translate_text(text))
                print(translated_text)
                data.page_content += translated_text
            return [data]

def split_text(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    chunks = text_splitter.split_documents(data)
    return chunks

def add_to_vector_store(chunks, source):
    if not vector_store.document_exists(source):
        vector_store.add_document(source, chunks)

def ingest_pdf(doc_path, language="en"):
    if vector_store.document_exists(doc_path):
        print(f"{doc_path} is already in store")
        return
    print(f"Adding {doc_path} to vector store")
    data = load_pdf(doc_path, language)
    chunks = split_text(data)
    add_to_vector_store(chunks, doc_path)
    print(f"Added {doc_path} to vector store")

if __name__ == "__main__":
    ingest_pdf("data/pdfs/history.pdf", language="ne")
    # print(vector_store.get_similar_documents("Nepali history"))

