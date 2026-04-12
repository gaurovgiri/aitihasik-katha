import os
import tempfile
import gc
import asyncio
from pdf2image import convert_from_path
from pypdf import PdfReader

from config import settings
from translate import translate_text
from vector_store import vector_store
from langchain_text_splitters import RecursiveCharacterTextSplitter
from image2text import extract_text


class Document:
    """
    A simple document class to store text with metadata.
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
    """
    Convert PDF pages to text in batches.
    Supports translation if language is 'ne' (Nepali).
    """
    if not doc_path:
        return []
        
    data = Document(metadata={"source": doc_path}, page_content="")
    
    reader = PdfReader(doc_path)
    total_pages = len(reader.pages)
    
    for start_page in range(1, total_pages + 1, batch_size):
        end_page = min(start_page + batch_size - 1, total_pages)
        print(f"Processing pages {start_page} to {end_page} of {total_pages}")
        
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_path(
                doc_path, 
                first_page=start_page, 
                last_page=end_page,
                output_folder=path
            )
            
            for image in images:
                text = extract_text(image)
                
                if language == "ne":
                    text = asyncio.run(translate_text(text))
                
                data.page_content += text + "\n"
                
                image = None
                gc.collect()
    
    return [data]


def split_text(documents):
    """
    Split document text into chunks for embeddings.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    return text_splitter.split_documents(documents)


def add_to_vector_store(chunks, source):
    """
    Add document chunks to Vertex AI vector store.
    """
    if not vector_store.document_exists(source):
        vector_store.add_document(source, chunks)


def ingest_pdf(doc_path, language="en"):
    """
    Load, split, and add a PDF to the Vertex AI vector store.
    """
    if vector_store.document_exists(doc_path):
        print(f"{doc_path} is already in store")
        return

    print(f"Adding {doc_path} to vector store")
    
    data = load_pdf(doc_path, language)
    chunks = split_text(data)
    add_to_vector_store(chunks, doc_path)
    
    # Clear memory
    data = None
    chunks = None
    gc.collect()
    
    print(f"Added {doc_path} to vector store")
    print("------------------")


if __name__ == "__main__":
    en_dir = "data/pdfs/en"
    ne_dir = "data/pdfs/ne"
    
    en_files = os.listdir(en_dir)
    ne_files = os.listdir(ne_dir)

    for file in en_files:
        ingest_pdf(os.path.join(en_dir, file), language="en")
    for file in ne_files:
        ingest_pdf(os.path.join(ne_dir, file), language="ne")