# ==============================================================================
# PHẦN 1: TỆP src/ast_parser.py (NÂNG CẤP BĂM MẬT MÃ SHA-256 v1.5.1)
# Đường dẫn: src/ast_parser.py
# Kiến trúc: Cryptographic Masking Pattern & PEP 8 Import Compliant
# ==============================================================================

import hashlib
import re
from pathlib import Path

from markdown_it import MarkdownIt


class ASTParser:
    """Bộ phân tích Cây Cú Pháp Trừu Tượng (AST) phòng thủ hỗ trợ nhận diện Toán học và Bảng biểu GFM."""

    def __init__(
        self,
        encoding_standard: str = "utf-8",
        enable_math: bool = True,
        enable_tables: bool = True,
        math_syntax_delimiters: list | None = None,
    ):
        """Khởi tạo động cơ phân tích AST với chuẩn mã hóa cưỡng chế, cảm biến bảng GFM và danh sách ranh giới toán học."""
        self.encoding_standard = encoding_standard
        self.enable_math = enable_math
        self.enable_tables = enable_tables
        self.math_syntax_delimiters = math_syntax_delimiters or ["dollars", "brackets"]

        if self.enable_tables:
            self.md_engine = MarkdownIt("gfm-like")
        else:
            self.md_engine = MarkdownIt("commonmark")

        if self.enable_math:
            self._register_math_plugin()

    def _register_math_plugin(self) -> None:
        """Đăng ký plugin texmath chuyên biệt cấu hình chuẩn mặc định."""
        try:
            from mdit_py_plugins.texmath import texmath_plugin

            # Hủy bỏ vòng lặp gây xung đột quy tắc (Rule Collision).
            # Nạp duy nhất một lần. Cú pháp Brackets sẽ được đồng bộ hóa
            # sang Dollars thông qua màng lọc _unify_math_delimiters.
            self.md_engine.use(texmath_plugin)
        except ImportError as error:
            print(
                f"[CẢNH_BÁO_AST] Không thể nạp 'mdit_py_plugins.texmath': {error}. "
                "Hệ thống sẽ hạ cấp về chế độ phân tích văn bản thuần."
            )

    def _unify_math_delimiters(self, raw_text: str) -> str:
        """Đồng bộ hóa đa tiêu chuẩn LaTeX về chuẩn dollars bằng phương pháp Băm Mật mã SHA-256."""
        if not self.enable_math:
            return raw_text

        code_blocks = {}
        block_counter = 0

        def mask_code(match: re.Match) -> str:
            nonlocal block_counter
            block_counter += 1
            code_snippet = match.group(0)

            # Khởi tạo chữ ký băm mật mã SHA-256 từ nội dung khối mã và bộ đếm cục bộ
            hash_input = f"salt_key_{block_counter}_{code_snippet}".encode(
                self.encoding_standard
            )
            hash_signature = hashlib.sha256(hash_input).hexdigest()

            # Mã định danh độc nhất không thể đoán trước (Cryptographic Placeholder)
            placeholder = f"__CRYPTO_MASK_{hash_signature[:16]}_{block_counter}__"
            code_blocks[placeholder] = code_snippet
            return placeholder

        # 1. Dán mặt nạ bảo vệ: Che các khối mã nguồn nhiều dòng (```...```) và nội dòng (`...`)
        masked_text = re.sub(r"(?s)```.*?```", mask_code, raw_text)
        masked_text = re.sub(r"`[^`\n]+`", mask_code, masked_text)

        # 2. Phun sơn đồng bộ: Chuyển đổi cú pháp Brackets sang Dollars vô điều kiện
        masked_text = re.sub(r"(?s)\\\[(.*?)\\\]", r"$$\1$$", masked_text)
        masked_text = re.sub(r"\\\((.*?)\\\)", r"$\1$", masked_text)

        # 3. Lột mặt nạ: Trả lại nguyên trạng các khối mã nguồn đã được bảo vệ
        for placeholder, original_code in code_blocks.items():
            masked_text = masked_text.replace(placeholder, original_code)

        return masked_text

    def parse_markdown_file(self, file_path: Path) -> list:
        """Đọc tệp Markdown theo chuẩn UTF-8 và phân rã thành danh sách các Nút AST (Tokens)."""
        if not file_path.exists():
            raise FileNotFoundError(
                f"[LỖI_I/O] Không tìm thấy tệp đầu vào tại: {file_path}"
            )

        try:
            with open(file_path, "r", encoding=self.encoding_standard) as file_stream:
                raw_text = file_stream.read()

            # Bật màng lọc tiền xử lý toán học trước khi đẩy vào máy phân tích AST
            unified_text = self._unify_math_delimiters(raw_text)
            tokens = self.md_engine.parse(unified_text)

            return tokens
        except UnicodeDecodeError as error:
            raise UnicodeDecodeError(
                error.encoding,
                error.object,
                error.start,
                error.end,
                f"[LỖI_MÃ_HÓA] Không thể đọc tệp bằng chuẩn {self.encoding_standard}: {error}",
            )
