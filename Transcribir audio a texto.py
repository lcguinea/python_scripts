# %%
from pydub import AudioSegment
import speech_recognition as sr

# Step 2: Convert M4A to WAV
audio = AudioSegment.from_file(input("Introduce la ruta del archivo:"), format="m4a")
audio = audio.normalize()  # Normalize audio
audio_path = "converted_audio.wav"
audio.export(audio_path, format="wav")

# Step 3: Transcribe audio to text
recognizer = sr.Recognizer()

# Function to transcribe audio in chunks
def transcribe_audio(audio_path):
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")  # Specify Spanish language
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Split audio into larger chunks and transcribe each chunk
chunk_length_ms = 60000  # 60 seconds
chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

full_transcription = ""
for i, chunk in enumerate(chunks):
    chunk_path = f"chunk{i}.wav"
    chunk.export(chunk_path, format="wav")
    transcription = transcribe_audio(chunk_path)
    full_transcription += transcription + " "

# Export transcription to a text file
with open("transcription.txt", "w", encoding="utf-8") as file:
    file.write(full_transcription)

print("Full Transcription: ", full_transcription)

