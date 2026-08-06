# ==============================================================================
# BỘ PHÂN TÍCH CÂY CÚ PHÁP TRỪU TƯỢNG (AST PARSER MODULE)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.2.0 - Tích hợp Math Plugin)
# Kiến trúc: Defensive Programming & Isolation Layer
# ==============================================================================

from pathlib import Path

from markdown_it import MarkdownIt


class ASTParser:
    """Bộ phân tích Cây Cú Pháp Trừu Tượng (AST) phòng thủ hỗ trợ nhận diện Toán học."""

    def __init__(self, encoding_standard: str = "utf-8", enable_math: bool = True):
        """Khởi tạo động cơ phân tích AST với chuẩn mã hóa cưỡng chế và bộ lọc toán học.

        Args:
            encoding_standard (str): Chuẩn mã hóa luồng I/O (mặc định 'utf-8').
            enable_math (bool): Cờ bật/tắt tính năng nhận diện ký hiệu toán học TeX.
        """
        # 1. Cưỡng chế chuẩn mã hóa UTF-8 theo yêu cầu kiến trúc phòng thủ
        self.encoding_standard = encoding_standard
        self.enable_math = enable_math

        # 2. Khởi tạo động cơ phân tích markdown-it-py chuẩn CommonMark
        self.md_engine = MarkdownIt("commonmark")

        # 3. Lắp đặt "Bộ Ống Kính X-Quang" (Plugin Toán học) nếu cờ cấu hình bật
        if self.enable_math:
            self._register_math_plugin()

    def _register_math_plugin(self) -> None:
        """Đăng ký plugin texmath để nhận diện ranh giới ký tự $ và $$."""
        try:
            from mdit_py_plugins.texmath import texmath_plugin

            # Kích hoạt plugin với quy tắc nhận diện dấu dollar ($ inline và $$ block)
            self.md_engine.use(texmath_plugin, macros={"delimiters": "dollars"})
        except ImportError as error:
            # Aptomat phòng thủ: Nếu thiếu thư viện mdit-py-plugins, cảnh báo và hạ cấp an toàn
            print(
                f"[CẢNH_BÁO_AST] Không thể nạp 'mdit_py_plugins.texmath': {error}. "
                "Hệ thống sẽ hạ cấp về chế độ phân tích văn bản thuần."
            )

    def parse_markdown_file(self, file_path: Path) -> list:
        """Đọc tệp Markdown theo chuẩn UTF-8 và phân rã thành danh sách các Nút AST (Tokens).

        Args:
            file_path (Path): Đường dẫn tuyệt đối hoặc tương đối tới tệp Markdown đầu vào.

        Returns:
            list: Danh sách các đối tượng Token chứa thông tin phân rã cấu trúc.

        Raises:
            FileNotFoundError: Khi tệp đầu vào không tồn tại trên đĩa cứng.
            UnicodeDecodeError: Khi tệp bị xung đột mã hóa khác UTF-8.
        """
        if not file_path.exists():
            raise FileNotFoundError(
                f"[LỖI_I/O] Không tìm thấy tệp đầu vào tại: {file_path}"
            )

        try:
            # Ngăn chặn sự cố trôi dạt mã hóa cp1252 trên Windows 11 bằng UTF-8 cưỡng chế
            with open(file_path, "r", encoding=self.encoding_standard) as file_stream:
                raw_text = file_stream.read()

            # Phân rã văn bản thành chuỗi các đối tượng Token (Bao gồm cả các Nút toán học)
            tokens = self.md_engine.parse(raw_text)
            return tokens
        except UnicodeDecodeError as error:
            raise UnicodeDecodeError(
                error.encoding,
                error.object,
                error.start,
                error.end,
                f"[LỖI_MÃ_HÓA] Không thể đọc tệp bằng chuẩn {self.encoding_standard}: {error}",
            )