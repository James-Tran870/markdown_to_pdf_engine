# ==============================================================================
# MÔ-ĐUN KIỂM THỬ 04: DOCUMENT FEATURES & BOOKMARKS (test_04_document_features.py)
# Dự án: markdown_to_pdf_engine (Phiên bản v2.4.0 - Typography & GFM Alerts)
# Kiến trúc: GFM Tables, APA Standards, PyMuPDF Bookmarks & GFM Alerts Mesh
# ==============================================================================

import shutil
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pymupdf as fitz

from src.ast_parser import ASTParser
from src.html_renderer import HTMLRenderer
from src.pdf_compiler import PDFCompiler
from src.pdf_metadata_injector import MetadataInjector


class DocumentFeaturesTests(unittest.TestCase):
    """Mô-đun 04: Kiểm thử Bảng GFM, Tiêu đề mồ côi, Bookmarks PyMuPDF và GFM Alerts."""

    def setUp(self) -> None:
        """Khởi tạo môi trường kiểm thử và các thực thể động cơ lõi."""
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / "tests" / "temp_redteam_workspace"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.parser = ASTParser(encoding_standard="utf-8", enable_math=True, enable_tables=True)
        self.renderer = HTMLRenderer(
            theme_name="monokai",
            max_bookmark_level=6,
            enable_heading_anchors=True,
            normalize_anchor_ascii=True,
            enable_math=True,
            table_config={"enable_gfm_tables": True, "overflow_strategy": "clip_and_warn"},
        )
        self.compiler = PDFCompiler(
            output_encoding="utf-8",
            layout_config={"page_size": "A4", "margin": "20mm", "code_overflow_handling": "break-word"},
            academic_config={"active_standard": "apa", "prevent_orphans_and_widows": True},
        )

    def tearDown(self) -> None:
        """Thu hồi và giải phóng không gian bộ nhớ tạm thời sau mỗi ca kiểm thử."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_scenario_2_heading_spoofing_simulation(self) -> None:
        """Scenario 2: Bẫy tiêu đề giả mạo trong Code Block."""
        spoof_content = "# Tiêu đề Cấp 1\n```python\n## Tiêu đề Giả mạo\n```\n"
        _css, rendered_html = self.renderer.convert_to_html(spoof_content)

        self.assertIn('<h1 id="tieu-de-cap-1" data-level="1">', rendered_html)
        self.assertNotIn('<h2 id="tieu-de-gia-mao"', rendered_html)

    def test_scenario_8_gfm_table_parsing_and_structure(self) -> None:
        """Scenario 8: Bóc tách và tạo khung lưới cho Bảng GFM."""
        table_md = "| Cột 1 | Cột 2 |\n| :--- | :--- |\n| Dữ liệu 1 | Dữ liệu 2 |\n"
        sample_file = self.temp_dir / "table.md"
        sample_file.write_text(table_md, encoding="utf-8")

        tokens = self.parser.parse_markdown_file(sample_file)
        token_types = [t.type for t in tokens]
        self.assertIn("table_open", token_types)

        _css, rendered_html = self.renderer.convert_to_html(table_md)
        self.assertIn("<table>", rendered_html)

    def test_scenario_10_academic_apa_profile_and_break_avoidance(self) -> None:
        """Scenario 10: Quy chuẩn in ấn APA và chống ngắt trang."""
        academic_content = "# Báo Cáo APA\n\n```python\ndef test(): pass\n```\n"
        pygments_css, rendered_html = self.renderer.convert_to_html(academic_content)
        output_pdf = self.temp_dir / "apa_test.pdf"

        try:
            self.compiler.compile_to_pdf(rendered_html, pygments_css, output_pdf)
            self.assertTrue(output_pdf.exists())
        finally:
            if output_pdf.exists():
                output_pdf.unlink()

    def test_scenario_13_post_processing_metadata_outline_verification(self) -> None:
        """Scenario 13: Tiêm Cây Mục lục Bookmarks đến Cấp 6 qua PyMuPDF."""
        sample_md = (
            "# Cấp 1\nText 1\n"
            "## Cấp 2\nText 2\n"
            "### Cấp 3\nText 3\n"
            "#### Cấp 4\nText 4\n"
            "##### Cấp 5\nText 5\n"
            "###### Cấp 6\nText 6\n"
        )
        pygments_css, rendered_html = self.renderer.convert_to_html(sample_md)
        output_pdf = self.temp_dir / "metadata_level6.pdf"

        self.compiler.compile_to_pdf(rendered_html, pygments_css, output_pdf)

        injector = MetadataInjector(max_bookmark_level=6)
        is_injected = injector.inject_metadata(output_pdf, rendered_html)
        self.assertTrue(is_injected)

        doc = fitz.open(output_pdf)
        toc = doc.get_toc()
        doc.close()

        self.assertGreaterEqual(len(toc), 6)
        self.assertEqual(toc[5][0], 6)

    def test_scenario_14_orphaned_heading_tree_injection(self) -> None:
        """Scenario 14: Tiêm Cây Tiêu đề mồ côi khuyết cấp."""
        orphaned_md = "### Tiêu đề Cấp 3 Mồ Côi\nText\n##### Tiêu đề Cấp 5 Nhảy Cấp\nText\n"
        pygments_css, rendered_html = self.renderer.convert_to_html(orphaned_md)

        injector = MetadataInjector(max_bookmark_level=6)
        output_pdf = self.temp_dir / "orphaned_heading.pdf"
        try:
            self.compiler.compile_to_pdf(rendered_html, pygments_css, output_pdf)
            is_injected = injector.inject_metadata(output_pdf, rendered_html)
            self.assertTrue(is_injected)

            doc = fitz.open(output_pdf)
            toc = doc.get_toc()
            doc.close()

            self.assertEqual(len(toc), 2)
            self.assertEqual(toc[0][0], 1)
        finally:
            if output_pdf.exists():
                output_pdf.unlink()

    def test_scenario_15_gfm_alerts_semantic_parsing_and_isolation(self) -> None:
        """Scenario 15: Kiểm toán bóc tách cú pháp GFM Alerts và chống rò rỉ tiền tố (v2.4.0)."""
        alerts_md = """
