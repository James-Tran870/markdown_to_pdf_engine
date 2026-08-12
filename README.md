# MARKDOWN TO PDF ENGINE (Lõi Biên dịch Tài liệu Cục bộ & Kiến trúc Động cơ Toán học Lai - Phiên bản v2.3.0)

Một hệ thống đường ống dữ liệu (**Data Pipeline**) tự động hóa toàn diện, chuyên trách chuyển đổi hàng loạt tệp Markdown phức tạp sang định dạng PDF chuẩn Typography xuất bản. Hệ thống tích hợp **Kiến trúc Động cơ Toán học Lai (Hybrid Math Engine Architecture)** cho phép rẽ nhánh giữa đúc DOM KaTeX tốc độ cao và đúc Đồ họa Vector SVG MathJax v3 sắc nét, bảng biểu GFM khung lưới hoàn chỉnh, cùng cây mỏ neo điều hướng **Bookmarks nhị phân Cấp 6** ngay trên môi trường Windows 11 cục bộ.

Dự án được xây dựng dựa trên tư duy phân tách hệ thống nghiêm ngặt (**Separation of Concerns - SoC**), khép kín và độc lập ngoại tuyến (**Offline-first**). Hệ thống nói KHÔNG với các dịch vụ đám mây (Cloud API), máy chủ web bên ngoài hay cơ sở dữ liệu phức tạp. Mọi tiến trình biên dịch đều diễn ra hoàn toàn trên máy cục bộ, bảo đảm tính bảo mật dữ liệu tuyệt đối và khả năng can thiệp tham số linh hoạt thông qua hệ thống cấu hình DTO Pydantic v2 tách biệt.

---

## CHƯƠNG 1: TRIẾT LÝ KIẾN TRÚC VÀ 7 TRỤ CỘT PHÒNG THỦ (ARCHITECTURAL PHILOSOPHY v2.3.0)

Để hình dung phương thức vận hành của hệ thống, hãy tưởng tượng dự án giống như một **Xưởng In ấn Đồ họa Hiện đại Khép kín**. Thay vì cho phép công nhân tự do can thiệp thủ công vào dây chuyền, xưởng vận hành dựa trên 7 trụ cột kiến trúc bất biến nhằm loại trừ hoàn toàn mọi rủi ro gián đoạn tiến trình hay đứt gãy mỹ thuật:

### 1. Phân tách Mối quan tâm (SoC) & Truyền dẫn Dữ liệu Động (Pydantic DTO & Dynamic Unpacking - v2.3.0)

- **Ẩn dụ đời thực:** Trong một xưởng đúc phim điện ảnh, Trình chiếu phim (Mã logic Python) không bao giờ tự mình điều chỉnh độ sáng hay phông chữ của phụ đề; nó hoạt động dựa trên một tệp kịch bản định dạng do Đạo diễn thiết lập. Khi cần đổi kiểu chữ hay độ phân giải, Đạo diễn chỉ việc sửa kịch bản mà không cần tháo lắp máy chiếu.

- **Áp dụng vào hệ thống:** Tách rời hoàn toàn tham số điều khiển khỏi mã nguồn xử lý chính. Mọi tiến trình biên dịch đều nạp cấu hình từ tệp YAML chuyên biệt (`config/settings.yaml`). Toàn bộ dữ liệu cấu hình được chuyển đổi thành các **Data Transfer Objects (DTO)** tĩnh thông qua thư viện **Pydantic v2**. Hàm điều phối `execute_single_file_pipeline` sử dụng cú pháp giải nén từ điển động `**app_config.heading_retention_depth.model_dump()`, bảo đảm các tham số như `enable_heading_anchors` tự động chảy trôi chảy vào `HTMLRenderer` mà không bị trôi dạt. Quy tắc chặn đứng (**Hard-Block Rule**) được thiết lập để hủy bỏ tiến trình ngay lập tức nếu tham số `max_bookmark_level` vượt quá giới hạn vật lý cấp 6.

### 2. Kiến trúc Băm Mật mã Bảo vệ Khối Mã (SHA-256 Cryptographic Masking - v2.3.0)

- **Ẩn dụ đời thực:** Khi lưu trữ linh kiện quý trong kho, thay vì dán một con tem giấy ngẫu nhiên dễ bị kẻ gian làm giả để đánh tráo linh kiện, thủ kho sử dụng một **Mã băm Niêm phong Mật mã** được tính toán trực tiếp từ trọng lượng, kích thước và mã số của chính linh kiện đó.

- **Áp dụng vào hệ thống:** Trong quá trình đồng bộ hóa cú pháp toán học TeX/LaTeX2e, hệ thống cần dán mặt nạ bảo vệ các khối mã nguồn (`code fence`) để tránh việc Biểu thức Chính quy (Regex) can thiệp sai. Hệ thống áp dụng thuật toán băm mật mã **`hashlib.sha256()`**. Khóa giữ chỗ `__CRYPTO_MASK_{hash}_{counter}__` được tính toán trực tiếp từ nội dung khối mã, chuỗi muối ngẫu nhiên và bộ đếm cục bộ, triệt tiêu 100% rủi ro va chạm Regex (**Regex Collision Attack**) do chuỗi mã đầu vào chứa ký tự đặc biệt.

### 3. Bộ Nhớ Tạm Vô Danh & Cách Ly Tiến Trình Đa Nhiệm (Process Isolation & Ephemeral Memory - v2.3.0)

- **Ẩn dụ đời thực:** Khi các bác sĩ phẫu thuật làm việc, thay vì dùng chung một bàn dụng cụ cố định ngoài hành lang (dễ gây nhiễm khuẩn chéo giữa các ca mổ), mỗi ca mổ được cấp một **Phòng phẫu thuật Khép kín Dùng Một lần**. Khi ca mổ kết thúc, toàn bộ thiết bị tạm thời được tự động thu hồi và tiêu hủy ngay lập tức.

- **Áp dụng vào hệ thống:** Module `src/pdf_compiler.py` tích hợp công cụ `tempfile.NamedTemporaryFile` của Hệ điều hành, phân bổ một không gian bộ nhớ tạm ẩn danh hoàn toàn độc lập cho mỗi tiến trình. Toàn bộ kiến trúc kiểm thử đa nhiệm vận hành trên mô hình **Đa tiến trình Vật lý (`ProcessPoolExecutor`)**. Việc tách tiến trình vật lý cung cấp cho mỗi thể hiện Playwright Chromium một **Vòng lặp Sự kiện (Event Loop)** riêng biệt, triệt tiêu 100% rủi ro va chạm bộ nhớ và lỗi sập Event Loop.

### 4. Tiêm Siêu dữ liệu Hậu kỳ & Dấu trang Cấp 6 (Post-Processing Metadata Injection - v2.3.0)

- **Ẩn dụ đời thực:** Một cuốn sách giáo khoa sau khi được máy in đúc ra toàn bộ hình ảnh và chữ viết sắc nét trên giấy phẳng, sẽ được chuyển sang **Phân xưởng Đóng bìa & Dán Dấu trang**. Tại đây, người thợ đính thêm các thẻ phân đoạn bằng nhựa vào gáy sách giúp độc giả lật mở nhanh từng chương.

- **Áp dụng vào hệ thống:** Động cơ Chromium Headless chỉ xuất bản bản in đồ họa phẳng và từ chối biên dịch thuộc tính CSS `bookmark-label` thành cây điều hướng PDF nhị phân. Mô-đun hậu kỳ `src/pdf_metadata_injector.py` bóc tách Cây Cú pháp Trừu tượng (AST) từ các thẻ `<hX data-level="...">`, sử dụng thư viện **PyMuPDF (`fitz`)** quét nhị phân tệp PDF phẳng, nội suy tọa độ trang vật lý và tiêm trực tiếp **Cây Mục lục (Outline Tree / Bookmarks)** đến tận **Heading Cấp 6** vào lớp siêu dữ liệu nhị phân.

