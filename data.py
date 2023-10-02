from contextlib import contextmanager
from pymongo import MongoClient
import streamlit as st


@contextmanager
def MongoDBConnector():
    try:
        client = MongoClient(st.secrets["DB_URI"])
        database = client[st.secrets["DB_NAME"]]
        collection = database[st.secrets["COLLECTION_NAME"]]

        yield collection

    except Exception as e:
        st.error(e)
    finally:
        client.close()


@st.cache_data(show_spinner="Fetching data from database...")
def load_sections(section):
    with MongoDBConnector() as collection:
        result = list(collection.find({'section': section}, {'_id':0}))
    return result


def append_new_exercise(new_exercise, section_name, subsection_number):    
    # Filter to identify the document to update
    filter = {
        "section": section_name,
        "subsection_number": subsection_number
    }

    # Push the new exercise to the 'exercises' array
    append = {
        "$push": {
            "exercises": new_exercise[0]
            }
        }

    with MongoDBConnector() as collection:
        try:
            # Update the document
            exercises_appended = collection.update_one(filter, append)
            collection

            if exercises_appended.modified_count > 0:
                st.success(f"Exercises added successfully: {exercises_appended.modified_count}.")
            else:
                st.error("No documents were added.")
        
        except Exception as e:
            st.error(e)
    
    # Clear values from *all* in-memory or on-disk cached functions
    st.cache_data.clear()
