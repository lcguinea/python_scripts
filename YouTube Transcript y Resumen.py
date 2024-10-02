# %%
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from pytube import YouTube
import re
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from docx import Document

# Fetch the transcript and video title
video_id = 'TeIvGktnaMY'  # Replace with your YouTube video ID
video_url = f"https://www.youtube.com/watch?v={video_id}"

# Get video title
yt = YouTube(video_url)
video_title = yt.title

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
except NoTranscriptFound:
    print("No Spanish transcript found.")
    transcript = []

# Handle the transcript data
transcript_text = ""
for entry in transcript:
    transcript_text += f"{entry['start']} - {entry.get('end', entry['start'] + 5)}: {entry['text']}\n"

# Clean the transcript
cleaned_lines = []
for line in transcript_text.split('\n'):
    cleaned_line = re.sub(r'^\d+\.\d+ - \d+\.\d+: ', '', line)
    cleaned_lines.append(cleaned_line)
cleaned_text = " ".join(cleaned_lines).strip()

# Summarize the cleaned transcript using the Hugging Face Transformers library (Spanish)
print(f"Versión de PyTorch: {torch.__version__}")
device = 0 if torch.cuda.is_available() else -1
print(f"Usando dispositivo: {'GPU' if device == 0 else 'CPU'}")

# Split the content into smaller chunks
max_chunk_size = 1000  # Adjust the chunk size as needed
chunks = [cleaned_text[i:i + max_chunk_size] for i in range(0, len(cleaned_text), max_chunk_size)]

# Initialize the model and tokenizer
model_name = "mrm8488/bert2bert_shared-spanish-finetuned-summarization"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=device)

# Generate the summary for each chunk and concatenate the results
summary_text = ""
for chunk in chunks:
    summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
    summary_text += summary[0]['summary_text'] + " "

# Create a Word document and save the cleaned transcript and summary
doc = Document()
doc.add_heading(video_title, 0)

doc.add_heading('Transcripción Limpia', level=1)
doc.add_paragraph(cleaned_text)

doc.add_heading('Resumen', level=1)
doc.add_paragraph(summary_text.strip())

output_file_path = f"{video_title}.docx"
doc.save(output_file_path)

print(f"Transcripción limpia y resumen guardados en {output_file_path}")