### 5. Đóng Gói Tài Nguyên Nội Tuyến & Khiên An Ninh Trình Duyệt (Inline Asset Embedding & Security Sandbox - v2.3.0)

- **Ẩn dụ đời thực:** Thay vì cho phép tài xế xe tải liên tục mở cổng bảo vệ xưởng in để đi ra ngoài lấy vật tư (dễ bị kẻ gian đột nhập), người quản xưởng đóng gói toàn bộ bản thiết kế, mực in và giấy vẽ vào bên trong thùng xe niêm phong ngay trước khi xe xuất phát.

- **Áp dụng vào hệ thống:** Mô-đun `src/html_renderer.py` sử dụng phương thức `Path.read_text()` đọc trực tiếp nội dung chuỗi thô của các tệp tĩnh KaTeX và MathJax. Nội dung này được nhúng trực tiếp vào giữa cặp thẻ `<style>` và `<script>` nội tuyến trong HTML. Nhờ đó, `src/pdf_compiler.py` loại bỏ hoàn toàn các cờ hạ bảo mật, giúp Playwright Chromium biên dịch đồ họa trong môi trường **Security Sandbox** cô lập tuyệt đối mà không cần quyền truy cập ổ đĩa tự do.

### 6. Ma trận In ấn Học thuật & Rào Chắn Đồ Họa Vector SVG (Academic Standards & SVG Boundaries - v2.3.0)

- **Ẩn dụ đời thực:** Khi xuất bản một ấn phẩm khoa học, nếu một hình vẽ sơ đồ hoặc biểu thức toán học có kích thước phình to bất thường, người thợ đóng khung sẽ dán một **Khung Rào Chắn Định Hình (Boundary Frame)** ép đối tượng đó tự động co rút vừa vặn với chiều rộng khổ trang giấy mà không làm xô lệch các dòng chữ xung quanh.

- **Áp dụng vào hệ thống:** Tích hợp bộ quy chuẩn học thuật quốc tế (APA 7th, IEEE). Bổ sung hệ thống rào chắn CSS Paged Media dành riêng cho Đồ họa Vector SVG sinh ra từ động cơ MathJax v3: `mjx-container[jax="SVG"] svg { max-width: 100% !important; height: auto !important; }`. Quy tắc này ép các công thức toán khối dài tự động thu nhỏ vừa vặn trong khung in an toàn 170mm của khổ A4, triệt tiêu 100% sự cố tràn lề và lỗi ngắt mạch thời gian (`PlaywrightTimeoutError`).

### 7. Động Cơ Toán Học Lai & Thuật Toán Bóc Tách Tiếng Việt Máy Chủ (Hybrid Math Engine & Python Dictionary Mapping - v2.3.0)

- **Ẩn dụ đời thực:** Trong một xưởng chế tác kim hoàn, đối với các chi tiết trang trí tiêu chuẩn thông thường, xưởng sử dụng máy đúc tự động dập nhanh; nhưng đối với các biểu tượng chứa văn bản đa ngữ phức tạp, xưởng sẽ tách riêng phần văn bản ra cho thợ khắc chữ xử lý riêng rồi mới hoán đổi gắn trả lại vào khung vàng.

- **Áp dụng vào hệ thống:** Thiết lập cờ rẽ nhánh `active_engine` trong `math_engine_routing`:

- **Nhánh `katex_placeholder` (Mặc định):** Kết hợp động cơ KaTeX với thuật toán **Server-side Python Dictionary Mapping & Client-side Swap**. Python quét các vĩ lệnh `\text{...}` chứa Tiếng Việt có dấu, bóc tách văn bản thô lưu vào từ điển JSON `self.vn_math_store` và thế bằng mã ASCII giữ chỗ `VILANGMASK0001`. Sau khi KaTeX đúc DOM cực nhanh, JavaScript Hậu kỳ duyệt các Nút văn bản (Text Nodes) và hoán đổi trả lại chuỗi Tiếng Việt nguyên khối. Cơ chế này giúp trình duyệt Chromium áp dụng bộ xếp chữ HarfBuzz bản địa, giải quyết triệt để lỗi Vòng đời DOM (Race Condition) làm vỡ kerning và bay dấu lơ lửng.

- **Nhánh `mathjax_svg` (Dự phòng nâng cao):** Khởi tạo môi trường MathJax v3 đúc biểu thức thành đồ họa Vector SVG sắc nét, đáp ứng các tài liệu chứa dòng diễn giải toán học siêu phức tạp.

---

## CHƯƠNG 2: BẢN ĐỒ CẤU TRÚC THƯ MỤC (DIRECTORY BLUEPRINT v2.3.0)

Dưới đây là sơ đồ không gian làm việc (**Workspace**) tiêu chuẩn trên Visual Studio Code. Mỗi thành phần đều duy trì ranh giới trách nhiệm duy nhất (**Single Responsibility Principle - SoC**):

```text
MARKDOWN_TO_PDF_ENGINE/
│
├── assets/                    # [Kho Tài Nguyên Tĩnh Offline] Chứa tài nguyên kết xuất đồ họa KaTeX và MathJax.
│   ├── katex/                 # Bảng CSS, thư viện JS và bộ phông chữ toán học .woff2 ngoại tuyến.
│   │   ├── fonts/             # Bộ phông chữ vector KaTeX (AMS, Main, Math, Size1).
│   │   ├── katex.min.css      # Định hình kiểu dáng và cấu trúc đồ họa công thức KaTeX.
│   │   ├── katex.min.js       # Động cơ phân tích cú pháp LaTeX client-side.
│   │   └── auto-render.min.js # Script tự động quét và đúc DOM toán học ($/$$/\[/\]).
│   └── mathjax/               # Thư viện đồ họa Vector SVG MathJax v3 ngoại tuyến.
│       └── tex-svg.js         # Động cơ đúc biểu thức TeX sang thẻ Đồ họa Vector <svg>.
│
├── config/
│   └── settings.yaml          # [Bảng Điều Khiển Trung Tâm] Khai báo 13 phân khu cấu hình DTO & Math Routing.
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
│   ├── html_renderer.py       # (Giai đoạn 2) Python Dictionary Mapping, tiêm MathJax/KaTeX Inline & tạo mỏ neo.
│   ├── pdf_compiler.py        # (Giai đoạn 3) Cấp phát tempfile vô danh, rào chắn SVG boundaries & xuất bản PDF.
│   └── pdf_metadata_injector.py # (Giai đoạn 4) Quét nhị phân PyMuPDF, nội suy vị trí & tiêm Bookmarks Cấp 6.
│
├── tests/                     # [Bộ Kiểm Thử Mô-đun Pytest] Hệ thống 6 tệp test hộp trắng biệt lập.
│   ├── __init__.py            # Khởi tạo gói kiểm thử.
│   ├── test_01_core_pipeline.py     # [Test 01] Kiểm thử I/O, quét đệ quy, cô lập tệp hỏng & batch processing.
│   ├── test_02_schema_layout.py     # [Test 02] Kiểm thử Pydantic DTO, YAML validation & A4 margin rules.
│   ├── test_03_math_base64.py       # [Test 03] Kiểm thử KaTeX Placeholder Swap, MathJax SVG & Unicode Tiếng Việt.
│   ├── test_04_document_features.py # [Test 04] Kiểm thử GFM Tables, APA Standards & PyMuPDF Bookmarks Level 6.
│   ├── test_05_concurrency_stress.py# [Test 05] Kiểm thử ProcessPoolExecutor, tempfile bộ nhớ tạm & Playwright.
│   └── test_06_hybrid_math_engine.py# [Test 06] Kiểm thử DTO Routing Validation, Python Mapping & SVG Boundaries.
│
├── .gitignore                 # Chỉ thị phòng thủ Git cách ly 100% I/O, bộ nhớ đệm Ruff, pytest, tempfile và venv.
├── main.py                    # [Quản Đốc Băng Chuyền] Điều phối Pipeline, xác thực Pydantic DTO & Unpacking DTO.
├── README.md                  # Cẩm nang vận hành và bản thiết kế kiến trúc toàn diện v2.3.0.
└── requirements.txt           # Bảng kê vật tư thư viện phụ thuộc (Playwright, Pydantic v2, PyMuPDF, Pytest).

```

