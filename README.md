# MARKDOWN TO PDF ENGINE (Lõi Biên dịch Tài liệu Cục bộ & Chuẩn in ấn Học thuật - Phiên bản v1.6.0)

Một hệ thống đường ống dữ liệu (**Data Pipeline**) tự động hóa toàn diện, chuyên trách chuyển đổi hàng loạt tệp Markdown sang định dạng PDF chuẩn Typography xuất bản, đồ họa toán học vector sắc nét qua động cơ Chromium, bảng biểu GFM khung lưới hoàn chỉnh và cây mỏ neo điều hướng **Bookmarks nhị phân Cấp 6** ngay trên môi trường Windows 11 cục bộ.

Dự án được xây dựng dựa trên tư duy phân tách hệ thống nghiêm ngặt (**Separation of Concerns - SoC**), khép kín và độc lập ngoại tuyến (**Offline-first**). Hệ thống nói KHÔNG với các công nghệ đám mây (Cloud), máy chủ web hay cơ sở dữ liệu phức tạp. Mọi tiến trình biên dịch đều diễn ra trên máy cục bộ, bảo đảm tính bảo mật dữ liệu tuyệt đối và khả năng can thiệp tham số linh hoạt thông qua hệ thống cấu hình DTO Pydantic v2 tách biệt.

---

## CHƯƠNG 1: TRIẾT LÝ KIẾN TRÚC VÀ 6 TRỤ CỘT PHÒNG THỦ (ARCHITECTURAL PHILOSOPHY v1.6.0)

Để hình dung phương thức vận hành của hệ thống, hãy tưởng tượng dự án giống như một **Xưởng In ấn Đồ họa Hiện đại Khép kín**. Thay vì cho phép công nhân tự do can thiệp vào dây chuyền, xưởng vận hành dựa trên 6 trụ cột kiến trúc bất biến nhằm loại trừ hoàn toàn mọi rủi ro gián đoạn tiến trình:

### 1. Phân tách Mối quan tâm (SoC) & Truyền dẫn Dữ liệu Động (Pydantic DTO & Dynamic Unpacking - v1.6.0)

- **Ẩn dụ đời thực:** Trong một xưởng đúc phim điện ảnh, Trình chiếu phim (Mã logic Python) không bao giờ tự mình điều khiển độ sáng hay phông chữ của phụ đề; nó hoạt động dựa trên một tệp kịch bản định dạng do Đạo diễn thiết lập. Khi cần đổi kiểu chữ hay độ phân giải, Đạo diễn chỉ việc sửa kịch bản mà không cần thay máy chiếu.
- **Áp dụng vào hệ thống:** Tách rời hoàn toàn tham số điều khiển khỏi mã nguồn xử lý chính. Mọi tiến trình biên dịch đều nạp cấu hình từ tệp YAML chuyên biệt (`config/settings.yaml`). Ở phiên bản v1.6.0, toàn bộ dữ liệu cấu hình được chuyển đổi thành các **Data Transfer Objects (DTO)** tĩnh thông qua thư viện **Pydantic v2**. Hàm điều phối `execute_single_file_pipeline` sử dụng cú pháp giải nén từ điển động `**config.heading_retention_depth.model_dump()`, bảo đảm các tham số như `enable_heading_anchors` tự động chảy trôi chảy vào `HTMLRenderer` mà không bị bỏ rơi. Quy tắc chặn đứng (**Hard-Block Rule**) được thiết lập để hủy bỏ tiến trình ngay lập tức nếu tham số `max_bookmark_level` vượt quá giới hạn vật lý cấp 6.

### 2. Kiến trúc Băm Mật mã Bảo vệ Khối Mã (SHA-256 Cryptographic Masking - v1.6.0)

- **Ẩn dụ đời thực:** Khi lưu trữ linh kiện quý trong kho, thay vì dán một con tem giấy ngẫu nhiên dễ bị kẻ gian làm giả để đánh tráo linh kiện, thủ kho sử dụng một **Mã băm Niêm phong Mật mã** được tính toán trực tiếp từ trọng lượng, kích thước và mã số của chính linh kiện đó.
- **Áp dụng vào hệ thống:** Trong quá trình đồng bộ hóa cú pháp toán học TeX/LaTeX2e, hệ thống cần dán mặt nạ bảo vệ các khối mã nguồn (`code fence`) để tránh việc Regex can thiệp sai. Hệ thống áp dụng thuật toán băm mật mã **`hashlib.sha256()`**. Khóa giữ chỗ `__CRYPTO_MASK_{hash}_{counter}__` được tính toán trực tiếp từ nội dung khối mã, chuỗi muối ngẫu nhiên và bộ đếm cục bộ, triệt tiêu 100% rủi ro va chạm Regex (**Regex Collision Attack**) do tin tặc tiêm chuỗi giả mạo.

### 3. Bộ Nhớ Tạm Vô Danh & Cách Ly Tiến Trình Đa Nhiệm (Process Isolation & Ephemeral Memory - v1.6.0)

- **Ẩn dụ đời thực:** Khi các bác sĩ phẫu thuật làm việc, thay vì dùng chung một bàn dụng cụ cố định ngoài hành lang (dễ gây nhiễm khuẩn chéo giữa các ca mổ), mỗi ca mổ được cấp một **Phòng phẫu thuật Khép kín Dùng Một lần**. Khi ca mổ kết thúc, toàn bộ thiết bị tạm thời được tự động thu hồi và tiêu hủy ngay lập tức.
- **Áp dụng vào hệ thống:** Module `src/pdf_compiler.py` tích hợp công cụ `tempfile.NamedTemporaryFile` của Hệ điều hành, phân bổ một không gian bộ nhớ tạm ẩn danh hoàn toàn độc lập cho mỗi tiến trình. Ở phiên bản v1.6.0, hệ thống nâng cấp toàn bộ kiến trúc kiểm thử đa nhiệm từ đa luồng (`ThreadPoolExecutor`) sang **Đa tiến trình Vật lý (`ProcessPoolExecutor`)**. Việc tách tiến trình vật lý cung cấp cho mỗi thể hiện Playwright Chromium một **Vòng lặp Sự kiện (Event Loop)** riêng biệt, triệt tiêu 100% rủi ro va chạm bộ nhớ và lỗi sập Event Loop.

### 4. Tiêm Siêu dữ liệu Hậu kỳ & Dấu trang Cấp 6 (Post-Processing Metadata Injection - v1.6.0)

- **Ẩn dụ đời thực:** Một cuốn sách giáo khoa sau khi được máy in đúc ra toàn bộ hình ảnh và chữ viết sắc nét trên giấy phẳng, sẽ được chuyển sang **Phân xưởng Đóng bìa & Dán Dấu trang**. Tại đây, người thợ đính thêm các thẻ phân đoạn bằng nhựa vào gáy sách giúp độc giả lật mở nhanh từng chương.
- **Áp dụng vào hệ thống:** Động cơ Chromium Headless chỉ xuất bản bản in đồ họa phẳng và từ chối biên dịch thuộc tính CSS `bookmark-label` thành cây điều hướng PDF nhị phân. Mô-đun hậu kỳ `src/pdf_metadata_injector.py` bóc tách Cây Cú pháp Trừu tượng (AST) từ các thẻ `<hX data-level="...">`, sử dụng thư viện **PyMuPDF (`fitz`)** quét nhị phân tệp PDF phẳng, nội suy tọa độ trang vật lý và tiêm trực tiếp **Cây Mục lục (Outline Tree / Bookmarks)** đến tận **Heading Cấp 6** vào lớp siêu dữ liệu nhị phân.

