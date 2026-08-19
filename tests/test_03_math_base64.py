# ==============================================================================
# MÔ-ĐUN KIỂM THỬ 03: MATH RENDERING & VIETNAMESE ISOLATION (test_03_math_base64.py)
# Dự án: markdown_to_pdf_engine (Phiên bản v2.5.2 - Python Dictionary Mapping)
# Kiến trúc: Server-side Python Mapping, VILANGMASK ASCII Armor & KaTeX TreeWalker Swap
# ==============================================================================

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
    """Mô-đun 03: Kiểm thử Động cơ KaTeX, Thuật toán Python Dictionary Mapping & Tiếng Việt trong Toán học."""

    def setUp(self) -> None:
        """Khởi tạo môi trường kiểm thử và các thực thể động cơ lõi."""
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / "tests" / "temp_redteam_workspace"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.parser = ASTParser(encoding_standard="utf-8", enable_math=True, enable_tables=True)
        self.renderer = HTMLRenderer(
            theme_name="monokai",
            enable_math=True,
            math_routing_config={"active_engine": "katex_placeholder"},
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

    def tearDown(self) -> None:
        """Thu hồi và giải phóng không gian bộ nhớ tạm thời sau mỗi ca kiểm thử."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_scenario_7_math_rendering_and_fault_tolerance(self) -> None:
        """Scenario 7: Đúc KaTeX & Phủ kín Inline/Block Math đạt chuẩn cú pháp TeX."""
        math_content = (
            "# Kiểm Thử Toán Học Cơ Bản\n\n"
            "Biểu thức nội dòng: $x=1$\n\n"
            "Biểu thức khối độc lập:\n\n"
            "$$\n"
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\n"
            "$$\n"
        )
        css, rendered_html = self.renderer.convert_to_html(math_content)

        # 1. Kiểm toán việc sinh thẻ ngữ nghĩa cho Inline Math và Block Math
        self.assertIn('<span class="math-tex">', rendered_html)
        self.assertIn('<div class="math-tex">', rendered_html)

        # 2. Kiểm toán đúc tệp PDF thực tế qua Chromium
        output_pdf = self.temp_dir / "temp_math_test.pdf"
        try:
            self.compiler.compile_to_pdf(rendered_html, css, output_pdf)
            self.assertTrue(output_pdf.exists())
            self.assertGreater(output_pdf.stat().st_size, 0)
        finally:
            if output_pdf.exists():
                output_pdf.unlink()

    def test_scenario_15_math_escaping_and_base64_injection(self) -> None:
        """Scenario 15: Kiểm thử Server-Side Python Dictionary Mapping cho Tiếng Việt trong KaTeX."""
        math_md = (
            "# Kiểm Thử Tiếng Việt Trong Toán Học\n\n"
            "Biểu thức toán học: $a = \\text{Cú pháp chuẩn} + \\text{Ngữ nghĩa sâu}$\n"
        )
        _css, rendered_html = self.renderer.convert_to_html(math_md)

        # 1. Kiểm toán việc bóc tách văn bản Tiếng Việt sang kho lưu trữ self.vn_math_store
        self.assertGreater(len(self.renderer.vn_math_store), 0)
        self.assertIn("VILANGMASK0001", self.renderer.vn_math_store)
        self.assertEqual(self.renderer.vn_math_store["VILANGMASK0001"], "Cú pháp chuẩn")
        self.assertIn("VILANGMASK0002", self.renderer.vn_math_store)
        self.assertEqual(self.renderer.vn_math_store["VILANGMASK0002"], "Ngữ nghĩa sâu")

        # 2. Kiểm toán việc nhúng chuỗi giữ chỗ VILANGMASK vào mã HTML
        self.assertIn("VILANGMASK0001", rendered_html)
        self.assertIn("VILANGMASK0002", rendered_html)

        # 3. Kiểm toán việc tiêm kịch bản TreeWalker Client-side Swap
        self.assertIn("var vnMap =", rendered_html)
        self.assertIn("renderMathInElement", rendered_html)

    def test_scenario_17_base64_math_ast_isolation(self) -> None:
        """Scenario 17: Kiểm toán cô lập ký tự nhạy cảm < và > trong biểu thức toán học."""
        dangerous_md = "# Kiểm Thử Ký Tự So Sánh\n\nBiểu thức: $0 < x \\le y > 1$\n"
        _css, rendered_html = self.renderer.convert_to_html(dangerous_md)

        # Kiểm toán các ký tự nhạy cảm HTML được mã hóa thực thể an toàn
        self.assertIn("&lt;", rendered_html)
        self.assertIn("&gt;", rendered_html)
        self.assertIn('<span class="math-tex">', rendered_html)

    def test_scenario_18_vietnamese_math_isolation_structure(self) -> None:
        """Scenario 18: Lớp giáp ASCII VILANGMASK bảo vệ Tiếng Việt trong vĩ lệnh KaTeX."""
        vietnamese_md = (
            "# Kiểm Thử Lớp Giáp VILANGMASK\n\n"
            "Biểu thức: $X = \\text{Thao tác số học phổ quát} \\times \\text{Toán học}$\n"
        )
        isolated = self.renderer._isolate_vietnamese_in_math(vietnamese_md)

        # 1. Kiểm toán hàm _isolate_vietnamese_in_math thay thế thành công mã giữ chỗ ASCII
        self.assertIn("\\text{VILANGMASK0001}", isolated)
        self.assertIn("\\text{VILANGMASK0002}", isolated)

        # 2. Kiểm toán chuyển đổi sang HTML giữ nguyên vẹn cấu trúc và đối soát từ điển
        _css, rendered_html = self.renderer.convert_to_html(vietnamese_md)
        self.assertIn("VILANGMASK0001", rendered_html)
        self.assertIn("VILANGMASK0002", rendered_html)
        self.assertEqual(self.renderer.vn_math_store["VILANGMASK0001"], "Thao tác số học phổ quát")
        self.assertEqual(self.renderer.vn_math_store["VILANGMASK0002"], "Toán học")
        self.assertIn("renderMathInElement", rendered_html)


if __name__ == "__main__":
    unittest.main()
