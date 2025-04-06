import markdown
from bs4 import BeautifulSoup
import requests
import textwrap
from conf.settings import api_key


# Convert Markdown to plain text
def md_to_text(md_content):
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


# Split text into chunks under max_chars, preserving sentence boundaries
def split_text(text, max_chars=1000):
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


def elevenlabs_tts(
    text, voice="nPczCjzI2devNBz1zQrb", api_key=api_key, out_path="out/eleven_labs.mp3"
):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}

    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved: {out_path}")
    else:
        print("❌ Error:", response.status_code, response.text)


# Full pipeline
def md_to_speech_pipeline(md_path, api_key):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    text = md_to_text(md_content)
    chunks = split_text(text, max_chars=1000)

    for idx, chunk in enumerate(chunks):
        if idx < 2:
            continue
        out_path = f"out/chunk_{idx}.mp3"
        print(f"🔊 Generating chunk {idx + 1}/{len(chunks)}...")
        elevenlabs_tts(chunk, api_key=api_key, out_path=out_path)
        break


md_to_speech_pipeline("txt/jager.md", api_key)
