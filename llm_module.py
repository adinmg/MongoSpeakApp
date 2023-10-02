from langchain.llms import Cohere
import streamlit as st
import random
import json


# Load environment variables
cohere_api_key = st.secrets["COHERE_API_KEY"]

# Initialize Cohere model
cohere = Cohere(model='command-nightly', temperature=0.9, max_tokens=100)

# Function to convert generated text to JSON
def convert_text_to_json(text, section, subsection_number, subsection_name, instruction, language, start):
    data = []

    sentences = text.strip().split('\n')

    for exercise_number, sentence_block in enumerate(sentences, start=start):
        sentences_lines = sentence_block.split('.')
        
        sentence = sentences_lines[0]
        answer = sentences_lines[1] if len(sentences_lines) > 1 else "?"

        item = {
            'exercise_number': exercise_number,
            'sentence': sentence,
            'answer': answer
        }

        data.append(item)

    section_data = {
        'section': section,
        'subsection_number': subsection_number,
        'subsection_name': subsection_name,
        'instruction': instruction,
        'language': language,
        'exercises': data
    }

    json_data = json.dumps([section_data], indent=2, ensure_ascii=False)
    return json_data


# Loop through the exercises and generate new sentences and answers
def generate_additional_sentences(exercises, section, subsection_number, subsection_name, instruction, language, start):
    example1 = random.sample(exercises, k=1)[-1]
    example2 = random.sample(exercises, k=1)[-1]
    
    text = f"""
Example 1:
{example1.get("sentence", None)} {example1.get("answer", None)}

Example 2:
{example2.get("sentence", None)} {example2.get("answer", None)}

Generate one example following the same structure. Exclude the introductory and concluding sentences.
"""

    new_sentences = cohere(text)
    new_sentences_json = convert_text_to_json(new_sentences, section, subsection_number, 
                                              subsection_name, instruction, language=language, start=start)
    
    return json.loads(new_sentences_json)
