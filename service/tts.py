import markdown
from bs4 import BeautifulSoup
import pyttsx3


def md_to_text(md_content):
    # Convert Markdown to HTML
    html = markdown.markdown(md_content)
    # Use BeautifulSoup to extract plain text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def md_file_to_speech(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    plain_text = md_to_text(md_content)
    speak_text(plain_text)


# Example usage
md_file_to_speech("txt/jager.md")