### 5. Đóng Gói Tài Nguyên Nội Tuyến & Khiên An Ninh Trình Duyệt (Inline Asset Embedding & Security Sandbox - v1.6.0)

- **Ẩn dụ đời thực:** Thay vì cho phép tài xế xe tải liên tục mở cổng bảo vệ xưởng in để đi ra ngoài lấy vật tư (dễ bị kẻ gian đột nhập), người quản xưởng đóng gói toàn bộ bản thiết kế, mực in và giấy vẽ vào bên trong thùng xe niêm phong ngay trước khi xe xuất phát.
- **Áp dụng vào hệ thống:** Ở phiên bản v1.6.0, mô-đun `src/html_renderer.py` sử dụng phương thức `Path.read_text()` đọc trực tiếp nội dung chuỗi thô của `katex.min.css`, `katex.min.js`, và `auto-render.min.js`. Nội dung này được nhúng trực tiếp vào giữa cặp thẻ `<style>` và `<script>` nội tuyến trong HTML. Nhờ đó, `src/pdf_compiler.py` loại bỏ hoàn toàn bộ 3 cờ hạ bảo mật (`--disable-web-security`, `--allow-file-access-from-files`, `--no-sandbox`), giúp Playwright Chromium biên dịch đồ họa trong môi trường **Security Sandbox** cô lập tuyệt đối mà không cần quyền truy cập đĩa cứng.

### 6. Ma trận In ấn Học thuật & Lớp Giáp CSS Căn Lề Trái Cưỡng Chế (Academic Standards & Strict Typography)

- **Ẩn dụ đời thực:** Trong một xưởng in sách giáo khoa, toàn bộ chữ viết và tiêu đề bắt buộc phải gióng thẳng hàng dọc bên lề trái để tạo độ trang trọng. Nếu một công thức toán học ở giữa trang tỏa ra năng lượng làm đẩy toàn bộ văn bản xung quanh ra giữa, người thợ in sẽ lắp một **Thước Kẹp Bằng Thép (Strict Left-Align Rules)** giữ chặt toàn bộ khối chữ không cho xô lệch.
- **Áp dụng vào hệ thống:** Tích hợp bộ quy chuẩn học thuật quốc tế [APA 7th, IEEE, Harvard]. Giới hạn tự động đánh số bằng CSS Counters ở cấp 4 (`h1` đến `h4`). Áp dụng triệt để thuộc tính `text-align: left !important;` cho toàn bộ `body`, `p`, `h1`-`h6`, `pre` và `.highlight` để triệt tiêu hoàn toàn sự cố rò rỉ căn giữa từ KaTeX, đồng thời giữ định dạng Bold/Italic cho `h5`/`h6` ở mức **11pt** hoàn toàn độc lập với bộ đếm chỉ số.

---

## CHƯƠNG 2: BẢN ĐỒ CẤU TRÚC THƯ MỤC (DIRECTORY BLUEPRINT v1.6.0)

Dưới đây là sơ đồ không gian làm việc (**Workspace**) tiêu chuẩn trên VSCode. Mỗi thành phần đều giữ một vùng trách nhiệm duy nhất (**Single Responsibility Principle**):

```text
MARKDOWN_TO_PDF_ENGINE/
│
├── assets/                    # [Kho Tài Nguyên Tĩnh Offline] Chứa tài nguyên kết xuất đồ họa KaTeX.
│   └── katex/                 # Bảng CSS, thư viện JS và bộ phông chữ toán học .woff2 ngoại tuyến.
│       ├── fonts/             # Bộ phông chữ vector KaTeX (AMS, Main, Math, Size1).
│       ├── katex.min.css      # Định hình kiểu dáng và cấu trúc đồ họa công thức.
│       ├── katex.min.js       # Động cơ phân tích cú pháp LaTeX client-side.
│       └── auto-render.min.js # Script tự động quét và đúc DOM toán học ($/$$/\[/\]).
│
├── config/
│   └── settings.yaml          # [Bảng Điều Khiển Trung Tâm] Khai báo 11 phân khu cấu hình DTO (Max Bookmark: 6).
│
├── input/                     # [Kho Nguyên Liệu Zero-Trust] Thư mục chứa các tệp .md đầu vào (Chặn 100% trên Git).
│   └── .gitkeep               # Tệp giữ cấu trúc thư mục cho Git.
│
├── output/                    # [Kho Thành Phẩm] Thư mục chứa các tệp .pdf thành phẩm (Tái tạo cây folder).
│   └── .gitkeep               # Tệp giữ cấu trúc thư mục cho Git.
│
├── src/                       # [Lõi Động Cơ Engine] Thư mục chứa các module mã nguồn xử lý logic.
│   ├── __init__.py            # Khởi tạo gói mã nguồn nội bộ.
│   ├── ast_parser.py          # (Giai đoạn 1) Quét AST (gfm-like) & dán mặt nạ băm SHA-256 bảo vệ khối mã.
│   ├── html_renderer.py       # (Giai đoạn 2) Nhúng tài nguyên Inline, nội suy cờ KaTeX động & tạo mỏ neo H1-H6.
│   ├── pdf_compiler.py        # (Giai đoạn 3) Cấp phát tempfile vô danh, bật Sandbox an toàn & xuất bản PDF.
│   └── pdf_metadata_injector.py # (Giai đoạn 4) Quét nhị phân PyMuPDF, nội suy vị trí & tiêm Bookmarks Cấp 6.
│
├── tests/                     # [Phòng Thử Nghiệm Va Chạm] Khu vực diễn tập phòng chống sự cố vật lý Red-Team.
│   ├── __init__.py            # Khởi tạo gói kiểm thử.
│   └── red_team_tests.py      # Bộ kiểm thử Hộp Trắng (13 Kịch bản va chạm Pydantic, Process Isolation & Level-6 Bookmarks).
│
├── .gitignore                 # Chỉ thị phòng thủ Git cách ly 100% I/O, bộ nhớ đệm Ruff, tempfile và venv.
├── main.py                    # [Quản Đốc Băng Chuyền] Điều phối Pipeline, xác thực Pydantic DTO & Dynamic Unpacking.
├── README.md                  # Cẩm nang vận hành và bản thiết kế kiến trúc toàn diện v1.6.0.
└── requirements.txt           # Bảng kê vật tư thư viện phụ thuộc (Playwright, Pydantic v2, PyMuPDF).
```

### Phân tích Chức năng Chi tiết Từng Thành phần Mã nguồn (v1.6.0)

- **`assets/katex/`**: Thư mục lưu trữ bộ tài nguyên tĩnh ngoại tuyến của KaTeX v0.16.9. Đảm bảo hệ thống biên dịch công thức toán sắc nét 100% mà không cần bất kỳ kết nối Internet nào.

- **`config/settings.yaml`**: Trái tim cấu hình của dự án. Quản lý 11 phân khu tham số. Nâng cấp tham số `max_bookmark_level: 6` mở rộng độ sâu điều hướng PDF.

