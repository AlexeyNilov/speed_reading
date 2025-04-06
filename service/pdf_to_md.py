import pymupdf4llm
import pathlib


name = "jager"
md_text = pymupdf4llm.to_markdown(f"in/{name}.pdf")
pathlib.Path(f"txt/{name}.md").write_bytes(md_text.encode())
