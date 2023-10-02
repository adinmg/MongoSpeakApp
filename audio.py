from gtts import gTTS
import tempfile

def generate_audio(text, language='en'):
    tts = gTTS(text, lang=language)

    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        tts.save(temp_audio.name)
    
    return temp_audio.name