### Phân tích Chức năng Chi tiết Từng Thành phần Mã nguồn (v2.3.0)

- **`assets/katex/` & `assets/mathjax/**`: Kho lưu trữ bộ tài nguyên tĩnh ngoại tuyến của KaTeX và MathJax v3. Đảm bảo hệ thống biên dịch công thức toán sắc nét 100% mà không cần kết nối Internet.

- **`config/settings.yaml`**: Trái tim cấu hình của dự án. Quản lý 13 phân khu tham số, bao gồm hai phân khu rẽ nhánh mới `math_engine_routing` và `mathjax_offline_config`.

- **`main.py`**: Quản đốc điều phối toàn bộ đường ống. Nạp tệp YAML qua `load_configuration()`, thực thi ép củng Lược đồ DTO qua Pydantic v2, trích xuất từ điển DTO `math_routing_config` và `mathjax_config` qua `.model_dump()` và truyền hạ nguồn.

- **`src/ast_parser.py`**: Đảm nhiệm **Giai đoạn 1**. Sử dụng `markdown-it-py` với preset `gfm-like`. Áp dụng cơ chế Băm Mật mã SHA-256 (`_unify_math_delimiters`) để che phủ khối mã nguồn và chuyển đổi cú pháp Brackets (`\[...\]`) sang Dollars (`$$`).

- **`src/html_renderer.py`**: Đảm nhiệm **Giai đoạn 2**. Nạp nội dung thô CSS/JS KaTeX hoặc MathJax v3. Thực thi thuật toán **Server-Side Python Dictionary Mapping** bóc tách Tiếng Việt có dấu trong `\text{...}` thành từ điển `self.vn_math_store` và nhét mã ASCII giữ chỗ `VILANGMASK0001`. Tiêm script Client-side hoán đổi Text Nodes Hậu kỳ.

- **`src/pdf_compiler.py`**: Đảm nhiệm **Giai đoạn 3**. Cấp phát tệp tạm vô danh qua `tempfile.NamedTemporaryFile`. Khởi chạy Playwright Chromium trong môi trường **Security Sandbox** an toàn. Bổ sung rào chắn Paged Media CSS `mjx-container[jax="SVG"] svg { max-width: 100% }` khống chế lề A4.

- **`src/pdf_metadata_injector.py`**: Đảm nhiệm **Giai đoạn 4**. Tiếp nhận chuỗi HTML trung gian, bóc tách cấu trúc thẻ `<hX data-level="...">` từ Cấp 1 đến Cấp 6, sử dụng **PyMuPDF (`fitz`)** quét vị trí văn bản trên PDF vật lý và tiêm Cây Mục lục nhị phân.

- **`tests/test_01_*.py` đến `test*06*\*.py**`: Hệ thống bộ kiểm thử mô-đun biệt lập vận hành bởi `pytest`. Thay thế tệp đơn khối `red_team_tests.py` cũ, giúp cách ly điểm gãy và tăng tốc độ gỡ lỗi lên gấp nhiều lần.

---

## CHƯƠNG 3: HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG VÀ HẠ TẦNG THỰC THI (ENVIRONMENT & INFRASTRUCTURE v2.3.0)

Chương này hướng dẫn chi tiết quy trình thiết lập Môi trường ảo (**Virtual Environment**), cài đặt bộ thư viện phụ thuộc mới nhất bao gồm **Pydantic v2**, **PyMuPDF**, **Playwright Chromium**, và bộ khung kiểm thử mô-đun **Pytest**.

---

### 1. YÊU CẦU HỆ THỐNG VÀ CÁC THÀNH PHẦN NỀN TẢNG (SYSTEM PREREQUISITES)

Để hạ tầng biên dịch tài liệu vận hành ổn định và đạt hiệu năng tối đa, không gian làm việc cục bộ cần đáp ứng các điều kiện tiêu chuẩn sau:

- **Hệ điều hành:** Microsoft Windows 10 hoặc Windows 11 64-bit (Khuyên dùng Windows 11 phiên bản 22H2/23H2 trở lên).
- **Môi trường Trình thông dịch Python:** Python phiên bản **3.10** trở lên (Khuyên dùng Python 3.11 hoặc 3.12 để tối ưu hóa tốc độ xử lý Pydantic DTO và mã hóa chuỗi UTF-8).

- **Trình biên tập Mã nguồn (IDE):** Visual Studio Code (VSCode) tích hợp các công cụ kiểm tra static type-checking như **Pylance** và bộ Linter **Ruff**.

- **Bộ Nhị phân Động cơ Trình duyệt (Headless Browser Binary):** Playwright Chromium Browser Engine (được tải cục bộ vào bộ nhớ đệm người dùng).

---

### 2. QUY TRÌNH KÍCH HOẠT MÔI TRƯỜNG VÀ CÀI ĐẶT THƯ VIỆN PHỤ THUỘC

Toàn bộ câu lệnh khởi tạo môi trường ảo, nâng cấp công cụ quản lý gói `pip`, cài đặt danh mục vật tư phụ thuộc từ `requirements.txt` và nạp bộ nhị phân Playwright Chromium được đóng gói trong **một khối mã lệnh duy nhất** bên dưới:

```powershell
# ==============================================================================
# QUY TRÌNH THỰC THI LỆNH TRÊN TERMINAL VSCODE (POWERSHELL) - PHIÊN BẢN v2.3.0
# ==============================================================================

# Bước 1: Khởi tạo Môi trường ảo Python (Virtual Environment) tại thư mục gốc dự án
python -m venv venv

# Bước 2: Kích hoạt Môi trường ảo trên Windows PowerShell
.\venv\Scripts\Activate.ps1

# Bước 3: Nâng cấp công cụ quản lý gói pip lên phiên bản mới nhất
python -m pip install --upgrade pip

# Bước 4: Thực thi cài đặt hàng loạt danh mục vật tư phụ thuộc từ requirements.txt
pip install -r requirements.txt

# Bước 5: Khởi tạo và tải bộ nhị phân Playwright Chromium Browser về máy cục bộ
playwright install chromium

```

---

### 3. PHÂN TÍCH CHỨC NĂNG HẠ TẦNG CỦA CÁC THƯ VIỆN PHỤ THUỘC CHỦ CHỐT (v2.3.0)

- **`pydantic>=2.5.0`:** Động cơ ép củng Lược đồ Cấu hình (**Schema Validation Engine**). Cưỡng chế kiểm tra kiểu dữ liệu tĩnh (Type Hints), kiểm soát thuộc tính rẽ nhánh `math_engine_routing` và áp đặt quy tắc chặn đứng (**Hard-Block Rules**) nếu cấu hình YAML vi phạm giới hạn vật lý (như `max_bookmark_level > 6`).

- **`pymupdf>=1.23.0` (PyMuPDF `fitz`):** Động cơ thao tác nhị phân PDF. Cho phép mở luồng nhị phân tệp PDF sau khi Playwright Chromium xuất bản, quét vị trí tiêu đề vật lý và tiêm **Cây Mục lục (Outline Tree / Bookmarks)** từ Heading Cấp 1 đến Cấp 6.

