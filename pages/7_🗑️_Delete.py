from data import MongoDBConnector
from bson import ObjectId
import streamlit as st
from ui import disable
from ui import logo


disable_buttons = disable()

if "query" not in st.session_state:
    st.session_state["query"] = ""

if "ID" not in st.session_state:
    st.session_state["ID"] = ""

# Page Header
st.subheader("Delete a Record")

# Form for deleting a Record
with st.form("delete"):
    st.session_state["ID"] = st.text_input("Enter the ID of the record you want to delete")
    find2delete = st.form_submit_button("Find a Record")

    # Find and display the document to delete
    if find2delete:
        with MongoDBConnector() as collection:
            st.session_state["query"] = {"_id": ObjectId(st.session_state["ID"])}
            document_to_delete = collection.find_one(st.session_state["query"])
    
            st.json(document_to_delete)

# Button to Delete a Record
if st.button("Delete a Record", disabled=disable_buttons):
    with MongoDBConnector() as collection:
        try:
            delete_result = collection.delete_one(st.session_state["query"])

            if delete_result.deleted_count > 0:
                st.success(f"Record with ID '{st.session_state['ID']}' deleted successfully.")

            else:
                st.error(f"No record found with ID {st.session_state['ID']}.")

        except Exception as e:
            st.error(f"An error occurred while deleting the record: {e}")


logo()