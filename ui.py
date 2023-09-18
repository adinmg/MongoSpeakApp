import audio
import llm_module
import streamlit as st

import random

# Function to display the home page content
def show_home_page():
    st.title("Welcome to My Portfolio App")
    st.write("This is a Streamlit app showcasing my portfolio. It includes exercises with audio, text-to-audio conversion, and data retrieved from MongoDB.")

    st.subheader("About Me")
    st.write("I am a physicist passionate about machine learning, deep learning, data and creating interactive web applications with Streamlit.")

    st.subheader("My Projects")
    st.write("Here are some of the projects I have worked on:")
    # Add project descriptions, links, or images here

    st.subheader("Tools and Packages")
    st.markdown("In this app, I have used various tools and packages to build its features, including:")
    st.markdown("- **Streamlit**: Interactive web app framework for Python.")
    st.markdown("- **MongoDB**: Database for storing and retrieving data.")
    st.markdown("- **PyMongo**: Python library containing tools for working with MongoDB.")
    st.markdown("- **gTTS**: Library for converting text to speech.")
    st.markdown("- **Base64**: Encoding and decoding binary data.")
    st.markdown("- **Tempfile**: Creating temporary files.")

    st.subheader("Contact Me")
    st.write("You can contact me at: josue.adin@gmail.com")


# Function to display a selected subsubsection
def show_subsubsection(selected_subsection_data, anchor_name):
    # Get subsection info
    subsection_number = selected_subsection_data.get("subsection_number")
    subsection_name = selected_subsection_data.get('subsection_name')

    # Create an anchor
    st.markdown(f'<a name="{anchor_name}"></a>', unsafe_allow_html=True)
    st.header(f"{subsection_number}. {subsection_name}. New Sentences")

    # Get the language
    language = selected_subsection_data.get("language")

    # Get the list of exercises for the selected subsection
    exercises = selected_subsection_data.get('exercises')

    # Loop through the exercises and display the sentences and answetext 
    for item in exercises:
        exercise_number = item.get('exercise_number')
        st.markdown(f"#### Exercise {exercise_number}")

        sentence = item.get('sentence')
        st.markdown(f"**A)** {sentence}")
        if len(sentence) > 1:
            st.audio(audio.generate_audio(sentence, language))

        # with st.expander("Answer"):
        answer = item.get('answer')
        st.markdown(f"**B)** {answer}")
        if len(answer) > 1:
            st.audio(audio.generate_audio(answer))


# Function to display a selected subsection
def show_subsection(selected_subsection_data):
    subsection_number = selected_subsection_data.get("subsection_number")
    subsection_name = selected_subsection_data.get('subsection_name')
    st.header(f"{subsection_number}. {subsection_name}")

    # Instructions
    instruction = selected_subsection_data.get("instruction")
    st.write(f"{instruction}")
    st.write("---")

    # Get the list of exercises for the selected subsection
    st.sidebar.subheader("Advance Mode")
    if st.sidebar.button(label='Suffle 5 Exercises'):
        exercises = random.sample(selected_subsection_data.get('exercises'), k=5)
    else:
        exercises = selected_subsection_data.get('exercises')

    # Loop through the exercises and display the sentences and answer text 
    for item in exercises:
        exercise_number = item.get('exercise_number')
        st.markdown(f"#### Exercise {exercise_number}")

        sentence = item.get('sentence')
        st.markdown(f"**Sentence**: {sentence}")
        base64_encoded_audio = item.get('sentence_audio')
        audio_path = audio.decode_text2audio(base64_encoded_audio)
        st.audio(audio_path)

        with st.expander("Answer"):
            answer = item.get('answer')
            st.markdown(f">{answer}")
            base64_encoded_audio = item.get('answer_audio')
            audio_path = audio.decode_text2audio(base64_encoded_audio)
            st.audio(audio_path)

    st.write("---")
    
    if st.sidebar.button('Generate 5 Exercises (_Cohere LLM_)', type='secondary', use_container_width=False):
        # Take 5 samples to generate new ones
        sample_exercises = random.sample(population=exercises, k=5)
        # Generate new sentences.
        new_sentences_json = llm_module.generate_additional_sentences(sample_exercises, subsection_number, subsection_name, selected_subsection_data, start=len(exercises)+1)
        show_subsubsection(new_sentences_json[0], anchor_name='NewSentences')

        # Create a hyperlink to the generated subsubsection in the sidebar
        st.sidebar.markdown(f'[Go to Generated Sentences](#NewSentences)')
        
def logo():
    st.sidebar.write("<br><div style='text-align: center; font-size: small;'>Developed by</div><div style='text-align: center; font-size: small;'><a href='https://github.com/adinmg/MongoSpeakApp'>Josue A. Minguela</a></div>", unsafe_allow_html=True)

