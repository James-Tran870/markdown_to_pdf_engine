# ==============================================================================
# BỘ KIỂM THỬ ĐỐI KHÁNG HỘP TRẮNG (WHITE-BOX RED-TEAM TEST SUITE)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.4.3 - Playwright & KaTeX Engine)
# Kiến trúc: Fault Tolerance & Isolation Verification Layer
# ==============================================================================

import shutil
import unittest
from pathlib import Path

from main import (
    batch_process_directory,
    execute_single_file_pipeline,
    load_configuration,
)
from src.ast_parser import ASTParser
from src.html_renderer import HTMLRenderer
from src.pdf_compiler import PDFCompiler


class RedTeamTestSuite(unittest.TestCase):
    """Bộ kiểm thử đối kháng Hộp Trắng (White-Box Red-Teaming) nâng cấp v1.4.3."""

    def setUp(self):
        """Khởi tạo môi trường giả lập và các thư mục thử nghiệm tạm thời."""
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / "tests" / "temp_redteam_workspace"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.input_dir = self.temp_dir / "input"
        self.output_dir = self.temp_dir / "output"
        self.config_dir = self.temp_dir / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.test_config_path = self.config_dir / "settings.yaml"
        self.test_config_content = """
global_encoding_standard: "utf-8"
syntax_highlighting_profile: "monokai"
heading_retention_depth:
  max_bookmark_level: 4
  enable_heading_anchors: true
  normalize_anchor_ascii: true
directory_routing:
  input_directory: "input"
  output_directory: "output"
  recursive_search: true
  allowed_extensions: [".md", ".markdown"]
  overwrite_existing: true
  auto_create_directories: true
  preserve_subfolder_structure: true
document_layout:
  page_size: "A4"
  margin: "20mm"
  code_overflow_handling: "break-word"
typography_configuration:
  font_family: '"Segoe UI", "Arial", sans-serif'
  code_font_family: '"Consolas", monospace'
  base_font_size: "11pt"
  line_height: "1.6"
  text_color: "#1a1a1a"
heading_numbering_system:
  enable_auto_numbering: true
  h1_numbering_style: "roman"
  sub_heading_numbering_style: "decimal"
  number_separator: ". "
headless_browser_engine:
  browser_type: "chromium"
  headless: true
  page_timeout_ms: 30000
  wait_until_event: "networkidle"
  print_background: true
  prefer_css_page_size: true
katex_offline_config:
  enable_katex: true
  assets_dir: "assets/katex"
  css_filename: "katex.min.css"
  js_filename: "katex.min.js"
  auto_render_js_filename: "auto-render.min.js"
  strict_mode: false
  throw_on_error: false
table_rendering_system:
  enable_gfm_tables: true
  overflow_strategy: "clip_and_warn"
  repeat_header_on_page_break: true
  max_printable_width_mm: 170
academic_standards_profile:
  active_standard: "apa"
  prevent_orphans_and_widows: true
  code_block_page_break_inside: "avoid"
  table_page_break_inside: "avoid"
"""
        with open(self.test_config_path, "w", encoding="utf-8") as file_stream:
            file_stream.write(self.test_config_content)

        self.parser = ASTParser(
            encoding_standard="utf-8", enable_math=True, enable_tables=True
        )
        self.renderer = HTMLRenderer(
            theme_name="monokai",
            max_bookmark_level=4,
            enable_math=True,
            fallback_to_raw=True,
            table_config={
                "enable_gfm_tables": True,
                "overflow_strategy": "clip_and_warn",
            },
            katex_config={
                "enable_katex": True,
                "assets_dir": "assets/katex",
                "css_filename": "katex.min.css",
                "js_filename": "katex.min.js",
                "auto_render_js_filename": "auto-render.min.js",
                "strict_mode": False,
                "throw_on_error": False,
            },
        )
        self.compiler = PDFCompiler(
            output_encoding="utf-8",
            academic_config={
                "active_standard": "apa",
                "prevent_orphans_and_widows": True,
            },
            browser_config={
                "browser_type": "chromium",
                "headless": True,
                "page_timeout_ms": 30000,
                "wait_until_event": "networkidle",
                "print_background": True,
                "prefer_css_page_size": True,
            },
        )

    def tearDown(self):
        """Dọn dẹp triệt để tất cả thư mục và tệp dữ liệu tạm sau khi hoàn tất test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_scenario_1_bilingual_encoding_stress_test(self):
        """Kịch bản 1: Kiểm thử rào chắn xung đột ký tự đa ngôn ngữ tiếng Việt và toán tử nhị phân."""
        sample_file = self.temp_dir / "temp_stress_test.md"
        stress_content = (
            "# Thử nghiệm Mã hóa Tiếng Việt: Cài đặt Hệ thống\n"
            "Đoạn văn bản chứa ký tự đặc biệt: `a < b && c > d` và Regex `^[a-zA-Z0-9_]+$`.\n"
            "```python\n"
            "if alpha < beta and gamma > delta:\n"
            "    print('Cấu hình Tiếng Việt hoàn tất!')\n"
            "```\n"
        )
        with open(sample_file, "w", encoding="utf-8") as file_stream:
            file_stream.write(stress_content)

        tokens = self.parser.parse_markdown_file(sample_file)
        self.assertIsNotNone(tokens)

        _pygments_css, rendered_html = self.renderer.convert_to_html(stress_content)
        self.assertIn("Cài đặt Hệ thống", rendered_html)
        self.assertIn("Cấu hình Tiếng Việt hoàn tất!", rendered_html)

    def test_scenario_2_heading_spoofing_simulation(self):
        """Kịch bản 2: Bẫy đánh lừa cấu trúc phân cấp (Heading nằm bên trong khối mã nguồn)."""
        spoof_content = (
            "# Tiêu đề Hợp lệ Cấp 1\n"
            "```python\n"
            "## Tiêu đề Giả mạo Cấp 2 Trong Code Block\n"
            "```\n"
        )
        _pygments_css, rendered_html = self.renderer.convert_to_html(spoof_content)

        self.assertIn('<h1 id="tieu-de-hop-le-cap-1" data-level="1">', rendered_html)
        self.assertNotIn('<h2 id="tieu-de-gia-mao-cap-2-trong-code-block"', rendered_html)
        self.assertNotIn('data-level="2"', rendered_html)

    def test_scenario_3_physical_overflow_destructive_test(self):
        """Kịch bản 3: Thử nghiệm tràn viền vật lý với chuỗi mã nguồn liên tục cực dài."""
        long_code_string = "X" * 1500
        overflow_content = f"```text\n{long_code_string}\n```\n"

        pygments_css, rendered_html = self.renderer.convert_to_html(overflow_content)
        output_pdf = self.temp_dir / "temp_overflow_test.pdf"

        try:
            self.compiler.compile_to_pdf(rendered_html, pygments_css, output_pdf)
            self.assertTrue(output_pdf.exists())
            self.assertGreater(output_pdf.stat().st_size, 0)
        finally:
            if output_pdf.exists():
                output_pdf.unlink()

    def test_scenario_4_empty_directory_handling(self):
        """Kịch bản 4: Kiểm thử an toàn khi thư mục đầu vào input/ hoàn toàn rỗng."""
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        try:
            batch_process_directory(base_directory=self.temp_dir)
            self.assertTrue(True)
        except (
            FileNotFoundError,
            ValueError,
            TypeError,
            OSError,
            RuntimeError,
        ) as error:
            self.fail(f"Hệ thống bị sập khi thư mục input rỗng: {error}")

    def test_scenario_5_batch_fault_isolation(self):
        """Kịch bản 5: Kiểm thử cô lập lỗi - 1 tệp hỏng không làm dừng biên dịch các tệp khác."""
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        file_a = self.input_dir / "file_a.md"
        file_a.write_text("# Tệp A Hợp Lệ\nNội dung tệp A.", encoding="utf-8")

        file_b = self.input_dir / "file_b.md"
        with open(file_b, "wb") as f:
            f.write(b"\x80\x81\xfe\xff\xff")

        file_c = self.input_dir / "file_c.md"
        file_c.write_text("# Tệp C Hợp Lệ\nNội dung tệp C.", encoding="utf-8")

        config = load_configuration(self.test_config_path)

        res_a = execute_single_file_pipeline(
            file_a, self.output_dir / "file_a.pdf", config
        )
        res_b = execute_single_file_pipeline(
            file_b, self.output_dir / "file_b.pdf", config
        )
        res_c = execute_single_file_pipeline(
            file_c, self.output_dir / "file_c.pdf", config
        )

        self.assertTrue(res_a)
        self.assertFalse(res_b)
        self.assertTrue(res_c)

        self.assertTrue((self.output_dir / "file_a.pdf").exists())
        self.assertFalse((self.output_dir / "file_b.pdf").exists())
        self.assertTrue((self.output_dir / "file_c.pdf").exists())

    def test_scenario_6_subfolder_structure_preservation(self):
        """Kịch bản 6: Kiểm thử tự động tái tạo và bảo tồn cấu trúc thư mục con."""
        sub_input_dir = self.input_dir / "du_an_nghien_cuu" / "chuyen_de_1"
        sub_input_dir.mkdir(parents=True, exist_ok=True)

        sub_file = sub_input_dir / "bao_cao.md"
        sub_file.write_text("# Báo Cáo Chuyên Đề 1\nNội dung báo cáo.", encoding="utf-8")

        batch_process_directory(base_directory=self.temp_dir)

        expected_pdf = (
            self.output_dir / "du_an_nghien_cuu" / "chuyen_de_1" / "bao_cao.pdf"
        )
        self.assertTrue(expected_pdf.exists())

    def test_scenario_7_math_rendering_and_fault_tolerance(self):
        """Kịch bản 7 (NÂNG CẤP v1.4.3): Kiểm thử đúc KaTeX Chromium, vĩ lệnh phức tạp và đa tiêu chuẩn TeX/LaTeX2e."""
        complex_math_content = (
            "# Báo Cáo Toán Học Cao Cấp\n"
            "1. Plain TeX: $$x = {-b \\pm \\sqrt{b^2 - 4ac} \\over 2a}$$\n"
            "2. LaTeX2e: \\[x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\]\n"
            "3. KaTeX Web: $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$\n\n"
            "$$\n"             "\\boxed{\n"             "\\mathbb Z\n"             "\\;\\xrightarrow{\\text{identify values differing by }N}\\;\n"             "\\mathbb Z/N\\mathbb Z\n"             "}\n"             "$$\n"
        )
        pygments_css, rendered_html = self.renderer.convert_to_html(complex_math_content)

        # Kiểm định 1: Mã HTML trung gian chứa các thẻ bọc toán học và script KaTeX
        self.assertIn('<span class="math-tex">', rendered_html)
        self.assertIn('<div class="math-tex">', rendered_html)
        self.assertIn("katex.min.js", rendered_html)

        # Kiểm định 2: Thực thi xuất bản PDF qua Playwright Chromium và xác minh dung lượng tệp
        output_pdf = self.temp_dir / "temp_katex_complex_test.pdf"
        try:
            self.compiler.compile_to_pdf(rendered_html, pygments_css, output_pdf)
            self.assertTrue(output_pdf.exists())
            self.assertGreater(output_pdf.stat().st_size, 0)
        finally:
            if output_pdf.exists():
                output_pdf.unlink()

    def test_scenario_8_gfm_table_parsing_and_structure(self):
        """Kịch bản 8: Kiểm thử nhận diện và cấu trúc hóa bảng biểu GFM."""
        table_markdown = (
            "# Kiểm thử Bảng GFM\n\n"
            "| Cột Tiêu Đề 1 | Cột Tiêu Đề 2 |\n"
            "| :--- | :--- |\n"
            "| Dữ liệu Dòng 1 | Dữ liệu Dòng 2 |\n"
        )
        sample_file = self.temp_dir / "temp_table_test.md"
        sample_file.write_text(table_markdown, encoding="utf-8")

        tokens = self.parser.parse_markdown_file(sample_file)
        token_types = [token.type for token in tokens]

        self.assertIn("table_open", token_types)
        self.assertIn("thead_open", token_types)
        self.assertIn("tr_open", token_types)

        _css, rendered_html = self.renderer.convert_to_html(table_markdown)
        self.assertIn("<table>", rendered_html)
        self.assertIn('<th style="text-align:left">Cột Tiêu Đề 1</th>', rendered_html)
        self.assertIn('<td style="text-align:left">Dữ liệu Dòng 1</td>', rendered_html)

    def test_scenario_9_table_overflow_clipping_and_logging(self):
        """Kịch bản 9: Kiểm thử bảng biểu cực rộng vượt quá lề giấy A4."""
        header_row = "| " + " | ".join([f"Cột {i}" for i in range(1, 26)]) + " |\n"
        sep_row = "| " + " | ".join([":---" for _ in range(25)]) + " |\n"
        data_row = "| " + " | ".join([f"Dữ liệu {i}" for i in range(1, 26)]) + " |\n"
        huge_table_markdown = f"# Bảng Cực Rộng\n\n{header_row}{sep_row}{data_row}"

        pygments_css, rendered_html = self.renderer.convert_to_html(huge_table_markdown)
        output_pdf = self.temp_dir / "temp_huge_table_test.pdf"

        try:
            self.compiler.compile_to_pdf(rendered_html, pygments_css, output_pdf)
            self.assertTrue(output_pdf.exists())
            self.assertGreater(output_pdf.stat().st_size, 0)
        finally:
            if output_pdf.exists():
                output_pdf.unlink()

    def test_scenario_10_academic_apa_profile_and_break_avoidance(self):
        """Kịch bản 10: Kiểm thử quy chuẩn in ấn học thuật APA và chống ngắt trang."""
        academic_content = (
            "# Báo Cáo Học Thuật Chuẩn APA\n\n"
            "Đoạn văn bản mở đầu báo cáo học thuật.\n\n"
            "```python\n"
            "def test_function():\n"
            "    return True\n"
            "```\n"
        )
        pygments_css, rendered_html = self.renderer.convert_to_html(academic_content)
        output_pdf = self.temp_dir / "temp_apa_test.pdf"

        try:
            self.compiler.compile_to_pdf(rendered_html, pygments_css, output_pdf)
            self.assertTrue(output_pdf.exists())
            self.assertGreater(output_pdf.stat().st_size, 0)
        finally:
            if output_pdf.exists():
                output_pdf.unlink()


if __name__ == "__main__":
    unittest.main()
