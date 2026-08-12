# ==============================================================================
# TỆP: src/pdf_metadata_injector.py (BỘ TIÊM SIÊU DỮ LIỆU HẬU KỲ v2.2.0)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Deterministic DOM Parsing, TOC Hierarchy Normalizer & PyMuPDF Compliant
# ==============================================================================

from pathlib import Path
from typing import Any

import pymupdf as fitz
from bs4 import BeautifulSoup


class MetadataInjector:
    """Bộ động cơ can thiệp nhị phân, trích xuất cấu trúc Heading qua BeautifulSoup4 và tiêm Bookmarks."""

    def __init__(self, max_bookmark_level: int = 6) -> None:
        """Khởi tạo cấu hình nội suy với giới hạn chiều sâu phân cấp Bookmark (Default: Level 6)."""
        self.max_bookmark_level = max_bookmark_level

    def _extract_headings_from_html(self, html_content: str) -> list[tuple[int, str]]:
        """Quét chuỗi HTML trung gian qua Đồ thị DOM BeautifulSoup4 để tái tạo Cây Mục Lục.
        
        Phương thức này tự động lột bỏ toàn bộ các thẻ HTML markup trong công thức toán
        (như <span class="vietnamese-math-text">) để thu về chuỗi văn bản sạch tuyệt đối.
        """
        if not html_content or not html_content.strip():
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        heading_tags = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        headings: list[tuple[int, str]] = []

        for tag in heading_tags:
            raw_level = tag.get("data-level")

            if isinstance(raw_level, str):
                try:
                    level = int(raw_level)
                except ValueError:
                    level = int(tag.name[1])
            elif isinstance(raw_level, list) and raw_level and isinstance(raw_level[0], str):
                try:
                    level = int(raw_level[0])
                except ValueError:
                    level = int(tag.name[1])
            else:
                level = int(tag.name[1])

            if level <= self.max_bookmark_level:
                # Trích xuất toàn bộ văn bản thuần, tự động lột bỏ các thẻ HTML toán học con
                clean_text = tag.get_text().strip()
                clean_text = " ".join(clean_text.split())

                if clean_text:
                    headings.append((level, clean_text))

        return headings

    def _normalize_toc_hierarchy(self, raw_toc: list[list[Any]]) -> list[list[Any]]:
        """Chuẩn hóa cấp độ phân cấp mảng TOC tuân thủ nghiêm ngặt quy tắc nhị phân của PyMuPDF.

        Quy tắc PyMuPDF:
        1. Phần tử đầu tiên (item 0) BẮT BUỘC có cấp độ bằng 1.
        2. Các phần tử tiếp theo không được nhảy cấp vượt quá (prev_level + 1).
        """
        if not raw_toc:
            return []

        normalized_toc: list[list[Any]] = []
        for idx, (level, title, page_num) in enumerate(raw_toc):
            if idx == 0:
                norm_level = 1
            else:
                prev_level = normalized_toc[idx - 1][0]
                if level > prev_level + 1:
                    norm_level = prev_level + 1
                else:
                    norm_level = level
            normalized_toc.append([norm_level, title, page_num])

        return normalized_toc

    def inject_metadata(self, pdf_path: Path, html_content: str) -> bool:
        """Thực thi tiến trình nội suy vị trí vật lý và tiêm cấu trúc Outline vào PDF."""
        headings = self._extract_headings_from_html(html_content)

        if not headings:
            return True

        if not pdf_path.exists():
            print(f"[CẢNH_BÁO_INJECTOR] Không tìm thấy tệp nhị phân mục tiêu tại: {pdf_path}")
            return False

        try:
            document = fitz.open(pdf_path)
            raw_toc: list[list[Any]] = []

            current_page_index = 0
            total_pages = len(document)

            for level, title in headings:
                found_page = current_page_index

                for page_num in range(current_page_index, total_pages):
                    page = document[page_num]
                    text_instances = page.search_for(title)
                    if text_instances:
                        found_page = page_num
                        current_page_index = page_num
                        break

                raw_toc.append([level, title, found_page + 1])

            # Chạy màng lọc chuẩn hóa cấp độ trước khi tiêm vào PyMuPDF
            normalized_toc = self._normalize_toc_hierarchy(raw_toc)

            document.set_toc(normalized_toc)
            document.saveIncr()
            document.close()

            print(f"    -> [SIÊU_DỮ_LIỆU] Tiêm thành công {len(normalized_toc)} dấu trang điều hướng (Bookmarks).")
            return True

        except (OSError, RuntimeError, ValueError) as error:
            print(f"    -> [LỖI_TIÊM_SIÊU_DỮ_LIỆU] Thất bại khi ghi Bookmarks vào {pdf_path.name}: {error}")
            return False
