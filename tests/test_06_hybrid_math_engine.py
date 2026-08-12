# ==============================================================================
# TỆP: tests/test_06_hybrid_math_engine.py (BỘ KIỂM THỬ ĐỘNG CƠ LAI v2.3.0)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Zero-Config Sys.path Injection, Pytest/Unittest & Hybrid Engine
# ==============================================================================

import sys
import tempfile
import unittest
from pathlib import Path

# ------------------------------------------------------------------------------
# TỰ ĐỘNG TIÊM THƯ MỤC GỐC DỰ ÁN VÀO SYS.PATH ĐỂ TRIỆT TIÊU LỖI ModuleNotFoundError
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent.resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pydantic import ValidationError

from main import AppConfig, load_configuration
from src.html_renderer import HTMLRenderer
from src.pdf_compiler import PDFCompiler


class TestHybridMathEngineArchitecture(unittest.TestCase):
    """Bộ kiểm thử hộp trắng chuyên biệt cho Kiến trúc Lai KaTeX & MathJax v3 (v2.3.0)."""

    def setUp(self) -> None:
        """Khởi tạo môi trường bộ đệm và tham số mẫu trước mỗi ca kiểm thử."""
        self.sample_vietnamese_math_md = (
            "# Kiểm thử Động cơ Toán học\n\n"
            "Công thức có chứa Tiếng Việt nội dòng: $a = \\text{Thao tác số học} + 10$\n\n"
            "Công thức khối độc lập:\n"
            "$$\n"
            "\\text{Optimization không bắt đầu từ CPU instruction.}\n"
            "$$"
        )
        self.config_path = BASE_DIR / "config" / "settings.yaml"

    def test_01_pydantic_routing_validation_success_and_failure(self) -> None:
        """Xác thực DTO Pydantic v2 chấp nhận cờ hợp lệ và ngắt mạch khi cờ sai."""
        # 1. Kiểm thử giá trị hợp lệ
        valid_config_data = {
            "math_engine_routing": {"active_engine": "katex_placeholder"}
        }
        app_config = AppConfig.model_validate(valid_config_data)
        self.assertEqual(app_config.math_engine_routing.active_engine, "katex_placeholder")

        valid_config_data_2 = {
            "math_engine_routing": {"active_engine": "MATHJAX_SVG "}
        }
        app_config_2 = AppConfig.model_validate(valid_config_data_2)
        self.assertEqual(app_config_2.math_engine_routing.active_engine, "mathjax_svg")

        # 2. Kiểm thử giá trị không hợp lệ -> Phải ném ngoại lệ ValidationError
        invalid_config_data = {
            "math_engine_routing": {"active_engine": "unknown_invalid_engine"}
        }
        with self.assertRaises(ValidationError):
            AppConfig.model_validate(invalid_config_data)

    def test_02_load_configuration_from_yaml_file(self) -> None:
        """Xác thực hàm load_configuration đọc đúng cấu hình DTO từ settings.yaml thực tế."""
        if self.config_path.exists():
            app_config = load_configuration(self.config_path)
            self.assertIsInstance(app_config, AppConfig)
            self.assertIn(
                app_config.math_engine_routing.active_engine,
                {"katex_placeholder", "mathjax_svg"},
            )

    def test_03_python_dictionary_mapping_katex_execution(self) -> None:
        """Xác thực thuật toán Server-side Python Dictionary Mapping cho nhánh KaTeX."""
        renderer = HTMLRenderer(
            math_routing_config={"active_engine": "katex_placeholder"},
            enable_math=True,
        )
        _pygments_css, rendered_html = renderer.convert_to_html(self.sample_vietnamese_math_md)

        # 1. Kiểm tra từ điển Python đã bóc tách được văn bản Tiếng Việt
        self.assertGreater(len(renderer.vn_math_store), 0)
        self.assertIn("VILANGMASK0001", renderer.vn_math_store)
        self.assertEqual(renderer.vn_math_store["VILANGMASK0001"], "Thao tác số học")

        # 2. Kiểm tra chuỗi HTML đã thế mã ASCII VILANGMASK
        self.assertIn("VILANGMASK0001", rendered_html)

        # 3. Kiểm tra kịch bản Swap Script Client-side được tiêm vào HTML
        self.assertIn("var vnMap =", rendered_html)
        self.assertIn("renderMathInElement", rendered_html)
        self.assertIn("createTreeWalker", rendered_html)

    def test_04_mathjax_svg_environment_generation(self) -> None:
        """Xác thực khả năng tiêm Môi trường Đồ họa Vector SVG cho nhánh MathJax v3."""
        renderer = HTMLRenderer(
            math_routing_config={"active_engine": "mathjax_svg"},
            mathjax_config={
                "enable_mathjax": True,
                "assets_dir": "assets/mathjax",
                "js_filename": "tex-svg.js",
                "font_cache": "global",
            },
            enable_math=True,
        )
        _pygments_css, rendered_html = renderer.convert_to_html(self.sample_vietnamese_math_md)

        # 1. Kiểm tra cấu hình window.MathJax được tiêm vào HTML
        self.assertIn("window.MathJax =", rendered_html)
        self.assertIn("fontCache: 'global'", rendered_html)

        # 2. Kiểm tra thẻ nạp script MathJax
        self.assertIn("tex-svg.js", rendered_html)

    def test_05_pdf_compiler_paged_media_svg_boundaries(self) -> None:
        """Xác thực bộ CSS Paged Media chứa rào chắn bảo vệ đồ họa SVG MathJax v3."""
        compiler = PDFCompiler()
        paged_css = compiler._build_paged_media_css(pygments_css="")

        # Kiểm tra sự tồn tại của các rào chắn CSS SVG
        self.assertIn("mjx-container", paged_css)
        self.assertIn("mjx-container[jax=\"SVG\"] svg", paged_css)
        self.assertIn("max-width: 100% !important;", paged_css)
        self.assertIn("overflow-x: auto !important;", paged_css)

    def test_06_end_to_end_pdf_compilation_with_hybrid_engine(self) -> None:
        """Thử nghiệm đúc PDF thực tế qua Playwright Chromium sử dụng thuật toán mới."""
        renderer = HTMLRenderer(
            math_routing_config={"active_engine": "katex_placeholder"},
            enable_math=True,
        )
        _pygments_css, rendered_html = renderer.convert_to_html(self.sample_vietnamese_math_md)

        compiler = PDFCompiler()
        with tempfile.TemporaryDirectory() as temp_dir:
            output_pdf_path = Path(temp_dir) / "test_hybrid_output.pdf"
            compiler.compile_to_pdf(
                html_content=rendered_html,
                pygments_css=_pygments_css,
                output_path=output_pdf_path,
            )

            # Kiểm tra tệp PDF được đúc ra thành công có dung lượng > 0 bytes
            self.assertTrue(output_pdf_path.exists())
            self.assertGreater(output_pdf_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
