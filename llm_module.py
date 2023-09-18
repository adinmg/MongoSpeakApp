from langchain.llms import Cohere
import json
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ.get("COHERE_API_KEY")

cohere = Cohere(model='command')

# Function to retrieve sentences from LLMs
def convert_text_to_json(text, section, subsection_number, subsection_name, language, start):
    data = []

    sentences = text.strip().split('\n\n')

    for exercise_number, sentence_block in enumerate(sentences, start=start):
        sentences_lines = sentence_block.split('\n')
        
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
        'language': language,
        'exercises': data
    }

    json_data = json.dumps([section_data], indent=2, ensure_ascii=False)
    return json_data

# Loop through the exercises and generate new sentences and answers
def generate_additional_sentences(exercises, subsection_number, subsection_name, selected_subsection_data, start):
    text = "Act as an English teacher. Generate five new pairs similar to the following sentences.\n"
    for item in exercises:
        sentence = item.get('sentence')
        answer = item.get('answer')
        text = text + sentence + "\n" + answer +"\n\n"
    
    text = text + "Show five pair as:\n'sentence'\n'sentence'\n\n\n'sentence'\n'sentence'\n\nDo not create the introductory and concluding sentences."
    new_sentences = cohere(text, temperature=0.6)
    new_sentences_text = convert_text_to_json(new_sentences, "Lesson 1 (gen)", subsection_number, 
                                              subsection_name, language=selected_subsection_data.get("language"), start=start)
    
    return json.loads(new_sentences_text)