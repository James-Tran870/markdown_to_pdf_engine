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
    """Bộ chuyển đổi AST sang HTML ngữ nghĩa tích hợp Pygments và Mỏ neo chuẩn hóa."""

    def __init__(self, theme_name: str = "monokai", max_bookmark_level: int = 4):
        self.theme_name = theme_name
        self.max_bookmark_level = max_bookmark_level
        self.md_engine = MarkdownIt("commonmark")
        self._register_custom_rules()

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

    def _register_custom_rules(self):
        """Ghi đè quy tắc render mặc định của markdown-it-py."""
        self.md_engine.add_render_rule("fence", self._render_code_fence)
        self.md_engine.add_render_rule("heading_open", self._render_heading_anchors)
        self.md_engine.add_render_rule("heading_close", self._render_heading_anchors)

    def convert_to_html(self, markdown_text: str) -> tuple[str, str]:
        """Thực thi chuyển đổi Markdown thành chuỗi HTML và StyleSheet CSS."""
        formatter = HtmlFormatter(style=self.theme_name)
        pygments_css = formatter.get_style_defs(".highlight")
        rendered_html = self.md_engine.render(markdown_text)
        return pygments_css, rendered_html