# ==============================================================================
# BỘ KẾT XUẤT HTML VÀ ĐÚC ĐỒ HỌA MATHML (HTML RENDERER MODULE)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.2.0 - Tích hợp MathML)
# Kiến trúc: Defensive Programming & Separation of Concerns (SoC)
# ==============================================================================

import re
import unicodedata

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound


def _slugify_text(text: str) -> str:
    """Chuyển đổi chuỗi văn bản tiếng Việt có dấu thành dạng Slug ASCII chuẩn hóa.

    Ví dụ: 'Tiêu đề Hợp lệ Cấp 1' -> 'tieu-de-hop-le-cap-1'
    """
    # 1. Chuyển đổi chữ đ/Đ thành d/D thủ công do unicodedata NFD không tách chữ đ
    normalized_text = text.replace("đ", "d").replace("Đ", "D")

    # 2. Tách các ký tự dấu ra khỏi chữ cái gốc (Chuyển sang dạng NFD)
    unicode_decomp = unicodedata.normalize("NFD", normalized_text)

    # 3. Lọc bỏ toàn bộ các ký tự dấu tổ hợp (Combining Diacritical Marks)
    ascii_bytes = unicode_decomp.encode("ascii", "ignore")
    ascii_text = ascii_bytes.decode("utf-8")

    # 4. Chuyển về chữ thường, loại bỏ ký tự đặc biệt và thay khoảng trắng bằng dấu gạch ngang
    clean_text = re.sub(r"[^\w\s-]", "", ascii_text.lower()).strip()
    clean_id = re.sub(r"[-\s]+", "-", clean_text)
    return clean_id


class HTMLRenderer:
    """Bộ chuyển đổi AST sang HTML ngữ nghĩa tích hợp Pygments, Mỏ neo và Động cơ MathML."""

    def __init__(
        self,
        theme_name: str = "monokai",
        max_bookmark_level: int = 4,
        enable_math: bool = True,
        fallback_to_raw: bool = True,
    ):
        """Khởi tạo bộ kết xuất HTML với cấu hình giao diện, mỏ neo và van điều khiển toán học.

        Args:
            theme_name (str): Chủ đề màu Pygments dùng cho khối mã nguồn.
            max_bookmark_level (int): Độ sâu phân cấp tiêu đề được gắn mỏ neo.
            enable_math (bool): Cờ bật/tắt tính năng biên dịch toán học sang MathML.
            fallback_to_raw (bool): Cờ hạ cấp an toàn khi công thức LaTeX bị lỗi cú pháp.
        """
        self.theme_name = theme_name
        self.max_bookmark_level = max_bookmark_level
        self.enable_math = enable_math
        self.fallback_to_raw = fallback_to_raw

        self.md_engine = MarkdownIt("commonmark")

        # Nạp plugin texmath cho động cơ HTML nếu cờ toán học bật
        if self.enable_math:
            self._register_math_plugin()

        self._register_custom_rules()

    def _register_math_plugin(self) -> None:
        """Đăng ký plugin texmath để động cơ HTML nhận diện ranh giới dấu $ và $$."""
        try:
            from mdit_py_plugins.texmath import texmath_plugin

            self.md_engine.use(texmath_plugin, macros={"delimiters": "dollars"})
        except ImportError as error:
            print(
                f"[CẢNH_BÁO_HTML] Không thể nạp 'mdit_py_plugins.texmath': {error}. "
                "Hệ thống sẽ hạ cấp về chế độ render văn bản thuần."
            )

    def _render_code_fence(self, tokens, idx, options, env):
        """Cô lập khối mã 'fence', ngăn chặn rò rỉ ký tự < và >."""
        token = tokens[idx]
        code_content = token.content
        language = token.info.strip() if token.info else ""

        try:
            lexer = (
                get_lexer_by_name(language)
                if language
                else guess_lexer(code_content)
            )
        except (ClassNotFound, ValueError):
            # Nếu không nhận diện được ngôn ngữ, chuyển về định dạng văn bản thuần
            lexer = get_lexer_by_name("text")

        formatter = HtmlFormatter(style=self.theme_name, noclasses=False)
        # Pygments tự động chuyển đổi các ký tự đặc biệt thành thẻ HTML an toàn
        return highlight(code_content, lexer, formatter)

    def _render_heading_anchors(self, tokens, idx, options, env):
        """Gắn thuộc tính id chuẩn hóa ASCII vào các thẻ tiêu đề để tạo mỏ neo."""
        token = tokens[idx]
        if token.nesting == 1:
            level = int(token.tag[1])
            # Trích xuất nội dung văn bản của tiêu đề
            title_text = tokens[idx + 1].content if (idx + 1) < len(tokens) else ""
            # Chuẩn hóa ID: chuyển tiếng Việt có dấu thành ASCII không dấu chuẩn SEO/HTML
            clean_id = _slugify_text(title_text)
            return f'<{token.tag} id="{clean_id}" data-level="{level}">'
        return f"</{token.tag}>\n"

    def _render_math_inline(self, tokens, idx, options, env):
        """Biên dịch Nút toán nội dòng ($...$) thành mã HTML MathML ngoại tuyến."""
        token = tokens[idx]
        latex_content = token.content.strip()

        if not self.enable_math:
            return f'<span class="math-raw">${latex_content}$</span>'

        try:
            from latex2mathml.converter import convert

            mathml_code = convert(latex_content)
            return f'<span class="math-inline">{mathml_code}</span>'
        except Exception as error:
            if self.fallback_to_raw:
                print(
                    f"[CẢNH_BÁO_MATH] Lỗi biên dịch LaTeX nội dòng '${latex_content}': {error}. "
                    "Chuyển hướng hạ cấp về văn bản thô."
                )
                return f'<span class="math-error">${latex_content}$</span>'
            raise

    def _render_math_block(self, tokens, idx, options, env):
        """Biên dịch Nút toán khối ($$...$$) thành mã HTML MathML ngoại tuyến."""
        token = tokens[idx]
        latex_content = token.content.strip()

        if not self.enable_math:
            return f'<div class="math-raw">$${latex_content}$$</div>\n'

        try:
            from latex2mathml.converter import convert

            mathml_code = convert(latex_content)
            return f'<div class="math-block">\n{mathml_code}\n</div>\n'
        except Exception as error:
            if self.fallback_to_raw:
                print(
                    f"[CẢNH_BÁO_MATH] Lỗi biên dịch LaTeX khối '$${latex_content}$$': {error}. "
                    "Chuyển hướng hạ cấp về văn bản thô."
                )
                return f'<div class="math-error">$${latex_content}$$</div>\n'
            raise

    def _register_custom_rules(self):
        """Ghi đè và bổ sung các quy tắc render tùy chỉnh vào markdown-it-py."""
        self.md_engine.add_render_rule("fence", self._render_code_fence)
        self.md_engine.add_render_rule("heading_open", self._render_heading_anchors)
        self.md_engine.add_render_rule("heading_close", self._render_heading_anchors)

        # Đăng ký hai quy tắc xử lý Nút Toán Học từ plugin texmath
        self.md_engine.add_render_rule("math_inline", self._render_math_inline)
        self.md_engine.add_render_rule("math_block", self._render_math_block)

    def convert_to_html(self, markdown_text: str) -> tuple[str, str]:
        """Thực thi chuyển đổi Markdown thành chuỗi HTML và StyleSheet CSS."""
        formatter = HtmlFormatter(style=self.theme_name)
        pygments_css = formatter.get_style_defs(".highlight")
        rendered_html = self.md_engine.render(markdown_text)
        return pygments_css, rendered_html