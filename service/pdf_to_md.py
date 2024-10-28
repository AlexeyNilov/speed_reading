import pymupdf4llm
import pathlib


name = "map"
md_text = pymupdf4llm.to_markdown(f"pdf/{name}.pdf")
pathlib.Path(f"txt/{name}.md").write_bytes(md_text.encode())
