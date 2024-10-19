from pydub import AudioSegment
import os

def convert_mp4_to_mp3(input_path, output_path):
    """Converts an MP4 file to MP3."""
    try:
        # Load the MP4 file
        audio = AudioSegment.from_file(input_path, format='mp4')
        
        # Export the audio as MP3
        audio.export(output_path, format='mp3')
        print(f"Conversion complete: {output_path}")
    except Exception as e:
        print(f"Error during conversion of {input_path}: {e}")

# Example usage
input_file = input("Enter the path to the MP4 file: ")
output_file = "/Users/luisguinea/Downloads/converted.mp3"

convert_mp4_to_mp3(input_file, output_file)