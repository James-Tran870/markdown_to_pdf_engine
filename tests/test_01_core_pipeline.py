# ==============================================================================
# MÔ-ĐUN KIỂM THỬ 01: CORE PIPELINE & I/O ISOLATION (test_01_core_pipeline.py v2.0.4)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Explicit Exception Handling & Zero-Warning Standard (Ruff BLE001 Compliant)
# ==============================================================================

import shutil
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pydantic import ValidationError

from main import (
    batch_process_directory,
    execute_single_file_pipeline,
    load_configuration,
)
from src.ast_parser import ASTParser
from src.html_renderer import HTMLRenderer


class CorePipelineTests(unittest.TestCase):
    """Mô-đun 01: Kiểm thử Luồng I/O Lõi, Quét đệ quy & Cô lập tệp hỏng."""

    def setUp(self):
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
  max_bookmark_level: 6
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
  enable_base64_math_encoding: true
  enable_vietnamese_math_isolation: true
  vietnamese_font_family: '"Times New Roman", "Segoe UI", Arial, sans-serif'
  enable_base64_font_embedding: true
  hybrid_typography_fallback: '"Cambria Math", "Times New Roman", serif'
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
        with open(self.test_config_path, "w", encoding="utf-8") as f:
            f.write(self.test_config_content)

        self.parser = ASTParser(encoding_standard="utf-8", enable_math=True, enable_tables=True)
        self.renderer = HTMLRenderer(
            theme_name="monokai",
            max_bookmark_level=6,
            enable_heading_anchors=True,
            normalize_anchor_ascii=True,
            enable_math=True,
            fallback_to_raw=True,
        )

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_scenario_1_bilingual_encoding_stress_test(self):
        """Scenario 1: Stress test mã hóa song ngữ Tiếng Việt."""
        sample_file = self.temp_dir / "temp_stress_test.md"
        stress_content = (
            "# Thử nghiệm Mã hóa Tiếng Việt: Cài đặt Hệ thống\n"
            "Đoạn văn bản chứa ký tự đặc biệt: `a < b && c > d` và Regex `^[a-zA-Z0-9_]+$`.\n"
            "```python\n"
            "if alpha < beta and gamma > delta:\n"
            "    print('Cấu hình Tiếng Việt hoàn tất!')\n"
            "```\n"
        )
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(stress_content)

        tokens = self.parser.parse_markdown_file(sample_file)
        self.assertIsNotNone(tokens)
        _css, rendered_html = self.renderer.convert_to_html(stress_content)
        self.assertIn("Cài đặt Hệ thống", rendered_html)

    def test_scenario_4_empty_directory_handling(self):
        """Scenario 4 [FIXED BLE001]: Xử lý thư mục input rỗng an toàn với danh sách ngoại lệ minh bạch."""
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
            ValidationError,
        ) as error:
            self.fail(f"Bị sập khi thư mục input rỗng do ngoại lệ: {error}")

    def test_scenario_5_batch_fault_isolation(self):
        """Scenario 5: Cô lập tệp hỏng nhị phân."""
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        file_a = self.input_dir / "file_a.md"
        file_a.write_text("# Tệp A Hợp Lệ\nNội dung A.", encoding="utf-8")

        file_b = self.input_dir / "file_b.md"
        with open(file_b, "wb") as f:
            f.write(b"\x80\x81\xfe\xff\xff")

        file_c = self.input_dir / "file_c.md"
        file_c.write_text("# Tệp C Hợp Lệ\nNội dung C.", encoding="utf-8")

        config = load_configuration(self.test_config_path)

        res_a = execute_single_file_pipeline(file_a, self.output_dir / "file_a.pdf", config)
        res_b = execute_single_file_pipeline(file_b, self.output_dir / "file_b.pdf", config)
        res_c = execute_single_file_pipeline(file_c, self.output_dir / "file_c.pdf", config)

        self.assertTrue(res_a)
        self.assertFalse(res_b)
        self.assertTrue(res_c)

    def test_scenario_6_subfolder_structure_preservation(self):
        """Scenario 6: Tái tạo cấu trúc thư mục con."""
        sub_input_dir = self.input_dir / "du_an" / "chuyen_de_1"
        sub_input_dir.mkdir(parents=True, exist_ok=True)

        sub_file = sub_input_dir / "bao_cao.md"
        sub_file.write_text("# Báo Cáo\nNội dung.", encoding="utf-8")

        batch_process_directory(base_directory=self.temp_dir)

        expected_pdf = self.output_dir / "du_an" / "chuyen_de_1" / "bao_cao.pdf"
        self.assertTrue(expected_pdf.exists())


if __name__ == "__main__":
    unittest.main()
