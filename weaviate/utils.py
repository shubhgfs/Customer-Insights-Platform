import weaviate
import os
from dotenv import load_dotenv
from weaviate.classes.config import Configure, Property, DataType
from weaviate.collections.classes.filters import Filter

load_dotenv()

def setup_weaviate_connection():
    return weaviate.connect_to_local()

def create_transcript_collection(client):
    collection_name = "Transcript"
    
    if collection_name not in client.collections.list_all():
        transcript_collection = client.collections.create(
            name=collection_name,
            vectorizer_config=Configure.Vectorizer.text2vec_ollama(
                api_endpoint="http://localhost:11434",
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

def create_sql_query_collection(client):
    collection_name = "SQLQuery"

    if collection_name not in client.collections.list_all():
        sql_query_collection = client.collections.create(
            name=collection_name,
            vectorizer_config=Configure.Vectorizer.text2vec_ollama(
                api_endpoint="http://localhost:11434",
                model="nomic-embed-text"
            ),
            generative_config=Configure.Generative.ollama(
                api_endpoint="http://localhost:11434"
            ),
            properties=[
                Property(name="query", data_type=DataType.TEXT),
                Property(name="result", data_type=DataType.TEXT),
            ]
        )
        print("✅ Collection created:", collection_name)
    else:
        sql_query_collection = client.collections.get(collection_name)
        print("✅ Collection already exists:", collection_name)
    return sql_query_collection

def load_transcripts(transcript_collection):
    folder_path = r'/home/shubh/Documents/Customer Insights Platform/weaviate'
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") and 'sql' not in filename:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

            title = os.path.splitext(filename)[0]

            existing = transcript_collection.query.fetch_objects(
                filters=Filter.by_property('title').equal(title)
            )

            if existing and len(existing.objects) > 0:
                print(f"✅ Already there: {title}")
                continue

            transcript_collection.data.insert({
                "title": title,
                "text": text
            })
            print(f"✅ Uploaded: {title}")

    print("🎉 All transcripts checked and uploaded!")

def delete_transcript(collection, uuid):
    collection.data.delete_by_id(uuid)

def list_collections(client):
    collections = client.collections.list_all()
    print("✅ Collections in Weaviate:")
    for name in collections:
        print("-", name)

def delete_collection(client, collection_name):
    client.collections.delete(name=collection_name)
    print(f"✅ {collection_name} collection deleted successfully!")

def main():
    client = setup_weaviate_connection()
    try:
        transcript_collection = create_transcript_collection(client)
        load_transcripts(transcript_collection)
        list_collections(client)
    finally:
        client.close()

if __name__ == "__main__":
    main()