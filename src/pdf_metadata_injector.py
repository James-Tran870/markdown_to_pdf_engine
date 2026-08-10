# ==============================================================================
# LỚP TIÊM SIÊU DỮ LIỆU HẬU KỲ (POST-PROCESSING METADATA INJECTOR v1.5.1)
# Đường dẫn: src/pdf_metadata_injector.py
# Kiến trúc: Forward Search Heuristic, Binary Outline Injection & Strict Exception
# ==============================================================================

import re
from pathlib import Path

import fitz  # PyMuPDF


class MetadataInjector:
    """Bộ động cơ can thiệp nhị phân, trích xuất cấu trúc Heading và tiêm Bookmarks vào PDF."""

    def __init__(self, max_bookmark_level: int = 4):
        """Khởi tạo cấu hình nội suy với giới hạn chiều sâu phân cấp Bookmark."""
        self.max_bookmark_level = max_bookmark_level

    def _extract_headings_from_html(self, html_content: str) -> list[tuple[int, str]]:
        """
        Quét chuỗi HTML trung gian để tái tạo cấu trúc Cây Mục Lục.
        Bóc tách độ sâu (level) từ thuộc tính data-level và nội dung văn bản.
        """
        # Bắt chính xác cấu trúc <hX id="..." data-level="X">Text</hX> từ HTMLRenderer
        pattern = re.compile(
            r'<h([1-6])[^>]*data-level="([^"]+)"[^>]*>(.*?)</h\1>',
            re.IGNORECASE | re.DOTALL,
        )
        headings = []

        for match in pattern.finditer(html_content):
            level_str = match.group(2)
            raw_text = match.group(3)

            try:
                level = int(level_str)
            except ValueError:
                continue

            # Rào chắn độ sâu cấu trúc theo cấu hình YAML
            if level <= self.max_bookmark_level:
                # Dọn dẹp các thẻ HTML nội dòng (<code>, <em>, <span class="math-tex">)
                clean_text = re.sub(r"<[^>]+>", "", raw_text).strip()
                
                # Giải mã các thực thể HTML cơ bản để đối chiếu chính xác với văn bản PDF
                clean_text = (
                    clean_text.replace("&amp;", "&")
                    .replace("&lt;", "<")
                    .replace("&gt;", ">")
                    .replace("&quot;", '"')
                )

                if clean_text:
                    headings.append((level, clean_text))

        return headings

    def inject_metadata(self, pdf_path: Path, html_content: str) -> bool:
        """
        Thực thi tiến trình nội suy vị trí vật lý và tiêm cấu trúc Outline vào PDF.
        Cơ chế: Tìm kiếm tịnh tiến văn bản (Forward Text Search) kết hợp Fallback logic.
        """
        headings = self._extract_headings_from_html(html_content)
        
        # Thoát sớm (Early Return) nếu tài liệu không có bất kỳ tiêu đề nào
        if not headings:
            return True

        if not pdf_path.exists():
            print(f"[CẢNH_BÁO_INJECTOR] Không tìm thấy tệp nhị phân mục tiêu tại: {pdf_path}")
            return False

        try:
            # Mở tệp nhị phân PDF qua engine MuPDF
            document = fitz.open(pdf_path)
            toc = []
            
            # Con trỏ trang tịnh tiến (Không bao giờ lùi lại để tối ưu hiệu năng)
            current_page_index = 0
            total_pages = len(document)

            for level, title in headings:
                found_page = current_page_index
                
                # Quét tuần tự từ trang hiện tại đến cuối tài liệu
                for page_num in range(current_page_index, total_pages):
                    page = document[page_num]
                    
                    # Xác thực sự tồn tại của chuỗi văn bản trên trang vật lý
                    text_instances = page.search_for(title)
                    if text_instances:
                        found_page = page_num
                        current_page_index = page_num  # Neo vị trí cho lần tìm kiếm tiếp theo
                        break

                # Cấu trúc Cây Mục lục của PyMuPDF yêu cầu định dạng mảng: [Level, Title, PageNumber]
                # Chỉ mục trang (PageNumber) của PyMuPDF tính từ 1 (1-based index)
                toc.append([level, title, found_page + 1])

            # Ghi đè toàn bộ Cây Mục lục vào lớp siêu dữ liệu của tệp
            document.set_toc(toc)
            
            # Lưu tệp bằng phương pháp Incremental Save để bảo toàn an toàn dữ liệu đồ họa
            document.saveIncr()
            document.close()
            
            print(f"    -> [SIÊU_DỮ_LIỆU] Tiêm thành công {len(toc)} dấu trang điều hướng (Bookmarks).")
            return True

        # Triệt tiêu cảnh báo BLE001 bằng cách cô lập chính xác 3 rủi ro I/O và Nhị phân
        except (OSError, RuntimeError, ValueError) as error:
            print(f"    -> [LỖI_TIÊM_SIÊU_DỮ_LIÊU] Thất bại khi ghi Bookmarks vào {pdf_path.name}: {error}")
            return False
