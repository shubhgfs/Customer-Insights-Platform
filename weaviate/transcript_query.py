from weaviate.collections.classes.filters import Filter
from weaviate.classes.generate import GenerativeConfig
from utils import setup_weaviate_connection, create_transcript_collection

def fetch_transcripts(collection, limit=5):
    results = collection.query.fetch_objects(limit=limit)
    return results.objects

def query_transcripts(transcript_collection, query_text, limit=5):
    print(f"\n🔍 Searching for: {query_text}\n")
    results = transcript_collection.query.near_text(query=query_text, limit=limit)
    for i, obj in enumerate(results.objects, 1):
        print(f"{i}. 📄 {obj.properties['title']}")
        print(f"   📝 Snippet: {obj.properties['text'][:200]}...\n")

def query_transcripts_ai(transcript_collection, query_text, limit=3):
    print(f"\n🔍 Searching for: {query_text}\n")
    
    results = transcript_collection.generate.near_text(
        query=query_text,
        single_prompt="Summarize this transcript: {text}",
        limit=limit
    )
    for obj in results.objects:
        print(f"Title: {obj.properties.get('title', 'No title')}")
        print(f"Generated: {obj.generated}")
        print("---")
    
    return results

def main():
    client = setup_weaviate_connection()
    
    try:
        transcript_collection = create_transcript_collection(client)
        
        results = fetch_transcripts(transcript_collection)
        for obj in results:
            print(obj)
        
        query_input = input("\n💬 Enter a search query: ")
        print("Text Based Search:\n")
        query_transcripts(transcript_collection, query_input)
        print("\n💬 Searching with AI...\n")
        query_transcripts_ai(transcript_collection, query_input)

    finally:
        client.close()

if __name__ == "__main__":
    main()