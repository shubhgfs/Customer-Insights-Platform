import uuid
import os
from azure.cosmos import CosmosClient, exceptions
from modules.cosmos_db_connection import get_cosmos_client

container = get_cosmos_client("Customer Insights Platform", "Citations")

def extract_and_format_citations(all_citations):
    citations_formatted = {}
    
    for i, citation in enumerate(all_citations):
        doc_id = f'doc{i+1}_{str(uuid.uuid4().hex)[:16]}'
        date = citation['filepath'][:12]
        year, month, day, time = date[:4], date[4:6], date[6:8], date[8:10] + '.' + date[10:]
        context = citation['content'].replace(citation['title'], '').strip()
        context = context[:context.rfind('.')] if context.rfind('.') != -1 else context
        if context[0] != '[':
            context = context[context.find('['):]
        citations_formatted[doc_id] = {
            'Date': f'{year}-{month}-{day} {time}',
            'Context': context
        }
    
    return citations_formatted

def update_citations_file(citations_formatted):
    for doc_id, citation in citations_formatted.items():
        try:
            container.upsert_item({
                "id": str(uuid.uuid4()),
                "doc_id": doc_id,
                "Date": citation['Date'],
                "Context": citation['Context']
            })
        except exceptions.CosmosResourceExistsError:
            continue

def replace_citation_links(msg, citations_formatted):
    for doc in citations_formatted:
        doc_name = doc.split("_")[0]
        doc_url = f' [[{doc_name} 📄]](document_viewer?doc_name={doc})'
        msg = msg.replace(f'[{doc_name}]', doc_url)
    return msg

def process_citations(completion):
    citations = completion.choices[0].message.model_extra.get("context", {}).get("citations", [])
    
    if citations:
        citations_formatted = extract_and_format_citations(citations)
        update_citations_file(citations_formatted)
        msg = replace_citation_links(completion.choices[0].message.content.replace('$', '\\$'), citations_formatted)
        return msg

    return completion.choices[0].message.content