- **`main.py`**: Quản đốc điều phối toàn bộ đường ống. Nạp tệp YAML qua `load_configuration()`, thực thi ép củng Lược đồ DTO, sử dụng toán tử giải nén động `**retention_config` để truyền tham số an toàn vào `HTMLRenderer`.

- **`src/ast_parser.py`**: Đảm nhiệm **Giai đoạn 1**. Sử dụng `markdown-it-py` với preset `gfm-like`. Áp dụng cơ chế Băm Mật mã SHA-256 (`_unify_math_delimiters`) để che phủ khối mã nguồn và chuyển đổi cú pháp Brackets (`\[...\]`) sang Dollars (`$$`).

- **`src/html_renderer.py`**: Đảm nhiệm **Giai đoạn 2**. Nạp nội dung thô CSS/JS KaTeX và nhúng trực tiếp nội tuyến (Inline Embedding). Trích xuất cờ `strict_mode` và `throw_on_error` từ YAML để nội suy động vào script đúc DOM.

- **`src/pdf_compiler.py`**: Đảm nhiệm **Giai đoạn 3**. Cấp phát tệp tạm vô danh qua `tempfile.NamedTemporaryFile`. Khởi chạy Playwright Chromium với khiên bảo mật **Security Sandbox** đầy đủ.

- **`src/pdf_metadata_injector.py`**: Đảm nhiệm **Giai đoạn 4**. Tiếp nhận chuỗi HTML trung gian, bóc tách cấu trúc thẻ `<hX data-level="...">` từ Cấp 1 đến Cấp 6, sử dụng `PyMuPDF` (`fitz`) quét vị trí văn bản trên PDF vật lý và tiêm Cây Mục lục nhị phân.

- **`tests/red_team_tests.py`**: Phòng thử nghiệm va chạm vật lý. Thực thi 13 kịch bản đối kháng hộp trắng bao phủ toàn bộ các điểm gãy tiềm ẩn (Pydantic Latency, ProcessPoolExecutor Concurrency, Level-6 Bookmarks Verification).

---

## CHƯƠNG 3: HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG VÀ HẠ TẦNG THỰC THI (ENVIRONMENT & INFRASTRUCTURE v1.6.0)

Chương này hướng dẫn chi tiết quy trình thiết lập Môi trường ảo (**Virtual Environment**), cài đặt hệ thống vật tư phụ thuộc mới nhất bao gồm **Pydantic v2**, **PyMuPDF**, và phân tích cơ chế đa tiến trình độc lập (`concurrent.futures`).

---

### 1. YÊU CẦU HỆ THỐNG VÀ CÁC THÀNH PHẦN NỀN TẢNG (SYSTEM PREREQUISITES)

Để hạ tầng biên dịch tài liệu vận hành ổn định, không gian làm việc cục bộ cần đáp ứng các điều kiện sau:

- **Hệ điều hành:** Microsoft Windows 10 hoặc Windows 11 (Khuyên dùng Windows 11 64-bit).
- **Môi trường Python:** Python phiên bản **3.10** trở lên (Khuyên dùng Python 3.11/3.12/3.14 để tối ưu tốc độ xử lý Pydantic).
- **Trình biên tập mã nguồn (IDE):** Visual Studio Code (VSCode) tích hợp công cụ kiểm tra tĩnh **Ruff Linter**.
- **Bộ nhị phân Động cơ Trình duyệt (Headless Browser Binary):** Playwright Chromium Browser Engine.

---

### 2. QUY TRÌNH KÍCH HOẠT MÔI TRƯỜNG VÀ CÀI ĐẶT THƯ VIỆN PHỤ THUỘC

Toàn bộ lệnh khởi tạo môi trường, nâng cấp gói vật tư và tải trình duyệt ngầm được đóng gói trong **một khối mã lệnh duy nhất** bên dưới:

```powershell
# ==============================================================================
# QUY TRÌNH THỰC THI LỆNH TRÊN TERMINAL VSCODE (POWERSHELL) - PHIÊN BẢN v1.6.0
# ==============================================================================

# Bước 1: Khởi tạo Môi trường ảo Python (Virtual Environment) tại thư mục gốc dự án
python -m venv venv

# Bước 2: Kích hoạt Môi trường ảo trên PowerShell
.\venv\Scripts\Activate.ps1

# Bước 3: Nâng cấp công cụ quản lý gói pip lên phiên bản mới nhất
python -m pip install --upgrade pip

# Bước 4: Thực thi cài đặt hàng loạt danh mục vật tư phụ thuộc từ requirements.txt
pip install -r requirements.txt

# Bước 5: Khởi tạo và tải bộ nhị phân Playwright Chromium Browser về máy cục bộ
playwright install chromium


```

---

### 3. PHÂN TÍCH CHỨC NĂNG HẠ TẦNG CỦA CÁC THƯ VIỆN PHỤ THUỘC CHỦ CHỐT (v1.6.0)

- **`pydantic>=2.5.0`:** Động cơ ép củng Lược đồ Cấu hình (**Schema Validation Engine**). Cưỡng chế kiểm tra kiểu dữ liệu tĩnh, áp đặt quy tắc chặn đứng (**Hard-Block Rules**) nếu cấu hình YAML vi phạm giới hạn vật lý.

- **`pymupdf>=1.23.0` (PyMuPDF `fitz`):** Động cơ thao tác nhị phân PDF. Cho phép mở luồng nhị phân tệp PDF sau khi Playwright Chromium xuất bản, nội suy vị trí tiêu đề vật lý và tiêm **Cây Mục lục (Outline Tree / Bookmarks)** đến Cấp 6.

- **`playwright>=1.40.0`:** Động cơ Trình duyệt Không đầu (**Headless Browser Engine**). Khởi chạy Chromium ngầm trong chế độ Sandbox an toàn, nạp tài nguyên Inline, đúc DOM toán học KaTeX và xuất bản PDF đồ họa phẳng chuẩn A4.

- **`concurrent.futures` (`ProcessPoolExecutor` - Thư viện chuẩn Python):** Động cơ quản lý Đa tiến trình Cấp Hệ điều hành. Cấp phát cho mỗi công việc một tiến trình Python độc lập với Vòng lặp Sự kiện (Event Loop) và không gian bộ nhớ riêng biệt. Điều này triệt tiêu hoàn toàn điểm mù sập Event Loop của Playwright khi thực thi song song hàng loạt tệp PDF.

- **`markdown-it-py>=3.0.0` & `mdit-py-plugins>=0.4.0`:** Bộ phân tích Cây Cú pháp Trừu tượng (AST Parser) tuân thủ tiêu chuẩn CommonMark và mở rộng GFM Tables (`gfm-like`).

- **`pygments>=2.17.0`:** Động cơ nhuộm màu cú pháp mã nguồn (**Syntax Highlighting Engine**).

---

## CHƯƠNG 4: GIẢI PHẪU LƯỢC ĐỒ CẤU HÌNH TRUNG TÂM (config/settings.yaml SCHEMA ANATOMY v1.6.0)

Tệp `config/settings.yaml` đóng vai trò là **Trung tâm Điều khiển Lược đồ (Schema Control Center)**. Ở phiên bản v1.6.0, toàn bộ 11 phân khu cấu hình được ánh xạ trực tiếp vào các mô hình **Pydantic DTO (Data Transfer Objects)** định nghĩa trong `main.py`.

Dưới đây là giải phẫu chi tiết logic kỹ thuật và tác động hệ thống của từng phân khu tham số:

