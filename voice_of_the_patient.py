# voice_of_the_patient.py

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Step1: Setup Audio recorder (ffmpeg & portaudio)
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Record audio from the microphone and save it as an MP3 file.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred while recording: {e}")

# Step2: Setup Speech to Text – STT – model for transcription
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
stt_model = "whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    if not GROQ_API_KEY:
        raise ValueError(" GROQ_API_KEY is missing! Please set it in your .env file.")

    client = Groq(api_key=GROQ_API_KEY)

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    # Print raw response for debugging
    #print("Raw response:", transcription)

    # Handle both dict and object-style responses
    if hasattr(transcription, "text"):
        return transcription.text
    elif isinstance(transcription, dict) and "text" in transcription:
        return transcription["text"]
    else:
        return None

# Runner
'''if __name__ == "__main__":
    audio_filepath = "patient_voice_test_for_patient.mp3"

    # Step 1: Record audio
    record_audio(file_path=audio_filepath)

    # Step 2: Transcribe audio
    result = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)

    if result:
        print("\n Transcription:", result)
    else:
        print("\n No transcription returned. Check API response above.")
# End of voice_of_the_patient.py
# This script records audio from the microphone, saves it as an MP3 file, '''