#-------------------------------------------------------------------------
# AUTHOR: Edwin Ly
# FILENAME: db_connection_mongo.py
# SPECIFICATION: This file contains the functions to create, update, delete documents and output inverted index ordered by term
# FOR: CS 4250- Assignment #2
# TIME SPENT: 4 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
from pymongo import MongoClient
import datetime

def connectDataBase():

    # Creating a database connection object using pymongo

    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary (document) to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.

    term_counts = {} 
    terms = docText.lower().split(" ")

    for term in terms:
        if term in term_counts:
            term_counts[term] +=1
        else:
            term_counts[term] = 1

    #create a list of dictionaries (documents) with each entry including a term, its occurrences, and its num_chars. Ex: [{term, count, num_char}]
    term_documents = [{
        "term": term,
        "count": count,
        "num_chars": len(term)
    }
    for term, count in term_counts.items()
    ]

    #Producing a final document as a dictionary including all the required fields
    document = {
        "_id": int(docId),
        "text": docText,
        "title": docTitle,
        "date": datetime.datetime.strptime(docDate, "%Y-%m-%d"),
        "category": docCat
    }

    #Insert the document
    try:
        col.insert_one(document)
        print("Document created.")
    except Exception as e:
        print("Error creating document.")

def deleteDocument(col, docId):
    # Delete the document from the database
    try:
        result = col.delete_one({"_id": int(docId)})
        if result.deleted_count>0:
            print("Document deleted.")
        else:
            print(f"No document found with ID {docId}.")
    except Exception as e:
        print("Error deleting document.")

def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Delete the document
    try: 
        result = col.delete_one({"_id": int(docId)})
        if result.deleted_count>0:
            print(f"Document with ID {docId} deleted.")
        else:
            print(f"No document found with ID {docId}.")
    except Exception as e:
        print("Error deleting document.")

    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):
    #Query the database to return the documents where each term occurs with their corresponding count. Output example:#
    #{'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3', ...}
    # We are simulating an inverted index here in memory.

    index = {}
    try:
        documents = col.find() 
        for doc in documents:
            doc_id = doc["_id"]
            title = doc["title"] 
            text = doc["text"]
            terms = text.lower().split()

            for term in terms:
                if term in index:
                    index[term].append(f"{title}:{doc_id}")
                else:
                    index[term] = [f"{title}:{doc_id}"]

        sorted_index = {word: ', '.join(set(refs)) for word, refs in index.items()}
        return dict(sorted(sorted_index.items())) 
    except Exception as e:
        print(f"Error retrieving index: {e}")
        return {}