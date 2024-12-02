import re
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['search_engine']
documents_collection = db['documents']

documents = [
    "After the medication, headache and nausea were reported by the patient.",
    "The patient reported nausea and dizziness caused by the medication.",
    "Headache and dizziness are common effects of this medication.",
    "The medication caused a headache and nausea, but no dizziness was reported."
]

def preprocess(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower() #removing punctuation and converting to lowercase
    return text

def store_documents(docs): #storing documents in mongodb
    documents_collection.delete_many({})
    for doc_id, content in enumerate(docs):
        cleaned_content=preprocess(content)
        documents_collection.insert_one({"_id": doc_id, "content": cleaned_content})

store_documents(documents)
print("Documents have been processed and stored in MongoDB.")
