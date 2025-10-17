"""
Function for indexing documents and performing similarity searches.
Function to interact with Chroma vector store.
"""

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os

# initialize embedding function
embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')

# initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                chunk_overlap=200,
                                                length_function=len)

# initialize chroma vector store
vectorstore = Chroma(persist_directory='./chroma_db',
                     embedding_function=embeddings)

# document loading and splitting
def load_and_split_document(file_path:str)->List[Document]:
    # loading different document types (pdf, docx, html)
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.html'):
        loader = UnstructuredHTMLLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    documents = loader.load()

    return text_splitter.split_documents(documents) # generate the split using text_splitter to create document chunks.

# indexing documents
def index_document_to_chroma(file_path:str, file_id:int)->bool:
    """
    Adding metadata (file_id) to each split.
    The metadata allows us to link vectore document chunks to our chroma vector store.
    """
    try:
        splits = load_and_split_document(file_path)
        for split in splits:
            split.metadata['file_id'] = file_id

        vectorstore.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False
    
# deleting documents
def delete_doc_from_chroma(file_id:int):
    """
    Deletes all document chunks associated with a given file ID from the Chroma Vector Store.
    """
    try:
        docs = vectorstore.get(where={"file_id":file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")

        vectorstore._collection.delete(where={"file_id":file_id})
        print(f"Deleted all documents with file_id {file_id}")
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from chroma: {str(e)}")
        return False
    

    

