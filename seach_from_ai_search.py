from promptflow import tool
from openai import OpenAI
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import json
import os

# Load .env file
load_dotenv()

#Azure AI Search setting
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")

search_client = SearchClient(
    endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
    # endpoint=AZURE_SEARCH_SERVICE_URL,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY))
    

@tool
def my_python_tool(input: str, input_embedding: str) -> str:
    r = search_client.search(input, 
                         query_type=QueryType.SEMANTIC, 
                         query_language="zh-tw",
                         semantic_configuration_name="default", 
                         top=3,
                         query_caption="extractive",
                         query_answer="extractive",
                         vector=input_embedding, 
                         top_k=50, 
                         vector_fields="embedding")
    results = []
    for json_doc in r:
        #print(json_doc)
        json_data = {
            "content": json_doc["content"],
            "sourcepage": json_doc["sourcepage"],
            "sourcefile": json_doc["sourcefile"]
            
        }
        results.append(json.dumps(json_data, ensure_ascii=False))
    content = "\n".join(results)
    return content
