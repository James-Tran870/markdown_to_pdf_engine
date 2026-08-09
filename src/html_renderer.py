# ==============================================================================
# BỘ KẾT XUẤT HTML VÀ ĐÚC ĐỒ HỌA MATHML (HTML RENDERER MODULE)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.3.0 - Tích hợp Bảng GFM & MathML)
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
    """Chuyển đổi chuỗi văn bản tiếng Việt có dấu thành dạng Slug ASCII chuẩn hóa."""
    normalized_text = text.replace("đ", "d").replace("Đ", "D")
    unicode_decomp = unicodedata.normalize("NFD", normalized_text)
    ascii_bytes = unicode_decomp.encode("ascii", "ignore")
    ascii_text = ascii_bytes.decode("utf-8")
    clean_text = re.sub(r"[^\w\s-]", "", ascii_text.lower()).strip()
    clean_id = re.sub(r"[-\s]+", "-", clean_text)
    return clean_id


class HTMLRenderer:
    """Bộ chuyển đổi AST sang HTML ngữ nghĩa tích hợp Pygments, Bảng GFM và MathML."""

    def __init__(
        self,
        theme_name: str = "monokai",
        max_bookmark_level: int = 4,
        enable_math: bool = True,
        fallback_to_raw: bool = True,
        table_config: dict | None = None,
    ):
        """Khởi tạo bộ kết xuất HTML với cấu hình giao diện, mỏ neo, bảng GFM và toán học."""
        self.theme_name = theme_name
        self.max_bookmark_level = max_bookmark_level
        self.enable_math = enable_math
        self.fallback_to_raw = fallback_to_raw
        self.table_config = table_config or {}

        # MỞ RỘNG v1.3.0: Chuyển đổi động cơ HTML sang gfm-like nếu cờ enable_gfm_tables bật
        enable_tables = self.table_config.get("enable_gfm_tables", True)
        if enable_tables:
            self.md_engine = MarkdownIt("gfm-like")
        else:
            self.md_engine = MarkdownIt("commonmark")

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
            lexer = get_lexer_by_name("text")

        formatter = HtmlFormatter(style=self.theme_name, noclasses=False)
        return highlight(code_content, lexer, formatter)

    def _render_heading_anchors(self, tokens, idx, options, env):
        """Gắn thuộc tính id chuẩn hóa ASCII vào các thẻ tiêu đề để tạo mỏ neo."""
        token = tokens[idx]
        if token.nesting == 1:
            level = int(token.tag[1])
            title_text = tokens[idx + 1].content if (idx + 1) < len(tokens) else ""
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
        self.md_engine.add_render_rule("math_inline", self._render_math_inline)
        self.md_engine.add_render_rule("math_block", self._render_math_block)

    def convert_to_html(self, markdown_text: str) -> tuple[str, str]:
        """Thực thi chuyển đổi Markdown thành chuỗi HTML và StyleSheet CSS."""
        formatter = HtmlFormatter(style=self.theme_name)
        pygments_css = formatter.get_style_defs(".highlight")
        rendered_html = self.md_engine.render(markdown_text)
        return pygments_css, rendered_html
