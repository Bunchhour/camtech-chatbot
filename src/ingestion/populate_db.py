import os
import sys
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def main():
    # 1. Load the data
    print(f"Loading markdown files from {config.DOCUMENTS_DIR}...")
    loader = DirectoryLoader(
        config.DOCUMENTS_DIR, 
        glob="**/*.md", 
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )
    documents = loader.load()
    
    if not documents:
        print("No markdown files found! Please check your data directory.")
        return

    print(f"Loaded {len(documents)} documents.")

    # 2. Split the data based on Markdown Headers
    print("Splitting documents...")
    headers_to_split_on = [
        ("#", "H1"),
        ("##", "H2"),
        ("###", "H3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    md_docs = []
    for doc in documents:
        splits = markdown_splitter.split_text(doc.page_content)
        for split in splits:
            split.metadata['source'] = doc.metadata.get('source', 'unknown')
        md_docs.extend(splits)

    # 3. Secondary chunking for large sections
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, 
        chunk_overlap=config.CHUNK_OVERLAP
    )
    final_chunks = text_splitter.split_documents(md_docs)
    print(f"Created {len(final_chunks)} total chunks.")

    # 4. Create Embeddings
    print(f"Initializing embeddings model: {config.EMBEDDING_MODEL}...")
    encode_kwargs = {"prompt_name": "STS"}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        encode_kwargs=encode_kwargs
    )

    # 5. Save to Postgres
    print(f"Connecting to database: {config.CONNECTION_STRING}")
    try:
        vectorstore = PGVector.from_documents(
            documents=final_chunks,
            embedding=embeddings,
            collection_name=config.COLLECTION_NAME,
            connection=config.CONNECTION_STRING,
            use_jsonb=True
        )
        print("✅ Successfully ingested data into PostgreSQL!")
    except Exception as e:
        print(f"❌ Failed to connect to database. Make sure it is running. Error: {e}")

if __name__ == "__main__":
    main()
