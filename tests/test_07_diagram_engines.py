import pytest
from src.html_renderer import HTMLRenderer
from bs4 import BeautifulSoup

def test_mermaid_rendering():
    """Kiểm thử việc bẫy và bọc khối mã Mermaid vào thẻ div.mermaid"""
    markdown_text = "```mermaid\ngraph TD;\n    A-->B;\n```"
    diagram_config = {
        "enable_mermaid": True,
        "mermaid_assets_dir": "assets/mermaid",
        "mermaid_js_filename": "mermaid.min.js",
        "enable_d2": False
    }
    renderer = HTMLRenderer(diagram_config=diagram_config)
    _, html = renderer.convert_to_html(markdown_text)
    
    soup = BeautifulSoup(html, "html.parser")
    mermaid_div = soup.find("div", class_="mermaid")
    
    assert mermaid_div is not None
    assert "graph TD;" in mermaid_div.text

def test_d2_rendering_disabled():
    """Kiểm thử khi tắt D2, mã D2 sẽ bị highlight như code text bình thường."""
    markdown_text = "```d2\nx -> y\n```"
    diagram_config = {
        "enable_mermaid": False,
        "enable_d2": False
    }
    renderer = HTMLRenderer(diagram_config=diagram_config)
    _, html = renderer.convert_to_html(markdown_text)
    
    soup = BeautifulSoup(html, "html.parser")
    highlight_div = soup.find("div", class_="highlight")
    
    assert highlight_div is not None
    assert "x -> y" in highlight_div.text
    # Không được xuất hiện thẻ img base64 vì đã tắt
    assert soup.find("div", class_="d2-diagram") is None
