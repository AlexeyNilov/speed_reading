import markdown
from bs4 import BeautifulSoup
from gtts import gTTS


def md_to_text(md_content):
    # Convert Markdown to HTML
    html = markdown.markdown(md_content)
    # Extract plain text from HTML
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


def md_file_to_mp3(md_path, output_path="out/output.mp3", lang="en"):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    plain_text = md_to_text(md_content)

    tts = gTTS(text=plain_text, lang=lang)
    tts.save(output_path)
    print(f"✅ MP3 file saved as: {output_path}")


# Example usage
md_file_to_mp3("txt/jager.md", "output.mp3")
