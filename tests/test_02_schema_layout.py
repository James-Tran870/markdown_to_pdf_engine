# ==============================================================================
# MÔ-ĐUN KIỂM THỬ 02: SCHEMA & LAYOUT VALIDATION (test_02_schema_layout.py)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Pydantic DTO Strict Validation, ExecutionContext & Layout Margin
# ==============================================================================

import shutil
import sys
import time
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pydantic import ValidationError

from main import AppConfig, ExecutionContext, load_configuration
from src.pdf_compiler import PDFCompiler


class SchemaAndLayoutTests(unittest.TestCase):
    """Mô-đun 02: Kiểm thử Lược đồ Pydantic, Giới hạn Bookmark và Lề Trang in động."""

    def setUp(self):
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / "tests" / "temp_redteam_workspace"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

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

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_scenario_3_physical_overflow_destructive_test(self):
        """Scenario 3: Xử lý tràn viền vật lý với chuỗi mã nguồn liên tục cực dài."""
        compiler = PDFCompiler(
            output_encoding="utf-8",
            layout_config={"page_size": "A4", "margin": "20mm"},
        )
        long_code = "X" * 1500
        overflow_content = f"```text\n{long_code}\n```\n"
        output_pdf = self.temp_dir / "temp_overflow_test.pdf"

        try:
            compiler.compile_to_pdf(overflow_content, "", output_pdf)
            self.assertTrue(output_pdf.exists())
            self.assertGreater(output_pdf.stat().st_size, 0)
        finally:
            if output_pdf.exists():
                output_pdf.unlink()

    def test_scenario_11_schema_validation_hard_block_and_latency(self):
        """Scenario 11: Đo kiểm thời gian chặn đứng từ Pydantic khi cấu hình YAML sai định dạng."""
        invalid_content = self.test_config_content.replace("max_bookmark_level: 6", "max_bookmark_level: 10")
        invalid_path = self.config_dir / "invalid_settings.yaml"
        invalid_path.write_text(invalid_content, encoding="utf-8")

        start_time = time.time()
        with self.assertRaises(ValidationError):
            load_configuration(invalid_path)
        latency_ms = (time.time() - start_time) * 1000

        self.assertLess(latency_ms, 500.0, "Thời gian phản hồi Pydantic vượt quá ngưỡng 500ms.")

    def test_scenario_16_layout_injection_and_context_verification(self):
        """Scenario 16: Kiểm chứng ExecutionContext DTO và nạp Layout CSS động."""
        custom_layout = {
            "page_size": "Letter",
            "margin": "123mm",
            "code_overflow_handling": "break-word",
        }
        compiler = PDFCompiler(output_encoding="utf-8", layout_config=custom_layout)
        generated_css = compiler._build_paged_media_css("")

        self.assertIn("size: Letter;", generated_css)
        self.assertIn("margin: 123mm;", generated_css)

        app_config: AppConfig = load_configuration(self.test_config_path)
        app_config.document_layout.margin = "123mm"

        context = ExecutionContext(
            config=app_config,
            input_md_path=self.temp_dir / "sample.md",
            output_pdf_path=self.temp_dir / "sample.pdf",
        )
        self.assertEqual(context.config.document_layout.margin, "123mm")


if __name__ == "__main__":
    unittest.main()
