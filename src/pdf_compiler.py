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
        # Đảm bảo tuân thủ quy tắc linter Ruff (BLE001) và duy trì tính an toàn hệ thống
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

    def __init__(self, output_encoding: str = "utf-8"):
        self.output_encoding = output_encoding

    def compile_to_pdf(
        self, html_content: str, pygments_css: str, output_path: Path
    ) -> None:
        """Đóng gói HTML và CSS Paged Media thành tệp PDF hoàn chỉnh chuẩn Typography."""
        paged_media_css = """
        @page { 
            size: A4; 
            margin: 20mm; 
        }
        
        body {
            font-family: "Segoe UI", "Arial", "Calibri", "Tahoma", sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: "Segoe UI Semibold", "Arial Bold", sans-serif;
            font-weight: bold;
            color: #000000;
            line-height: 1.3;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            word-spacing: normal;
            bookmark-label: content();
        }

        h1 { bookmark-level: 1; font-size: 20pt; }
        h2 { bookmark-level: 2; font-size: 15pt; }
        h3 { bookmark-level: 3; font-size: 13pt; }
        h4 { bookmark-level: 4; font-size: 11pt; }

        code, pre { 
            font-family: "Consolas", "Courier New", monospace;
            font-size: 9.5pt;
            word-break: break-all; 
            white-space: pre-wrap; 
        }

        .highlight {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 1em;
        }
        """

        full_document = f"""<!DOCTYPE html>
        <html lang="vi"><head><meta charset="{self.output_encoding}">
        <style>{pygments_css}\n{paged_media_css}</style>
        </head><body>{html_content}</body></html>"""

        # Cô lập luồng xuất C-Runtime trong suốt quá trình biên dịch vật lý PDF
        with _suppress_c_stderr():
            HTML(string=full_document).write_pdf(target=output_path)
            
        print(f"[THÀNH_CÔNG] Đã xuất bản tệp PDF sắc nét tại: {output_path}")