- **`playwright>=1.40.0`:** Động cơ Trình duyệt Không đầu (**Headless Browser Engine**). Khởi chạy Chromium ngầm trong chế độ Security Sandbox an toàn, nạp tài nguyên Inline, đúc DOM toán học KaTeX hoặc Vector SVG MathJax v3 và xuất bản PDF đồ họa phẳng chuẩn A4.

- **`pytest>=8.0.0` (BỔ SUNG v2.3.0):** Khung bộ kiểm thử mô-đun hộp trắng (**Modular Testing Framework**). Tự động phát hiện và thực thi chuỗi 6 tệp test (`test_01` đến `test_06`), cung cấp giao diện báo lỗi trực quan và đo lường độ bao phủ logic hệ thống.

- **`markdown-it-py>=3.0.0` & `mdit-py-plugins>=0.4.0`:** Bộ phân tích Cây Cú pháp Trừu tượng (AST Parser) tuân thủ tiêu chuẩn CommonMark và mở rộng GFM Tables (`gfm-like`), Footnotes, Front-Matter.

- **`pygments>=2.17.0`:** Động cơ nhuộm màu cú pháp mã nguồn (**Syntax Highlighting Engine**). Chuyển đổi các khối mã `code fence` thành chuỗi HTML mang style CSS chỉ định.

- **`beautifulsoup4>=4.12.0`:** Bộ phân tích Đồ thị DOM HTML. Hỗ trợ `src/pdf_metadata_injector.py` trích xuất chính xác cấu trúc thẻ tiêu đề `<hX data-level="...">` để xây dựng danh sách mục lục.

---

## CHƯƠNG 4: GIẢI PHẪU LƯỢC ĐỒ CẤU HÌNH TRUNG TÂM (config/settings.yaml SCHEMA ANATOMY v2.3.0)

Tệp `config/settings.yaml` đóng vai trò là **Nguồn Sự thật Duy nhất (Single Source of Truth - SSOT)** cho toàn bộ hệ thống. Tệp này định hình bức tranh vận hành của 13 phân khu cấu hình, được nạp và kiểm định chặt chẽ bởi mô hình **Pydantic DTO (`AppConfig`)** trong `main.py`.

Áp dụng nguyên tắc **Don't Repeat Yourself (DRY)**, tài liệu dưới đây tập trung phân tích chuyên sâu **Logic Kỹ thuật (Technical Logic)** và **Tác động Hệ thống (System Impact)** của từng phân khu tham số thay vì chép lại mã nguồn YAML thô.

---

### 1. CHUẨN MÃ HÓA TOÀN CỤC (`global_encoding_standard`)

- **Logic Kỹ thuật:** Khai báo hằng số mã hóa cưỡng chế cho toàn bộ các thao tác I/O trong hệ thống (`utf-8`).

- **Tác động Hệ thống:** Bắt buộc áp dụng UTF-8 khi đọc tệp Markdown nguồn, ghi tệp HTML trung gian, nạp cấu hình YAML và xuất bản PDF. Triệt tiêu 100% các ngoại lệ `UnicodeDecodeError` cũng như sự cố biến dạng phông chữ Tiếng Việt Quốc ngữ trên môi trường Windows 11 (ngăn chặn việc rơi vào bảng mã mặc định `cp1252`).

---

### 2. ĐIỀU HƯỚNG THƯ MỤC VÀ XỬ LÝ HÀNG LOẠT (`directory_routing`)

- **Logic Kỹ thuật:** Quản lý quy trình quét đệ quy tệp đầu vào, phân loại đuôi mở rộng và tái tạo cấu trúc không gian lưu trữ.

- **Tác động Hệ thống:**
- `input_directory` & `output_directory`: Định vị thư mục nguồn (`input/`) và thư mục đích (`output/`).

- `recursive_search: true`: Kích hoạt phương thức `rglob("*")` quét sâu vào mọi cấp thư mục con bên trong `input/`.

- `allowed_extensions`: Màng lọc danh sách đuôi tệp hợp lệ (`[".md", ".markdown", ".mdown"]`).

- `overwrite_existing: true`: Cờ ghi đè tệp PDF thành phẩm nếu đã tồn tại bên thư mục đích.

- `auto_create_directories: true`: Tự động khởi tạo thư mục `input/` và `output/` nếu chưa có trên ổ đĩa.

- `preserve_subfolder_structure: true`: Tự động dựng lại chính xác cây thư mục con từ `input/` sang `output/` (Ví dụ: `input/phan1/bai1.md` -> `output/phan1/bai1.pdf`).

---

### 3. NHUỘM MÀU CÚ PHÁP MÃ NGUỒN (`syntax_highlighting_profile`)

- **Logic Kỹ thuật:** Quy định Profile bảng màu CSS do thư viện Pygments phát sinh cho các khối mã nguồn (`code fence`).

- **Tác động Hệ thống:** Chuyển đổi mã nguồn trong Markdown thành các phần tử HTML bọc class `.highlight` với phối màu chuẩn (Mặc định: `"monokai"`), bảo đảm tính tương phản cao và dễ đọc trên bản in.

---

### 4. GIỚI HẠN ĐỘ SÂU MỎ NEO VÀ DẤU TRANG (`heading_retention_depth`)

- **Logic Kỹ thuật:** Quy định ranh giới phân cấp tiêu đề, gắn mỏ neo ASCII và tiêm Cây Mục lục Bookmarks.

- **Tác động Hệ thống:**
- `max_bookmark_level`: Giới hạn độ sâu phân cấp Bookmark [Mức 6]. Được kiểm soát bởi `@field_validator("max_bookmark_level")` trong Pydantic DTO (`main.py`). Nếu giá trị vi phạm ranh giới vật lý (nhỏ hơn 1 hoặc lớn hơn 6), Pydantic sẽ lập tức ném lỗi `ValidationError` ngắt mạch tiến trình.

- `enable_heading_anchors: true`: Cưỡng chế sinh thuộc tính `id` cho các thẻ `<hX data-level="...">`.

- `normalize_anchor_ascii: true`: Kích hoạt hàm `_slugify_text()` chuyển đổi chuỗi tiêu đề Tiếng Việt có dấu thành dạng Slug ASCII chuẩn hóa (Ví dụ: `"Chương 1: Khởi Tạo"` -> `"chuong-1-khoi-tao"`).

---

### 5. THÔNG SỐ TRANG IN VẬT LÝ (`document_layout`)

- **Logic Kỹ thuật:** Thiết lập thông số hình học cho trang in theo quy chuẩn CSS Paged Media `@page`.

- **Tác động Hệ thống:**
- `page_size: "A4"`: Khổ giấy in tiêu chuẩn [210mm x 297mm].

- `margin: "20mm"`: Khung lề an toàn 4 phía [20mm], tạo vùng in vật lý có chiều rộng 170mm.

- `code_overflow_handling: "break-word"`: Cưỡng chế bẻ dòng tự động cho các dòng mã nguồn quá dài, triệt tiêu sự cố mã tràn ra ngoài lề trang in.

---

### 6. CẤU HÌNH MỸ THUẬT VÀ PHÔNG CHỮ HỆ THỐNG (`typography_configuration`)

- **Logic Kỹ thuật:** Khởi tạo bộ Font Stack phòng thủ chống lỗi vỡ phông Tiếng Việt Unicode.

- **Tác động Hệ thống:**
- `font_family`: Font Stack văn bản chính (`"Segoe UI", "Arial", "Calibri", "Tahoma", sans-serif`).

- `code_font_family`: Phông chữ cố định chiều rộng dành riêng cho mã nguồn (`"Consolas", "Courier New", monospace`).

- `base_font_size: "11pt"` & `line_height: "1.6"`: Kích thước chữ cơ sở và khoảng cách dòng chuẩn xuất bản.

