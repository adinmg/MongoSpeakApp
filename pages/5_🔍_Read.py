from data import MongoDBConnector
import streamlit as st
from ui import logo

# Read page content
st.subheader("Read a Record")
section_to_read = st.number_input("Section Number", value=0, format="%d")
subsection_to_read = st.number_input("Subsection Number", value=0, format="%d")

# Check if either section or subsection is provided
if not section_to_read and not subsection_to_read == 0:
    st.warning("Please provide a proper Section Name or a Subsection Number.")
    
if st.button("Read a Record"):
    with MongoDBConnector() as collection:
        # Define a query to match the specific section and subsection
        query = {
            "section": f"Lesson {section_to_read}",
            "subsection_number": subsection_to_read
        }

        # Count documents that match the query
        document_count = collection.count_documents(query)

        # Check if there are any documents
        if document_count == 0:
            st.warning("No documents found for the specified criteria.")
        else:
            # Process and display the retrieved documents
            st.success(f"Total documents found: {document_count}.")
            documents = collection.find(query)
            for document in documents:
                st.json(document)

logo()