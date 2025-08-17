# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text="Hi this is Ai with Raja!"
#text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# helper: list all voices in your ElevenLabs account
def list_voices():
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    voices = client.voices.get_all()
    print("Available Voices:")
    for v in voices.voices:
        print(f"Name: {v.name}, ID: {v.voice_id}")

# uncomment this to see your voices and IDs
# list_voices()

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    # 🔴 change this to a valid voice_id from list_voices()
    voice_id = "CwhRBWXzGAHq8TQ4Fs17"  

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_turbo_v2",
        text=input_text
    )
    elevenlabs.save(audio, output_filepath)

# run TTS with ElevenLabs
#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3")

#step2a:use Model for text output to voice output
import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    # Save the audio file
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Re-encode with ffmpeg to improve playback compatibility
            fixed_path = output_filepath.replace(".mp3", "_fixed.mp3")
            subprocess.run([
                "ffmpeg", "-y", "-i", output_filepath,
                "-ar", "44100", "-ac", "2", "-b:a", "128k", fixed_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['ffplay', '-nodisp', '-autoexit', fixed_path])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

input_text="New versone autoplaytesting !"
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")

#step2b: eleven labs autoplay

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    # change this to a valid voice_id from list_voices()
    voice_id = "CwhRBWXzGAHq8TQ4Fs17"  

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_turbo_v2",
        text=input_text
    )
    elevenlabs.save(audio, output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Re-encode with ffmpeg to improve playback compatibility
            fixed_path = output_filepath.replace(".mp3", "_fixed.mp3")
            subprocess.run([
                "ffmpeg", "-y", "-i", output_filepath,
                "-ar", "44100", "-ac", "2", "-b:a", "128k", fixed_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            subprocess.run(['ffplay', '-nodisp', '-autoexit', fixed_path])

        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# run TTS with ElevenLabs
text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")