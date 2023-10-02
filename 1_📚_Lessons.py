from data import load_sections
from ui import disable
import streamlit as st
from ui import logo
import ui


# Load authenticatication state to disable buttons
disable_button = disable()

# Initialize new_sentences_json in session_state
if "new_sentences_json" not in st.session_state:
    st.session_state["new_sentences_json"] = []

# Create a list of section names from JSON data
section_names = [f"Lesson {n}" for n in range(1,11)]

# Sections - Sidebar
box_sidebar_section = st.sidebar.selectbox(label="Sections", options=section_names)

# Load from database the selected section
json_data = load_sections(box_sidebar_section)

# Create a dictionary of subsection names and subsection numbers from the JSON data
subsection_number = {item.get('subsection_name'): item.get('subsection_number') for item in json_data}

# Get the current page section number from the query parameters
query_params = st.experimental_get_query_params()

# Initialize subsection_number in session state
st.session_state['current_subsection'] = int(query_params['subsection'][0]) if 'subsection' in query_params else 1
# Get the current exercise number from the query parameters
st.session_state['current_exercise'] = int(query_params["exercise"][0]) if "exercise" in query_params else 1

# Sidebar content - Select the subsection
box_sidebar_subsections = st.sidebar.selectbox(label="Subsections", options=list(subsection_number.keys()))

# Update subsection number if it changes
st.session_state['current_subsection'] = subsection_number[box_sidebar_subsections]

# Find the selected subsection data
selected_subsection_data = json_data[st.session_state['current_subsection']-1]

# Set the query parameters to navigate to the selected section
st.experimental_set_query_params(subsection=st.session_state['current_subsection'], exercise=st.session_state['current_exercise'])

# Main content
intro = st.empty()
with intro.expander(label="", expanded=True):
    st.success(
"""
## MongoSpeakApp 🎓🇲🇽 🇺🇸

This is a Streamlit app designed to improve your English fluency. 
It offers speaking exercises with paraphrasing, translation, numbers, and vocabulary.

You can freely navigate through all the app pages without any restrictions. 
However, please note that access to Create, Update, and Delete Operations is currently restricted.

Enjoy exploring the app and improving your English fluency! 🌟
""")
    close_button = st.button("Close")

if close_button:
    intro.empty()

st.subheader(f"{box_sidebar_section}: Section {st.session_state['current_subsection']}")
st.subheader(f"{box_sidebar_subsections}")

if selected_subsection_data is not None:
    # Show the selected subsection content
    ui.show_subsection(selected_subsection_data, disable_button)    
else:
    st.error("Selected subsection not found in the data.")


logo()