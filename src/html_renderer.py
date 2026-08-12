# ==============================================================================
# TỆP: src/html_renderer.py (BỘ KẾT XUẤT HTML & HYBRID MATH ENGINE v2.3.0)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Python Dictionary Mapping (KaTeX) & Vector SVG Environment (MathJax v3)
# ==============================================================================

import base64
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

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
    ascii_text = ascii_bytes.decode()
    clean_text = re.sub(r"[^\w\s-]", "", ascii_text.lower()).strip()
    clean_id = re.sub(r"[-\s]+", "-", clean_text)
    return clean_id


class HTMLRenderer:
    """Bộ chuyển đổi AST sang HTML ngữ nghĩa hỗ trợ Kiến trúc Lai KaTeX & MathJax v3."""

    def __init__(
        self,
        theme_name: str = "monokai",
        max_bookmark_level: int = 6,
        enable_heading_anchors: bool = True,
        normalize_anchor_ascii: bool = True,
        enable_math: bool = True,
        fallback_to_raw: bool = True,
        table_config: dict[str, Any] | None = None,
        math_syntax_delimiters: list[str] | None = None,
        katex_config: dict[str, Any] | None = None,
        math_routing_config: dict[str, Any] | None = None,
        mathjax_config: dict[str, Any] | None = None,
        encoding_standard: str = "utf-8",
    ) -> None:
        """Khởi tạo cấu hình HTMLRenderer và nạp các tùy chọn Routing, KaTeX, MathJax và Pygments."""
        self.theme_name = theme_name
        self.max_bookmark_level = max_bookmark_level
        self.enable_heading_anchors = enable_heading_anchors
        self.normalize_anchor_ascii = normalize_anchor_ascii
        self.enable_math = enable_math
        self.fallback_to_raw = fallback_to_raw
        self.table_config = table_config or {}
        self.math_syntax_delimiters = math_syntax_delimiters or ["dollars", "brackets"]
        self.encoding_standard = encoding_standard

        # Nạp DTO Cấu hình Rẽ nhánh Động cơ Toán học (v2.3.0)
        self.math_routing_config = math_routing_config or {"active_engine": "katex_placeholder"}
        self.active_engine = self.math_routing_config.get("active_engine", "katex_placeholder").lower()

        # Nạp DTO Cấu hình KaTeX Offline
        self.katex_config = katex_config or {
            "enable_katex": True,
            "assets_dir": "assets/katex",
            "css_filename": "katex.min.css",
            "js_filename": "katex.min.js",
            "auto_render_js_filename": "auto-render.min.js",
            "strict_mode": False,
            "throw_on_error": False,
            "enable_base64_math_encoding": True,
            "enable_vietnamese_math_isolation": True,
            "vietnamese_font_family": '"Times New Roman", "Segoe UI", Arial, sans-serif',
            "enable_base64_font_embedding": True,
            "hybrid_typography_fallback": '"Cambria Math", "Times New Roman", serif',
            "delimiters": [
                {"left": "$$", "right": "$$", "display": True},
                {"left": "$", "right": "$", "display": False},
                {"left": "\\[", "right": "\\]", "display": True},
                {"left": "\\(", "right": "\\)", "display": False},
            ],
        }

        # Nạp DTO Cấu hình MathJax v3 Offline
        self.mathjax_config = mathjax_config or {
            "enable_mathjax": True,
            "assets_dir": "assets/mathjax",
            "js_filename": "tex-svg.js",
            "font_cache": "global",
            "scale": 1.0,
            "inline_math_delimiters": [["$", "$"], ["\\(", "\\)"]],
            "display_math_delimiters": [["$$", "$$"], ["\\[", "\\]"]],
        }

        # Kho lưu trữ bảng băm ánh xạ văn bản Tiếng Việt trong công thức (Server-side Dictionary)
        self.vn_math_store: dict[str, str] = {}
        self._vn_mask_counter: int = 0

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
            print(f"[CẢNH_BÁO_HTML] Không thể nạp 'mdit_py_plugins.texmath': {error}")

    def _isolate_vietnamese_in_math(self, latex_text: str) -> str:
        """Thuật toán Server-Side Python Dictionary Mapping: Bóc tách văn bản Tiếng Việt sang mã ASCII giữ chỗ."""
        if not self.katex_config.get("enable_vietnamese_math_isolation", True):
            return latex_text

        vietnamese_char_pattern = re.compile(
            r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]"
        )

        def replace_with_ascii_mask(match: re.Match[str]) -> str:
            cmd = match.group(1)
            content = match.group(2)
            if vietnamese_char_pattern.search(content):
                self._vn_mask_counter += 1
                mask_key = f"VILANGMASK{self._vn_mask_counter:04d}"
                self.vn_math_store[mask_key] = content
                return f"\\{cmd}{{{mask_key}}}"
            return match.group(0)

        pattern = re.compile(r"\\(text|textbf|textit|textmd|textsf|mathtt)\{([^}]+)\}")
        isolated_latex = pattern.sub(replace_with_ascii_mask, latex_text)
        return isolated_latex

    def _unify_math_delimiters(self, raw_text: str) -> str:
        """Đồng bộ hóa đa tiêu chuẩn LaTeX về chuẩn dollars bằng phương pháp Băm Mật mã SHA-256."""
        if not self.enable_math:
            return raw_text

        normalized_raw_text = unicodedata.normalize("NFC", raw_text)

        code_blocks: dict[str, str] = {}
        block_counter = 0

        def mask_code(match: re.Match[str]) -> str:
            nonlocal block_counter
            block_counter += 1
            code_snippet = match.group(0)

            hash_input = f"salt_key_{block_counter}_{code_snippet}".encode(self.encoding_standard)
            hash_signature = hashlib.sha256(hash_input).hexdigest()

            placeholder = f"__CRYPTO_MASK_{hash_signature[:16]}_{block_counter}__"
            code_blocks[placeholder] = code_snippet
            return placeholder

        masked_text = re.sub(r"(?s)\`\`\`.*?\`\`\`", mask_code, normalized_raw_text)
        masked_text = re.sub(r"\`[^\`\n]+\`", mask_code, masked_text)

        masked_text = re.sub(r"(?s)\\\[(.*?)\\\]", r"$$\1$$", masked_text)
        masked_text = re.sub(r"\\\((.*?)\\\)", r"$\1$", masked_text)

        for placeholder, original_code in code_blocks.items():
            masked_text = masked_text.replace(placeholder, original_code)

        return masked_text

    def _render_code_fence(self, tokens: list[Any], idx: int, options: dict[str, Any], env: dict[str, Any]) -> str:
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

    def _render_heading_anchors(self, tokens: list[Any], idx: int, options: dict[str, Any], env: dict[str, Any]) -> str:
        """Gắn thuộc tính id chuẩn hóa ASCII và data-level vào các thẻ tiêu đề để tạo mỏ neo."""
        token = tokens[idx]
        if token.nesting == 1:
            level = int(token.tag[1])

            text_fragments = []
            curr_idx = idx + 1
            while curr_idx < len(tokens) and tokens[curr_idx].type != "heading_close":
                if tokens[curr_idx].content:
                    text_fragments.append(tokens[curr_idx].content)
                curr_idx += 1
            title_text = " ".join(text_fragments).strip()

            if self.enable_heading_anchors:
                if self.normalize_anchor_ascii:
                    clean_id = _slugify_text(title_text)
                else:
                    clean_id = title_text.strip().replace(" ", "-")
                return f'<{token.tag} id="{clean_id}" data-level="{level}">'
            return f'<{token.tag} data-level="{level}">'
        return f"</{token.tag}>\n"

    def _render_math_inline(self, tokens: list[Any], idx: int, options: dict[str, Any], env: dict[str, Any]) -> str:
        """Đóng gói Nút toán nội dòng, giải mã Base64, tiêm giáp Tiếng Việt và mã hóa thực thể HTML."""
        token = tokens[idx]
        raw_content = token.content.strip()

        if not self.enable_math:
            return f'<span class="math-raw">{raw_content}</span>'

        b64_match = re.search(r'data-math-b64="([^"]+)"', raw_content)
        if b64_match:
            try:
                decoded_bytes = base64.b64decode(b64_match.group(1))
                latex_content = decoded_bytes.decode(self.encoding_standard)
            except (ValueError, UnicodeDecodeError):
                latex_content = raw_content
        else:
            latex_content = raw_content

        if self.active_engine == "katex_placeholder":
            latex_content = self._isolate_vietnamese_in_math(latex_content)

        latex_content = unicodedata.normalize("NFC", latex_content)
        latex_content = latex_content.replace("<", "&lt;").replace(">", "&gt;")

        return f'<span class="math-tex">${latex_content}$</span>'

    def _render_math_block(self, tokens: list[Any], idx: int, options: dict[str, Any], env: dict[str, Any]) -> str:
        """Đóng gói Nút toán khối, giải mã Base64, tiêm giáp Tiếng Việt và mã hóa thực thể HTML."""
        token = tokens[idx]
        raw_content = token.content.strip()

        if not self.enable_math:
            return f'<div class="math-raw">{raw_content}</div>\n'

        b64_match = re.search(r'data-math-b64="([^"]+)"', raw_content)
        if b64_match:
            try:
                decoded_bytes = base64.b64decode(b64_match.group(1))
                latex_content = decoded_bytes.decode(self.encoding_standard)
            except (ValueError, UnicodeDecodeError):
                latex_content = raw_content
        else:
            latex_content = raw_content

        if self.active_engine == "katex_placeholder":
            latex_content = self._isolate_vietnamese_in_math(latex_content)

        latex_content = unicodedata.normalize("NFC", latex_content)
        latex_content = latex_content.replace("<", "&lt;").replace(">", "&gt;")

        return f'<div class="math-tex">$$\n{latex_content}\n$$</div>\n'

    def _generate_katex_assets_and_script(self) -> str:
        """Đóng gói KaTeX Offline với Thuật toán Python Dictionary Mapping & Client-Side Swap (v2.3.0)."""
        if not self.enable_math or not self.katex_config.get("enable_katex", True):
            return ""

        assets_dir = Path(self.katex_config.get("assets_dir", "assets/katex")).resolve()

        css_file = assets_dir / self.katex_config.get("css_filename", "katex.min.css")
        js_file = assets_dir / self.katex_config.get("js_filename", "katex.min.js")
        auto_render_file = assets_dir / self.katex_config.get("auto_render_js_filename", "auto-render.min.js")

        css_content = css_file.read_text(encoding=self.encoding_standard) if css_file.exists() else ""
        js_content = js_file.read_text(encoding=self.encoding_standard) if js_file.exists() else ""
        auto_render_content = auto_render_file.read_text(encoding=self.encoding_standard) if auto_render_file.exists() else ""

        base64_fonts_css = ""
        enable_font_embed = self.katex_config.get("enable_base64_font_embedding", True)

        if enable_font_embed:
            fonts_dir = assets_dir / "fonts"
            if fonts_dir.exists() and fonts_dir.is_dir():
                font_css_rules = []
                for font_path in fonts_dir.glob("*.woff2"):
                    try:
                        font_bytes = font_path.read_bytes()
                        b64_str = base64.b64encode(font_bytes).decode("ascii")
                        font_name = font_path.stem

                        family, variant = font_name.split("-", 1) if "-" in font_name else (font_name, "Regular")
                        font_style = "italic" if "Italic" in variant else "normal"
                        font_weight = "bold" if "Bold" in variant else "normal"

                        rule = (
                            f"@font-face {{\n"
                            f"  font-family: '{family}';\n"
                            f"  font-style: {font_style};\n"
                            f"  font-weight: {font_weight};\n"
                            f"  src: url('data:font/woff2;charset=utf-8;base64,{b64_str}') format('woff2');\n"
                            f"}}\n"
                        )
                        font_css_rules.append(rule)
                    except OSError:
                        pass

                base64_fonts_css = "\n".join(font_css_rules)

        strict_mode_str = str(self.katex_config.get("strict_mode", False)).lower()
        throw_on_error_str = str(self.katex_config.get("throw_on_error", False)).lower()

        raw_delimiters = self.katex_config.get("delimiters", [])
        if not raw_delimiters:
            raw_delimiters = [
                {"left": "$$", "right": "$$", "display": True},
                {"left": "$", "right": "$", "display": False},
                {"left": "\\[", "right": "\\]", "display": True},
                {"left": "\\(", "right": "\\)", "display": False},
            ]
        delimiters_json_str = json.dumps(raw_delimiters)

        # Chuyển đổi từ điển Python mapping sang JSON client-side
        vn_map_json_str = json.dumps(self.vn_math_store, ensure_ascii=False)

        # [LỚP GIÁP CLIENT-SIDE SWAP v2.3.0]: KaTeX đúc ASCII -> JS hoán đổi trả lại Tiếng Việt nguyên khối
        swap_script = f"""
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                if (typeof renderMathInElement === "function") {{
                    var vnMap = {vn_map_json_str};

                    // Bước 1: Cho KaTeX đúc DOM toán học với các chuỗi ASCII giữ chỗ
                    renderMathInElement(document.body, {{
                        delimiters: {delimiters_json_str},
                        strict: {strict_mode_str},
                        throwOnError: {throw_on_error_str},
                        trust: true
                    }});

                    // Bước 2: Quét lại DOM KaTeX thành phẩm và hoán đổi trả lại văn bản Tiếng Việt nguyên bản
                    if (Object.keys(vnMap).length > 0) {{
                        var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                        var node;
                        while (walker.nextNode()) {{
                            node = walker.currentNode;
                            if (node.nodeValue) {{
                                for (var maskKey in vnMap) {{
                                    if (node.nodeValue.indexOf(maskKey) !== -1) {{
                                        node.nodeValue = node.nodeValue.replace(maskKey, vnMap[maskKey]);
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        </script>
        """

        return f"""
        <!-- KHỐI TÀI NGUYÊN KATEX OFFLINE & PYTHON DICTIONARY SWAP (v2.3.0) -->
        <style>
        {base64_fonts_css}
        {css_content}
        </style>
        <script>
        {js_content}
        </script>
        <script>
        {auto_render_content}
        </script>
        {swap_script}
        """

    def _generate_mathjax_assets_and_script(self) -> str:
        """Đóng gói Động cơ MathJax v3 Vector SVG Offline (v2.3.0)."""
        if not self.enable_math or not self.mathjax_config.get("enable_mathjax", True):
            return ""

        assets_dir = Path(self.mathjax_config.get("assets_dir", "assets/mathjax")).resolve()
        js_file = assets_dir / self.mathjax_config.get("js_filename", "tex-svg.js")

        js_content = js_file.read_text(encoding=self.encoding_standard) if js_file.exists() else ""

        font_cache = self.mathjax_config.get("font_cache", "global")
        scale = self.mathjax_config.get("scale", 1.0)
        inline_delims = json.dumps(self.mathjax_config.get("inline_math_delimiters", [["$", "$"], ["\\(", "\\)"]]))
        display_delims = json.dumps(self.mathjax_config.get("display_math_delimiters", [["$$", "$$"], ["\\[", "\\]"]]))

        mathjax_config_script = f"""
        <script>
            window.MathJax = {{
                tex: {{
                    inlineMath: {inline_delims},
                    displayMath: {display_delims},
                    processEscapes: true
                }},
                svg: {{
                    fontCache: '{font_cache}',
                    scale: {scale}
                }}
            }};
        </script>
        """

        if js_content:
            mathjax_engine_script = f"<script>{js_content}</script>"
        else:
            # Fallback nếu chưa tải tệp local tex-svg.js
            mathjax_engine_script = f'<script id="MathJax-script" async src="file:///{js_file.as_posix()}"></script>'

        return f"""
        <!-- KHỐI TÀI NGUYÊN MATHJAX V3 VECTOR SVG OFFLINE (v2.3.0) -->
        {mathjax_config_script}
        {mathjax_engine_script}
        """

    def _generate_math_assets_and_script(self) -> str:
        """Định tuyến tiêm Script tương ứng với active_engine được cấu hình (v2.3.0)."""
        if self.active_engine == "mathjax_svg":
            return self._generate_mathjax_assets_and_script()
        return self._generate_katex_assets_and_script()

    def _register_custom_rules(self) -> None:
        """Ghi đè và bổ sung các quy tắc render tùy chỉnh vào markdown-it-py."""
        self.md_engine.add_render_rule("fence", self._render_code_fence)
        self.md_engine.add_render_rule("heading_open", self._render_heading_anchors)
        self.md_engine.add_render_rule("heading_close", self._render_heading_anchors)
        self.md_engine.add_render_rule("math_inline", self._render_math_inline)
        self.md_engine.add_render_rule("math_block", self._render_math_block)

    def convert_to_html(self, markdown_text: str) -> tuple[str, str]:
        """Thực thi chuyển đổi Markdown thành chuỗi HTML và StyleSheet CSS."""
        # Reset bộ đếm mask và kho lưu trữ trước mỗi lần render tệp
        self.vn_math_store.clear()
        self._vn_mask_counter = 0

        formatter = HtmlFormatter(style=self.theme_name)
        pygments_css = formatter.get_style_defs(".highlight")

        normalized_markdown = unicodedata.normalize("NFC", markdown_text)
        unified_text = self._unify_math_delimiters(normalized_markdown)
        rendered_html = self.md_engine.render(unified_text)

        def decode_b64_html_placeholders(match: re.Match[str]) -> str:
            b64_str = match.group(1)
            is_block = match.group(0).startswith("<div")
            try:
                decoded_latex = base64.b64decode(b64_str).decode(self.encoding_standard)
                if self.active_engine == "katex_placeholder":
                    decoded_latex = self._isolate_vietnamese_in_math(decoded_latex)
                decoded_latex = decoded_latex.replace("<", "&lt;").replace(">", "&gt;")
                if is_block:
                    return f'<div class="math-tex">$$\n{decoded_latex}\n$$</div>\n'
                return f'<span class="math-tex">${decoded_latex}$</span>'
            except (ValueError, UnicodeDecodeError):
                return match.group(0)

        rendered_html = re.sub(
            r'<(?:div|span) class="math-tex-b64" data-math-b64="([^"]+)"></(?:div|span)>',
            decode_b64_html_placeholders,
            rendered_html,
        )

        math_script_block = self._generate_math_assets_and_script()
        final_html = f"{rendered_html}\n{math_script_block}"

        return pygments_css, final_html
