import markdown
from bs4 import BeautifulSoup
import textwrap
from gtts import gTTS


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


def md_file_to_mp3(text, out_path="out/output.mp3", lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save(out_path)
    print(f"✅ MP3 file saved as: {out_path}")


# Full pipeline
def md_to_speech_pipeline(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    text = md_to_text(md_content)
    chunks = split_text(text, max_chars=1000)

    for idx, chunk in enumerate(chunks):
        out_path = f"out/gtts_{idx}.mp3"
        print(f"🔊 Generating chunk {idx + 1}/{len(chunks)}...")
        md_file_to_mp3(chunk, out_path=out_path)
        break


md_to_speech_pipeline("txt/jager.md")
