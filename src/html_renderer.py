# ==============================================================================
# TỆP: src/html_renderer.py (BỘ KẾT XUẤT HTML & INLINE ASSETS EMBEDDING v1.6.1)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Inline Asset Embedding, Dynamic Flag Interpolation & UP012 Optimized
# ==============================================================================

import hashlib
import re
import unicodedata
from pathlib import Path

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
    
    # KHẮC PHỤC RUFF UP012: Sử dụng .decode() mặc định thay vì .decode("utf-8")
    ascii_text = ascii_bytes.decode()
    
    clean_text = re.sub(r"[^\w\s-]", "", ascii_text.lower()).strip()
    clean_id = re.sub(r"[-\s]+", "-", clean_text)
    return clean_id


class HTMLRenderer:
    """Bộ chuyển đổi AST sang HTML ngữ nghĩa tích hợp Pygments, Bảng GFM và KaTeX Client-side Engine."""

    def __init__(
        self,
        theme_name: str = "monokai",
        max_bookmark_level: int = 6,
        enable_heading_anchors: bool = True,
        normalize_anchor_ascii: bool = True,
        enable_math: bool = True,
        fallback_to_raw: bool = True,
        table_config: dict | None = None,
        math_syntax_delimiters: list | None = None,
        katex_config: dict | None = None,
    ):
        """Khởi tạo bộ kết xuất HTML hỗ trợ giải nén DTO động từ AppConfig."""
        self.theme_name = theme_name
        self.max_bookmark_level = max_bookmark_level
        self.enable_heading_anchors = enable_heading_anchors
        self.normalize_anchor_ascii = normalize_anchor_ascii
        self.enable_math = enable_math
        self.fallback_to_raw = fallback_to_raw
        self.table_config = table_config or {}
        self.math_syntax_delimiters = math_syntax_delimiters or ["dollars", "brackets"]
        self.katex_config = katex_config or {
            "enable_katex": True,
            "assets_dir": "assets/katex",
            "css_filename": "katex.min.css",
            "js_filename": "katex.min.js",
            "auto_render_js_filename": "auto-render.min.js",
            "strict_mode": False,
            "throw_on_error": False,
        }

        enable_tables = self.table_config.get("enable_gfm_tables", True)
        if enable_tables:
            self.md_engine = MarkdownIt("gfm-like")
        else:
            self.md_engine = MarkdownIt("commonmark")

        if self.enable_math:
            self._register_math_plugin()

        self._register_custom_rules()

    def _register_math_plugin(self) -> None:
        """Đăng ký plugin texmath chuyên biệt cấu hình chuẩn mặc định."""
        try:
            from mdit_py_plugins.texmath import texmath_plugin

            self.md_engine.use(texmath_plugin)
        except ImportError as error:
            print(
                f"[CẢNH_BÁO_HTML] Không thể nạp 'mdit_py_plugins.texmath': {error}. "
                "Hệ thống sẽ hạ cấp về chế độ render văn bản thuần."
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

            # KHẮC PHỤC RUFF UP012: Lược bỏ đối số "utf-8" thừa thãi, tận dụng luồng mã hóa C nội tại
            hash_input = f"salt_key_{block_counter}_{code_snippet}".encode()
            hash_signature = hashlib.sha256(hash_input).hexdigest()

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
        """Gắn thuộc tính id chuẩn hóa ASCII và data-level vào các thẻ tiêu đề để tạo mỏ neo."""
        token = tokens[idx]
        if token.nesting == 1:
            level = int(token.tag[1])
            title_text = tokens[idx + 1].content if (idx + 1) < len(tokens) else ""
            
            if self.enable_heading_anchors:
                if self.normalize_anchor_ascii:
                    clean_id = _slugify_text(title_text)
                else:
                    clean_id = title_text.strip().replace(" ", "-")
                return f'<{token.tag} id="{clean_id}" data-level="{level}">'
            return f'<{token.tag} data-level="{level}">'
        return f"</{token.tag}>\n"

    def _render_math_inline(self, tokens, idx, options, env):
        """Đóng gói Nút toán nội dòng vào thẻ HTML ngữ nghĩa dành cho KaTeX Auto-Render."""
        token = tokens[idx]
        latex_content = token.content.strip()

        if not self.enable_math:
            return f'<span class="math-raw">{latex_content}</span>'

        return f'<span class="math-tex">${latex_content}$</span>'

    def _render_math_block(self, tokens, idx, options, env):
        """Đóng gói Nút toán khối vào thẻ HTML ngữ nghĩa dành cho KaTeX Auto-Render."""
        token = tokens[idx]
        latex_content = token.content.strip()

        if not self.enable_math:
            return f'<div class="math-raw">{latex_content}</div>\n'

        return f'<div class="math-tex">$$\n{latex_content}\n$$</div>\n'

    def _generate_katex_assets_and_script(self) -> str:
        """Đóng gói Nhúng Trực tiếp (Inline Embedding) CSS/JS KaTeX và Nội suy Cờ Logic động."""
        if not self.enable_math or not self.katex_config.get("enable_katex", True):
            return ""

        assets_dir = Path(
            self.katex_config.get("assets_dir", "assets/katex")
        ).resolve()
        
        css_file = assets_dir / self.katex_config.get("css_filename", "katex.min.css")
        js_file = assets_dir / self.katex_config.get("js_filename", "katex.min.js")
        auto_render_file = assets_dir / self.katex_config.get(
            "auto_render_js_filename", "auto-render.min.js"
        )

        # Đọc trực tiếp nội dung thô của các tệp tĩnh dưới dạng chuỗi UTF-8
        css_content = css_file.read_text(encoding="utf-8") if css_file.exists() else ""
        js_content = js_file.read_text(encoding="utf-8") if js_file.exists() else ""
        auto_render_content = (
            auto_render_file.read_text(encoding="utf-8") if auto_render_file.exists() else ""
        )

        # Trích xuất biến boolean động và chuyển thành chuỗi JavaScript hợp lệ
        strict_mode_str = str(self.katex_config.get("strict_mode", False)).lower()
        throw_on_error_str = str(self.katex_config.get("throw_on_error", False)).lower()

        return f"""
        <!-- KHỐI TÀI NGUYÊN KATEX OFFLINE BỌC TRỰC TIẾP NỘI TUYẾN (INLINE EMBEDDING v1.6.0) -->
        <style>
        {css_content}
        </style>
        <script>
        {js_content}
        </script>
        <script>
        {auto_render_content}
        </script>
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                if (typeof renderMathInElement === "function") {{
                    renderMathInElement(document.body, {{
                        delimiters: [
                            {{left: '$$', right: '$$', display: true}},
                            {{left: '$', right: '$', display: false}},
                            {{left: '\\\\[', right: '\\\\]', display: true}},
                            {{left: '\\\\(', right: '\\\\)', display: false}}
                        ],
                        strict: {strict_mode_str},
                        throwOnError: {throw_on_error_str},
                        trust: true
                    }});
                }}
            }});
        </script>
        """

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

        # 1. Bật màng lọc tiền xử lý toán học trước khi chuyển đổi giao diện đồ họa HTML
        unified_text = self._unify_math_delimiters(markdown_text)
        rendered_html = self.md_engine.render(unified_text)

        # 2. Tiêm khối tài nguyên nhúng trực tiếp và script kích hoạt KaTeX Offline vào cuối tệp HTML
        katex_script_block = self._generate_katex_assets_and_script()
        final_html = f"{rendered_html}\n{katex_script_block}"

        return pygments_css, final_html