> [!Note] MỤC TIÊU & CÂU HỎI KHAI PHÓNG
>
> Thí nghiệm chữ sau ký tự Dấu trích dẫn khối

> [!WARNING]
> Cảnh báo rủi ro về mặt kiến trúc hệ thống.

> [!TIP]
> Sử dụng phím tắt và auto-formatting để tăng tốc độ soạn thảo Markdown.

> [!IMPORTANT]
> Đây là thông điệp tối quan trọng cần lưu ý.

> [!CAUTION]
> Dữ liệu nhạy cảm cần được bảo vệ cẩn mật.

> Đây là đoạn trích dẫn tiêu chuẩn thông thường không phải Alert.
"""
        _css, rendered_html = self.renderer.convert_to_html(alerts_md)

        # 1. Kiểm toán việc sinh đúng thẻ ngữ nghĩa div.markdown-alert
        self.assertIn('<div class="markdown-alert markdown-alert-note">', rendered_html)
        self.assertIn('<div class="markdown-alert markdown-alert-warning">', rendered_html)
        self.assertIn('<div class="markdown-alert markdown-alert-tip">', rendered_html)
        self.assertIn('<div class="markdown-alert markdown-alert-important">', rendered_html)
        self.assertIn('<div class="markdown-alert markdown-alert-caution">', rendered_html)

        # 2. Kiểm toán việc triệt tiêu hoàn toàn tiền tố [!TYPE] khỏi văn bản con
        self.assertNotIn("[!Note]", rendered_html)
        self.assertNotIn("[!WARNING]", rendered_html)
        self.assertNotIn("[!TIP]", rendered_html)
        self.assertNotIn("[!IMPORTANT]", rendered_html)
        self.assertNotIn("[!CAUTION]", rendered_html)

        # 3. Kiểm toán việc giữ nguyên trạng thẻ blockquote đối với trích dẫn thông thường
        self.assertIn("<blockquote>", rendered_html)
        self.assertIn("<p>Đây là đoạn trích dẫn tiêu chuẩn thông thường không phải Alert.</p>", rendered_html)

    def test_scenario_16_inline_code_backtick_and_css_rules_verification(self) -> None:
        """Scenario 16: Kiểm toán kết xuất chữ trong dấu Backtick và Ma trận CSS Paged Media (v2.4.0)."""
        mixed_md = """
### `Thí nghiệm chữ trong dấu nháy ngược (Backtick)`

`Thí nghiệm chữ trong dấu nháy ngược (Backtick)`

---

### Thí nghiệm chữ sau ký tự Dấu trích dẫn khối `>`

> [!WARNING]
> Cảnh báo rủi ro với tệp `config.local.yaml` và tham số `active_engine`.
"""
        pygments_css, rendered_html = self.renderer.convert_to_html(mixed_md)

        # 1. Kiểm toán sinh mã HTML cho Inline Code
        self.assertIn("<code>Thí nghiệm chữ trong dấu nháy ngược (Backtick)</code>", rendered_html)
        self.assertIn("<code>&gt;</code>", rendered_html)
        self.assertIn("<code>config.local.yaml</code>", rendered_html)

        # 2. Kiểm toán Ma trận CSS Paged Media được sinh từ PDFCompiler
        paged_media_css = self.compiler._build_paged_media_css(pygments_css)

        self.assertIn(":not(pre) > code", paged_media_css)
        self.assertIn("rgba(175, 184, 193, 0.2)", paged_media_css)
        self.assertIn("blockquote {", paged_media_css)
        self.assertIn(".markdown-alert {", paged_media_css)
        self.assertIn(".markdown-alert-note", paged_media_css)
        self.assertIn(".markdown-alert-warning", paged_media_css)
        self.assertIn("break-inside: avoid;", paged_media_css)


if __name__ == "__main__":
    unittest.main()