---

### 1. CHUẨN MÃ HÓA TOÀN CỤC (`global_encoding_standard`)

- **Logic kỹ thuật:** Khai báo hằng số mã hóa cưỡng chế cho toàn bộ luồng I/O trong hệ thống.
- **Tác động:** Áp đặt giá trị `"utf-8"` bắt buộc cho mọi thao tác đọc tệp Markdown, ghi tệp HTML trung gian và nạp tệp YAML. Triệt tiêu hoàn toàn sự cố sập luồng do lỗi `UnicodeDecodeError` hoặc vỡ phông Tiếng Việt Unicode trên bảng mã mặc định `cp1252` của Windows 11.

---

### 2. ĐIỀU HƯỚNG THƯ MỤC VÀ XỬ LÝ HÀNG LOẠT (`directory_routing`)

- **Logic kỹ thuật:** Quản lý dây chuyền quét, phân loại và tái tạo cấu trúc không gian lưu trữ tệp.
- **Chi tiết tham số:**
  - `input_directory` & `output_directory`: Khai báo tên thư mục đầu vào (`"input"`) và đầu ra (`"output"`).
  - `recursive_search: true`: Bật cơ chế quét đệ quy (`rglob`) đào sâu vào tất cả các cấp thư mục con bên trong `input/`.
  - `allowed_extensions`: Danh sách mảng lọc các đuôi tệp văn bản hợp lệ (`[".md", ".markdown", ".mdown"]`).
  - `overwrite_existing`: Cờ cho phép ghi đè tệp PDF thành phẩm nếu đã tồn tại bên thư mục đầu ra.
  - `auto_create_directories: true`: Tự động khởi tạo hạ tầng thư mục nếu chưa tồn tại trên đĩa cứng.
  - `preserve_subfolder_structure: true`: Tự động dựng lại chính xác cây thư mục con từ `input/` sang `output/` (Ví dụ: `input/nhom1/bai1.md` -> `output/nhom1/bai1.pdf`).

---

### 3. NHUỘM MÀU CÚ PHÁP MÃ NGUỒN (`syntax_highlighting_profile`)

- **Logic kỹ thuật:** Định danh bảng màu CSS (Theme Profile) do thư viện `Pygments` phát sinh.
- **Tác động:** Chuyển đổi các khối mã nguồn (`code fence`) thành chuỗi HTML được tô màu từ khóa, hàm, chuỗi và biến số theo chủ đề được chọn (Mặc định: `"monokai"`).

---

### 4. GIỚI HẠN ĐỘ SÂU MỎ NEO VÀ DẤU TRANG (`heading_retention_depth`)

- **Logic kỹ thuật:** Quy định ranh giới phân cấp tiêu đề, gắn mỏ neo ASCII và tiêm Bookmarks PDF.
- **Chi tiết tham số:**
  - `max_bookmark_level`: Giới hạn độ sâu phân cấp Bookmark [**NÂNG CẤP v1.6.0: Đã mở rộng lên Mức 6**]. **Rào chắn Pydantic DTO:** Được kiểm soát chặt chẽ bởi quy tắc `@field_validator` trong `main.py`. Nếu người dùng khai báo giá trị vượt quá cấp 6 (như `10`), Pydantic sẽ phát tín hiệu ngoại lệ `ValidationError` và ngắt tiến trình ngay lập tức để bảo vệ cấu trúc PDF.
  - `enable_heading_anchors: true`: Tự động sinh thuộc tính `id` mỏ neo cho các thẻ `<hX data-level="...">`.
  - `normalize_anchor_ascii: true`: Chuẩn hóa chuỗi tiêu đề Tiếng Việt có dấu thành chuỗi ASCII Slug không dấu (Ví dụ: `"Kiến Trúc"` -> `"kien-truc"`).

---

### 5. THÔNG SỐ TRANG IN VẬT LÝ (`document_layout`)

- **Logic kỹ thuật:** Thiết lập thông số hình học cho trang in theo chuẩn CSS Paged Media `@page`.
- **Chi tiết tham số:**
  - `page_size: "A4"`: Định dạng khổ giấy in tiêu chuẩn [210mm x 297mm].
  - `margin: "20mm"`: Thiết lập khoảng cách lề an toàn 4 phía [Tròn 20mm].
  - `code_overflow_handling: "break-word"`: Áp dụng thuộc tính bẻ dòng tự động cho khối mã nguồn, triệt tiêu sự cố văn bản mã tràn ra khỏi lề giấy A4.

---

### 6. CẤU HÌNH MỸ THUẬT VÀ PHÔNG CHỮ HỆ THỐNG (`typography_configuration`)

- **Logic kỹ thuật:** Xây dựng bộ Font Stack phòng thủ chống lỗi vỡ phông Tiếng Việt Unicode.
- **Chi tiết tham số:**
  - `font_family`: Chuỗi ưu tiên phông chữ văn bản chính (`"Segoe UI", "Arial", "Calibri", "Tahoma", sans-serif`).
  - `code_font_family`: Phông chữ cố định chiều rộng dành riêng cho Code Block (`"Consolas", "Courier New", monospace`).
  - `base_font_size: "11pt"` & `line_height: "1.6"`: Kích thước chữ cơ sở và khoảng cách dòng chuẩn in ấn xuất bản.
  - `text_color: "#1a1a1a"`: Màu văn bản chuẩn xám đen, giảm mỏi mắt so với màu đen tuyệt đối (`#000000`).

---

### 7. CẤU HÌNH ĐÁNH SỐ TIÊU ĐỀ TỰ ĐỘNG (`heading_numbering_system`)

- **Logic kỹ thuật:** Điều khiển động cơ CSS Counters tự động đếm và chèn chỉ số phân cấp vào trước tiêu đề.
- **Chi tiết tham số:**
  - `enable_auto_numbering: true`: Bật/Tắt tính năng đánh số tiêu đề tự động.
  - `h1_numbering_style: "roman"`: Định dạng chữ số La Mã (`I., II., III.`) cho tiêu đề Cấp 1 [H1].
  - `sub_heading_numbering_style: "decimal"`: Định dạng phân cấp số tự nhiên (`1.1, 1.1.1`) cho tiêu đề H2 đến H4.
  - `number_separator: ". "`: Chuỗi ký tự phân cách giữa chỉ số thứ tự và nội dung tiêu đề.

---

### 8. ĐIỀU HƯỚNG TRÌNH DUYỆT NGẦM PLAYWRIGHT (`headless_browser_engine`)

- **Logic kỹ thuật:** Quản lý vòng đời và tham số xuất bản PDF của trình duyệt Playwright Chromium.
- **Chi tiết tham số:**
  - `browser_type: "chromium"`: Cưỡng chế sử dụng động cơ Chromium Headless.
  - `headless: true`: Chạy ngầm trình duyệt không giao diện GUI để đạt hiệu năng tối đa.
  - `page_timeout_ms: 30000`: Thời gian chờ tối đa 30.000ms (30 giây) cho tiến trình nạp tệp tạm và đúc DOM.
  - `wait_until_event: "networkidle"`: Buộc Chromium chờ cho đến khi toàn bộ tài nguyên tĩnh và script nạp xong 100%.
  - `print_background: true`: Kích hoạt in màu nền và đồ họa background CSS.
  - `prefer_css_page_size: true`: Cho phép quy tắc lề trang trong khối CSS `@page` ghi đè thiết lập mặc định của Chromium.

