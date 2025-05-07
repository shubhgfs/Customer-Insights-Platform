from weaviate.collections.classes.filters import Filter
from weaviate.classes.generate import GenerativeConfig
from utils import setup_weaviate_connection, create_sql_query_collection

def fetch_sql_queries(collection, limit=5):
    results = collection.query.fetch_objects(limit=limit)
    return results.objects

def query_sql_examples(sql_collection, query_text, limit=5):
    print(f"\n🔍 Searching for SQL examples related to: {query_text}\n")
    results = sql_collection.query.near_text(query=query_text, limit=limit)
    for i, obj in enumerate(results.objects, 1):
        print(f"{i}. 📄 SQL Query:")
        print(f"   {obj.properties['query']}")
        print(f"   📝 Result: {obj.properties['result'][:200]}...\n")

def query_sql_with_ai(sql_collection, query_text, limit=3):
    print(f"\n🔍 Analyzing SQL queries related to: {query_text}\n")
    
    results = sql_collection.generate.near_text(
        query=query_text,
        single_prompt="Analyze this SQL query and its results, explaining what it does and any key insights: Query: {query}\nResults: {result}",
        limit=limit
    )
    for obj in results.objects:
        print(f"Query:")
        print(f"{obj.properties.get('query', 'No query available')}")
        print(f"\nAI Analysis:")
        print(f"{obj.generated}")
        print("-" * 50)
    
    return results

def main():
    client = setup_weaviate_connection()
    
    try:
        sql_collection = create_sql_query_collection(client)
        
        # Show available SQL queries
        print("\nAvailable SQL Queries:")
        results = fetch_sql_queries(sql_collection)
        for obj in results:
            print(f"- {obj.properties['query'][:100]}...")
        
        # Get user input
        query_input = input("\n💬 Enter your SQL-related search query: ")
        
        # Show text-based search results
        print("\nRelevant SQL Examples:")
        query_sql_examples(sql_collection, query_input)
        
        # Show AI-powered analysis
        print("\n💬 AI Analysis of Related SQL Queries:")
        query_sql_with_ai(sql_collection, query_input)

    finally:
        client.close()

if __name__ == "__main__":
    main()