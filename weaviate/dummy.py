import weaviate
import os
from dotenv import load_dotenv
from weaviate.classes.config import Configure, Property, DataType
from weaviate.collections.classes.filters import Filter
from weaviate.classes.generate import GenerativeConfig

load_dotenv()

def setup_weaviate_connection():
    # Connect to local Weaviate instance
    client = weaviate.connect_to_local()
    return client

def create_transcript_collection(client):
    collection_name = "Transcript"
    
    # Create collection if it doesn't exist
    if collection_name not in client.collections.list_all():
        transcript_collection = client.collections.create(
            name=collection_name,
            vectorizer_config=Configure.Vectorizer.text2vec_ollama(
                api_endpoint="http://localhost:11434",  # Use localhost with host network mode
                model="nomic-embed-text"
            ),
            generative_config=Configure.Generative.ollama(
                api_endpoint="http://localhost:11434"
            ),
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="text", data_type=DataType.TEXT),
            ]
        )
        print("✅ Collection created:", collection_name)
    else:
        transcript_collection = client.collections.get(collection_name)
        print("✅ Collection already exists:", collection_name)
    
    return transcript_collection

def load_transcripts(transcript_collection):
    folder_path = r'/home/shubh/Documents/Customer Insights Platform/weaviate'
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

            title = os.path.splitext(filename)[0]

            # Check if transcript with same title already exists
            existing = transcript_collection.query.fetch_objects(
                filters=Filter.by_property('title').equal(title)
            )

            if existing and len(existing.objects) > 0:
                print(f"✅ Already there: {title}")
                continue

            # Insert if not already there
            transcript_collection.data.insert({
                "title": title,
                "text": text
            })
            print(f"✅ Uploaded: {title}")

    print("🎉 All transcripts checked and uploaded!")

def fetch_transcripts(collection, limit=5):
    # Fetch objects with specified limit
    results = collection.query.fetch_objects(limit=limit)
    return results.objects

def delete_transcript(collection, uuid):
    # Delete a specific transcript by UUID
    collection.data.delete_by_id(uuid)

def list_collections(client):
    collections = client.collections.list_all()
    print("✅ Collections in Weaviate:")
    for name in collections:
        print("-", name)

def delete_collection(client, collection_name):
    client.collections.delete(name=collection_name)
    print(f"✅ {collection_name} collection deleted successfully!")

def query_transcripts(transcript_collection, query_text, limit=5):
    print(f"\n🔍 Searching for: {query_text}\n")
    results = transcript_collection.query.near_text(query=query_text, limit=limit)
    for i, obj in enumerate(results.objects, 1):
        print(f"{i}. 📄 {obj.properties['title']}")
        print(f"   📝 Snippet: {obj.properties['text'][:200]}...\n")  # Preview first 200 chars

def query_transcripts_ai(transcript_collection, query_text, limit=3):
    print(f"\n🔍 Searching for: {query_text}\n")
    
    # You need to provide either single_prompt or grouped_task
    results = transcript_collection.generate.near_text(
        query=query_text,
        single_prompt="Summarize this transcript: {text}",  # Replace {content} with your actual property name
        # OR use grouped_task for a single response across all results
        # grouped_task="Write a summary of these transcripts.",
        limit=limit
    )
    # For single_prompt
    for obj in results.objects:
        print(f"Title: {obj.properties.get('title', 'No title')}")
        print(f"Generated: {obj.generated}")
        print("---")
    
    # For grouped_task
    # print(f"Generated response: {results.generated}")

    return results

def main():
    # Initialize connection
    client = setup_weaviate_connection()
    
    try:
        # Create collection
        transcript_collection = create_transcript_collection(client)
        
        # Load transcripts
        load_transcripts(transcript_collection)
        
        # List all collections
        list_collections(client)
        
        # Fetch and display transcripts
        results = fetch_transcripts(transcript_collection)
        for obj in results:
            print(obj)
        
        query_input = input("\n💬 Enter a search query: ")
        print("Text Based Search:\n")
        query_transcripts(transcript_collection, query_input)
        print("\n💬 Searching with AI...\n")
        query_transcripts_ai(transcript_collection, query_input)

    finally:
        # Clean up resources
        client.close()

if __name__ == "__main__":
    main()