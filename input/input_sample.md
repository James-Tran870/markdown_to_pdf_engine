# 1. BẢO TỒN CẤU TRÚC VÀ MÃ HÓA TIẾNG VIỆT

Tài liệu này phục vụ mục đích kiểm thử đường ống biên dịch Markdown sang PDF tự động chạy trên môi trường Windows 11. Chúng ta cần đảm bảo các ký tự tiếng Việt có dấu như: **Thử nghiệm hệ thống**, *Chuyển đổi dữ liệu cục bộ*, và `Mã nguồn phòng thủ` được hiển thị hoàn hảo không bị lỗi mã hóa I/O.

## 1.1. Thử Nghiệm Toán Tử Nhị Phân Và Ký Tự Đặc Biệt

Trong quá trình xử lý văn bản thô, các toán tử logic trong lập trình như `alpha < beta` hoặc `gamma > delta` cũng như biểu thức chính quy Regex `^[a-zA-Z0-9_]+$` phải được giữ nguyên dạng mà không làm hỏng cấu trúc HTML trung gian.

### 1.1.1. Phân Cấp Tiêu Đề Cấp 3 Hợp Lệ

Thẻ tiêu đề này nằm ở cấp độ 3 và sẽ được động cơ `HTMLRenderer` tự động dập mỏ neo `id="111-phan-cap-tieu-de-cap-3-hop-le"` để WeasyPrint ánh xạ thành Dấu trang (Bookmark) cấp 3 trong tệp PDF.

#### 1.1.1.1. Phân Cấp Tiêu Đề Cấp 4 Giới Hạn Cấu Trúc

Đây là cấp tiêu đề H4 cuối cùng được phép chuyển đổi thành Dấu trang theo cấu hình `max_bookmark_level: 4` trong tệp `settings.yaml`.

##### 1.1.1.1.1. Tiêu Đề Cấp 5 Không Ánh Xạ Bookmark

Tiêu đề H5 này sẽ chỉ hiển thị dưới dạng văn bản nhấn mạnh trên trang in và không xuất hiện trong cây thư mục Bookmark bên lề của PDF.

---

# 2. DIỄN TẬP BẪY ĐÁNH LƯA CẤU TRÚC VÀ KHỐI MÃ

Dưới đây là một khối mã nguồn Python chứa cú pháp tiêu đề giả mạo nằm bên trong nhằm thử nghiệm năng lực cô lập không gian của Cây Cú Pháp Trừu Tượng (AST):

```python
# Đây là đoạn mã Python ví dụ
def calculate_metrics(alpha: float, beta: float) -> bool:
    """
    ## Tiêu đề Giả mạo Cấp 2 Trong Code Block
    Lưu ý: Dòng trên không được phép biến thành thẻ <h2> hay Bookmark trong PDF.
    """
    if alpha < beta and beta > 0:
        print("Xử lý thành công điều kiện logic < và >")
        return True
    return False