---

### 9. BỘ KẾT XUẤT TOÁN HỌC KATEX OFFLINE (`katex_offline_config`)

- **Logic kỹ thuật:** Điều khiển tài nguyên JS/CSS cục bộ để kết xuất 100% vĩ lệnh LaTeX không cần Internet.
- **Chi tiết tham số:**
  - `enable_katex: true`: Cờ bật/tắt chính cho động cơ kết xuất toán học KaTeX.
  - `assets_dir: "assets/katex"`: Đường dẫn tương đối trỏ đến kho tài nguyên tĩnh KaTeX Offline.
  - `css_filename`, `js_filename`, `auto_render_js_filename`: Khai báo tên các tệp tĩnh.
  - `strict_mode: false` & `throw_on_error: false`: Van ngắt mạch an toàn. **NÂNG CẤP v1.6.0:** Các biến boolean này được trích xuất trực tiếp từ DTO và nội suy f-string động vào chuỗi script đúc DOM KaTeX trong `HTMLRenderer` thay vì gán cứng.
  - `delimiters`: Danh sách mảng lọc 4 ranh giới nhận diện công thức toán học (`$$...$$`, `$..$`, `\[...\]`, `\(...\)`).

---

### 10. CẤU HÌNH BỘ XỬ LÝ BẢNG BIỂU GFM (`table_rendering_system`)

- **Logic kỹ thuật:** Điều khiển bộ phân tích bảng Markdown GFM và quản lý tràn viền vật lý A4.
- **Chi tiết tham số:**
  - `enable_gfm_tables: true`: Kích hoạt bộ phân tích bảng GFM trong AST Parser.
  - `overflow_strategy: "clip_and_warn"`: Chiến lược cắt bỏ phần thừa tràn ngang lề A4 và ghi nhật ký cảnh báo ra Terminal.
  - `repeat_header_on_page_break: true`: Tự động lặp lại hàng tiêu đề (Table Header) khi bảng bị cắt ngắt sang trang mới.
  - `max_printable_width_mm: 170`: Ngưỡng độ rộng vùng in an toàn của khổ A4 [210mm - 40mm lề = 170mm].

---

### 11. MA TRẬN QUY CHUẨN IN ẤN HỌC THUẬT (`academic_standards_profile`)

- **Logic kỹ thuật:** Định hình phong cách trình bày văn bản theo các tiêu chuẩn xuất bản quốc tế [APA 7th, IEEE].
- **Chi tiết tham số:**
  - `active_standard: "apa"`: Kích hoạt bộ quy chuẩn học thuật APA 7th.
  - `prevent_orphans_and_widows: true`: Ép chỉ thị CSS `orphans: 2; widows: 2;` chống dòng mồ côi và góa phụ.
  - `code_block_page_break_inside: "avoid"` & `table_page_break_inside: "avoid"`: Ép chỉ thị CSS `break-inside: avoid;` ngăn chặn việc ngắt trang xẻ đôi giữa chừng khối mã nguồn hoặc bảng biểu.

---

## CHƯƠNG 5: QUY TRÌNH VẬN HÀNH VÀ BẢN ĐỒ LUỒNG DỮ LIỆU ĐA CHẶNG (OPERATIONAL PIPELINE v1.6.0)

Chương này trình bày chi tiết quy trình di chuyển dữ liệu 4 Giai đoạn khép kín, phân tích cơ chế điều phối của tệp `main.py` dựa trên Lược đồ Pydantic DTO và giải phẫu 5 tầng bẫy lỗi cô lập sự cố.

---

### 1. SƠ ĐỒ LUỒNG DI CHUYỂN DỮ LIỆU 4 GIAI ĐOẠN (4-STAGE DATA PIPELINE v1.6.0)

Hãy tưởng tượng đường ống biên dịch tài liệu vận hành như một **Dây chuyền Sản xuất Sách Chuyên nghiệp** gồm 4 phân xưởng nối tiếp nhau:

```text
[Thư mục input/] ───> (Quét đệ quy tệp .md) ───> [main.py: AppConfig DTO Validation & Unpacking]
                                                        │
┌───────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┐
│                                                                                                               │
▼                                                                                                               ▼
[GIAI ĐOẠN 1: AST PARSER]                                                       [GIAI ĐOẠN 2: HTML RENDERER]
- Tệp: src/ast_parser.py                                                        - Tệp: src/html_renderer.py
- Động cơ: markdown-it-py (preset: gfm-like)                                    - Kỹ thuật: Inline Asset Embedding (CSS/JS)
- Kỹ thuật: Băm Mật mã SHA-256 (_unify_math_delimiters)                          - Kỹ thuật: Nội suy cờ KaTeX & Slugify ASCII (H1-H6)
- Đầu ra: Danh sách Nút AST (Tokens)                                            - Đầu ra: Chuỗi HTML Đóng gói + Pygments CSS
│                                                                               │
└───────────────────────────────────────────┬───────────────────────────────────┘
                                            │
                                            ▼
[GIAI ĐOẠN 3: PDF COMPILER]
- Tệp: src/pdf_compiler.py
- Động cơ: Playwright Chromium Headless (Security Sandbox)
- Kỹ thuật: Ephemeral Memory System (tempfile.NamedTemporaryFile)
- Đầu ra: Tệp PDF Đồ họa Phẳng (Flat Graphics PDF)
│
▼
[GIAI ĐOẠN 4: METADATA INJECTOR]
- Tệp: src/pdf_metadata_injector.py
- Động cơ: PyMuPDF (fitz) Binary Engine (Max Level: 6)
- Kỹ thuật: Forward Text Search & Binary Outline Injection
- Đầu ra: Tệp PDF Hoàn chỉnh mang Cây Mục lục (Bookmarks/Outline Tree Cấp 6)
│
▼
[Thư mục output/ (PDF Thành phẩm)]

```

#### Phân tích Chi tiết Nhiệm vụ Kỹ thuật tại Mỗi Giai đoạn Pipeline

- **Giai đoạn 1 (AST Parser - `src/ast_parser.py`):** Tiếp nhận đường dẫn tệp `.md`. Đọc văn bản thô chuẩn `utf-8`. Bật màng lọc `_unify_math_delimiters()` băm mật mã **SHA-256** bảo vệ Code Block, chuyển đổi đồng bộ `\[...\]` sang `$$...$$`. Đẩy qua `markdown-it-py` để phân rã thành mảng Nút AST ngữ nghĩa.

- **Giai đoạn 2 (HTML Renderer - `src/html_renderer.py`):** Tiếp nhận văn bản Markdown. Nhuộm màu mã nguồn qua `Pygments`. Sinh mỏ neo ASCII `<hX id="..." data-level="...">` cho toàn bộ tiêu đề từ H1 đến H6. Đọc trực tiếp chuỗi thô của tệp CSS/JS KaTeX từ đĩa cứng qua `Path.read_text()` và đóng gói **Inline Embedding** vào thẻ `<style>` và `<script>` nội tuyến. Trích xuất cờ cấu hình `strict_mode` và `throw_on_error` từ DTO để nội suy f-string động vào script đúc DOM.

