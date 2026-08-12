# ==============================================================================
# MÔ-ĐUN KIỂM THỬ 03: MATH BASE64 & TYPOGRAPHY ISOLATION (test_03_math_base64.py)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Base64 Math AST Isolation & Vietnamese Math Armor
# ==============================================================================

import base64
import re
import shutil
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ast_parser import ASTParser
from src.html_renderer import HTMLRenderer
from src.pdf_compiler import PDFCompiler


class MathBase64Tests(unittest.TestCase):
    """Mô-đun 03: Kiểm thử Độc lập Base64 TeX, KaTeX, & Tiếng Việt trong Toán học."""

    def setUp(self):
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / "tests" / "temp_redteam_workspace"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.parser = ASTParser(encoding_standard="utf-8", enable_math=True, enable_tables=True)
        self.renderer = HTMLRenderer(
            theme_name="monokai",
            enable_math=True,
            katex_config={
                "enable_katex": True,
                "assets_dir": "assets/katex",
                "css_filename": "katex.min.css",
                "js_filename": "katex.min.js",
                "auto_render_js_filename": "auto-render.min.js",
                "strict_mode": False,
                "throw_on_error": False,
                "enable_base64_math_encoding": True,
                "enable_vietnamese_math_isolation": True,
                "vietnamese_font_family": '"Times New Roman", "Segoe UI", Arial, sans-serif',
            },
        )
        self.compiler = PDFCompiler(
            output_encoding="utf-8",
            layout_config={"page_size": "A4", "margin": "20mm"},
        )

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_scenario_7_math_rendering_and_fault_tolerance(self):
        """Scenario 7: Đúc KaTeX & Phủ kín Inline/Block Math."""
        math_content = (
            "# Math Test\n"
            "Inline: $x = 1$\n"
            "Block: $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$\n"
        )
        css, rendered_html = self.renderer.convert_to_html(math_content)
        self.assertTrue('<span class="math-tex-b64"' in rendered_html or '<span class="math-tex">' in rendered_html)
        self.assertTrue('<div class="math-tex-b64"' in rendered_html or '<div class="math-tex">' in rendered_html)

        output_pdf = self.temp_dir / "temp_math_test.pdf"
        try:
            self.compiler.compile_to_pdf(rendered_html, css, output_pdf)
            self.assertTrue(output_pdf.exists())
        finally:
            if output_pdf.exists():
                output_pdf.unlink()

    def test_scenario_15_math_escaping_and_base64_injection(self):
        """Scenario 15: Kiểm thử Base64 Math AST Isolation & Typography Isolation."""
        math_md = "$$\\boxed{\\text{Syntax} \\neq \\text{Semantic}}$$\n"
        _css, rendered_html = self.renderer.convert_to_html(math_md)
        self.assertIn('class="math-tex-b64"', rendered_html)
        self.assertIn("vietnamese-math-text", rendered_html)

    def test_scenario_17_base64_math_ast_isolation(self):
        """Scenario 17: Cô lập ký tự nhạy cảm <, %, _ trong toán học."""
        dangerous_md = "$ 0 < % \\leq \\text{Lỗi} $"
        _css, rendered_html = self.renderer.convert_to_html(dangerous_md)

        self.assertNotIn("0 < %", rendered_html)
        self.assertIn('class="math-tex-b64"', rendered_html)

        b64_match = re.search(r'data-math-b64="([^"]+)"', rendered_html)
        self.assertIsNotNone(b64_match)
        if b64_match:
            decoded = base64.b64decode(b64_match.group(1)).decode("utf-8")
            self.assertIn("0 < % \\leq", decoded)

    def test_scenario_18_vietnamese_math_isolation_structure(self):
        """Scenario 18: Lớp giáp Typography Tiếng Việt trong vĩ lệnh KaTeX."""
        vietnamese_md = "\\[ \\boxed{\\text{Thao tác số học phổ quát} \\neq \\text{Toán học}} \\]"
        isolated = self.renderer._isolate_vietnamese_in_math(vietnamese_md)
        self.assertIn("\\htmlClass{vietnamese-math-text}{\\text{Thao tác số học phổ quát}}", isolated)

        _css, rendered_html = self.renderer.convert_to_html(vietnamese_md)
        self.assertIn("position: static !important;", rendered_html)


if __name__ == "__main__":
    unittest.main()
