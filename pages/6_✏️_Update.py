from data import MongoDBConnector
from bson import ObjectId
from ui import disable
import streamlit as st
from ui import logo
import json


disable_buttons = disable()


# Define "query" in Session State
if "query" not in st.session_state:
    st.session_state["query"] = ""

st.subheader("Update a Record")

# Input field to specify the ID of the record to update
record_id_to_update = st.text_input("Enter the ID of the record you want to update")

if st.button("Find Record"):
    with MongoDBConnector() as collection:
        # Create a query to find the document by its ID
        st.session_state["query"] = {"_id": ObjectId(record_id_to_update)}
        document_to_update = collection.find_one(st.session_state["query"])

    if document_to_update:
        # Display the current document for modification
        st.write("Current Document:")
        st.json(document_to_update, expanded=True)
    else:
        st.warning(f"No record found with ID {record_id_to_update}.")

# Text area for specifying updates
text = st.text_area("Insert the fields that you want to update as a key-value pairs")
update_json = '{"$set": {' + text + '}}'

if text:
    try:
        update = json.loads(update_json)
        st.write("Your update operation will look like this:")
        st.json(update)
        st.success("JSON is OK.")
    except Exception as e:
        st.error(e)

update_button = st.button("Update Record", disabled=disable_buttons)

if update_button:

    # Perform the update operation
    with MongoDBConnector() as collection:
        update_result = collection.update_one(st.session_state["query"], update)

    if update_result.modified_count > 0:
        st.success(f"Record with ID {record_id_to_update} updated successfully.")
    else:
        st.warning("No modifications were made.")

logo()