# ==============================================================================
# BỘ KIỂM THỬ ĐỐI KHÁNG HỘP TRẮNG (WHITE-BOX RED-TEAM TEST SUITE)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.2.0 - Tích hợp MathML)
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
    """Bộ kiểm thử đối kháng Hộp Trắng (White-Box Red-Teaming) nâng cấp v1.2.0."""

    def setUp(self):
        """Khởi tạo môi trường giả lập và các thư mục thử nghiệm tạm thời."""
        self.base_dir = Path(__file__).parent
        self.temp_dir = self.base_dir / "temp_redteam_workspace"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.input_dir = self.temp_dir / "input"
        self.output_dir = self.temp_dir / "output"
        self.config_dir = self.temp_dir / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Khởi tạo tệp cấu hình tạm thời cho bộ test (Tích hợp Math Rendering System v1.2.0)
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
  code_overflow_handling: "break-all"
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
math_rendering_system:
  enable_math_rendering: true
  fallback_to_raw_on_error: true
"""
        with open(self.test_config_path, "w", encoding="utf-8") as file_stream:
            file_stream.write(self.test_config_content)

        self.parser = ASTParser(encoding_standard="utf-8", enable_math=True)
        self.renderer = HTMLRenderer(
            theme_name="monokai",
            max_bookmark_level=4,
            enable_math=True,
            fallback_to_raw=True,
        )
        self.compiler = PDFCompiler(output_encoding="utf-8")

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

        # Kiểm tra tiêu đề hợp lệ được gắn thẻ h1 kèm thuộc tính id mỏ neo ASCII
        self.assertIn('<h1 id="tieu-de-hop-le-cap-1" data-level="1">', rendered_html)

        # Kiểm tra tiêu đề giả mạo bên trong Code Block KHÔNG tạo thẻ h2 hay mỏ neo Bookmarks
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

        # Tệp B hỏng (Ghi dữ liệu nhị phân không hợp lệ để gây lỗi mã hóa UTF-8)
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
        """Kịch bản 7 (MỚI v1.2.0): Kiểm thử biên dịch MathML và cơ chế hạ cấp lỗi LaTeX."""
        # 1. Thử nghiệm công thức toán chuẩn
        valid_math_content = (
            "# Báo Cáo Toán Học\n"
            "Công thức nội dòng $2^{30}$ và công thức khối:\n\n"
            "$$\\frac{a}{b}$$\n"
        )
        _css, rendered_html = self.renderer.convert_to_html(valid_math_content)

        # Kiểm tra mã HTML có chứa các thẻ đánh dấu MathML chuẩn
        self.assertIn('<span class="math-inline">', rendered_html)
        self.assertIn('<div class="math-block">', rendered_html)
        self.assertIn("<math", rendered_html)

        # 2. Thử nghiệm hạ cấp an toàn khi công thức LaTeX bị lỗi cú pháp
        invalid_math_content = "Công thức lỗi: $\\invalidlatex_command{{{$"
        _css_err, rendered_err_html = self.renderer.convert_to_html(invalid_math_content)

        # Kiểm tra hệ thống tự hạ cấp về thẻ math-error mà không làm sập tiến trình
        self.assertIn('<span class="math-error">', rendered_err_html)


if __name__ == "__main__":
    unittest.main()

# ==============================================================================
# CÂY LỆNH THỰC THI KIỂM THỬ TRÊN TERMINAL VSCODE:
# python -m unittest tests/red_team_tests.py
# ==============================================================================