- **Giai đoạn 3 (PDF Compiler - `src/pdf_compiler.py`):** Tạo tệp tạm ẩn danh ngẫu nhiên qua `tempfile.NamedTemporaryFile`. Đúc chuỗi HTML ngữ nghĩa thành tệp tạm vật lý. Khởi chạy Playwright Chromium với **Khiên Bảo mật Sandbox đầy đủ** (Đã gỡ bỏ cờ `--disable-web-security`). Điều hướng Chromium nạp tệp tạm qua giao thức `file:///`, chờ KaTeX đúc xong DOM toán học `.katex` và xuất bản tệp PDF đồ họa phẳng chuẩn A4. Tự động xóa tệp tạm trong khối `finally:`.

- **Giai đoạn 4 (Metadata Injector - `src/pdf_metadata_injector.py`):** Nhận tệp PDF phẳng và chuỗi HTML trung gian. Quét các thẻ `<hX data-level="...">` bóc tách danh sách tiêu đề từ Cấp 1 đến Cấp 6. Mở tệp PDF qua **PyMuPDF (`fitz`)**. Sử dụng thuật toán tìm kiếm tịnh tiến (`search_for`) xác định chỉ mục trang vật lý của từng tiêu đề. Tiêm mảng Cây Mục lục nhị phân `[Level, Title, PageNumber]` vào gáy siêu dữ liệu và thực thi lưu tịnh tiến `saveIncr()`.

---

### 2. GIẢI PHẪU 5 TẦNG BẪY LỖI CÔ LẬP SỰ CỐ (5-TIER FAULT ISOLATION ARCHITECTURE)

Để bảo đảm một tệp Markdown bị hỏng không thể làm dừng tiến trình xử lý hàng loạt của toàn bộ hệ thống, `markdown_to_pdf_engine` v1.6.0 được thiết lập 5 tầng bẫy lỗi phòng thủ:

#### Tầng 1: Cô lập Ngoại lệ Cấp Đơn Tệp (Single-File Failure Isolation)

- **Cơ chế:** Trong `main.py`, hàm `execute_single_file_pipeline()` bọc toàn bộ 4 giai đoạn xử lý trong khối `try...except` diện rộng, bẫy đích danh các lỗi `FileNotFoundError`, `UnicodeDecodeError`, `ValueError`, `TypeError`, `OSError`, `RuntimeError`.

- **Tác động:** Khi phát hiện một tệp bị hỏng nhị phân hoặc sai định dạng, hệ thống ghi nhận sự cố ra Terminal, trả về `False` và lập tức chuyển sang biên dịch tệp tiếp theo trong danh sách chờ.

#### Tầng 2: Rào chắn Lược đồ DTO & Dynamic Unpacking (Schema Barrier & Unpacking)

- **Cơ chế:** Trước khi khởi chạy pipeline, hàm `load_configuration()` thực thi ép củng kiểu dữ liệu qua `AppConfig.model_validate()`. Hàm `execute_single_file_pipeline` giải nén từ điển `**config.heading_retention_depth.model_dump()` trực tiếp vào `HTMLRenderer`.

- **Tác động:** Nếu tham số `max_bookmark_level` trong YAML bị sửa thành giá trị vi phạm (như cấp `10`), trang trí `@field_validator` sẽ ngắt tiến trình trong dưới 500ms và bắn thông báo `ValidationError` chi tiết. Cơ chế giải nén động triệt tiêu 100% rủi ro bỏ quên biến cấu hình.

#### Tầng 3: Phòng thủ Băm Mật mã Chống Va chạm Regex (Cryptographic Masking Defense)

- **Cơ chế:** Trong `src/ast_parser.py` và `src/html_renderer.py`, hàm `_unify_math_delimiters()` tạo mặt nạ bảo vệ Code Block bằng thuật toán `hashlib.sha256()`.

- **Tác động:** Khóa giữ chỗ `__CRYPTO_MASK_{hash}_{counter}__` vô hiệu hóa hoàn toàn mọi nỗ lực tiêm chuỗi giả mạo nhằm đánh sập Cây Cú pháp Trừu tượng (AST).

#### Tầng 4: Bộ Nhớ Tạm Vô Danh & Khiên Security Sandbox (Ephemeral Memory & Security Sandbox)

- **Cơ chế:** Trong `src/pdf_compiler.py`, tệp HTML trung gian được khởi tạo bằng `tempfile.NamedTemporaryFile`. Trình duyệt Playwright Chromium chạy trong chế độ Security Sandbox cô lập.

- **Tác động:** Nhờ tài nguyên KaTeX đã được nhúng nội tuyến (Inline Embedding) ở Giai đoạn 2, Chromium không cần đọc tệp cục bộ bên ngoài. Việc gỡ bỏ cờ `--disable-web-security` giúp ngăn chặn triệt tiêu các đòn tấn công đọc lén hệ thống tệp (Local File Inclusion / XSS) qua mã Markdown độc hại.

#### Tầng 5: Giới hạn Ngoại lệ Có Chủ đích tại Mô-đun Tiêm Nhị phân (Targeted Exception Containment)

- **Cơ chế:** Trong `src/pdf_metadata_injector.py`, phương thức `inject_metadata()` chỉ bẫy chính xác 3 nhóm lỗi `(OSError, RuntimeError, ValueError)`.

- **Tác động:** Tuân thủ quy chuẩn `BLE001` của Ruff Linter, triệt tiêu rủi ro nuốt chửng ngoại lệ hệ thống (`blind-except`), bảo toàn vệt vết Traceback phục vụ gỡ lỗi nâng cao.

---

## CHƯƠNG 6: MA TRẬN KIỂM THỬ ĐỐI KHÁNG RED-TEAM HỘP TRẮNG (RED-TEAMING MATRIX v1.6.0)

Tệp `tests/red_team_tests.py` đóng vai trò là **Phòng Thử nghiệm Va chạm Vật lý**. 13 kịch bản kiểm thử hộp trắng (**White-box Unit Tests**) được thiết kế để chủ động tiêm dữ liệu độc hại, phá hoại cấu trúc, ép tải đa tiến trình và kiểm tra tính toàn vẹn của siêu dữ liệu nhị phân nhằm xác minh độ kiên cố của hệ thống.

---

### PHÂN TÍCH CHI TIẾT 13 KỊCH BẢN KIỂM THỬ ĐỐI KHÁNG (v1.6.0)

#### Kịch bản 1: Kiểm thử Xung đột Ký tự Đa ngôn ngữ (`test_scenario_1_bilingual_encoding_stress_test`)

- **Mục tiêu:** Kiểm tra khả năng chịu tải mã hóa Unicode Tiếng Việt có dấu kết hợp các toán tử logic nhị phân (`a < b && c > d`) và chuỗi biểu thức chính quy [Regex].
- **Phương pháp:** Ép `ASTParser` và `HTMLRenderer` xử lý chuỗi văn bản phức tạp chứa ký tự đặc biệt.
- **Kết quả kỳ vọng:** Văn bản Tiếng Việt không bị vỡ font, các ký tự so sánh logic không làm rò rỉ hoặc hỏng thẻ bọc HTML.

#### Kịch bản 2: Giả lập Tiêu đề Giả mạo trong Code Block (`test_scenario_2_heading_spoofing_simulation`)

