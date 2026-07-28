from pathlib import Path

from markdown_it import MarkdownIt


class ASTParser:
    """Bộ phân tích Cây Cú Pháp Trừu Tượng (AST) phòng thủ."""

    def __init__(self, encoding_standard: str = "utf-8"):
        # Cưỡng chế chuẩn mã hóa UTF-8 theo yêu cầu PRD
        self.encoding_standard = encoding_standard
        # Khởi tạo động cơ phân tích markdown-it-py
        self.md_engine = MarkdownIt("commonmark")

    def parse_markdown_file(self, file_path: Path) -> list:
        """Đọc tệp Markdown với UTF-8 và phân rã thành các Nút AST."""
        if not file_path.exists():
            raise FileNotFoundError(
                f"[LỖI_I/O] Không tìm thấy tệp đầu vào tại: {file_path}"
            )

        try:
            # Ngăn chặn sự cố trôi dạt mã hóa cp1252 trên Windows 11
            with open(file_path, "r", encoding=self.encoding_standard) as file_stream:
                raw_text = file_stream.read()

            # Phân rã văn bản thành chuỗi các đối tượng Token
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