from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
from config import TESS_NEP_CONFIG
from vector_store import vector_store
from translate import translate_text
import asyncio
from image2text import extract_text
import gc
import os, tempfile
from pypdf import PdfReader


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


def load_pdf(doc_path, language="en", batch_size=50):
    """Process PDF in batches to avoid memory issues"""
    if not doc_path:
        return []
        
    data = Document(metadata={"source": doc_path}, page_content="")
    
    
    # Get total page count to determine batches
    reader = PdfReader(doc_path)
    total_pages = len(reader.pages)
    
    # Process in batches
    for start_page in range(1, total_pages + 1, batch_size):
        end_page = min(start_page + batch_size - 1, total_pages)
        print(f"Processing pages {start_page} to {end_page} of {total_pages}")
        
        # Convert limited pages to images
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_path(
                doc_path, 
                first_page=start_page, 
                last_page=end_page,
                output_folder=path
            )
            
            for image in images:
                if language == "en":
                    text = extract_text(image)
                    data.page_content += text + "\n"
                elif language == "ne":
                    text = extract_text(image)
                    translated_text = asyncio.run(translate_text(text))
                    data.page_content += translated_text + "\n"
                
                # Force garbage collection after each page
                image = None
                gc.collect()
    
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
    
    # Clear memory after each file
    data = None
    chunks = None
    gc.collect()
    
    print(f"Added {doc_path} to vector store")
    print("------------------")



if __name__ == "__main__":
    import os
    
    en_files = os.listdir("data/pdfs/en")
    ne_files = os.listdir("data/pdfs/ne")

    for file in en_files:
        ingest_pdf(f"data/pdfs/en/{file}", "en")
    for file in ne_files:
        ingest_pdf(f"data/pdfs/ne/{file}", "ne")

