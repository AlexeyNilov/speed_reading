import os
import markdown
import textwrap
from bs4 import BeautifulSoup
from google.cloud import texttospeech
from pydub import AudioSegment


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "conf/text-to-speech-key.json"


# Convert Markdown to plain text
def md_to_text(md_content):
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


# Split text into chunks under max_chars, preserving sentence boundaries
def split_text(text, max_chars=5000):
    chunks = []
    current_chunk = ""

    for paragraph in text.split("\n\n"):
        for line in textwrap.wrap(
            paragraph, width=max_chars, break_long_words=False, replace_whitespace=False
        ):
            if len(current_chunk) + len(line) + 2 <= max_chars:
                current_chunk += line + "\n\n"
            else:
                chunks.append(current_chunk.strip())
                current_chunk = line + "\n\n"
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


# Combine multiple mp3 files
def merge_mp3s(mp3_paths, output_path="final_output.mp3"):
    combined = AudioSegment.empty()
    for path in mp3_paths:
        combined += AudioSegment.from_mp3(path)
    combined.export(output_path, format="mp3")
    print(f"✅ Final audio saved as: {output_path}")


# Generate MP3 using Google Cloud TTS
def synthesize_speech(
    text,
    out_path,
    language_code="en-US",
    voice_name="en-US-Standard-D",
    speaking_rate=1.0,
):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_rate
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(out_path, "wb") as out:
        out.write(response.audio_content)
    print(f"✅ MP3 file saved as: {out_path}")


# Full pipeline
def md_to_speech_pipeline(md_path, output_dir="out", start=0, stop=1):
    os.makedirs(output_dir, exist_ok=True)

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    text = md_to_text(md_content)
    chunks = split_text(text, max_chars=1000)

    temp_files = []
    for idx, chunk in enumerate(chunks):
        if idx < start:
            continue
        out_path = os.path.join(output_dir, f"google_tts_{idx}.mp3")
        print(f"🔊 Generating chunk {idx}/{len(chunks)}...")
        synthesize_speech(chunk, out_path)
        temp_files.append(out_path)
        if idx == stop:
            break

    merge_mp3s(temp_files, output_path=f"out/final_output_{stop}.mp3")

    # Optional cleanup
    for f in temp_files:
        os.remove(f)


# Example usage
md_to_speech_pipeline("txt/jager.md")
