import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# HuggingFace token
HF_TOKEN = os.getenv("HUGGING_FACE") or os.getenv("HF_TOKEN")

# Embedding Model
EMBEDDING_MODEL = "google/embeddinggemma-300m"

# Document Configuration
DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Vector db: PostgreSQL
# Try to get from env first, fallback to default local docker connection
CONNECTION_STRING = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/camtech_chatbot")
COLLECTION_NAME = "camtech_docs"

# Chunking Configuration
CHUNK_SIZE = 1000  # Number of characters per chunk
CHUNK_OVERLAP = 50  # Overlap between chunks

# Retrieval Configuration
NUM_RETRIEVED_DOCS = 3  # Number of document chunks to retrieve

# LLM Configuration
TEMPERATURE = 0  # Lower temperature = more focused answers
MODEL_NAME = "llama-3.3-70b-versatile" 