from dotenv import load_dotenv
import streamlit as st
import data
import ui
import os


def main():

    # Home button
    home_button = st.sidebar.button("Home", type="primary", help="Return to home page", use_container_width=False)

    # Sidebar title
    section_name = json_data[0].get('section')
    st.sidebar.title(f"{section_name}")

    # Create a list of subsection names from the JSON data
    subsection_names = [item.get('subsection_name') for item in json_data]

    # Sidebar content - Select the subsection
    box_sidebar_subsections = st.sidebar.selectbox("Subsections", subsection_names)

    # Add an horizontal line for separation
    st.sidebar.write("---")

    if box_sidebar_subsections == "Home" or home_button:
        ui.show_home_page()
    else:
        # Find the selected subsection in the JSON data
        selected_subsection_data = None
        for item in json_data:
            if item.get('subsection_name') == box_sidebar_subsections:
                selected_subsection_data = item
                break

        if selected_subsection_data is not None:
            # Show the selected subsection content
            ui.show_subsection(selected_subsection_data)
            
            # Add an horizontal line for separation
            st.sidebar.write("---")
            
            ui.logo()
        else:
            st.write("Selected subsection not found in the data.")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    connection_string = os.environ.get("DB_URL")
    database_name = os.environ.get("DB_NAME")
    collection_name = os.environ.get("COLLECTION_NAME")
    
    json_data = data.get_mongodb_data(connection_string, database_name, collection_name)

    os.environ.get("COHERE_API_KEY")
    # Run the main app
    main()