- `text_color: "#1a1a1a"`: Màu chữ xám đen chuyên nghiệp, tối ưu độ tương phản in ấn.

---

### 7. CẤU HÌNH ĐÁNH SỐ TIÊU ĐỀ TỰ ĐỘNG (`heading_numbering_system`)

- **Logic Kỹ thuật:** Điều khiển động cơ CSS Counters tự động đếm và chèn chỉ số phân cấp vào trước tiêu đề.

- **Tác động Hệ thống:**
- `enable_auto_numbering: true`: Bật/tắt tính năng đánh số tiêu đề.

- `h1_numbering_style: "roman"`: Đánh số La Mã (`I., II., III.`) cho tiêu đề H1.

- `sub_heading_numbering_style: "decimal"`: Đánh số thập phân (`1.1, 1.1.1`) cho tiêu đề H2 đến H4.

- `number_separator: ". "`: Chuỗi phân cách giữa chỉ số và nội dung chữ.

---

### 8. ĐIỀU HƯỚNG TRÌNH DUYỆT NGẦM PLAYWRIGHT (`headless_browser_engine`)

- **Logic Kỹ thuật:** Quản lý tham số kết xuất và vòng đời của trình duyệt ngầm Playwright Chromium.

- **Tác động Hệ thống:**
- `browser_type: "chromium"`: Cưỡng chế động cơ Chromium.

- `headless: true`: Chạy không giao diện để đạt hiệu năng tối đa.

- `page_timeout_ms: 30000`: Thời gian Timeout tối đa 30 giây cho mỗi trang in.

- `wait_until_event: "networkidle"`: Buộc Chromium chờ toàn bộ tài nguyên tĩnh và script thực thi xong 100%.

- `print_background: true` & `prefer_css_page_size: true`: Kích hoạt in màu nền và ưu tiên quy tắc khổ giấy trong CSS `@page`.

---

### 9. ĐIỀU HƯỚNG CÔNG TẮC ĐỘNG CƠ TOÁN HỌC (`math_engine_routing` - NÂNG CẤP v2.3.0)

- **Logic Kỹ thuật:** Trung tâm rẽ nhánh quyết định động cơ biên dịch công thức toán học.

- **Tác động Hệ thống:**
- `active_engine`: Nhận một trong hai giá trị chuỗi:

- `"katex_placeholder"` (Mặc định): Sử dụng KaTeX Offline kết hợp thuật toán **Server-Side Python Dictionary Mapping & Client-Side Swap** để đạt tốc độ biên dịch tối đa.

- `"mathjax_svg"`: Kích hoạt động cơ MathJax v3 Offline đúc công thức thành Đồ họa Vector SVG, phục vụ các tài liệu chứa dòng diễn giải toán học siêu phức tạp.

- **Rào chắn Pydantic DTO:** Phương thức `@field_validator("active_engine")` trong `MathEngineRoutingConfig` (`main.py`) thực thi chuyển về chuỗi chữ thường và kiểm tra sự tồn tại trong tập hợp `{"katex_placeholder", "mathjax_svg"}`. Nếu giá trị sai lệch, hệ thống lập tức báo lỗi `ValidationError` ngắt luồng.

---

### 10. BỘ KẾT XUẤT TOÁN HỌC KATEX OFFLINE (`katex_offline_config` - CẬP NHẬT v2.3.0)

- **Logic Kỹ thuật:** Quản lý tài nguyên cục bộ KaTeX và kích hoạt màng lọc bóc tách Tiếng Việt phía máy chủ.

- **Tác động Hệ thống:**
- `enable_katex: true` & `assets_dir: "assets/katex"`: Nạp tài nguyên tĩnh từ thư mục cục bộ.

- `enable_vietnamese_math_isolation: true`: Kích hoạt phương thức `_isolate_vietnamese_in_math()` trong `src/html_renderer.py`. Python quét các vĩ lệnh `\text{...}` chứa Tiếng Việt có dấu, bóc tách chuỗi thô lưu vào từ điển `self.vn_math_store`, nhét mã ASCII giữ chỗ `VILANGMASK0001` và đóng gói đối tượng JSON `vnMap` truyền xuống JavaScript Hậu kỳ hoán đổi Text Nodes.

- `enable_base64_font_embedding: true`: Tiêm phông chữ nhị phạm `.woff2` dạng Base64 trực tiếp vào CSS để hiển thị các ký hiệu toán học đặc biệt (như $\neq$).

- `delimiters`: Cấu hình danh sách 4 ranh giới toán học (`$$...$$`, `$..$`, `\[...\]`, `\(...\)`).

---

### 11. BỘ KẾT XUẤT TOÁN HỌC MATHJAX V3 OFFLINE (`mathjax_offline_config` - MỚI v2.3.0)

- **Logic Kỹ thuật:** Quản lý kho tài nguyên và thông số khởi tạo Môi trường Vector SVG cho MathJax v3.

- **Tác động Hệ thống:**
- `enable_mathjax: true` & `assets_dir: "assets/mathjax"`: Nạp tệp nhị phân `tex-svg.js` từ đĩa cứng.

- `font_cache: "global"`: Cấu hình bộ đệm phông chữ dạng toàn cục trong thẻ SVG, giúp giảm thiểu dung lượng tệp PDF thành phẩm và tăng tốc độ đúc đồ họa của Chromium.

- `scale: 1.0`: Tỷ lệ co giãn mặc định của đồ họa biểu thức toán.

- `inline_math_delimiters` & `display_math_delimiters`: Khởi tạo đối tượng `window.MathJax` tiêm trực tiếp vào HTML để MathJax v3 nhận diện chính xác ranh giới công thức toán nội dòng và toán khối.

---

### 12. CẤU HÌNH BỘ XỬ LÝ BẢNG BIỂU GFM (`table_rendering_system`)

- **Logic Kỹ thuật:** Điều khiển bộ phân tích bảng Markdown GFM và quản lý rào chắn tràn viền vật lý A4.

- **Tác động Hệ thống:**
- `enable_gfm_tables: true`: Kích hoạt quy tắc phân tích bảng GFM trong AST Parser.

- `overflow_strategy: "clip_and_warn"`: Chiến lược tự động cắt bỏ phần thừa tràn lề ngang và ghi nhật ký cảnh báo.

- `repeat_header_on_page_break: true`: Tự động lặp lại hàng tiêu đề (`<thead>`) khi bảng bị cắt ngắt sang trang mới.

- `max_printable_width_mm: 170`: Ngưỡng độ rộng vùng in an toàn khổ A4 [170mm].

---

### 13. MA TRẬN QUY CHUẨN IN ẤN HỌC THUẬT (`academic_standards_profile`)

- **Logic Kỹ thuật:** Định hình phong cách trình bày văn bản theo tiêu chuẩn xuất bản quốc tế [APA 7th, IEEE].

- **Tác động Hệ thống:**
- `active_standard: "apa"`: Bật profile học thuật APA 7th.

- `prevent_orphans_and_widows: true`: Ép chỉ thị CSS `orphans: 2; widows: 2;` ngăn chặn hiện tượng dòng chữ mồ côi hoặc góa phụ đứng cô đơn ở đầu/cuối trang in.

- `code_block_page_break_inside: "avoid"` & `table_page_break_inside: "avoid"`: Ép chỉ thị CSS `break-inside: avoid;` ngăn chặn việc trang in xẻ đôi giữa chừng khối mã nguồn hoặc bảng biểu.

---

## CHƯƠNG 5: QUY TRÌNH VẬN HÀNH VÀ BẢN ĐỒ LUỒNG DỮ LIỆU ĐA CHẶNG (OPERATIONAL PIPELINE v2.3.0)

