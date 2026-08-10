# ==============================================================================
# BỘ BIÊN DỊCH PDF VÀ ĐỊNH DẠNG PAGED MEDIA (PDF COMPILER MODULE v1.6.0)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Ephemeral Memory, Security Sandbox & CSS Counter Decoupling
# ==============================================================================

import tempfile
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


class PDFCompiler:
    """Động cơ biên dịch HTML và CSS Paged Media thành tệp PDF qua Playwright Chromium."""

    def __init__(
        self,
        output_encoding: str = "utf-8",
        numbering_config: dict | None = None,
        academic_config: dict | None = None,
        browser_config: dict | None = None,
    ):
        """Khởi tạo động cơ PDF Compiler với tham số mã hóa, đánh số, học thuật và Playwright."""
        self.output_encoding = output_encoding
        self.numbering_config = numbering_config or {}
        self.academic_config = academic_config or {}
        self.browser_config = browser_config or {
            "browser_type": "chromium",
            "headless": True,
            "page_timeout_ms": 30000,
            "wait_until_event": "networkidle",
            "print_background": True,
            "prefer_css_page_size": True,
        }

    def _generate_css_counters(self) -> str:
        """Xây dựng khối quy tắc CSS Counters tự động đếm và chèn số vào tiêu đề (Tối đa Cấp 4 theo APA)."""
        enable_auto = self.numbering_config.get("enable_auto_numbering", True)
        if not enable_auto:
            return ""

        h1_style = self.numbering_config.get("h1_numbering_style", "roman")
        sub_style = self.numbering_config.get("sub_heading_numbering_style", "decimal")
        separator = self.numbering_config.get("number_separator", ". ")

        h1_counter_type = "upper-roman" if h1_style == "roman" else "decimal"

        if sub_style == "none":
            return f"""
            body {{
                counter-reset: h1counter;
            }}
            h1::before {{
                counter-increment: h1counter;
                content: counter(h1counter, {h1_counter_type}) "{separator}";
            }}
            """

        return f"""
        body {{
            counter-reset: h1counter h2counter h3counter h4counter;
        }}
        h1 {{
            counter-reset: h2counter;
        }}
        h2 {{
            counter-reset: h3counter;
        }}
        h3 {{
            counter-reset: h4counter;
        }}
        h1::before {{
            counter-increment: h1counter;
            content: counter(h1counter, {h1_counter_type}) "{separator}";
        }}
        h2::before {{
            counter-increment: h2counter;
            content: counter(h2counter, decimal) "{separator}";
        }}
        h3::before {{
            counter-increment: h3counter;
            content: counter(h2counter, decimal) "." counter(h3counter, decimal) "{separator}";
        }}
        h4::before {{
            counter-increment: h4counter;
            content: counter(h2counter, decimal) "." counter(h3counter, decimal) "." counter(h4counter, decimal) "{separator}";
        }}
        """

    def _build_paged_media_css(self, pygments_css: str) -> str:
        """Tạo lập bộ CSS Paged Media hoàn chỉnh bao bọc toàn bộ quy chuẩn in ấn và Typography."""
        dynamic_counters_css = self._generate_css_counters()

        prevent_orphans = self.academic_config.get("prevent_orphans_and_widows", True)
        orphans_widows_css = "orphans: 2; widows: 2;" if prevent_orphans else ""

        return f"""
        {pygments_css}

        @page {{ 
            size: A4; 
            margin: 20mm; 
        }}
        
        /* CƯỠNG CHẾ CĂN LỀ TRÁI TOÀN BỘ VĂN BẢN (TRIỆT TIÊU LỖI RÒ RỈ CĂN GIỮA) */
        body, p, ul, ol, li, blockquote {{
            text-align: left !important;
            font-family: "Segoe UI", "Arial", "Calibri", "Tahoma", sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            {orphans_widows_css}
        }}

        p {{
            {orphans_widows_css}
            text-align: left !important;
        }}

        /* ================================================================== */
        /* CẤU HÌNH TYPOGRAPHY TIÊU ĐỀ CHUẨN APA / IEEE (HEADING STYLING)     */
        /* Cưỡng chế BOLD & LEFT-ALIGN cho H1-H6, độc lập hoàn toàn với Bookmark */
        /* ================================================================== */
        h1, h2, h3, h4, h5, h6 {{
            text-align: left !important;
            font-family: "Segoe UI Semibold", "Arial Bold", sans-serif;
            font-weight: bold !important;
            color: #000000;
            line-height: 1.3;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            word-spacing: normal;
            page-break-after: avoid;
            break-after: avoid;
        }}

        h1 {{ font-size: 20pt; }}
        h2 {{ font-size: 15pt; }}
        h3 {{ font-size: 13pt; }}
        h4 {{ font-size: 11pt; }}
        
        h5 {{ 
            font-size: 11pt !important; 
            font-style: italic; 
        }}
        
        h6 {{ 
            font-size: 11pt !important; 
            font-style: italic; 
            color: #333333; 
        }}

        {dynamic_counters_css}

        /* ================================================================== */
        /* KIỂM SOÁT BẺ DÒNG VÀ CĂN LỀ KHỐI MÃ (CODE BLOCK)                   */
        /* ================================================================== */
        code, pre, .highlight {{ 
            text-align: left !important;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 9.5pt;
            overflow-wrap: break-word;
            word-wrap: break-word;
            white-space: pre-wrap; 
        }}

        pre {{
            page-break-inside: avoid;
            break-inside: avoid;
            text-align: left !important;
        }}

        .highlight {{
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 1em;
            page-break-inside: avoid;
            break-inside: avoid;
            text-align: left !important;
        }}

        /* ================================================================== */
        /* NÂNG CẤP ĐỊNH DẠNG KHUNG VIỀN VÀ TRÁNH NGẮT TRANG BẢNG (TABLES)   */
        /* ================================================================== */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1.2em;
            margin-bottom: 1.2em;
            page-break-inside: avoid;
            break-inside: avoid;
            text-align: left !important;
        }}

        th, td {{
            border: 1pt solid #1a1a1a;
            padding: 8px 12px;
            text-align: left !important;
            vertical-align: top;
            font-size: 10pt;
        }}

        th {{
            background-color: #f2f2f2;
            font-weight: bold;
            color: #000000;
        }}

        tr {{
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        /* ================================================================== */
        /* CHỈ CĂN GIỮA DUY NHẤT KHỐI TOÁN HỌC (ISOLATED KATEX BLOCK)         */
        /* ================================================================== */
        .math-tex {{
            display: inline-block;
            text-align: initial;
            margin: 0 0.1em;
        }}

        div.math-tex {{
            display: block;
            text-align: center !important;
            margin: 1.2em 0;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .katex-display {{
            text-align: center !important;
            margin: 0.5em 0 !important;
            overflow-x: auto;
            overflow-y: hidden;
        }}

        .math-error, .math-raw {{
            font-family: "Consolas", "Courier New", monospace;
            color: #c93b2b;
            background-color: #f8f9fa;
            border: 1px solid #eaecf0;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
            text-align: left !important;
        }}
        """

    def compile_to_pdf(
        self, html_content: str, pygments_css: str, output_path: Path
    ) -> None:
        """Đóng gói HTML và render PDF thông qua Playwright Chromium Headless Engine."""
        paged_media_css = self._build_paged_media_css(pygments_css)

        full_document = f"""<!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="{self.output_encoding}">
            <style>{paged_media_css}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>"""

        timeout_ms = self.browser_config.get("page_timeout_ms", 30000)
        wait_until = self.browser_config.get("wait_until_event", "networkidle")
        print_bg = self.browser_config.get("print_background", True)
        prefer_css_page = self.browser_config.get("prefer_css_page_size", True)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 1. Cấp phát tệp bộ nhớ tạm thời ẩn danh ngẫu nhiên từ Hệ điều hành (Ephemeral File System)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding=self.output_encoding,
            suffix=".html",
            delete=False,
        ) as temp_file:
            temp_file.write(full_document)
            temp_path = Path(temp_file.name)

        try:
            with sync_playwright() as p:
                # KHIÊN AN NINH v1.6.0: Gỡ bỏ hoàn toàn bộ 3 cờ hạ bảo mật (--disable-web-security, --allow-file-access-from-files, --no-sandbox)
                browser = p.chromium.launch(
                    headless=True
                )
                page = browser.new_page()

                try:
                    # 2. Điều hướng Chromium bằng giao thức an toàn file:/// trỏ đến tệp tạm ngầm
                    page.goto(
                        temp_path.as_uri(),
                        timeout=timeout_ms,
                        wait_until=wait_until,
                    )

                    # 3. Đợi mỏ neo KaTeX đúc xong DOM toán học nếu có công thức
                    if (
                        '<span class="math-tex">' in html_content
                        or '<div class="math-tex">' in html_content
                    ):
                        try:
                            page.wait_for_selector(".katex", timeout=5000)
                        except PlaywrightTimeoutError:
                            print(
                                "    -> [THÔNG_TIN] Trình duyệt đã bỏ qua pha kết xuất DOM toán học "
                                "(Tài liệu không chứa công thức phức tạp hoặc thời gian Timeout kết thúc sớm)."
                            )

                    # 4. Xuất bản tệp PDF chuẩn trang in A4 qua Playwright API
                    page.pdf(
                        path=str(output_path),
                        format="A4",
                        print_background=print_bg,
                        prefer_css_page_size=prefer_css_page,
                        margin={
                            "top": "20mm",
                            "bottom": "20mm",
                            "left": "20mm",
                            "right": "20mm",
                        },
                    )
                finally:
                    browser.close()
        finally:
            # 5. Ràng buộc Chu trình Sống (Context Management): Đảm bảo giải phóng tệp tạm dù tiến trình thành công hay ngắt đột ngột
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)

        print(
            f"[THÀNH_CÔNG] Đã xuất bản tệp PDF sắc nét qua Chromium tại: {output_path}"
        )
