import tempfile
import base64

from gtts import gTTS


# Function to decode 64 based text to audio
def decode_text2audio(base64_encoded_audio):
    audio_binary_data = base64.b64decode(base64_encoded_audio)

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
        temp_audio.write(audio_binary_data)
        audio_path = temp_audio.name
    
    return audio_path

def generate_audio(text, language='en'):
    tts = gTTS(text, lang=language)

    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        tts.save(temp_audio.name)
    return temp_audio.name