Chương này trình bày chi tiết quy trình di chuyển dữ liệu 4 Giai đoạn khép kín được nâng cấp trong phiên bản **v2.3.0**, phân tích cơ chế điều phối của tệp `main.py` dựa trên Lược đồ Pydantic DTO và giải phẫu 5 tầng bẫy lỗi cô lập sự cố.

---

### 1. SƠ ĐỒ LUỒNG DI CHUYỂN DỮ LIỆU 4 GIAI ĐOẠN (4-STAGE DATA PIPELINE v2.3.0)

Hệ thống đường ống dữ liệu biên dịch tài liệu vận hành như một **Dây chuyền Sản xuất Sách Chuyên nghiệp Đa động cơ** gồm 4 phân xưởng nối tiếp nhau:

```text
[Thư mục input/] ───> (Quét đệ quy tệp .md) ───> [main.py: AppConfig DTO Validation & Unpacking]
                                                        │
┌───────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┐
│                                                                                                               │
▼                                                                                                               ▼
[GIAI ĐOẠN 1: AST PARSER]                                                       [GIAI ĐOẠN 2: HTML RENDERER]
- Tệp: src/ast_parser.py                                                        - Tệp: src/html_renderer.py
- Động cơ: markdown-it-py (preset: gfm-like)                                    - Kỹ thuật: Python Dictionary Mapping (\text{...})
- Kỹ thuật: Băm Mật mã SHA-256 (_unify_math_delimiters)                          - Kỹ thuật: Routing KaTeX Swap / MathJax v3 Vector SVG
- Đầu ra: Danh sách Nút AST (Tokens)                                            - Đầu ra: Chuỗi HTML Đóng gói + Pygments CSS
│                                                                               │
└───────────────────────────────────────────┬───────────────────────────────────┘
                                            │
                                            ▼
[GIAI ĐOẠN 3: PDF COMPILER]
- Tệp: src/pdf_compiler.py
- Động cơ: Playwright Chromium Headless (Security Sandbox)
- Kỹ thuật: Paged Media CSS SVG Boundaries (max-width: 100%) & Ephemeral Memory (tempfile)
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

- **Giai đoạn 1 (AST Parser - `src/ast_parser.py`):** Tiếp nhận đường dẫn tệp `.md`. Đọc văn bản thô chuẩn `utf-8`. Cưỡng chế chuẩn hóa Unicode NFC toàn cục (`unicodedata.normalize("NFC")`). Bật màng lọc `_unify_math_delimiters()` băm mật mã **SHA-256** bảo vệ Code Block, chuyển đổi đồng bộ `\[...\]` sang `$$...$$` và `\(...\)` sang `$..$`. Đẩy qua `markdown-it-py` để phân rã thành mảng Nút AST ngữ nghĩa.

- **Giai đoạn 2 (HTML Renderer - `src/html_renderer.py`):** Tiếp nhận văn bản Markdown và DTO cấu hình rẽ nhánh `math_routing_config`. Nhuộm màu mã nguồn qua `Pygments`. Sinh mỏ neo ASCII `<hX id="..." data-level="...">` cho toàn bộ tiêu đề từ H1 đến H6. Tùy thuộc cờ `active_engine`:

- Nếu `active_engine == "katex_placeholder"`: Động cơ kích hoạt thuật toán **Server-Side Python Dictionary Mapping**. Quét các vĩ lệnh `\text{...}` chứa Tiếng Việt, bóc tách chuỗi thô vào từ điển `self.vn_math_store`, thế bằng mã ASCII giữ chỗ `VILANGMASK0001`. Đóng gói từ điển dạng JSON nhúng vào script Client-Side Swap Hậu kỳ.

- Nếu `active_engine == "mathjax_svg"`: Động cơ tiêm đối tượng cấu hình `window.MathJax` (`fontCache: 'global'`) và nhúng trực tiếp script `tex-svg.js` từ `assets/mathjax/` để đúc đồ họa Vector SVG.

- **Giai đoạn 3 (PDF Compiler - `src/pdf_compiler.py`):** Cấp phát tệp tạm ẩn danh ngẫu nhiên qua `tempfile.NamedTemporaryFile`. Đúc chuỗi HTML ngữ nghĩa thành tệp tạm vật lý. Khởi chạy Playwright Chromium trong môi trường **Security Sandbox** an toàn. Điều hướng Chromium nạp tệp tạm qua giao thức `file:///`, áp dụng rào chắn Paged Media CSS `mjx-container[jax="SVG"] svg { max-width: 100% !important; height: auto !important; }` khống chế lề A4 170mm. Chờ mỏ neo DOM `.katex, mjx-container, svg` kết xuất xong và xuất bản tệp PDF đồ họa phẳng chuẩn A4. Tự động giải phóng tệp tạm trong khối `finally:`.

- **Giai đoạn 4 (Metadata Injector - `src/pdf_metadata_injector.py`):** Nhận tệp PDF phẳng và chuỗi HTML trung gian. Quét các thẻ `<hX data-level="...">` bóc tách danh sách tiêu đề từ Cấp 1 đến Cấp 6. Mở tệp PDF qua **PyMuPDF (`fitz`)**. Sử dụng thuật toán tìm kiếm tịnh tiến (`search_for`) xác định chỉ mục trang vật lý của từng tiêu đề. Chuẩn hóa cấp độ bằng `_normalize_toc_hierarchy()`, tiêm mảng Cây Mục lục nhị phân `[Level, Title, PageNumber]` vào gáy siêu dữ liệu và thực thi lưu tịnh tiến `saveIncr()`.

---

### 2. GIẢI PHẪU 5 TẦNG BẪY LỖI CÔ LẬP SỰ CỐ (5-TIER FAULT ISOLATION ARCHITECTURE v2.3.0)

Để bảo đảm một tệp Markdown bị hỏng không thể làm dừng tiến trình xử lý hàng loạt của toàn bộ hệ thống, `markdown_to_pdf_engine` v2.3.0 được thiết lập 5 tầng bẫy lỗi phòng thủ:

#### Tầng 1: Cô lập Ngoại lệ Cấp Đơn Tệp (Single-File Failure Isolation)

- **Cơ chế:** Trong `main.py`, hàm `execute_single_file_pipeline()` bọc toàn bộ 4 giai đoạn xử lý trong khối `try...except` diện rộng, bẫy đích danh các lỗi `FileNotFoundError`, `UnicodeDecodeError`, `ValueError`, `TypeError`, `OSError`, `RuntimeError`.

- **Tác động:** Khi phát hiện một tệp bị hỏng nhị phân hoặc sai định dạng, hệ thống ghi nhận sự cố ra Terminal, trả về `False` và lập tức chuyển sang biên dịch tệp tiếp theo trong danh sách chờ.

#### Tầng 2: Rào chắn Lược đồ DTO & Dynamic Unpacking (Schema Barrier & Unpacking)

- **Cơ chế:** Trước khi khởi chạy pipeline, hàm `load_configuration()` thực thi ép củng kiểu dữ liệu qua `AppConfig.model_validate()`. Phương thức `@field_validator("active_engine")` trong `MathEngineRoutingConfig` kiểm tra cờ rẽ nhánh thuộc tập hợp `{"katex_placeholder", "mathjax_svg"}`. Hàm `execute_single_file_pipeline` giải nén từ điển `math_routing_config` và `mathjax_config` qua `.model_dump()` truyền trực tiếp hạ nguồn.

- **Tác động:** Nếu tham số `active_engine` bị nhập sai hoặc `max_bookmark_level` vi phạm ranh giới vật lý, Pydantic v2 sẽ ngắt tiến trình trong dưới 500ms và bắn thông báo `ValidationError` chi tiết. Cơ chế giải nén động triệt tiêu 100% rủi ro trôi dạt cấu hình.

