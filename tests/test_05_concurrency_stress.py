# ==============================================================================
# MÔ-ĐUN KIỂM THỬ 05: MULTIPROCESSING STRESS TEST (test_05_concurrency_stress.py)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: ProcessPoolExecutor Isolation & Chromium Event Loop Concurrency
# ==============================================================================

import shutil
import sys
import unittest
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.html_renderer import HTMLRenderer
from src.pdf_compiler import PDFCompiler


def _worker_compile_process_task(args: tuple[str, str, Path, dict, dict, dict]) -> bool:
    """Hàm thực thi độc lập cấp mô-đun dành riêng cho ProcessPoolExecutor."""
    html_content, pygments_css, output_pdf_path, layout_config, academic_config, browser_config = args
    try:
        compiler = PDFCompiler(
            output_encoding="utf-8",
            layout_config=layout_config,
            academic_config=academic_config,
            browser_config=browser_config,
        )
        compiler.compile_to_pdf(html_content, pygments_css, output_pdf_path)
        return output_pdf_path.exists()
    except (OSError, RuntimeError) as e:
        print(f"Lỗi tiến trình tại {output_pdf_path.name}: {e}")
        return False


class ConcurrencyStressTests(unittest.TestCase):
    """Mô-đun 05: Giả lập đa tiến trình cách ly bộ nhớ vật lý."""

    def setUp(self):
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / "tests" / "temp_redteam_workspace"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.renderer = HTMLRenderer(theme_name="monokai", enable_math=True)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_scenario_12_ephemeral_memory_concurrency_stress(self):
        """Scenario 12: Đa tiến trình cách ly bộ nhớ vật lý."""
        markdown_content = "# Báo cáo Đa tiến trình\nNội dung kiểm thử chống va chạm."
        pygments_css, rendered_html = self.renderer.convert_to_html(markdown_content)

        layout_config = {"page_size": "A4", "margin": "20mm", "code_overflow_handling": "break-word"}
        academic_config = {"active_standard": "apa", "prevent_orphans_and_widows": True}
        browser_config = {
            "browser_type": "chromium",
            "headless": True,
            "page_timeout_ms": 30000,
            "wait_until_event": "networkidle",
            "print_background": True,
            "prefer_css_page_size": True,
        }

        num_tasks = 10
        task_args = [
            (
                rendered_html,
                pygments_css,
                self.temp_dir / f"process_output_{i}.pdf",
                layout_config,
                academic_config,
                browser_config,
            )
            for i in range(num_tasks)
        ]

        success_count = 0
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(_worker_compile_process_task, arg) for arg in task_args]
            for future in as_completed(futures):
                if future.result():
                    success_count += 1

        self.assertEqual(success_count, num_tasks, "Sự cố va chạm tiến trình Playwright.")


if __name__ == "__main__":
    unittest.main()
