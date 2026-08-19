# ==============================================================================
# TỆP: src/pdf_compiler.py (BỘ BIÊN DỊCH PDF & PAGED MEDIA WINDOWS 11 v2.5.7)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Native Formula Box, Khắc phục Ảo ảnh Viewport & Shrink-To-Fit Radar
# ==============================================================================

import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


class PDFCompiler:
    """Động cơ biên dịch HTML và CSS Paged Media thành tệp PDF tối ưu hóa cho Windows 11."""

    def __init__(
        self,
        output_encoding: str = "utf-8",
        layout_config: dict[str, Any] | None = None,
        numbering_config: dict[str, Any] | None = None,
        academic_config: dict[str, Any] | None = None,
        browser_config: dict[str, Any] | None = None,
        table_config: dict[str, Any] | None = None,
    ) -> None:
        """Khởi tạo động cơ PDF Compiler với tham số trang in, mã hóa, đánh số, học thuật, bảng biểu và Playwright."""
        self.output_encoding = output_encoding
        self.layout_config = layout_config or {
            "page_size": "A4",
            "margin": "20mm",
            "code_overflow_handling": "break-word",
        }
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
        self.table_config = table_config or {
            "enable_gfm_tables": True,
            "overflow_strategy": "clip_and_warn",
            "repeat_header_on_page_break": True,
            "max_printable_width_mm": 170,
        }

    def _generate_css_counters(self) -> str:
        """Xây dựng khối quy tắc CSS Counters tự động đếm và chèn số vào tiêu đề (Tối đa Cấp 4)."""
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
        """Tạo lập bộ CSS Paged Media Windows 11 bao bọc Typography Song ngữ, Backtick, Callouts và Formula Box."""
        dynamic_counters_css = self._generate_css_counters()

        page_size = self.layout_config.get("page_size", "A4")
        margin = self.layout_config.get("margin", "20mm")
        code_overflow = self.layout_config.get("code_overflow_handling", "break-word")
        max_printable_width = self.table_config.get("max_printable_width_mm", 170)

        prevent_orphans = self.academic_config.get("prevent_orphans_and_widows", True)
        orphans_widows_css = "orphans: 2; widows: 2;" if prevent_orphans else ""

        return f"""
        {pygments_css}

        @page {{ 
            size: {page_size}; 
            margin: {margin}; 
        }}
        
        /* 1. HỆ THỐNG PHÔNG CHỮ CHUẨN HÓA WINDOWS 11 SONG NGỮ (VI - EN) */
        body, p, ul, ol, li {{
            text-align: left !important;
            font-family: "Segoe UI Variable Text", "Segoe UI", "Calibri", Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.65;
            color: #1a1a1a;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            {orphans_widows_css}
        }}

        p {{
            {orphans_widows_css}
            text-align: left !important;
            margin-top: 0.4em;
            margin-bottom: 0.8em;
        }}

        /* 2. CẤU HÌNH TIÊU ĐỀ TYPOGRAPHY APA / IEEE CHO WINDOWS 11 */
        h1, h2, h3, h4, h5, h6 {{
            text-align: left !important;
            font-family: "Segoe UI Variable Display", "Segoe UI Semibold", "Segoe UI", "Arial Bold", sans-serif;
            font-weight: 700 !important;
            color: #0d1117;
            line-height: 1.35;
            margin-top: 1.4em;
            margin-bottom: 0.6em;
            page-break-after: avoid;
            break-after: avoid;
        }}

        h1 {{ font-size: 20pt; }}
        h2 {{ font-size: 15pt; }}
        h3 {{ font-size: 13pt; }}
        h4 {{ font-size: 11pt; }}
        h5 {{ font-size: 11pt !important; font-style: italic; }}
        h6 {{ font-size: 11pt !important; font-style: italic; color: #4b5563; }}

        {dynamic_counters_css}

        /* 3. KHỐI MÃ NGUỒN NHIỀU DÒNG VỚI CASCADIA CODE (WINDOWS 11 NATIVE) */
        pre, .highlight {{ 
            text-align: left !important;
            font-family: "Cascadia Code", "Cascadia Mono", Consolas, "Courier New", monospace !important;
            font-size: 9.5pt;
            overflow-wrap: {code_overflow};
            word-wrap: {code_overflow};
            white-space: pre-wrap; 
        }}

        .highlight {{
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 1em;
            page-break-inside: avoid;
            break-inside: avoid;
            text-align: left !important;
        }}

        .highlight pre {{
            page-break-inside: avoid;
            break-inside: avoid;
            text-align: left !important;
            padding: 0 !important;
            margin: 0 !important;
            background-color: transparent !important;
            border: none !important;
        }}

        pre {{
            page-break-inside: avoid;
            break-inside: avoid;
            text-align: left !important;
        }}

        /* 4. ĐỊNH HÌNH CHỮ TRONG DẤU NHÁY NGƯỢC (INLINE CODE / BACKTICK) */
        :not(pre) > code {{
            background-color: rgba(175, 184, 193, 0.22) !important;
            padding: 0.15em 0.45em !important;
            border-radius: 5px !important;
            font-size: 88% !important;
            color: #0969da !important;
            font-family: "Cascadia Code", "Cascadia Mono", Consolas, "Courier New", monospace !important;
            white-space: pre-wrap !important;
            border: 1px solid rgba(175, 184, 193, 0.35) !important;
            font-weight: 500 !important;
        }}

        /* 5. KHỐI TRÍCH DẪN TIÊU CHUẨN (STANDARD BLOCKQUOTE) */
        blockquote {{
            margin: 1.2em 0 !important;
            padding: 0.6em 1.2em !important;
            color: #57606a !important;
            border-left: 4px solid #d0d7de !important;
            background-color: #f6f8fa !important;
            border-radius: 0 6px 6px 0 !important;
            text-align: left !important;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}

        blockquote > p {{
            margin: 0.4em 0 !important;
            color: #57606a !important;
        }}

        /* ==========================================================================
           6. MA TRẬN CSS OBSIDIAN CALLOUTS & GFM ALERTS ĐA TẦNG (GENERIC & SPECIFIC)
           ========================================================================== */
        
        /* Cấu trúc Hộp Chứa Cơ Sở Toàn Năng cho Mọi Callout [data-callout] */
        .markdown-alert, [data-callout] {{
            padding: 12px 16px 14px 18px !important;
            margin: 1.2em 0 !important;
            border-left: 5px solid #6b7280 !important;
            background-color: rgba(243, 244, 246, 0.7) !important;
            border-radius: 6px !important;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            text-align: left !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        }}

        /* Thanh Tiêu Đề Ngữ Nghĩa của Callout */
        .markdown-alert-title {{
            display: flex !important;
            align-items: center !important;
            font-weight: 700 !important;
            font-size: 11pt !important;
            margin-bottom: 8px !important;
            text-transform: none !important;
            letter-spacing: 0.3px;
        }}

        .markdown-alert-icon {{
            margin-right: 8px !important;
            font-size: 12pt !important;
            display: inline-block !important;
        }}

        .markdown-alert > p {{
            margin: 0.3em 0 !important;
        }}

        .markdown-alert > p:first-of-type {{
            margin-top: 0 !important;
        }}

        .markdown-alert > p:last-child {{
            margin-bottom: 0 !important;
        }}

        /* NHÓM 1: Note & Info (Xanh lam) */
        [data-callout="note"], [data-callout="info"], .markdown-alert-note, .markdown-alert-info {{
            border-left-color: #0969da !important;
            background-color: rgba(9, 105, 218, 0.05) !important;
        }}
        [data-callout="note"] .markdown-alert-title, [data-callout="info"] .markdown-alert-title {{
            color: #0969da !important;
        }}
        [data-callout="note"] .markdown-alert-icon::before, [data-callout="info"] .markdown-alert-icon::before {{
            content: "ℹ️";
        }}

        /* NHÓM 2: Tip, Success & Done (Xanh lá) */
        [data-callout="tip"], [data-callout="success"], [data-callout="done"], .markdown-alert-tip {{
            border-left-color: #1a7f37 !important;
            background-color: rgba(26, 127, 55, 0.05) !important;
        }}
        [data-callout="tip"] .markdown-alert-title, [data-callout="success"] .markdown-alert-title {{
            color: #1a7f37 !important;
        }}
        [data-callout="tip"] .markdown-alert-icon::before {{
            content: "💡";
        }}
        [data-callout="success"] .markdown-alert-icon::before, [data-callout="done"] .markdown-alert-icon::before {{
            content: "✅";
        }}

        /* NHÓM 3: Important & Todo (Tím thạch anh) */
        [data-callout="important"], [data-callout="todo"], .markdown-alert-important {{
            border-left-color: #8250df !important;
            background-color: rgba(130, 80, 223, 0.05) !important;
        }}
        [data-callout="important"] .markdown-alert-title, [data-callout="todo"] .markdown-alert-title {{
            color: #8250df !important;
        }}
        [data-callout="important"] .markdown-alert-icon::before {{
            content: "💬";
        }}
        [data-callout="todo"] .markdown-alert-icon::before {{
            content: "📋";
        }}

        /* NHÓM 4: Warning & Attention (Vàng cam) */
        [data-callout="warning"], [data-callout="attention"], .markdown-alert-warning {{
            border-left-color: #9a6700 !important;
            background-color: rgba(154, 103, 0, 0.06) !important;
        }}
        [data-callout="warning"] .markdown-alert-title, [data-callout="attention"] .markdown-alert-title {{
            color: #9a6700 !important;
        }}
        [data-callout="warning"] .markdown-alert-icon::before, [data-callout="attention"] .markdown-alert-icon::before {{
            content: "⚠️";
        }}

        /* NHÓM 5: Caution, Danger, Error & Bug (Đỏ thẫm) */
        [data-callout="caution"], [data-callout="danger"], [data-callout="error"], [data-callout="bug"], .markdown-alert-caution {{
            border-left-color: #d1242f !important;
            background-color: rgba(209, 36, 47, 0.05) !important;
        }}
        [data-callout="caution"] .markdown-alert-title, [data-callout="danger"] .markdown-alert-title {{
            color: #d1242f !important;
        }}
        [data-callout="caution"] .markdown-alert-icon::before, [data-callout="danger"] .markdown-alert-icon::before {{
            content: "🛑";
        }}
        [data-callout="bug"] .markdown-alert-icon::before {{
            content: "🪲";
        }}

        /* NHÓM 6: Quote & Cite (Xám kim loại) */
        [data-callout="quote"], [data-callout="cite"], .markdown-alert-quote {{
            border-left-color: #57606a !important;
            background-color: rgba(87, 96, 106, 0.06) !important;
        }}
        [data-callout="quote"] .markdown-alert-title, [data-callout="cite"] .markdown-alert-title {{
            color: #57606a !important;
        }}
        [data-callout="quote"] .markdown-alert-icon::before, [data-callout="cite"] .markdown-alert-icon::before {{
            content: "❞";
        }}

        /* 7. ĐỊNH DẠNG KHUNG BẢNG BIỂU GFM (TABLES) */
        table {{
            width: 100%;
            max-width: {max_printable_width}mm !important;
            overflow-x: auto;
            border-collapse: collapse;
            margin-top: 1.2em;
            margin-bottom: 1.2em;
            page-break-inside: avoid;
            break-inside: avoid;
            text-align: left !important;
        }}

        th, td {{
            border: 1pt solid #d0d7de;
            padding: 8px 12px;
            text-align: left !important;
            vertical-align: top;
            font-size: 10pt;
        }}

        th {{
            background-color: #f6f8fa;
            font-weight: 700;
            color: #24292f;
        }}

        tr {{
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        /* 8. ĐỊNH DẠNG CÔNG THỨC TOÁN HỌC (KATEX & MATHJAX TYPOGRAPHY) */
        .math-tex {{
            display: inline-block;
            text-align: initial;
            margin: 0 0.1em;
            font-family: "KaTeX_Math", "Cambria Math", "Times New Roman", serif !important;
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
            margin: 0.6em 0 !important;
            overflow-x: auto;
            overflow-y: hidden;
        }}

        mjx-container {{
            max-width: 100% !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            vertical-align: middle !important;
            outline: none !important;
        }}

        mjx-container[display="true"] {{
            display: block !important;
            text-align: center !important;
            margin: 1em 0 !important;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        mjx-container[jax="SVG"] svg {{
            max-width: 100% !important;
            height: auto !important;
            vertical-align: middle !important;
            display: inline-block !important;
        }}

        svg {{
            max-width: 100%;
            height: auto;
        }}

        .vietnamese-math-text {{
            font-family: "Segoe UI", "Times New Roman", Arial, sans-serif !important;
            display: inline-block !important;
        }}

        /* 9. HỘP CÔNG THỨC TOÁN HỌC ĐỘC LẬP (NATIVE FORMULA BOX) */
        .formula-box {{
            padding: 14px 18px 16px 18px !important;
            margin: 1.5em 0 !important;
            border: 1.5pt solid #0969da !important;
            border-left: 5px solid #0969da !important;
            background-color: rgba(9, 105, 218, 0.04) !important;
            border-radius: 6px !important;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            text-align: left !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            position: relative !important;
        }}

        .formula-box::before {{
            content: "📐 Formula (Công Thức)" !important;
            display: block !important;
            font-family: "Segoe UI Variable Display", "Segoe UI Semibold", "Segoe UI", Arial, sans-serif !important;
            font-weight: 700 !important;
            font-size: 11pt !important;
            color: #0969da !important;
            margin-bottom: 10px !important;
            border-bottom: 1px dashed rgba(9, 105, 218, 0.25) !important;
            padding-bottom: 6px !important;
            letter-spacing: 0.3px !important;
        }}

        .formula-box > .math-tex, 
        .formula-box > div.math-tex, 
        .formula-box > .katex-display {{
            margin-top: 0.4em !important;
            margin-bottom: 0.4em !important;
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
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                try:
                    page.goto(
                        temp_path.as_uri(),
                        timeout=timeout_ms,
                        wait_until=wait_until,
                    )

                    if (
                        '<span class="math-tex">' in html_content
                        or '<div class="math-tex">' in html_content
                        or 'class="math-tex-b64"' in html_content
                        or 'MathJax' in html_content
                        or 'formula-box' in html_content
                    ):
                        try:
                            page.wait_for_selector(".katex, mjx-container, svg", timeout=5000)
                        except PlaywrightTimeoutError:
                            print(
                                "    -> [THÔNG_TIN] Trình duyệt đã hoàn tất kết xuất layout "
                                "(Bỏ qua đợi mỏ neo DOM toán học)."
                            )

                    # [NÂNG CẤP LÕI KẾT XUẤT 3.0]: Bơm Kịch bản Radar JS Ép khuôn Chân không (Shrink-to-Fit)
                    js_script = """
                        document.querySelectorAll('.katex-display, mjx-container[display="true"], div.math-tex').forEach(container => {
                            // 1. Định vị phần tử đồ họa cốt lõi
                            const coreElement = container.querySelector('.katex') 
                                || container.querySelector('svg') 
                                || container;
                                
                            // 2. KỸ THUẬT ÉP KHUÔN (SHRINK-TO-FIT): 
                            // Tạm thời tước bỏ thuộc tính Block để vô hiệu hóa sự giãn nở ảo của Bounding Box
                            const originalCssText = coreElement.style.cssText;
                            coreElement.style.setProperty('display', 'inline-block', 'important');
                            coreElement.style.setProperty('width', 'max-content', 'important');
                            coreElement.style.setProperty('white-space', 'nowrap', 'important');
                            
                            // Trích xuất bề ngang vật lý chính xác đến từng điểm ảnh của các nét vẽ toán học
                            const scrollWidth = Math.max(
                                coreElement.scrollWidth || 0,
                                coreElement.offsetWidth || 0,
                                coreElement.getBoundingClientRect().width || 0
                            );
                            
                            // Hoàn trả nguyên trạng thuộc tính hiển thị gốc
                            coreElement.style.cssText = originalCssText;
                            
                            // 3. Quy đổi giới hạn in ấn
                            const MAX_PRINTABLE_WIDTH_PX = MAX_WIDTH_MM_PLACEHOLDER * (96 / 25.4);
                            
                            const parentBox = container.closest('.formula-box') || container.parentElement;
                            const clientWidth = parentBox ? parentBox.clientWidth : document.body.clientWidth;
                            
                            const safeWidth = Math.min(clientWidth, MAX_PRINTABLE_WIDTH_PX);
                            
                            // 4. Phán Quyết Thực Thi: Lệnh Zoom chỉ kích hoạt KHI VÀ CHỈ KHI công thức thực sự tràn lề
                            if (scrollWidth > safeWidth && safeWidth > 0) {
                                const scaleRatio = (safeWidth / scrollWidth) * 0.98;
                                container.style.zoom = scaleRatio;
                            }
                        });
                    """.replace("MAX_WIDTH_MM_PLACEHOLDER", str(self.table_config.get("max_printable_width_mm", 170)))

                    page.evaluate(js_script)

                    page.pdf(
                        path=str(output_path),
                        format=self.layout_config.get("page_size", "A4"),
                        print_background=print_bg,
                        prefer_css_page_size=prefer_css_page,
                        margin={
                            "top": self.layout_config.get("margin", "20mm"),
                            "bottom": self.layout_config.get("margin", "20mm"),
                            "left": self.layout_config.get("margin", "20mm"),
                            "right": self.layout_config.get("margin", "20mm"),
                        },
                    )
                finally:
                    browser.close()
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass

        print(
            f"[THÀNH_CÔNG] Đã xuất bản tệp PDF sắc nét qua Chromium tại: {output_path}"
        )
