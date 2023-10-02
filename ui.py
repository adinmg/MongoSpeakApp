import audio
import llm_module
import streamlit as st
from data import append_new_exercise

# Function to disable Create, Update and Delete buttons
def disable():
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None
        return True
    elif st.session_state["authentication_status"] == True:
        return False
    else:
        return True


# Function to display a selected subsubsection
def show_subsubsection(selected_subsection_data):
    language = selected_subsection_data.get("language")
    exercises = selected_subsection_data.get('exercises')

    for item in exercises:
        exercise_number = item.get('exercise_number')
        st.markdown(f"#### Exercise {exercise_number}")

        sentence = item.get('sentence')
        st.markdown(f"**A)** {sentence}")
        if len(sentence) > 1:
            st.audio(audio.generate_audio(sentence, language))

        answer = item.get('answer')
        st.markdown(f"**B)** {answer}")
        if len(answer) > 1:
            st.audio(audio.generate_audio(answer))


# Function to display a selected subsection
def show_subsection(selected_subsection_data, disable_button):
    container = st.container()
    section_name= selected_subsection_data.get("section")
    subsection_number = selected_subsection_data.get("subsection_number")
    subsection_name = selected_subsection_data.get('subsection_name')
    language = selected_subsection_data.get("language")
    instruction = selected_subsection_data.get("instruction")

    container.info(f"{instruction}")

    exercises = selected_subsection_data.get('exercises')

    # Get the current page section number from the query parameters
    query_params = st.experimental_get_query_params()
    # Get the current exercise number from the query parameters
    st.session_state['current_exercise'] = int(query_params["exercise"][0]) if "exercise" in query_params else 1
    
    # Set the query parameters to navigate to the selected section
    st.experimental_set_query_params(subsection=st.session_state['current_subsection'], exercise=st.session_state['current_exercise'])

    # Create buttons to navigate to the next and previous exercises
    col1, _, col2 = st.columns([1, 0.2, 1])
    with col1:
        if st.button("⏮️", use_container_width=True):
            st.session_state['current_exercise'] -= 1
            if st.session_state['current_exercise'] == 0:
                st.session_state['current_exercise'] = len(exercises)
            # Set the query parameters to navigate to the previous exercise
            st.experimental_set_query_params(subsection=st.session_state['current_subsection'], exercise=st.session_state['current_exercise'])
    with col2:
        if st.button("⏭️", use_container_width=True):
            st.session_state['current_exercise'] += 1
            if st.session_state['current_exercise'] == len(exercises)+1:
                st.session_state['current_exercise'] = 1
            # Set the query parameters to navigate to the next exercise
            st.experimental_set_query_params(subsection=st.session_state['current_subsection'], exercise=st.session_state['current_exercise'])

    if 1<= st.session_state['current_exercise'] <= len(exercises):
        exercise = exercises[st.session_state['current_exercise']-1]
        exercise_number = exercise.get("exercise_number")
        container.markdown(f"#### Exercise {exercise_number}")

        sentence = exercise.get('sentence')
        container.markdown(f"**Sentence**: {sentence}")
        container.audio(audio.generate_audio(sentence, language=language))

        with container.expander("Answer"):
            answer = exercise.get('answer')
            st.markdown(f"{answer}")
            st.audio(audio.generate_audio(answer))

    st.sidebar.write("---")
    
    if st.sidebar.button('Generate (_Cohere LLM_)', type='secondary', use_container_width=False):
        with st.spinner("Please wait..."):
            new_sentences_json = llm_module.generate_additional_sentences(exercises, section_name, subsection_number, subsection_name, instruction, language=language, start=len(exercises)+1)
            st.session_state["new_sentences_json"] = new_sentences_json[0]
    
    if st.session_state["new_sentences_json"]:
        show_subsubsection(st.session_state["new_sentences_json"])
        st.write("---")
        st.write(st.session_state["new_sentences_json"])

        append_button = st.button("Append", disabled=disable_button)
        if append_button:
            append_new_exercise(st.session_state["new_sentences_json"]["exercises"], section_name, subsection_number)


def logo():
    st.sidebar.write("<br><div style='text-align: center; font-size: small;'>Made by </div><div style='text-align: center; font-size: small;'><a href='https://github.com/adinmg/MongoSpeakApp'>@adinmg</a></div>", unsafe_allow_html=True)