- **Mục tiêu:** Bẫy đánh lừa bộ bóc tách tiêu đề bằng cách đưa chuỗi `## Tiêu đề Giả mạo` vào bên trong khối mã nguồn Python (`code fence`).
- **Phương pháp:** Quét chuỗi HTML đầu ra của `HTMLRenderer`.
- **Kết quả kỳ vọng:** Thẻ `<h2 data-level="2">` chỉ sinh ra cho tiêu đề thật, khối mã nguồn cô lập hoàn toàn tiêu đề giả mạo không cho sinh mỏ neo.

#### Kịch bản 3: Thử nghiệm Tràn lề Vật lý Chuỗi Mã Cực dài (`test_scenario_3_physical_overflow_destructive_test`)

- **Mục tiêu:** Tiêm một chuỗi mã liền mạch 1.500 ký tự `X` không chứa khoảng trắng để thử nghiệm ranh giới lề giấy A4.
- **Phương pháp:** Đẩy dữ liệu qua `PDFCompiler` để Playwright kết xuất tệp PDF vật lý.
- **Kết quả kỳ vọng:** Quy tắc CSS `overflow-wrap: break-word` tự động ngắt dòng tự nhiên, xuất bản tệp PDF thành công mà không làm tràn văn bản khỏi lề giấy A4.

#### Kịch bản 4: Xử lý Thư mục Đầu vào Rỗng (`test_scenario_4_empty_directory_handling`)

- **Mục tiêu:** Kiểm tra phản ứng phòng thủ của hệ thống khi thư mục `input/` hoàn toàn trống rỗng không có tệp `.md`.
- **Phương pháp:** Kích hoạt hàm `batch_process_directory()` trên không gian làm việc rỗng.
- **Kết quả kỳ vọng:** Hệ thống hiển thị nhật ký hướng dẫn và kết thúc tiến trình an toàn mà không ném ngoại lệ ngắt luồng.

#### Kịch bản 5: Kiểm thử Cô lập Tệp Hỏng Nhị phân (`test_scenario_5_batch_fault_isolation`)

- **Mục tiêu:** Đưa 1 tệp chứa chuỗi byte hỏng `\x80\x81\xfe\xff\xff` xen giữa 2 tệp Markdown hợp lệ.
- **Phương pháp:** Chạy toàn bộ danh sách qua hàm `execute_single_file_pipeline()`.
- **Kết quả kỳ vọng:** Tệp hợp lệ xuất bản PDF thành công; tệp hỏng bị bẫy lỗi cô lập, không làm dừng tiến trình biên dịch của các tệp còn lại.

#### Kịch bản 6: Tự động Tái tạo Cấu trúc Thư mục Con (`test_scenario_6_subfolder_structure_preservation`)

- **Mục tiêu:** Kiểm tra khả năng bảo tồn và tái tạo cây phân tầng thư mục con phức tạp (Ví dụ: `input/du_an/chuyen_de_1/bao_cao.md`).
- **Phương pháp:** Thực thi quét đệ quy và đối chiếu đường dẫn PDF đầu ra.
- **Kết quả kỳ vọng:** Tệp PDF thành phẩm xuất hiện chính xác tại vị trí `output/du_an/chuyen_de_1/bao_cao.pdf`.

#### Kịch bản 7: Kết xuất KaTeX Đa Tiêu chuẩn & Vĩ lệnh Phức tạp (`test_scenario_7_math_rendering_and_fault_tolerance`)

- **Mục tiêu:** Đúc đồng thời Plain TeX (`$$`), LaTeX2e (`\[...\]`), KaTeX Web Standard và các vĩ lệnh ma trận phức tạp `\boxed`, `\xrightarrow`.
- **Phương pháp:** Chạy qua Playwright Chromium và xác minh phần tử DOM `.katex`.
- **Kết quả kỳ vọng:** Trình duyệt đúc thành công công thức toán vector sắc nét, xuất bản tệp PDF có dung lượng lớn hơn 0 bytes.

#### Kịch bản 8: Nhận diện và Cấu trúc hóa Bảng GFM (`test_scenario_8_gfm_table_parsing_and_structure`)

- **Mục tiêu:** Kiểm tra khả năng bóc tách và tạo khung lưới cho bảng GFM chứa cú pháp căn lề `| :--- |`.
- **Phương pháp:** Kiểm tra danh sách Token AST và cấu trúc HTML `<table>`.
- **Kết quả kỳ vọng:** AST Parser sinh đầy đủ các Token `table_open`, `thead_open`, `tr_open`; HTMLRenderer kết xuất bảng với thuộc tính căn lề và đường viền 1pt chuẩn mực.

#### Kịch bản 9: Cắt Lề Bảng Cực Rộng Quá Khổ A4 (`test_scenario_9_table_overflow_clipping_and_logging`)

- **Mục tiêu:** Tiêm một bảng Markdown gồm 25 cột dữ liệu vượt quá độ rộng vùng in an toàn 170mm của khổ giấy A4.
- **Phương pháp:** Đẩy dữ liệu qua `PDFCompiler` để kiểm tra chiến lược `overflow_strategy: "clip_and_warn"`.
- **Kết quả kỳ vọng:** Lớp giáp CSS tự động cắt phần thừa tràn lề, bảo vệ thẩm mỹ bản in mà không làm ngắt tiến trình.

#### Kịch bản 10: Quy chuẩn Học thuật APA & Chống Ngắt Trang (`test_scenario_10_academic_apa_profile_and_break_avoidance`)

- **Mục tiêu:** Xác minh chỉ thị chống ngắt trang xẻ đôi khối mã nguồn và bảng biểu theo chuẩn APA.
- **Phương pháp:** Biên dịch văn bản qua `PDFCompiler` với cờ `active_standard: "apa"`.
- **Kết quả kỳ vọng:** Bảng StyleSheet CSS áp dụng thành công chỉ thị `orphans: 2; widows: 2;` và `break-inside: avoid;`.

#### Kịch bản 11: Đo lường Độ trễ Chặn đứng của Pydantic DTO (`test_scenario_11_schema_validation_hard_block_and_latency`)

- **Mục tiêu:** Kiểm tra phản ứng ngắt mạch và đo độ trễ khi tệp YAML khai báo tham số vi phạm `max_bookmark_level: 10`.
- **Phương pháp:** Nạp tệp YAML lỗi qua `load_configuration()` và tính thời gian phản hồi bằng `time.time()`.
- **Kết quả kỳ vọng:** Pydantic DTO kích hoạt ngoại lệ `ValidationError` chặn đứng tiến trình với thời gian trễ dưới **500ms**.

#### Kịch bản 12: Ép Tải Đa Tiến Trình Cách Ly Bộ Nhớ Vật Lý (`test_scenario_12_ephemeral_memory_concurrency_stress` - NÂNG CẤP v1.6.0)

- **Mục tiêu:** Chứng minh kiến trúc **Đa tiến trình Vật lý (`ProcessPoolExecutor`)** triệt tiêu 100% sự cố sập Vòng lặp Sự kiện (Event Loop Crash) và va chạm bộ nhớ tạm khi Playwright Chromium vận hành song song.
- **Phương pháp:** Sử dụng `ProcessPoolExecutor` từ thư viện `concurrent.futures`, phân bổ 10 công việc xuất bản PDF đồng thời cho 4 tiến trình worker độc lập (`_worker_compile_process_task`). Mỗi tiến trình tự khởi tạo một thể hiện Chromium và Event Loop riêng biệt.
- **Kết quả kỳ vọng:** Toàn bộ 10/10 tiến trình xuất bản PDF thành công, tỷ lệ va chạm bộ nhớ 0%, không có ngoại lệ Event Loop.