#### Tầng 3: Phòng thủ Băm Mật mã Chống Va chạm Regex (Cryptographic Masking Defense)

- **Cơ chế:** Trong `src/ast_parser.py` và `src/html_renderer.py`, hàm `_unify_math_delimiters()` tạo mặt nạ bảo vệ Code Block bằng thuật toán `hashlib.sha256()`.

- **Tác động:** Khóa giữ chỗ `__CRYPTO_MASK_{hash}_{counter}__` vô hiệu hóa hoàn toàn mọi nỗ lực tiêm chuỗi giả mạo nhằm đánh sập Cây Cú pháp Trừu tượng (AST).

#### Tầng 4: Bộ Nhớ Tạm Vô Danh & Rào Chắn Đồ Họa Vector (Ephemeral Memory & SVG Boundaries)

- **Cơ chế:** Trong `src/pdf_compiler.py`, tệp HTML trung gian được khởi tạo bằng `tempfile.NamedTemporaryFile`. Trình duyệt Playwright Chromium chạy trong chế độ Security Sandbox cô lập. Bộ CSS Paged Media áp đặt chỉ thị `mjx-container[jax="SVG"] svg { max-width: 100% !important; height: auto !important; }`.

- **Tác động:** Ép các biểu thức toán Vector SVG tự động co rút theo tỷ lệ hình học chuẩn khung in A4 170mm, loại bỏ rủi ro tràn lề vật lý và triệt tiêu lỗi `PlaywrightTimeoutError`.

#### Tầng 5: Giới hạn Ngoại lệ Có Chủ đích tại Mô-đun Tiêm Nhị phân (Targeted Exception Containment)

- **Cơ chế:** Trong `src/pdf_metadata_injector.py`, phương thức `inject_metadata()` chỉ bẫy chính xác 3 nhóm lỗi `(OSError, RuntimeError, ValueError)`.

- **Tác động:** Tuân thủ quy chuẩn `BLE001` của Ruff Linter, triệt tiêu rủi ro nuốt chửng ngoại lệ hệ thống (`blind-except`), bảo toàn vệt vết Traceback phục vụ gỡ lỗi nâng cao.

---

## CHƯƠNG 6: MA TRẬN KIỂM THỬ MÔ-ĐƯN HỘP TRẮNG (MODULAR TESTING SUITE - PYTEST v2.3.0)

Trong phiên bản **v2.3.0**, toàn bộ bộ kiểm thử đơn khối `red_team_tests.py` cũ đã được **đại phẫu hoàn toàn**. Hệ thống chuyển đổi sang mô hình **Modular Testing Suite** gồm 6 tệp kiểm thử hộp trắng biệt lập đặt trong thư mục `tests/`, vận hành bởi khung bộ kiểm thử `pytest` hoặc `unittest`.

Sự chuyển đổi này mang lại vòng lặp phản hồi siêu nhanh (Ultra-Fast Feedback Loop), cho phép kiểm thử từng tính năng riêng biệt trong dưới 1 giây mà không cần chạy lại toàn bộ bài stress test đa tiến trình nặng.

---

### PHÂN TÍCH CHỨC NĂNG CHUYÊN BIỆT CỦA 6 TỆP KIỂM THỬ

```text
tests/
├── __init__.py                  # Khởi tạo gói Python package cho môi trường test.
├── test_01_core_pipeline.py     # [LUỒNG LÕI] Kiểm thử I/O, quét đệ quy, cô lập tệp hỏng & batch processing.
├── test_02_schema_layout.py     # [XÁC THỰC LƯỢC ĐỒ] Kiểm thử Pydantic DTO, YAML validation & A4 margin rules.
├── test_03_math_base64.py       # [CÚ PHÁP KATEX] Kiểm thử ranh giới TeX, Base64 math AST isolation & HTML escaping.
├── test_04_document_features.py # [MỸ THUẬT TÀI LIỆU] Kiểm thử GFM Tables, APA Standards & PyMuPDF Bookmarks Level 6.
├── test_05_concurrency_stress.py# [ÉP TẢI VẬT LÝ] Kiểm thử ProcessPoolExecutor, tempfile bộ nhớ tạm & Playwright.
└── test_06_hybrid_math_engine.py# [ĐỘNG CƠ LAI] Kiểm thử DTO Routing, Python Mapping, MathJax SVG & SVG Boundaries.

```

#### 1. `test_01_core_pipeline.py` (Core Engine & Batch Routing)

- **Chức năng:** Kiểm thử luồng vận hành I/O cơ bản và điều phối quét hàng loạt.

- **Các kịch bản phủ:**
- Kiểm thử `execute_single_file_pipeline` biên dịch thành công tệp Markdown tiêu chuẩn sang PDF.

- Kiểm thử cơ chế quét đệ quy (`recursive_search: true`) và tự động tạo thư mục đầu ra.

- Kiểm thử tính năng bảo tồn cấu trúc thư mục con (`preserve_subfolder_structure: true`) từ `input/` sang `output/`.

- Kiểm thử khả năng cô lập lỗi khi gặp tệp chứa chuỗi byte hỏng nhị phân trong lượt chạy batch.

#### 2. `test_02_schema_layout.py` (Pydantic DTO & Layout Boundaries)

- **Chức năng:** Kiểm thử tính đúng đắn của Lược đồ Cấu hình DTO và quy tắc bố cục trang in.

- **Các kịch bản phủ:**
- Kiểm thử nạp tệp cấu hình thực tế `config/settings.yaml` qua `load_configuration()`.

- Kiểm thử rào chắn Pydantic `@field_validator("max_bookmark_level")` ném lỗi `ValidationError` ngắt mạch dưới 500ms khi giá trị lớn hơn 6 hoặc nhỏ hơn 1.

- Kiểm thử tính toàn vẹn của các thuộc tính `DocumentLayoutConfig` (A4, margin 20mm, code overflow).

#### 3. `test_03_math_base64.py` (KaTeX Syntax & AST Isolation)

- **Chức năng:** Kiểm thử màng lọc cú pháp KaTeX, cô lập biểu thức TeX và chống nuốt DOM.

- **Các kịch bản phủ:**
- Kiểm thử hàm `_unify_math_delimiters()` chuẩn hóa đồng bộ Brackets `\[...\]` và `\(...\)` sang Dollars `$$...$$` và `$..$`.

- Kiểm thử mã hóa thực thể HTML (`&lt;` và `&gt;`) cho các toán tử so sánh `<` và `>` bên trong khối toán học.

- Kiểm thử cơ chế dán mặt nạ băm SHA-256 bảo vệ khối mã nguồn không bị biến dạng bởi Regex toán học.

#### 4. `test_04_document_features.py` (GFM Tables, APA & PyMuPDF Bookmarks)

- **Chức năng:** Kiểm thử các tính năng định dạng tài liệu nâng cao và tiêm siêu dữ liệu nhị phân.

- **Các kịch bản phủ:**
- Kiểm thử bóc tách và kết xuất bảng biểu GFM (`overflow_strategy: clip_and_warn`).

- Kiểm thử quy chuẩn in ấn học thuật APA (chống dòng mồ côi/góa phụ `orphans: 2; widows: 2;` và `break-inside: avoid;`).

- Kiểm thử động cơ **PyMuPDF (`fitz`)** quét vị trí văn bản vật lý và tiêm Cây Mục lục Bookmarks từ Heading Cấp 1 đến **Cấp 6**.

#### 5. `test_05_concurrency_stress.py` (Process Isolation & Ephemeral Memory)

- **Chức năng:** Ép tải đa tiến trình vật lý và kiểm tra sức chịu tải hệ thống.

- **Các kịch bản phủ:**
- Ép tải đa tiến trình song song qua `ProcessPoolExecutor` (Phân bổ 10 công việc biên dịch PDF đồng thời trên 4 workers).

