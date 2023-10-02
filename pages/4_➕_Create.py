from data import MongoDBConnector
import streamlit as st
from ui import disable
from ui import logo


disable_buttons = disable()

# Function to create exercises from user input
def create_exercises(text_area_input):
    sentences = [sentence.strip() for sentence in text_area_input.split("\n") if sentence.strip()]
    exercises = []
    for idx in range(len(sentences)//2):
        sentence = sentences[2*idx]
        answer = sentences[2*idx+1]
        exercise = {
            "exercise_number": idx,
            "sentence": sentence,
            "answer": answer
        }
        exercises.append(exercise)
    return exercises


# Create page content
st.subheader("Create a Section")

with st.form("new_section"):
    input_section_name = st.text_input("Section")
    input_subsection_number = st.number_input("Subsection Number", value=1, format="%d")
    input_subsection_name = st.text_input("Subsection")
    input_instruction = st.text_input("Instruction")
    input_language = st.text_input("Language", max_chars=2, placeholder="'en' or 'es'")
    txt = st.text_area("Insert your sentences")
    
    # Create exercise objects from user input
    exercises = create_exercises(txt)
    
    new_section = {
        "section": input_section_name,
        "subsection_number": input_subsection_number,
        "subsection_name": input_subsection_name,
        "instruction": input_instruction,
        "language": input_language,
        "exercises": exercises
    }
    
    st.write(new_section)
    submit = st.form_submit_button("Create a Section", disabled=disable_buttons)
    
    if submit:
        with MongoDBConnector() as collection:
            # Create a new section
            collection.insert_one(new_section)
        st.success("You have successfully created a new Section.")

logo()