#### Kịch bản 13: Kiểm định Nhị phân Cây Mục lục Bookmarks Cấp 6 (`test_scenario_13_post_processing_metadata_outline_verification` - NÂNG CẤP v1.6.0)

- **Mục tiêu:** Quét nhị phân chếu xác nhận Cây Mục lục (Outline Tree / Bookmarks) thực sự được tiêm trọn vẹn từ Heading Cấp 1 đến **Heading Cấp 6** vào tệp PDF[cite: 5, 6].
- **Phương pháp:** Biên dịch PDF phẳng, thực thi tiêm siêu dữ liệu bằng `MetadataInjector(max_bookmark_level=6)`, dùng động cơ **PyMuPDF (`fitz.open()`)** đọc lại mảng `get_toc()`.
- **Kết quả kỳ vọng:** Mảng TOC trả về chính xác 6 nút phân cấp. Khẳng định `self.assertEqual(toc[4][0], 5)` xác nhận Mức 5 và `self.assertEqual(toc[5][0], 6)` xác nhận Mức 6 xuất hiện hợp lệ trong gáy siêu dữ liệu nhị phân PDF.

---

### QUY TRÌNH THỰC THI KIỂM THỬ TRÊN TERMINAL

Để tránh lỗi phân giải Không gian tên Mô-đun (`ModuleNotFoundError`) trên Windows PowerShell, người dùng nên thực thi tệp kiểm thử trực tiếp bằng lệnh dưới đây:

```powershell
# ==============================================================================
# QUY TRÌNH THỰC THI BỘ KIỂM THỬ RED-TEAM HỘP TRẮNG (POWERSHELL v1.6.0)
# ==============================================================================

# Kích hoạt môi trường ảo Python
.\venv\Scripts\Activate.ps1

# Thực thi trực tiếp kịch bản kiểm thử đối kháng
python tests/red_team_tests.py

```

**Kết quả kỳ vọng khi 13 kịch bản đều vượt qua 100%:**

```text
.............
----------------------------------------------------------------------
Ran 13 tests in 3.450s

OK

```

---

## CHƯƠNG 7: LỊCH SỬ PHIÊN BẢN (CHANGELOG v1.6.0)

### Phiên bản v1.6.0 (Bản Nâng cấp Hiện tại - Expanded Bookmark Depth & Dynamic Routing)

- **Mở rộng Lược đồ Dấu trang Cấp 6:** Nâng tham số `max_bookmark_level` trong `config/settings.yaml` và `main.py` từ 4 lên 6. Mở rộng khả năng điều hướng ẩn cho Cây Mục lục PDF mà không vi phạm quy tắc đánh số APA.

- **Truyền dẫn Dữ liệu Động (Dynamic Sub-Schema Unpacking):** Tái cấu trúc hàm `execute_single_file_pipeline` trong `main.py`. Áp dụng cú pháp giải nén từ điển `**config.heading_retention_depth.model_dump()`, bảo đảm `enable_heading_anchors` và `normalize_anchor_ascii` truyền chảy trôi chảy vào `HTMLRenderer`.

- **Đóng gói Tài nguyên Nội tuyến (Inline Asset Embedding):** Viết lại hàm `_generate_katex_assets_and_script` trong `src/html_renderer.py`. Đọc trực tiếp chuỗi thô của `katex.min.css`, `katex.min.js`, và `auto-render.min.js` qua `Path.read_text()` và nhúng trực tiếp vào thẻ `<style>` và `<script>` nội tuyến.

- **Nội suy Cờ Logic KaTeX Động:** Xóa bỏ giá trị gán cứng `strict: false` và `throwOnError: false` trong JavaScript. Trực tiếp nội suy chuỗi boolean động từ biến DTO `self.katex_config`.

- **Khiên An ninh Trình duyệt (Security Sandbox Activation):** Gỡ bỏ hoàn toàn bộ 3 cờ hạ bảo mật (`--disable-web-security`, `--allow-file-access-from-files`, `--no-sandbox`) trong `src/pdf_compiler.py`. Playwright Chromium hiện biên dịch tài liệu trong môi trường Sandbox cô lập tuyệt đối.

- **Tách rời CSS Counters & Độc lập Typography:** Giới hạn CSS Counters ở cấp 4 trong `_generate_css_counters()`, đồng thời giữ định dạng Bold/Italic cho H5 và H6 trong `_build_paged_media_css()` hoàn toàn độc lập với chỉ số thứ tự.

- **Đa tiến trình Độc lập (Multiprocessing Concurrency):** Thay thế `ThreadPoolExecutor` bằng `ProcessPoolExecutor` trong Kịch bản 12 của `tests/red_team_tests.py`. Cấp phát Vòng lặp Sự kiện (Event Loop) riêng biệt cho từng Chromium worker, triệt tiêu lỗi sập bộ nhớ.

- **Phong tỏa 100% I/O Git (Zero-Trust Git Isolation):** Loại bỏ ngoại lệ `!input/input_sample.md` trong `.gitignore`. Thư mục `input/` bị chặn tuyệt đối để bảo vệ dữ liệu cá nhân của người dùng.

- **Tối ưu hóa PEP 3120 (Ruff UP012 Compliant):** Lược bỏ các đối số `"utf-8"` thừa thãi trong lệnh `.encode()` tại `src/html_renderer.py`, tận dụng luồng mã hóa C nội tại của Python 3.

### Phiên bản v1.5.3 (Bản Nâng cấp Metadata Injector & Strict Schema)

- **Ép củng Lược đồ DTO (Pydantic v2):** Thay thế toàn bộ phương thức truy xuất `.get()` thô trong `main.py` bằng mô hình Pydantic DTO (`AppConfig`).

- **Băm Mật mã SHA-256 (Cryptographic Masking):** Nâng cấp hàm `_unify_math_delimiters()` trong `src/ast_parser.py` và `src/html_renderer.py` bằng `hashlib.sha256()`.

- **Không gian Bộ nhớ Dùng Một lần (Ephemeral File System):** Tích hợp `tempfile.NamedTemporaryFile` trong `src/pdf_compiler.py`.

- **Tiêm Siêu dữ liệu Hậu kỳ (Metadata Injector):** Xây dựng mô-đun `src/pdf_metadata_injector.py` dựa trên `PyMuPDF` (`fitz`).

### Phiên bản v1.4.3 (Playwright Chromium & KaTeX Engine)

- Chuyển đổi từ `WeasyPrint` sang động cơ trình duyệt không đầu **Playwright Chromium** kết hợp bộ đúc DOM **KaTeX Offline**.

- Triển khai lớp giáp CSS cưỡng chế căn lề trái `text-align: left !important`.

### Phiên bản v1.3.2 (GFM Tables & APA Academic Profile)

- Tích hợp bộ phân tích bảng biểu GFM (`gfm-like`) và chiến lược cắt lề bảng quá khổ `clip_and_warn`.

- Áp dụng ma trận quy chuẩn in ấn học thuật quốc tế APA 7th.

### Phiên bản v1.0.0 (Bản Khởi tạo Nền tảng)

- Hoàn thiện luồng pipeline 3 giai đoạn ngoại tuyến (Offline-first): `ASTParser` -> `HTMLRenderer` -> `PDFCompiler`.

---