- Kiểm thử cấp phát và tự động dọn dẹp tệp bộ nhớ tạm vô danh (`tempfile.NamedTemporaryFile`).

- Xác minh mỗi worker Playwright Chromium sở hữu một Event Loop riêng biệt, không gây ra sự cố treo hay sập tiến trình.

#### 6. `test_06_hybrid_math_engine.py` (Hybrid Math Engine & SVG Boundaries)

- **Chức năng:** Kiểm thử toàn diện Kiến trúc Động cơ Toán học Lai mới bổ sung ở phiên bản v2.3.0.

- **Các kịch bản phủ:**
- Kiểm thử Pydantic DTO validator cho cờ `math_engine_routing.active_engine` (Chấp nhận `"katex_placeholder"` và `"mathjax_svg"`, chặn đứng các chuỗi không hợp lệ).

- Kiểm thử thuật toán **Server-Side Python Dictionary Mapping**: Xác minh văn bản Tiếng Việt trong `\text{...}` được bóc tách vào `self.vn_math_store`, nhét mã ASCII `VILANGMASK0001` và tiêm script Swap Hậu kỳ.

- Kiểm thử Môi trường MathJax v3 Vector SVG: Xác minh đối tượng `window.MathJax` (`fontCache: 'global'`) và script `tex-svg.js` được tiêm chính xác khi chọn nhánh `mathjax_svg`.

- Kiểm thử bộ CSS Paged Media chứa rào chắn bảo vệ `mjx-container[jax="SVG"] svg { max-width: 100% !important; }`.

- Thử nghiệm đúc PDF End-to-End thực tế qua Playwright Chromium sử dụng thuật toán mới.

---

### HƯỚNG DẪN LỆNH THỰC THI BỘ KIỂM THỬ TRÊN POWERSHELL

Bạn có thể chạy toàn bộ 6 tệp kiểm thử hoặc chọn từng tệp riêng biệt bằng các câu lệnh dưới đây:

```powershell
# ==============================================================================
# LỆNH THỰC THI KIỂM THỬ VỚI PYTEST VÀ UNITTEST (WINDOWS POWERSHELL)
# ==============================================================================

# Kích hoạt môi trường ảo Python
.\venv\Scripts\Activate.ps1

# CÁCH 1: Chạy TOÀN BỘ 6 tệp kiểm thử trong thư mục tests/ qua Pytest
pytest tests/ -v

# CÁCH 2: Chỉ chạy DUY NHẤT tệp test_06 cho Kiến trúc Động cơ Toán học Lai v2.3.0
pytest tests/test_06_hybrid_math_engine.py -v

# CÁCH 3: Chạy trực tiếp qua trình thông dịch Python bản địa (Không cần cài Pytest)
python tests/test_06_hybrid_math_engine.py

```

---

## CHƯƠNG 7: LỊCH SỬ PHIÊN BẢN (CHANGELOG)

### Phiên bản v2.3.0 (Bản Nâng cấp Hybrid Math Engine & Modular Pytest Suite - Hiện tại)

- **Kiến trúc Động cơ Toán học Lai (Hybrid Math Engine Architecture):** Bổ sung phân khu `math_engine_routing` trong `config/settings.yaml`. Khởi tạo cờ chuyển mạch `active_engine` cho phép linh hoạt rẽ nhánh giữa động cơ KaTeX (tốc độ cao) và động cơ MathJax v3 Vector SVG Offline (mỹ thuật hoàn hảo).

- **Thuật toán Server-Side Python Dictionary Mapping:** Tái cấu trúc phương thức `_isolate_vietnamese_in_math()` trong `src/html_renderer.py`. Python thực hiện bóc tách văn bản Tiếng Việt trong `\text{...}` ngay tại máy chủ, lưu vào từ điển `self.vn_math_store`, thay bằng mã ASCII `VILANGMASK0001`. Đóng gói từ điển dạng JSON và tiêm script Client-Side Swap Hậu kỳ. Trình duyệt Chromium dùng bộ xếp chữ HarfBuzz bản địa hoán đổi Text Nodes, triệt tiêu 100% lỗi Vòng đời DOM (Race Condition) làm vỡ kerning và lệch dấu Tiếng Việt.

- **Tích hợp Môi trường MathJax v3 Vector SVG Offline:** Bổ sung phân khu `mathjax_offline_config` trong `config/settings.yaml` và tệp nhị phân `assets/mathjax/tex-svg.js`. Tiêm đối tượng cấu hình `window.MathJax` (`fontCache: 'global'`) đúc biểu thức toán thành đồ họa Vector sắc nét.

- **Rào chắn Paged Media SVG Boundaries:** Bổ sung quy tắc CSS Paged Media trong `src/pdf_compiler.py`: `mjx-container[jax="SVG"] svg { max-width: 100% !important; height: auto !important; }`. Ép các công thức SVG tự động co ngót chuẩn khung lề A4 170mm, triệt tiêu lỗi tràn lề và ngắt mạch `PlaywrightTimeoutError`.

- **Đại phẫu Hạ tầng Kiểm thử (Modular Pytest Architecture):** Xóa bỏ tệp đơn khối `red_team_tests.py` cũ. Xây dựng hệ thống 6 tệp kiểm thử mô-đun biệt lập (`test_01_*.py` đến `test_06_*.py`) vận hành bởi `pytest`, nâng cao khả năng cách ly điểm gãy và tăng tốc độ gỡ lỗi.

- **Đồng bộ hóa Linter (Zero-Warning Standard):** Cập nhật mã nguồn dọn sạch 100% cảnh báo Linter từ Ruff (`C414`, `F401`, `RUF059`) và Pylance (`reportSelfClsParameterName`, `reportUndefinedVariable`). Bổ sung cơ chế tự động tiêm `sys.path` vào đầu tệp test để thực thi độc lập mượt mà.

---

### Phiên bản v2.2.0 (Bản Cải tiến AST-Level Math Escape & Strict CSS Typography)

- **Thoát Ký tự Toán học Cấp AST:** Thực thi chuẩn hóa HTML Entities (`&lt;` và `&gt;`) trực tiếp trên các Token AST toán học trong `src/html_renderer.py`.

- **Chuẩn hóa Unicode NFC Toàn cục:** Tích hợp `unicodedata.normalize("NFC", ...)` tại `src/ast_parser.py` và `src/html_renderer.py`, gộp toàn bộ ký tự Tiếng Việt tổ hợp NFD về dạng nguyên khối Unicode chuẩn.

- **Gia cố Lớp giáp Typography:** Cấu hình thuộc tính CSS `position: static !important;` và `display: inline-block !important;` cho thẻ `.vietnamese-math-text` trong `src/pdf_compiler.py`.

---

### Phiên bản v2.0.0 (Bản Nâng cấp Base64 AST Isolation & Context Architecture)

- **Kiến trúc ExecutionContext SSOT:** Khởi tạo lớp DTO `ExecutionContext` trong `main.py`, đóng gói toàn bộ `AppConfig` và thông tin đường dẫn I/O nhằm triệt tiêu sự cố trôi dạt tham số.

- **Giải nén DTO Không Thất thoát (Zero-Loss Unpacking):** Sử dụng `.model_dump()` trích xuất từ điển cấu hình từ Pydantic DTO và truyền trực tiếp hạ nguồn.

- **Mã hóa Base64 TeX AST Isolation:** Tích hợp tùy chọn mã hóa Base64 biểu thức toán học thô trong `src/html_renderer.py` để bảo vệ cú pháp TeX.

- **Mở rộng Dấu trang Cấp 6:** Nâng tham số `max_bookmark_level` trong Pydantic DTO từ 4 lên 6, cho phép PyMuPDF tiêm Cây Mục lục PDF sâu đến Heading Cấp 6.
