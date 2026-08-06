import io
import os
import sys
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def _suppress_c_stderr():
    """Bộ điều hướng tạm thời cô lập luồng C-Runtime stderr (File Descriptor 2).
    
    Triệt tiêu hoàn toàn các thông báo nhiễu cấp hệ điều hành từ thư viện C (GLib/GIO/GTK3)
    trên Windows 11 mà không ảnh hưởng đến luồng xử lý ngoại lệ của Python.
    """
    if sys.platform != "win32":
        yield
        return

    # Tắt các cấp độ log thông thường của GLib qua biến môi trường
    os.environ["G_MESSAGES_DEBUG"] = "none"
    os.environ["GLIB_LOG_LEVEL"] = "4"
    os.environ["G_ENABLE_DIAGNOSTIC"] = "0"

    try:
        # Lưu lại bản sao của File Descriptor stderr gốc (FD 2)
        stderr_fd = sys.stderr.fileno()
        saved_stderr_fd = os.dup(stderr_fd)
        
        # Mở thiết bị null của hệ thống để hứng rác
        devnull_fd = os.open(os.devnull, os.O_WRONLY)
        
        # Ghi đè FD 2 bằng devnull FD
        os.dup2(devnull_fd, stderr_fd)
        os.close(devnull_fd)
        
        try:
            yield
        finally:
            # Khôi phục lại FD stderr gốc sau khi hoàn tất thao tác nạp thư viện
            os.dup2(saved_stderr_fd, stderr_fd)
            os.close(saved_stderr_fd)
    except (AttributeError, io.UnsupportedOperation, OSError):
        # Khoanh vùng chính xác các ngoại lệ khi thao tác File Descriptor thất bại
        yield


def _register_gtk_dll_directories() -> None:
    """Tự động phát hiện và đăng ký đường dẫn DLL của GTK3 trên Windows 11."""
    if sys.platform == "win32":
        possible_gtk_paths = [
            Path(r"C:\Program Files\GTK3-Runtime Win64\bin"),
            Path(r"C:\Program Files (x86)\GTK3-Runtime Win64\bin"),
            Path(r"C:\msys64\ucrt64\bin"),
            Path(r"C:\msys64\mingw64\bin"),
        ]
        for gtk_path in possible_gtk_paths:
            if gtk_path.exists():
                os.add_dll_directory(str(gtk_path))
                os.environ["PATH"] = str(gtk_path) + os.pathsep + os.environ.get("PATH", "")
                break


# Thực thi đăng ký đường dẫn DLL GTK3
_register_gtk_dll_directories()

# Khởi chạy bộ cô lập C-Runtime stderr khi nạp thư viện WeasyPrint
with _suppress_c_stderr():
    try:
        from weasyprint import HTML
    except OSError as error:
        raise ImportError(
            f"[LỖI_HỆ_THỐNG] Không thể nạp thư viện WeasyPrint/GTK3: {error}"
        ) from error


class PDFCompiler:
    """Động cơ biên dịch HTML và CSS Paged Media thành tệp PDF chất lượng cao."""

    def __init__(
        self,
        output_encoding: str = "utf-8",
        numbering_config: dict | None = None,
    ):
        """Khởi tạo động cơ PDF Compiler với tham số mã hóa và cấu hình đánh số."""
        self.output_encoding = output_encoding
        self.numbering_config = numbering_config or {}

    def _generate_css_counters(self) -> str:
        """Xây dựng khối quy tắc CSS Counters tự động đếm và chèn số vào tiêu đề."""
        enable_auto = self.numbering_config.get("enable_auto_numbering", True)
        if not enable_auto:
            return ""

        h1_style = self.numbering_config.get("h1_numbering_style", "roman")
        sub_style = self.numbering_config.get("sub_heading_numbering_style", "decimal")
        separator = self.numbering_config.get("number_separator", ". ")

        # Ánh xạ kiểu đánh số La Mã (upper-roman) hoặc số tự nhiên (decimal)
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

    def compile_to_pdf(
        self, html_content: str, pygments_css: str, output_path: Path
    ) -> None:
        """Đóng gói HTML và CSS Paged Media thành tệp PDF hoàn chỉnh chuẩn Typography."""
        dynamic_counters_css = self._generate_css_counters()

        paged_media_css = f"""
        @page {{ 
            size: A4; 
            margin: 20mm; 
        }}
        
        body {{
            font-family: "Segoe UI", "Arial", "Calibri", "Tahoma", sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: "Segoe UI Semibold", "Arial Bold", sans-serif;
            font-weight: bold;
            color: #000000;
            line-height: 1.3;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            word-spacing: normal;
            bookmark-label: content();
        }}

        h1 {{ bookmark-level: 1; font-size: 20pt; }}
        h2 {{ bookmark-level: 2; font-size: 15pt; }}
        h3 {{ bookmark-level: 3; font-size: 13pt; }}
        h4 {{ bookmark-level: 4; font-size: 11pt; }}

        {dynamic_counters_css}

        code, pre {{ 
            font-family: "Consolas", "Courier New", monospace;
            font-size: 9.5pt;
            word-break: break-all; 
            white-space: pre-wrap; 
        }}

        .highlight {{
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 1em;
        }}

        /* ================================================================== */
        /* LỚP GIÁP CSS PHÒNG THỦ: TOÁN HỌC (DEFENSIVE MATHML STYLING)        */
        /* ================================================================== */
        
        /* Cưỡng chế neo chặt đáy công thức toán học vào đường cơ sở của văn bản */
        .math-inline {{
            display: inline-block;
            vertical-align: baseline;
            margin: 0 0.1em;
        }}

        /* Định dạng hiển thị độc lập cho khối công thức toán lớn */
        .math-block {{
            display: block;
            text-align: center;
            margin: 1.2em 0;
            page-break-inside: avoid;
        }}

        /* 1. Kìm hãm kích thước khối toán học đồng nhất với văn bản xung quanh */
        math {{
            font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", serif;
            font-size: 0.95em; 
        }}

        /* 2. Ép buộc nâng cao hệ số mũ và hạ thấp cơ số dưới bằng CSS thuần */
        /* Cơ chế này triệt tiêu hoàn toàn lỗi hiển thị 230 nếu GTK3 hỏng */
        msup > *:nth-child(2) {{
            vertical-align: super;
            font-size: 0.75em;
        }}

        msub > *:nth-child(2) {{
            vertical-align: sub;
            font-size: 0.75em;
        }}

        /* Khung cảnh báo màu đỏ dành riêng cho các đoạn công thức hỏng */
        .math-error, .math-raw {{
            font-family: "Consolas", "Courier New", monospace;
            color: #c93b2b;
            background-color: #f8f9fa;
            border: 1px solid #eaecf0;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        """

        full_document = f"""<!DOCTYPE html>
        <html lang="vi"><head><meta charset="{self.output_encoding}">
        <style>{pygments_css}\n{paged_media_css}</style>
        </head><body>{html_content}</body></html>"""

        # Cô lập luồng xuất C-Runtime trong suốt quá trình biên dịch vật lý PDF
        with _suppress_c_stderr():
            HTML(string=full_document).write_pdf(target=output_path)
            
        print(f"[THÀNH_CÔNG] Đã xuất bản tệp PDF sắc nét tại: {output_path}")