from pymongo import MongoClient
import streamlit as st

@st.cache_data()
def get_mongodb_data(connection_string, database_name, collection_name):
    # Connect to MongoDB
    client = MongoClient(connection_string)
    database = client[database_name]
    collection = database[collection_name]

    # Retrieve data from collection
    cursor = collection.find({}, {'_id':0})
    data = list(cursor)

    # Close the connection
    client.close()

    return data
