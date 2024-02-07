import os
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings


class VectorStore:
    
    def __init__(self, root_dir, persist_dir = 'novel-db', retrieval_size = 2):
        print(root_dir)
        
        self.instructor_embeddings = HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-base')
        self.persist_db_dir = persist_dir
        self.db = None
        

        
        if not os.path.exists(os.path.join(os.getcwd(), self.persist_db_dir)):
            print('setting up vector store. This might take a while ...')
            self.data_loader = DirectoryLoader(f'{root_dir}/data/', glob = './*.txt',show_progress=True)
            self.documents = self.data_loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size= 1500, chunk_overlap = 50)
            texts = text_splitter.split_documents(self.documents)
            self.db = Chroma.from_documents(documents = texts,
                                        embedding = self.instructor_embeddings,
                                        persist_directory = self.persist_db_dir)
        else:
            print('Vector store already exists')
            try:
                self.db = Chroma(persist_directory=self.persist_db_dir, embedding_function=self.instructor_embeddings)
            except Exception as e:
                print(f'Error reloading persistent Vector Store: {e}')
                self.db = None
        
        
        
        self.retriever = self.db.as_retriever(
            search_type="similarity", search_kwargs={"k": retrieval_size}
        )

        


