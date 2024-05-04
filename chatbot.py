from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.palm import PaLM
from llama_index.core import ServiceContext
from llama_index.core import Prompt
import os

# Load text files from the 'data' folder
documents = SimpleDirectoryReader("./data").load_data()

# Set the Google API key for PaLM
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBtiKS9S3em36aFTQpJ97PrZ3IMw8wpk4M'

# Initialize the PaLM language model
llm = PaLM()

# Initialize the Hugging Face embedding model
embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-large-en-v1.5')

#Create a service context for the index.
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model, chunk_size=800, chunk_overlap=20 )

# Create a VectorStoreIndex from the documents and service context
index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)

# Persist the index to storage for later use
index.storage_context.persist()


# Define a custom prompt
template = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, please answer the question and each answer should start with code word Smart Bank:. And if the answer is not in given context should reply with sorry. {query_str}\n"
)
qa_template = Prompt(template)

query_engine = index.as_query_engine(text_qa_template=qa_template,response_mode='tree_summarize')
response = query_engine.query(input("Enter your questions about the loan: "))
print(response)