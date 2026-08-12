# ==============================================================================
# TỆP: src/ast_parser.py (BỘ PHÂN TÍCH CÂY CÚ PHÁP TRỪU TƯỢNG AST v2.2.0)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Base64 Math AST Isolation, SHA-256 Code Masking & NFC Normalization
# ==============================================================================

import base64
import hashlib
import re
import unicodedata
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin


class ASTParser:
    """Động cơ phân tích cú pháp Markdown sang Cây AST với màng lọc Base64 cô lập toán học."""

    def __init__(
        self,
        encoding_standard: str = "utf-8",
        enable_math: bool = True,
        enable_tables: bool = True,
        enable_base64_math: bool = True,
    ) -> None:
        """Khởi tạo cấu hình ASTParser và nạp các Trình cắm (Plugins) mở rộng."""
        self.encoding_standard = encoding_standard
        self.enable_math = enable_math
        self.enable_tables = enable_tables
        self.enable_base64_math = enable_base64_math

        # Khởi tạo động cơ markdown-it-py với cấu hình chuẩn CommonMark/GFM
        self.md_engine = MarkdownIt("commonmark", {"html": True, "xhtml_out": True})

        # Kích hoạt các trình cắm bổ trợ cú pháp
        self.md_engine.use(front_matter_plugin)
        self.md_engine.use(footnote_plugin)
        self.md_engine.use(tasklists_plugin)

        if self.enable_tables:
            self.md_engine.enable("table")

        if self.enable_math and not self.enable_base64_math:
            self._register_math_plugin()

    def _register_math_plugin(self) -> None:
        """Đăng ký plugin texmath để phân rã Nút toán học chuẩn hóa (Dự phòng khi tắt Base64)."""
        try:
            from mdit_py_plugins.texmath import texmath_plugin
            self.md_engine.use(texmath_plugin)
        except ImportError as error:
            print(f"[CẢNH_BÁO_AST] Không thể nạp 'mdit_py_plugins.texmath': {error}")

    def _isolate_and_encode_math_to_base64(self, text_with_masks: str) -> str:
        """Mã hóa toàn bộ khối công thức toán học thô sang dạng chuỗi Base64 an toàn.
        
        Phương thức này quét các biểu thức LaTeX toán học và chuyển đổi chúng thành
        thẻ HTML giữ chỗ mang thuộc tính data-math-b64. Điều này triệt tiêu hoàn toàn
        sự cố markdown-it-py nhận diện nhầm các ký tự '<', '%', '_' trong toán học.
        """
        if not self.enable_math or not self.enable_base64_math:
            return text_with_masks

        # 1. Mã hóa công thức dạng Khối (Block Math: $$...$$)
        def encode_block_math(match: re.Match[str]) -> str:
            latex_raw = match.group(1).strip()
            if not latex_raw:
                return ""
            b64_bytes = base64.b64encode(latex_raw.encode("utf-8"))
            b64_str = b64_bytes.decode("ascii")
            return f'\n<div class="math-tex-b64" data-math-b64="{b64_str}"></div>\n'

        # Pattern khớp khối toán $$...$$
        block_pattern = re.compile(r"\$\$\n?([\s\S]*?)\n?\$\$")
        processed_text = block_pattern.sub(encode_block_math, text_with_masks)

        # 2. Mã hóa công thức dạng Nội dòng (Inline Math: $...$)
        def encode_inline_math(match: re.Match[str]) -> str:
            latex_raw = match.group(1).strip()
            if not latex_raw:
                return ""
            b64_bytes = base64.b64encode(latex_raw.encode("utf-8"))
            b64_str = b64_bytes.decode("ascii")
            return f'<span class="math-tex-b64" data-math-b64="{b64_str}"></span>'

        # Pattern khớp công thức $...$ (sử dụng negative lookbehind/lookahead tránh trùng $$)
        inline_pattern = re.compile(r"(?<!\$)\$([^\$\n]+?)\$(?!\$)")
        processed_text = inline_pattern.sub(encode_inline_math, processed_text)

        return processed_text

    def _unify_math_delimiters(self, raw_text: str) -> str:
        """Đồng bộ ranh giới toán học, cưỡng chế NFC, dán mặt nạ SHA-256 mã nguồn và mã hóa Base64 toán."""
        if not raw_text:
            return ""

        # 1. CƯỠNG CHẾ NFC TOÀN CỤC: Gộp ký tự tiếng Việt dạng NFD tổ hợp về NFC nguyên khối
        normalized_raw_text = unicodedata.normalize("NFC", raw_text)

        # 2. Dán mặt nạ bảo vệ các khối mã nguồn (Code Blocks & Inline Code)
        code_placeholders: dict[str, str] = {}
        counter = 0

        def preserve_code(match: re.Match[str]) -> str:
            nonlocal counter
            counter += 1
            code_snippet = match.group(0)
            hash_input = f"salt_key_{counter}_{code_snippet}".encode(self.encoding_standard)
            hash_sig = hashlib.sha256(hash_input).hexdigest()[:16]
            placeholder = f"___PROTECTED_CODE_BLOCK_{hash_sig}_{counter}___"
            code_placeholders[placeholder] = code_snippet
            return placeholder

        code_pattern = re.compile(r"(```[\s\S]*?```|`[^`\n]+`)")
        protected_text = code_pattern.sub(preserve_code, normalized_raw_text)

        if not self.enable_math:
            # Trả lại mã nguồn nếu toán bị tắt
            for placeholder, original_code in code_placeholders.items():
                protected_text = protected_text.replace(placeholder, original_code)
            return protected_text

        # 3. Chuẩn hóa ranh giới Brackets \[...\] và \(...\) sang Dollars $$...$$ và $...$
        sanitized_text = re.sub(r"(?s)\\\[([\s\S]*?)\\\]", r"$$\1$$", protected_text)
        sanitized_text = re.sub(r"\\\(([\s\S]*?)\\\)", r"$\1$", sanitized_text)

        # 4. THỰC THI KIẾN TRÚC BASE64 MATH ISOLATION
        # Mã hóa toàn bộ toán học sang thẻ HTML Placeholder chứa chuỗi Base64
        isolated_text = self._isolate_and_encode_math_to_base64(sanitized_text)

        # 5. Trả lại nguyên trạng các khối mã nguồn đã bảo vệ
        for placeholder, original_code in code_placeholders.items():
            isolated_text = isolated_text.replace(placeholder, original_code)

        return isolated_text

    def parse_markdown_text(self, raw_markdown_text: str) -> list[Any]:
        """Chuyển đổi chuỗi văn bản Markdown thô thành danh sách các Nút AST Tokens."""
        if not raw_markdown_text:
            return []

        # Chuẩn hóa NFC, dán mặt nạ SHA-256 mã nguồn và cô lập toán học Base64 trước khi phân rã AST
        unified_text = self._unify_math_delimiters(raw_markdown_text)
        tokens = self.md_engine.parse(unified_text)
        return tokens

    def parse_markdown_file(self, file_path: Path) -> list[Any]:
        """Đọc tệp Markdown từ đĩa cứng theo mã hóa chuẩn và chuyển đổi sang AST Tokens."""
        if not file_path.exists():
            raise FileNotFoundError(
                f"[LỖI_AST_PARSER] Tệp nguồn Markdown không tồn tại: {file_path}"
            )

        try:
            with open(file_path, "r", encoding=self.encoding_standard) as stream:
                content = stream.read()
            return self.parse_markdown_text(content)

        except UnicodeDecodeError as error:
            raise UnicodeDecodeError(
                error.encoding,
                error.object,
                error.start,
                error.end,
                f"[LỖI_MÃ_HÓA] Không thể đọc tệp {file_path.name} với chuẩn {self.encoding_standard}.",
            ) from error
