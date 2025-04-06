import os
from google.cloud import texttospeech
from pydub import AudioSegment
import re


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "conf/text-to-speech-key.json"


def restore_text(text):
    # Remove lines that contain only dashes (like page breaks)
    text = re.sub(r"\n?^-{5,}\n?", " ", text, flags=re.MULTILINE)

    # Replace newlines followed/preceded by non-punctuation characters with a space (to reconnect broken sentences)
    text = re.sub(r"(?<![\.\!\?])\n(?![\n\.\!\?])", " ", text)

    # Collapse multiple spaces into one
    text = re.sub(r"\s{2,}", " ", text)

    text = re.sub(r"\[(\d+)\]", " ", text)

    return text.strip()


def split_text(text, max_chars=1000):
    # Use regex to split by sentence-ending punctuation followed by whitespace and capital letter
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk += (" " if current_chunk else "") + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            # If the sentence itself is too long, break it hard (optional: use smarter splitting)
            if len(sentence) > max_chars:
                parts = [
                    sentence[i : i + max_chars]
                    for i in range(0, len(sentence), max_chars)
                ]
                chunks.extend(parts[:-1])
                current_chunk = parts[-1]
            else:
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# Combine multiple mp3 files
def merge_mp3s(mp3_paths, output_path="final_output.mp3", cleanup=True):
    combined = AudioSegment.empty()
    for path in mp3_paths:
        combined += AudioSegment.from_mp3(path)
    combined.export(output_path, format="mp3")
    print(f"✅ Final audio saved as: {output_path}")
    if cleanup:
        for f in mp3_paths:
            os.remove(f)


# Generate MP3 using Google Cloud TTS
def synthesize_speech(
    text,
    out_path,
    language_code="en-US",
    voice_name="en-US-Standard-D",
    speaking_rate=0.9,
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
def md_to_speech_pipeline(md_path, output_dir="out", start=0, stop=50):
    os.makedirs(output_dir, exist_ok=True)

    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = restore_text(text)
    chunks = split_text(text)

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

    merge_mp3s(temp_files, output_path=f"out/final_output_{start}-{stop}.mp3")


md_to_speech_pipeline("txt/jager.md")
