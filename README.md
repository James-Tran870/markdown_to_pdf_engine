# MARKDOWN TO PDF ENGINE (Lõi Biên dịch Tài liệu Cục bộ, Động cơ Toán học Lai & Dynamic Obsidian Callouts - Phiên bản v2.5.1)

Một hệ thống đường ống dữ liệu (**Data Pipeline**) tự động hóa toàn diện, chuyên trách chuyển đổi hàng loạt tệp Markdown phức tạp sang định dạng PDF chuẩn Typography xuất bản thương mại. Hệ thống tích hợp **Kiến trúc Động cơ Toán học Lai (Hybrid Math Engine Architecture)** cho phép rẽ nhánh giữa đúc DOM KaTeX tốc độ cao và đúc Đồ họa Vector SVG MathJax v3 ngoại tuyến sắc nét, xử lý bảng biểu GFM khung lưới hoàn chỉnh, đúc mộc **Động cơ Obsidian Callouts Động** đa sắc thái, phủ giáp hệ phông chữ **Typography Windows 11 Bản địa (Cascadia Code & Segoe UI Variable)**, cùng cây mỏ neo điều hướng **Bookmarks nhị phân Cấp 6** ngay trên môi trường máy trạm cục bộ.

Dự án được xây dựng dựa trên tư duy phân tách hệ thống nghiêm ngặt (**Separation of Concerns - SoC**), khép kín và độc lập ngoại tuyến (**Offline-first**). Hệ thống nói KHÔNG với các dịch vụ đám mây (Cloud API), máy chủ web bên ngoài hay cơ sở dữ liệu phức tạp. Mọi tiến trình biên dịch đều diễn ra hoàn toàn trên máy tính cá nhân, bảo đảm tính bảo mật dữ liệu tuyệt đối và khả năng can thiệp tham số linh hoạt thông qua hệ thống cấu hình DTO Pydantic v2 tách biệt.

---

## CHƯƠNG 1: TRIẾT LÝ KIẾN TRÚC VÀ 8 TRỤ CỘT PHÒNG THỦ (ARCHITECTURAL PHILOSOPHY v2.5.1)

Để hình dung phương thức vận hành của hệ thống, hãy tưởng tượng dự án giống như một **Xưởng In ấn Đồ họa Hiện đại Khép kín**. Thay vì cho phép công nhân tự do can thiệp thủ công vào dây chuyền, xưởng vận hành dựa trên 8 trụ cột kiến trúc bất biến nhằm loại trừ hoàn toàn mọi rủi ro gián đoạn tiến trình hay đứt gãy mỹ thuật:

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

### 8. Động Cơ Can Thiệp Vòng Đời AST Callouts Động & Hệ Typography Windows 11 Bản Địa (Dynamic Callout Interception & Windows 11 Typography Stack - MỚI v2.5.1)

- **Ẩn dụ đời thực:** Trong một xưởng in báo chí cao cấp, thay vì chỉ chuẩn bị 5 con dấu gỗ cố định với các chữ in sẵn dễ gãy nét, xưởng trang bị một **Máy Khắc Dấu Tự Động Quang Học** có khả năng đọc lướt tiêu đề để khắc tức thì bất kỳ con dấu chuyên biệt nào (từ ghi chú, cảnh báo, trích dẫn, câu hỏi cho đến các nhãn tùy biến do tác giả tự đặt). Đồng thời, xưởng thay thế toàn bộ con chữ chì cổ điển bằng **Bộ Khuôn Chữ Hợp Kim Đa Ngữ Nguyên Khối**, được tiện gọt riêng cho máy in phẳng hiện đại để từng nét chữ Tiếng Việt và từng ký tự mã nguồn luôn sắc nét, không bao giờ bị lem mực hay răng cưa.

- **Áp dụng vào hệ thống:** Nâng cấp đồng bộ cả tầng phân tích ngữ nghĩa lẫn tầng kết xuất đồ họa trang in:

- **Tầng Phân rã AST Động (`src/html_renderer.py`):** Triển khai Thuật toán Can thiệp Vòng đời AST (AST Lifecycle Interception) qua Biểu thức Chính quy tổng quát `r"^\[!([a-zA-Z0-9_-]+)\]([+-]?)[ \t]*(.*)"`. Cơ chế này xóa bỏ hoàn toàn rào cản từ khóa tĩnh, tự động nhận diện mọi định danh Obsidian Callouts / GFM Alerts mở rộng (`note`, `tip`, `warning`, `caution`, `important`, `quote`, `todo`, `bug`, `example`, v.v.), bóc tách cờ thu gọn `fold_flag` và tiêu đề tùy biến `custom_title`. Động cơ tái cấu trúc cây Token con `inline_token.children`, triệt tiêu hoàn toàn dòng cú pháp thô khỏi đoạn văn `<p>`, và xuất thẻ ngữ nghĩa chuyên biệt `<div class="markdown-alert markdown-alert-{type}" data-callout="{type}">` kèm thanh tiêu đề độc lập `<div class="markdown-alert-title">`.

- **Tầng Typography Windows 11 Bản địa (`src/pdf_compiler.py`):** Thiết lập Font Stack hệ thống hiện đại dành riêng cho môi trường Windows 11. Văn bản chính sử dụng `"Segoe UI Variable Text"` kết hợp `"Segoe UI"`, tối ưu hóa việc xếp chữ Tiếng Việt Unicode NFC chuẩn mực; các khối mã nguồn và Inline Code (`:not(pre) > code`) được trang bị bộ phông chữ bản địa `"Cascadia Code"` và `"Cascadia Mono"`, mang lại tỷ lệ hình học tuyệt hảo, độ tương phản cao và khử răng cưa tuyệt đối trên bản in PDF.

- **Ma trận CSS Callouts Phân tầng:** Thiết lập kiểu dáng nền tảng toàn năng cho bộ chọn `[data-callout]` với cơ chế phòng thủ in ấn `break-inside: avoid;`, bảo đảm Playwright Chromium không xẻ đôi khối cảnh báo qua hai trang giấy vật lý.

---

## CHƯƠNG 2: BẢN ĐỒ CẤU TRÚC THƯ MỤC (DIRECTORY BLUEPRINT v2.5.1)

Dưới đây là sơ đồ không gian làm việc (**Workspace Blueprint**) tiêu chuẩn trên Visual Studio Code cho phiên bản v2.5.1. Mỗi thành phần đều duy trì ranh giới trách nhiệm duy nhất (**Single Responsibility Principle - SoC**) và tuân thủ nghiêm ngặt chuẩn Zero-Trust:

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
│   ├── html_renderer.py       # (Giai đoạn 2 - v2.5.0) Can thiệp AST Callouts Động, Python Mapping & Mỏ neo.
│   ├── pdf_compiler.py        # (Giai đoạn 3 - v2.5.1) Paged Media CSS Windows 11, Cascadia Code & Flat Callouts.
│   └── pdf_metadata_injector.py # (Giai đoạn 4) Quét nhị phân PyMuPDF, nội suy vị trí & tiêm Bookmarks Cấp 6.
│
├── tests/                     # [Bộ Kiểm Thử Mô-đun Pytest] Hệ thống 6 tệp test hộp trắng biệt lập.
│   ├── __init__.py            # Khởi tạo gói kiểm thử.
│   ├── test_01_core_pipeline.py     # [Test 01] Kiểm thử I/O, quét đệ quy, cô lập tệp hỏng & batch processing.
│   ├── test_02_schema_layout.py     # [Test 02] Kiểm thử Pydantic DTO, YAML validation & A4 margin rules.
│   ├── test_03_math_base64.py       # [Test 03] Kiểm thử KaTeX Placeholder Swap, MathJax SVG & Unicode Tiếng Việt.
│   ├── test_04_document_features.py # [Test 04 - v2.5.0] Bảng GFM, Bookmarks Cấp 6, GFM Alerts & Cascadia Code.
│   ├── test_05_concurrency_stress.py# [Test 05] Kiểm thử ProcessPoolExecutor, tempfile bộ nhớ tạm & Playwright.
│   └── test_06_hybrid_math_engine.py# [Test 06] Kiểm thử DTO Routing Validation, Python Mapping & SVG Boundaries.
│
├── .gitignore                 # Chỉ thị phòng thủ Git cách ly 100% I/O, bộ nhớ đệm Ruff, pytest, tempfile và venv.
├── main.py                    # [Quản Đốc Băng Chuyền] Điều phối Pipeline, xác thực Pydantic DTO & Unpacking DTO.
├── README.md                  # Cẩm nang vận hành và bản thiết kế kiến trúc toàn diện v2.5.1.
└── requirements.txt           # Bảng kê vật tư thư viện phụ thuộc (Playwright, Pydantic v2, PyMuPDF, Pytest).

```

### Phân tích Chức năng Chi tiết Từng Thành phần Mã nguồn (v2.5.1)

- **`assets/katex/` & `assets/mathjax/`:** Kho lưu trữ bộ tài nguyên tĩnh ngoại tuyến của KaTeX và MathJax v3. Đảm bảo hệ thống biên dịch công thức toán sắc nét 100% mà không cần kết nối Internet.

- **`config/settings.yaml`:** Trái tim cấu hình của dự án. Quản lý 13 phân khu tham số, bao gồm hai phân khu rẽ nhánh `math_engine_routing` và `mathjax_offline_config`.

- **`main.py`:** Quản đốc điều phối toàn bộ đường ống. Nạp tệp YAML qua `load_configuration()`, thực thi ép củng Lược đồ DTO qua Pydantic v2, trích xuất từ điển DTO `math_routing_config` và `mathjax_config` qua `.model_dump()` và truyền hạ nguồn an toàn.

- **`src/ast_parser.py`:** Đảm nhiệm **Giai đoạn 1**. Sử dụng `markdown-it-py` với preset `commonmark` mở rộng. Áp dụng cơ chế Băm Mật mã SHA-256 (`_unify_math_delimiters`) để che phủ khối mã nguồn và chuyển đổi cú pháp Brackets (`\[...\]`) sang Dollars (`$$`).

- **`src/html_renderer.py` (Phiên bản nâng cấp v2.5.0):** Đảm nhiệm **Giai đoạn 2**. Thực thi thuật toán **Can thiệp Vòng đời AST Callout Động** bóc tách mọi biến thể Callout/Alert, loại bỏ triệt để cú pháp thô khỏi thẻ `<p>`, và sinh cấu trúc thẻ tiêu đề ngữ nghĩa `<div class="markdown-alert-title">`. Đồng thời duy trì thuật toán **Server-Side Python Dictionary Mapping** cho KaTeX và tích hợp đối tượng môi trường Vector SVG cho MathJax v3.

- **`src/pdf_compiler.py` (Phiên bản nâng cấp v2.5.1):** Đảm nhiệm **Giai đoạn 3**. Cấp phát tệp tạm vô danh qua `tempfile.NamedTemporaryFile` và khởi chạy Playwright Chromium trong môi trường **Security Sandbox** an toàn. Trang bị hệ thống CSS Paged Media tối ưu cho Windows 11 với bộ phông chữ `"Cascadia Code"`, `"Segoe UI Variable Text"`, Ma trận Callout đa tầng sắc nét, và rào chắn chống xẻ đôi khối in `break-inside: avoid;`. Mã nguồn đạt chuẩn Zero-Warning với cấu trúc Import Module-level tuyệt đối.

- **`src/pdf_metadata_injector.py`:** Đảm nhiệm **Giai đoạn 4**. Tiếp nhận chuỗi HTML trung gian, bóc tách cấu trúc thẻ `<hX data-level="...">` từ Cấp 1 đến Cấp 6, sử dụng **PyMuPDF (`fitz`)** quét vị trí văn bản trên PDF vật lý và tiêm Cây Mục lục nhị phân hoàn chỉnh.

- **`tests/test_01_*.py` đến `test_06_*.py`:** Hệ thống bộ kiểm thử mô-đun biệt lập vận hành bởi `pytest`. Trong đó, tệp `test_04_document_features.py` được tích hợp hai kịch bản mới (`Scenario 15` và `Scenario 16`) để kiểm toán toàn diện tính năng bóc tách Callouts và CSS Paged Media của chữ trong dấu Backtick.

- **`.gitignore`:** Chỉ thị phòng thủ Git cách ly 100% thư mục nguyên liệu `input/`, thành phẩm `output/`, bộ nhớ đệm Ruff, pytest, tệp tạm thời `tempfile` và môi trường ảo `venv/`.

- **`requirements.txt`:** Bảng kê khai danh mục vật tư phụ thuộc chuẩn hóa phiên bản, bảo đảm khả năng tái tạo môi trường thực thi đồng nhất trên mọi máy trạm Windows 11.

---

## CHƯƠNG 3: HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG VÀ HẠ TẦNG THỰC THI (ENVIRONMENT & INFRASTRUCTURE v2.5.1)

Chương này cung cấp quy trình thiết lập môi trường phát triển cục bộ khép kín (**Offline-First Local Environment**) trên hệ điều hành Windows 11, đảm bảo tính độc lập và khả năng tái lập hoàn toàn (Reproducibility) của toàn bộ đường ống biên dịch.

---

### 1. YÊU CẦU HỆ THỐNG VÀ ĐIỀU KIỆN TIÊN QUYẾT (SYSTEM PREREQUISITES)

Để hệ thống biên dịch vận hành đạt độ tin cậy tuyệt đối và không phát sinh xung đột tài nguyên, máy trạm cần đáp ứng các tiêu chuẩn phần cứng và phần mềm sau:

- **Hệ điều hành:** Microsoft Windows 11 64-bit (Khuyến nghị phiên bản 22H2/23H2 hoặc mới hơn để tận dụng bộ phông chữ hệ thống thế hệ mới `Cascadia Code` và `Segoe UI Variable Text`).

- **Môi trường Trình thông dịch Python:** Python phiên bản **3.10** trở lên (Khuyến nghị Python 3.11 hoặc 3.12 để tối ưu hóa hiệu năng phân giải chuỗi UTF-8 và tăng tốc độ thực thi của Pydantic v2).

- **Môi trường Biên tập (IDE):** Visual Studio Code tích hợp bộ công cụ kiểm tra kiểu tĩnh **Pylance** và bộ phân tích cú pháp **Ruff** (đã cấu hình theo chuẩn Zero-Warning).

- **Động cơ Trình duyệt Ngầm (Headless Browser Engine):** Playwright Chromium Driver bản địa (được cài đặt cục bộ vào bộ nhớ đệm của người dùng).

---

### 2. PHÂN TÍCH CHỨC NĂNG HẠ TẦNG CỦA CÁC THƯ VIỆN PHỤ THUỘC (DEPENDENCY MATRIX)

Mỗi thư viện được khai báo trong `requirements.txt` đều gánh vác một mắt xích độc lập trong kiến trúc phân tách mối quan tâm (**SoC**) của dự án:

- **`pydantic>=2.5.0`:** Động cơ kiểm định lược đồ (**Schema Validation Engine**). Chịu trách nhiệm nạp dữ liệu YAML, cưỡng chế kiểu dữ liệu tĩnh (Type Hints), kiểm tra tính hợp lệ của cờ chuyển mạch `math_engine_routing` và kích hoạt quy tắc chặn đứng (**Hard-Block Rule**) nếu tham số cấu hình vi phạm ranh giới vật lý.

- **`pymupdf>=1.23.0` (PyMuPDF `fitz`):** Động cơ thao tác nhị phân PDF hậu kỳ. Đảm nhiệm việc mở tệp PDF thành phẩm từ Playwright, quét vị trí tọa độ của từng tiêu đề văn bản và tiêm trực tiếp Cây Mục lục nhị phân (**Bookmarks/Outline Tree**) từ Cấp 1 đến Cấp 6 vào lớp siêu dữ liệu của tệp.

- **`playwright>=1.40.0`:** Động cơ Trình duyệt Không đầu (**Headless Browser Engine**). Khởi chạy Chromium ngầm trong chế độ Sandbox bảo mật, nạp chuỗi HTML ngữ nghĩa cùng hệ thống CSS Paged Media để kết xuất đồ họa trang in PDF đạt chuẩn Typography.

- **`pytest>=8.0.0`:** Khung kiểm thử mô-đun hộp trắng (**Modular Testing Framework**). Tự động quét và thực thi ma trận 6 tệp kiểm thử độc lập (`test_01` đến `test_06`), cung cấp cơ chế cách ly điểm gãy và đo lường độ bao phủ logic toàn dự án.

- **`markdown-it-py>=3.0.0` & `mdit-py-plugins>=0.4.0`:** Động cơ phân tích Cây Cú pháp Trừu tượng (AST Parser) tuân thủ đặc tả CommonMark và mở rộng bảng biểu GFM, chú thích cuối trang (Footnotes) và Front-Matter.

- **`pygments>=2.17.0`:** Động cơ nhuộm màu cú pháp mã nguồn. Phân tích cấu trúc từ vựng của các đoạn mã trong khối `code fence` và chuyển hóa thành các thẻ HTML mang bảng màu tương phản cao (mặc định: `monokai`).

- **`beautifulsoup4>=4.12.0`:** Bộ phân tích đồ thị DOM HTML. Hỗ trợ mô-đun `src/pdf_metadata_injector.py` bóc tách chính xác danh sách các thẻ `<hX data-level="...">` và lột bỏ các thẻ con phức tạp để lấy chuỗi văn bản thuần túy.

---

## CHƯƠNG 4: GIẢI PHẪU LƯỢC ĐỒ CẤU HÌNH TRUNG TÂM (`config/settings.yaml` SCHEMA ANATOMY v2.5.1)

Tệp `config/settings.yaml` giữ vai trò là **Nguồn Sự Thật Duy Nhất (Single Source of Truth - SSOT)** điều phối toàn bộ hành vi của hệ thống. Khi ứng dụng khởi động, toàn bộ tệp này được mô-đun `main.py` nạp và chuyển đổi thành mô hình **Pydantic DTO (`AppConfig`)**.

Dưới đây là bản phân tích chuyên sâu về **Logic Kỹ thuật** và **Tác động Hệ thống** của toàn bộ 13 phân khu cấu hình:

---

### 1. CHUẨN MÃ HÓA TOÀN CỤC (`global_encoding_standard`)

- **Logic Kỹ thuật:** Thiết lập hằng số mã hóa ký tự chuẩn hóa xuyên suốt toàn bộ các tiến trình I/O của hệ thống (mặc định: `"utf-8"`).

- **Tác động Hệ thống:** Cưỡng chế việc đọc tệp Markdown nguồn, ghi tệp HTML trung gian, nạp tệp cấu hình YAML và xuất bản PDF phải tuân thủ nghiêm ngặt bảng mã UTF-8. Điều này triệt tiêu 100% các lỗi giải mã `UnicodeDecodeError` và ngăn chặn trình biên dịch trên Windows 11 rơi vào bảng mã mặc định `cp1252`, bảo toàn tính nguyên vẹn của ký tự Tiếng Việt có dấu dạng Unicode NFC.

---

### 2. ĐIỀU HƯỚNG THƯ MỤC VÀ XỬ LÝ HÀNG LOẠT (`directory_routing`)

- **Logic Kỹ thuật:** Định nghĩa không gian làm việc đầu vào/đầu ra, chiến lược quét tệp đệ quy và quy tắc tái tạo cây thư mục.

- **Tác động Hệ thống:**
- `input_directory` & `output_directory`: Xác định vị trí thư mục nguyên liệu (`input/`) và thư mục thành phẩm (`output/`).

- `recursive_search: true`: Kích hoạt phương thức `rglob("*")` quét sâu vào toàn bộ các nhánh thư mục con bên trong thư mục nguồn.

- `allowed_extensions`: Màng lọc danh sách phần mở rộng hợp lệ (`[".md", ".markdown", ".mdown"]`), loại bỏ hoàn toàn các tệp rác hoặc tệp không đúng định dạng.

- `overwrite_existing`: Quyết định hành vi ghi đè nếu tệp PDF thành phẩm đã tồn tại tại đích đến.

- `auto_create_directories: true`: Tự động khởi tạo hệ thống thư mục `input/` và `output/` nếu chưa tồn tại trên ổ đĩa.

- `preserve_subfolder_structure: true`: Tự động sao chép chính xác cấu trúc phân cấp thư mục con từ thư mục nguồn sang thư mục đích (ví dụ: `input/giao_trinh/bai_01.md` -> `output/giao_trinh/bai_01.pdf`).

---

### 3. NHUỘM MÀU CÚ PHÁP MÃ NGUỒN (`syntax_highlighting_profile`)

- **Logic Kỹ thuật:** Khai báo Profile bảng màu sắc của thư viện Pygments áp dụng cho các khối mã nguồn (`code fence`).

- **Tác động Hệ thống:** Chuyển đổi mã nguồn trong các khối lệnh Markdown thành cấu trúc HTML có gắn các lớp CSS `.highlight` với phối màu sắc nét (mặc định: `"monokai"`), bảo đảm độ tương phản cao, dễ đọc khi in ấn hoặc xem trên màn hình.

---

### 4. GIỚI HẠN ĐỘ SÂU DẤU TRANG VÀ MỎ NEO TIÊU ĐỀ (`heading_retention_depth`)

- **Logic Kỹ thuật:** Quản lý chiều sâu phân cấp của Cây Mục lục Bookmarks và kiểm soát việc chuẩn hóa định danh ID cho tiêu đề.

- **Tác động Hệ thống:**
- `max_bookmark_level`: Giới hạn độ sâu phân cấp tối đa cho Bookmarks PDF (cấp 1 đến cấp 6). Trong Pydantic DTO (`main.py`), phương thức `@field_validator("max_bookmark_level")` thiết lập rào chắn cứng: nếu người dùng cấu hình giá trị lớn hơn 6 hoặc nhỏ hơn 1, hệ thống sẽ lập tức ném lỗi `ValidationError` và hủy bỏ tiến trình để bảo vệ tính toàn vẹn của tệp PDF nhị phân.

- `enable_heading_anchors: true`: Cưỡng chế sinh thuộc tính `id` và `data-level` cho toàn bộ các thẻ `<hX>` trong HTML.

- `normalize_anchor_ascii: true`: Kích hoạt thuật toán chuyển đổi chuỗi tiêu đề Tiếng Việt có dấu thành dạng Slug ASCII không dấu (ví dụ: `"Chương 1: Mở Đầu"` -> `id="chuong-1-mo-dau"`), ngăn ngừa lỗi điều hướng liên kết nội bộ.

---

### 5. THÔNG SỐ TRANG IN VẬT LÝ (`document_layout`)

- **Logic Kỹ thuật:** Thiết lập các thông số hình học cho trang in theo đặc tả quy chuẩn CSS Paged Media `@page`.

- **Tác động Hệ thống:**
- `page_size: "A4"`: Định dạng kích thước trang in tiêu chuẩn quốc tế (210mm x 297mm).

- `margin: "20mm"`: Thiết lập khoảng cách lề an toàn đồng đều 4 phía (20mm), tạo ra vùng in nội dung vật lý chuẩn có độ rộng 170mm.

- `code_overflow_handling: "break-word"`: Cưỡng chế cơ chế tự động ngắt và bẻ dòng đối với các chuỗi ký tự hoặc dòng mã nguồn quá dài, loại bỏ hoàn toàn sự cố mã nguồn tràn ra ngoài mép trang giấy in.

---

### 6. CẤU HÌNH MỸ THUẬT VÀ PHÔNG CHỮ HỆ THỐNG (`typography_configuration` - v2.5.1)

- **Logic Kỹ thuật:** Thiết lập Font Stack hệ thống bản địa tối ưu hóa cho môi trường Windows 11 song ngữ Anh - Việt.

- **Tác động Hệ thống:**
- `font_family`: Cấu hình Font Stack chính `"Segoe UI Variable Text", "Segoe UI", "Calibri", Arial, sans-serif`. Đây là các bộ phông chữ hệ thống cao cấp của Windows 11, hỗ trợ khử răng cưa mượt mà, căn chỉnh kerning hoàn hảo cho Tiếng Việt Unicode NFC và văn bản tiếng Anh.

- `code_font_family`: Cấu hình Font Stack cho khối mã và chữ trong dấu Backtick `"Cascadia Code", "Cascadia Mono", Consolas, "Courier New", monospace`. Phông chữ `Cascadia Code` mang lại tỷ lệ hình học Monospace chuẩn mực, nét chữ rõ ràng và tương phản cao trên nền xám mờ của tài liệu PDF.

- `base_font_size: "11pt"` & `line_height: "1.65"`: Tỷ lệ kích thước chữ và khoảng cách dòng đạt chuẩn xuất bản học thuật, mang lại trải nghiệm đọc tối ưu.

- `text_color: "#1a1a1a"`: Màu chữ than tối chuyên nghiệp, triệt tiêu hiện tượng lóa mắt trên màn hình và mờ nhạt trên bản in giấy.

---

### 7. CẤU HÌNH ĐÁNH SỐ TIÊU ĐỀ TỰ ĐỘNG (`heading_numbering_system`)

- **Logic Kỹ thuật:** Quản lý quy tắc CSS Counters tự động tính toán và chèn chỉ mục phân cấp vào trước nội dung tiêu đề.

- **Tác động Hệ thống:**
- `enable_auto_numbering: true`: Bật/tắt động cơ đánh số tự động.

- `h1_numbering_style: "roman"`: Đánh số La Mã hoa (`I., II., III.`) cho các tiêu đề cấp 1 (`<h1>`).

- `sub_heading_numbering_style: "decimal"`: Đánh số thập phân phân tầng (`1.1., 1.1.1.`) cho các tiêu đề phụ từ cấp 2 (`<h2>`) đến cấp 4 (`<h4>`).

- `number_separator: ". "`: Chuỗi ký tự ngăn cách giữa số thứ tự và nội dung tiêu đề.

---

### 8. ĐIỀU HƯỚNG TRÌNH DUYỆT NGẦM PLAYWRIGHT (`headless_browser_engine`)

- **Logic Kỹ thuật:** Cấu hình tham số thực thi và vòng đời của tiến trình Playwright Chromium Headless.

- **Tác động Hệ thống:**
- `browser_type: "chromium"`: Cưỡng chế sử dụng nhân trình duyệt Chromium.

- `headless: true`: Vận hành hoàn toàn không giao diện để đạt tốc độ xử lý và hiệu năng bộ nhớ cao nhất.

- `page_timeout_ms: 30000`: Hạn mức thời gian chờ kết xuất tối đa 30 giây cho mỗi tài liệu.

- `wait_until_event: "networkidle"`: Cưỡng chế Playwright chờ đợi cho đến khi toàn bộ tài nguyên đồ họa, phông chữ nhúng và script toán học thực thi xong hoàn toàn.

- `print_background: true`: Cho phép in các dải màu nền của khối mã nguồn, bảng biểu và các hộp Obsidian Callouts.

- `prefer_css_page_size: true`: Ưu tiên tuân thủ kích thước trang in được khai báo trong CSS `@page`.

---

### 9. ĐIỀU HƯỚNG CÔNG TẮC ĐỘNG CƠ TOÁN HỌC (`math_engine_routing` - v2.3.0)

- **Logic Kỹ thuật:** Khóa chuyển mạch quyết định động cơ biên dịch công thức toán học LaTeX.

- **Tác động Hệ thống:**
- `active_engine`: Cho phép rẽ nhánh giữa hai chế độ:

- `"katex_placeholder"` (Mặc định): Động cơ KaTeX ngoại tuyến kết hợp thuật toán **Server-Side Python Dictionary Mapping & Client-Side Swap**, mang lại tốc độ biên dịch cực nhanh và bảo toàn tuyệt đối tiếng Việt trong công thức.

- `"mathjax_svg"`: Động cơ MathJax v3 ngoại tuyến đúc công thức thành đồ họa Vector SVG sắc nét, đáp ứng các tài liệu học thuật có cấu trúc toán học phức tạp.

- **Rào chắn Pydantic DTO:** Hàm xác thực `@field_validator("active_engine")` trong `main.py` sẽ chặn đứng ngay lập tức nếu giá trị cấu hình không nằm trong danh sách được hỗ trợ.

---

### 10. BỘ KẾT XUẤT TOÁN HỌC KATEX OFFLINE (`katex_offline_config` - v2.3.0)

- **Logic Kỹ thuật:** Quản lý kho tài nguyên tĩnh KaTeX và kích hoạt màng lọc bóc tách Tiếng Việt tại máy chủ.

- **Tác động Hệ thống:**
- `enable_katex: true` & `assets_dir: "assets/katex"`: Xác định vị trí nạp tệp CSS, JS và font nhị phân `.woff2` ngoại tuyến.

- `enable_vietnamese_math_isolation: true`: Kích hoạt phương thức `_isolate_vietnamese_in_math()` tại `src/html_renderer.py`. Hệ thống quét các thẻ `\text{...}` chứa tiếng Việt, bóc tách lưu vào từ điển `self.vn_math_store`, thay thế bằng mã giữ chỗ `VILANGMASK0001` và dùng script hoán đổi Text Nodes hậu kỳ để khắc phục triệt để lỗi rơi dấu tiếng Việt do KaTeX gây ra.

- `enable_base64_font_embedding: true`: Tự động đọc và nhúng toàn bộ phông chữ toán học `.woff2` dưới dạng chuỗi Base64 vào CSS nội tuyến.

- `delimiters`: Thiết lập danh mục 4 cặp dấu phân cách toán học chuẩn (`$$...$$`, `$..$`, `\[...\]`, `\(...\)`).

---

### 11. BỘ KẾT XUẤT TOÁN HỌC MATHJAX V3 OFFLINE (`mathjax_offline_config` - v2.3.0)

- **Logic Kỹ thuật:** Quản lý tài nguyên và thông số vận hành của môi trường Vector SVG MathJax v3.

- **Tác động Hệ thống:**
- `enable_mathjax: true` & `assets_dir: "assets/mathjax"`: Nạp tệp nhị phân `tex-svg.js` từ đĩa cứng.

- `font_cache: "global"`: Cấu hình bộ đệm glyph toàn cục trong thẻ SVG, giúp tối ưu dung lượng tệp PDF và tăng tốc độ xử lý của Playwright.

- `scale: 1.0`: Tỷ lệ thu phóng kích thước đồ họa công thức toán.

- `inline_math_delimiters` & `display_math_delimiters`: Thiết lập ranh giới nhận diện công thức nội dòng và công thức khối cho MathJax.

---

### 12. CẤU HÌNH ĐỘNG CƠ XỬ LÝ BẢNG BIỂU GFM (`table_rendering_system`)

- **Logic Kỹ thuật:** Quản lý bộ phân giải bảng Markdown GFM và rào chắn chống tràn lề trang in.

- **Tác động Hệ thống:**
- `enable_gfm_tables: true`: Kích hoạt trình cắm bảng biểu trong động cơ AST Parser.

- `overflow_strategy: "clip_and_warn"`: Tự động khống chế độ rộng bảng và ngăn chặn vỡ khung giao diện.

- `repeat_header_on_page_break: true`: Tự động lặp lại hàng tiêu đề `<thead>` ở đầu trang tiếp theo khi bảng biểu bị ngắt qua nhiều trang in.

- `max_printable_width_mm: 170`: Giới hạn chiều rộng tối đa của bảng khớp hoàn hảo với vùng in A4.

---

### 13. MA TRẬN QUY CHUẨN IN ẤN HỌC THUẬT (`academic_standards_profile`)

- **Logic Kỹ thuật:** Áp đặt các quy tắc dàn trang in ấn theo tiêu chuẩn học thuật quốc tế (APA 7th, IEEE).

- **Tác động Hệ thống:**
- `active_standard: "apa"`: Kích hoạt hồ sơ định dạng học thuật.

- `prevent_orphans_and_widows: true`: Tiêm thuộc tính CSS `orphans: 2; widows: 2;` để ngăn chặn các dòng chữ đơn lẻ nằm cô lập ở đầu hoặc cuối trang.

- `code_block_page_break_inside: "avoid"` & `table_page_break_inside: "avoid"`: Áp dụng quy tắc `break-inside: avoid;` cho khối mã, bảng biểu và các hộp Obsidian Callouts, bảo đảm Playwright không bao giờ xẻ đôi các khối nội dung quan trọng này qua hai trang giấy in.

---

## TỔNG HỢP KHỐI MÃ LỆNH THỰC THI HẠ TẦNG (CONSOLIDATED POWERSHELL SETUP BLOCK)

Toàn bộ các câu lệnh khởi tạo môi trường ảo, nâng cấp pip, cài đặt danh mục phụ thuộc và tải động cơ trình duyệt Playwright Chromium trên Windows PowerShell được đóng gói trong duy nhất một khối mã dưới đây:

```powershell
# ==============================================================================
# HẠ TẦNG THỰC THI: KHỞI TẠO MÔI TRƯỜNG & CÀI ĐẶT THƯ VIỆN (WINDOWS 11 POWERSHELL)
# Dự án: markdown_to_pdf_engine (Phiên bản v2.5.1)
# ==============================================================================

# BƯỚC 1: Khởi tạo Môi trường ảo Python (Virtual Environment) tại thư mục gốc dự án
python -m venv venv

# BƯỚC 2: Kích hoạt Môi trường ảo trên Windows PowerShell
.\venv\Scripts\Activate.ps1

# BƯỚC 3: Nâng cấp công cụ quản lý gói pip lên phiên bản mới nhất
python -m pip install --upgrade pip

# BƯỚC 4: Cài đặt toàn bộ danh mục thư viện phụ thuộc từ tệp requirements.txt
pip install -r requirements.txt

# BƯỚC 5: Tải và cấu hình bộ nhị phân Playwright Chromium Browser về máy cục bộ
playwright install chromium

```

---

## CHƯƠNG 5: QUY TRÌNH VẬN HÀNH VÀ BẢN ĐỒ LUỒNG DỮ LIỆU ĐA CHẶNG (OPERATIONAL PIPELINE v2.5.1)

Chương này trình bày chi tiết quy trình di chuyển dữ liệu qua 4 Giai đoạn khép kín được nâng cấp toàn diện trong phiên bản **v2.5.1**, phân tích cơ chế điều phối của tệp `main.py` dựa trên Lược đồ Pydantic DTO, và giải phẫu 5 tầng bẫy lỗi cô lập sự cố bảo vệ tính toàn vẹn của toàn bộ dây chuyền.

---

### 1. SƠ ĐỒ LUỒNG DI CHUYỂN DỮ LIỆU 4 GIAI ĐOẠN (4-STAGE DATA PIPELINE v2.5.1)

Hệ thống đường ống dữ liệu biên dịch tài liệu vận hành như một **Dây chuyền Xuất bản Kỹ thuật số Đa Động cơ** bao gồm 4 phân xưởng xử lý nối tiếp nhau:

```text
[Thư mục input/] ───> (Quét đệ quy tệp .md) ───> [main.py: AppConfig DTO Validation & Unpacking]
                                                        │
┌───────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┐
│                                                                                                               │
▼                                                                                                               ▼
[GIAI ĐOẠN 1: AST PARSER]                                                       [GIAI ĐOẠN 2: HTML RENDERER]
- Tệp: src/ast_parser.py                                                        - Tệp: src/html_renderer.py
- Động cơ: markdown-it-py (preset: commonmark/gfm)                              - Kỹ thuật: Dynamic Callout AST Interception
- Kỹ thuật: Băm Mật mã SHA-256 (_unify_math_delimiters)                          - Kỹ thuật: Python Dictionary Mapping (\text{...})
- Đầu ra: Danh sách Nút AST (Tokens)                                            - Kỹ thuật: Routing KaTeX Swap / MathJax v3 SVG
│                                                                               - Đầu ra: Chuỗi HTML Ngữ Nghĩa + Pygments CSS
│                                                                               │
└───────────────────────────────────────────┬───────────────────────────────────┘
                                            │
                                            ▼
[GIAI ĐOẠN 3: PDF COMPILER]
- Tệp: src/pdf_compiler.py
- Động cơ: Playwright Chromium Headless (Security Sandbox)
- Kỹ thuật: Typography Windows 11 (Cascadia Code & Segoe UI Variable)
- Kỹ thuật: Ma trận CSS Callouts Phân tầng ([data-callout]) & :not(pre) > code
- Kỹ thuật: Ephemeral Memory (tempfile) & Rào chắn break-inside: avoid;
- Đầu ra: Tệp PDF Đồ họa Phẳng (Flat Graphics PDF)
│
▼
[GIAI ĐOẠN 4: METADATA INJECTOR]
- Tệp: src/pdf_metadata_injector.py
- Động cơ: PyMuPDF (fitz) Binary Engine (Max Level: 6)
- Kỹ thuật: BeautifulSoup4 DOM Scraping & Binary Outline Injection
- Đầu ra: Tệp PDF Hoàn chỉnh mang Cây Mục lục (Bookmarks/Outline Tree Cấp 6)
│
▼
[Thư mục output/ (PDF Thành phẩm Chuẩn Typography)]

```

#### Phân tích Chi tiết Nhiệm vụ Kỹ thuật tại Mỗi Giai đoạn Pipeline (v2.5.1)

- **Giai đoạn 1 (AST Parser - `src/ast_parser.py`):** Tiếp nhận đường dẫn tệp `.md` từ bộ điều phối. Đọc nội dung văn bản thô theo chuẩn mã hóa `utf-8`. Cưỡng chế chuẩn hóa Unicode NFC toàn cục thông qua phương thức `unicodedata.normalize("NFC", ...)` nhằm gộp các ký tự Tiếng Việt tổ hợp dạng NFD về dạng ký tự nguyên khối. Kích hoạt màng lọc `_unify_math_delimiters()` áp dụng thuật toán băm mật mã **SHA-256** để dán mặt nạ bảo vệ toàn bộ các khối mã nguồn (`code fence`) và mã nội dòng. Chuyển đổi đồng bộ các ký tự ranh giới toán học Brackets (`\[...\]`, `\(...\)`) sang dạng chuẩn Dollars (`$$...$$`, `$...$`). Phân rã văn bản qua động cơ `markdown-it-py` để sinh danh sách Token AST chuẩn hóa.

- **Giai đoạn 2 (HTML Renderer - `src/html_renderer.py`):** Tiếp nhận văn bản Markdown và các DTO cấu hình điều hướng. Khởi tạo động cơ nhuộm màu cú pháp Pygments để sinh bảng mã màu CSS cho các khối mã nguồn. Sinh mỏ neo chuẩn hóa Slug ASCII `<hX id="..." data-level="...">` cho toàn bộ các tiêu đề từ H1 đến H6. Thực thi **Thuật toán Can thiệp Vòng đời AST Callouts Động (Dynamic Callout AST Interception)**: Quét biểu thức chính quy mở `r"^\[!([a-zA-Z0-9_-]+)\]([+-]?)[ \t]*(.*)"` để bóc tách mọi loại Callout/Alert bất kỳ (từ `note`, `tip`, `warning`, `caution`, `important` cho đến `quote`, `todo`, `bug`, `example`), triệt tiêu hoàn toàn dòng cú pháp thô khỏi thẻ `<p>`, và xuất cấu trúc khối HTML ngữ nghĩa `<div class="markdown-alert markdown-alert-{type}" data-callout="{type}">` kèm thanh tiêu đề độc lập `<div class="markdown-alert-title">`. Đối với công thức toán học, động cơ tự động rẽ nhánh dựa trên cờ `active_engine`:

- Nếu `active_engine == "katex_placeholder"`: Động cơ áp dụng thuật toán **Server-Side Python Dictionary Mapping**, quét các thẻ `\text{...}` chứa Tiếng Việt, bóc tách chuỗi thô lưu vào từ điển `self.vn_math_store`, thay thế bằng mã giữ chỗ `VILANGMASK0001` và tiêm script Client-Side Swap để Chromium sử dụng bộ xếp chữ HarfBuzz bản địa hoán đổi lại chuỗi Tiếng Việt nguyên khối ở giai đoạn hậu kỳ.

- Nếu `active_engine == "mathjax_svg"`: Động cơ tiêm đối tượng cấu hình `window.MathJax` (`fontCache: 'global'`) và nhúng trực tiếp mã nguồn `tex-svg.js` từ `assets/mathjax/` để đúc đồ họa Vector SVG sắc nét.

- **Giai đoạn 3 (PDF Compiler - `src/pdf_compiler.py`):** Cấp phát một tệp HTML trung gian ẩn danh ngẫu nhiên trong bộ nhớ tạm thời thông qua `tempfile.NamedTemporaryFile`. Đóng gói chuỗi HTML ngữ nghĩa cùng toàn bộ tài nguyên CSS Paged Media tối ưu hóa riêng cho Windows 11:

- Phông chữ văn bản chính được thiết lập bằng bộ phông hệ thống `"Segoe UI Variable Text"` và `"Segoe UI"`, đảm bảo căn chỉnh kerning và dấu thanh Tiếng Việt Unicode NFC chuẩn mực.

- Khối mã nguồn nhiều dòng và khối mã nội dòng trong dấu Backtick (`:not(pre) > code`) được trang bị Font Stack `"Cascadia Code"`, `"Cascadia Mono"` và `Consolas`, mang lại tỷ lệ Monospace sắc nét, độ tương phản cao trên nền xám mờ `rgba(175, 184, 193, 0.22)`.

- Ma trận CSS Callouts phân tầng với bộ chọn toàn năng `[data-callout]` cùng các biến thể màu sắc chuyên biệt (`note`, `tip`, `important`, `warning`, `caution`, `quote`), gắn kèm cơ chế phòng thủ in ấn `break-inside: avoid;` nhằm ngăn chặn Chromium xẻ đôi khối cảnh báo qua hai trang giấy in.

- Rào chắn `mjx-container[jax="SVG"] svg { max-width: 100% !important; height: auto !important; }` khống chế kích thước biểu thức toán trong khung in an toàn 170mm của khổ A4.

- Khởi chạy Playwright Chromium trong môi trường **Security Sandbox** an toàn, điều hướng qua giao thức `file:///`, chờ đợi các mỏ neo DOM toán học và xuất bản tệp PDF đồ họa phẳng. Toàn bộ tệp tạm được dọn dẹp tuyệt đối trong khối `finally:`.

- **Giai đoạn 4 (Metadata Injector - `src/pdf_metadata_injector.py`):** Tiếp nhận tệp PDF phẳng vừa xuất bản và chuỗi HTML trung gian. Sử dụng thư viện **BeautifulSoup4** phân tích cây DOM, trích xuất danh sách các thẻ `<hX data-level="...">` từ Cấp 1 đến Cấp 6, tự động loại bỏ các thẻ HTML toán học con để thu về chuỗi văn bản sạch. Mở tệp PDF qua thư viện **PyMuPDF (`fitz`)**, kích hoạt thuật toán tìm kiếm tịnh tiến (`page.search_for`) để xác định chính xác chỉ mục trang vật lý của từng tiêu đề. Thực thi màng lọc chuẩn hóa phân cấp `_normalize_toc_hierarchy()` tuân thủ quy tắc nhị phân và tiêm trực tiếp Cây Mục lục (**Bookmarks / Outline Tree Cấp 6**) vào lớp siêu dữ liệu của tệp PDF thông qua phương thức `document.saveIncr()`.

---

### 2. GIẢI PHẪU 5 TẦNG BẪY LỖI CÔ LẬP SỰ CỐ (5-TIER FAULT ISOLATION ARCHITECTURE v2.5.1)

Để bảo đảm một tệp Markdown đầu vào bị hỏng cấu trúc hoặc sai định dạng không thể làm sập dây chuyền xử lý hàng loạt của toàn bộ hệ thống, `markdown_to_pdf_engine` v2.5.1 duy trì 5 tầng bẫy lỗi phòng thủ độc lập:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 5 TẦNG BẪY LỖI CÔ LẬP SỰ CỐ ZERO-TRUST (FAULT ISOLATION MATRIX v2.5.1)                           │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
  │
  ├──► [TẦNG 1]: CÔ LẬP NGOẠI LỆ CẤP ĐƠN TỆP (Single-File Failure Isolation)
  │    └─ Bẫy khối try...except bao bọc toàn bộ 4 giai đoạn tại execute_single_file_pipeline().
  │       Bỏ qua tệp lỗi, ghi log cảnh báo và tiếp tục xử lý các tệp tiếp theo trong hàng đợi.
  │
  ├──► [TẦNG 2]: RÀO CHẮN LƯỢC ĐỒ PYDANTIC DTO & GIẢI NÉN ĐỘNG (Schema Barrier & Unpacking)
  │    └─ AppConfig.model_validate() kiểm định cấu hình trong <500ms trước khi chạy đường ống.
  │       Chặn đứng các tham số vi phạm ranh giới vật lý (max_bookmark_level > 6, active_engine sai).
  │
  ├──► [TẦNG 3]: PHÒNG THỦ BĂM MẬT MÃ CHỐNG VA CHẠM REGEX (SHA-256 Masking Defense)
  │    └─ hashlib.sha256() niêm phong các khối mã nguồn trước khi phân tích toán học LaTeX.
  │       Vô hiệu hóa 100% nguy cơ biến dạng mã nguồn và lỗi xung đột ký tự đặc biệt.
  │
  ├──► [TẦNG 4]: BỘ NHỚ TẠM VÔ DANH & RÀO CHẮN ĐỒ HỌA IN ẤN (Ephemeral Memory & Boundaries)
  │    └─ tempfile.NamedTemporaryFile cấp phát bộ nhớ tạm ẩn danh, giải phóng hoàn toàn tại finally.
  │       Chỉ thị break-inside: avoid; và SVG max-width: 100% ngăn chặn tràn lề và lỗi rách trang in.
  │
  └──► [TẦNG 5]: GIỚI HẠN NGOẠI LỆ CÓ CHỦ ĐÍCH TẠI MÔ-ĐUN NHỊ PHÂN (Targeted Containment)
       └─ Mô-đun PyMuPDF chỉ bẫy đích danh 3 nhóm lỗi (OSError, RuntimeError, ValueError).
          Tuân thủ quy chuẩn Ruff BLE001, triệt tiêu nguy cơ nuốt chửng ngoại lệ và bảo toàn Traceback.

```

#### Phân tích Kỹ thuật 5 Tầng Phòng thủ

- **Tầng 1 - Cô lập Ngoại lệ Cấp Đơn Tệp (Single-File Failure Isolation):** Trong tệp `main.py`, hàm `execute_single_file_pipeline()` bao bọc toàn bộ chu trình xử lý của một tệp Markdown trong khối `try...except` diện rộng. Hệ thống bẫy đích danh các nhóm lỗi `(FileNotFoundError, UnicodeDecodeError, ValueError, TypeError, OSError, RuntimeError)`. Khi một tệp bị lỗi, tiến trình chỉ ghi nhận thông báo `[THẤT_BẠI_TỆP]` ra Terminal, trả về giá trị `False`, tăng biến đếm `failure_count` và lập tức chuyển sang tệp tiếp theo mà không làm gián đoạn toàn bộ tiến trình quét hàng loạt.

- **Tầng 2 - Rào chắn Lược đồ Pydantic DTO & Giải nén Động (Schema Barrier & Unpacking):** Trước khi bất kỳ thao tác đọc/ghi nào diễn ra, hàm `load_configuration()` kích hoạt phương thức `AppConfig.model_validate()` để đối soát toàn bộ tệp YAML. Phương thức `@field_validator("active_engine")` kiểm tra tính hợp lệ của cờ chuyển mạch động cơ toán học (`{"katex_placeholder", "mathjax_svg"}`), trong khi `@field_validator("max_bookmark_level")` chặn đứng ngay lập tức nếu giá trị vượt quá giới hạn Cấp 6. Mọi tham số được giải nén qua `.model_dump()` và truyền trực tiếp hạ nguồn, triệt tiêu hoàn toàn sự cố trôi dạt tham số (Parameter Drift).

- **Tầng 3 - Phòng thủ Băm Mật mã Chống Va chạm Regex (SHA-256 Masking Defense):** Trong `src/ast_parser.py` và `src/html_renderer.py`, phương thức `_unify_math_delimiters()` bảo vệ các khối mã nguồn bằng khóa băm `__CRYPTO_MASK_{hash}_{counter}__` được sinh ra từ hàm băm mật mã `hashlib.sha256()`. Cơ chế này ngăn chặn việc Biểu thức Chính quy phân tích toán học can thiệp nhầm vào các ký tự bên trong khối lệnh, loại bỏ 100% rủi ro tấn công va chạm Regex (Regex Collision).

- **Tầng 4 - Bộ Nhớ Tạm Vô Danh & Rào Chắn Đồ Họa In ấn (Ephemeral Memory & Boundaries):** Mô-đun `src/pdf_compiler.py` không bao giờ tạo các tệp HTML tĩnh cố định trên ổ đĩa làm rò rỉ dữ liệu. Tệp HTML trung gian được tạo ngẫu nhiên qua `tempfile.NamedTemporaryFile` và luôn được dọn dẹp sạch sẽ trong khối `finally:`. Đồng thời, các quy tắc CSS Paged Media áp đặt chỉ thị `break-inside: avoid;` cho toàn bộ các bảng biểu, khối mã và hộp Obsidian Callouts, kết hợp với rào chắn `max-width: 100% !important;` cho thẻ SVG của MathJax, triệt tiêu hoàn toàn hiện tượng tràn lề và lỗi ngắt mạch thời gian `PlaywrightTimeoutError`.

- **Tầng 5 - Giới hạn Ngoại lệ Có Chủ đích tại Mô-đun Nhị phân (Targeted Exception Containment):** Trong tệp `src/pdf_metadata_injector.py`, phương thức `inject_metadata()` chỉ bẫy chính xác 3 nhóm ngoại lệ có thể phát sinh từ thao tác nhị phân của PyMuPDF: `(OSError, RuntimeError, ValueError)`. Việc loại bỏ các lệnh `except Exception:` chung chung giúp hệ thống tuân thủ quy chuẩn Linter Ruff `BLE001`, bảo toàn các lỗi hệ thống nghiêm trọng (như `KeyboardInterrupt` hoặc `MemoryError`) để kỹ sư có thể gỡ lỗi chính xác.

---

## CHƯƠNG 6: MA TRẬN KIỂM THỬ MÔ-ĐUN HỘP TRẮNG (MODULAR PYTEST SUITE v2.5.1)

Dự án áp dụng mô hình kiểm thử **Modular Testing Suite** gồm 6 tệp kiểm thử hộp trắng hoàn toàn độc lập đặt trong thư mục `tests/`. Hệ thống vận hành trơn tru trên cả hai khung kiểm thử **Pytest** và **Unittest** bản địa.

Mô hình phân rã mô-đun mang lại vòng lặp phản hồi siêu tốc (Ultra-Fast Feedback Loop dưới 1 giây), cho phép kiểm tra cô lập từng thành phần tính năng mà không phải kích hoạt lại toàn bộ các bài ép tải đa tiến trình nặng.

---

### 1. BẢN ĐỒ MA TRẬN 6 MÔ-ĐUN KIỂM THỬ (TESTING MATRIX OVERVIEW)

```text
tests/
├── __init__.py                  # Khởi tạo gói Python package cho môi trường kiểm thử.
├── test_01_core_pipeline.py     # [MÔ-ĐUN 01] Kiểm thử I/O, quét đệ quy, cô lập tệp hỏng & batch processing.
├── test_02_schema_layout.py     # [MÔ-ĐUN 02] Kiểm thử Pydantic DTO, YAML validation & A4 margin rules.
├── test_03_math_base64.py       # [MÔ-ĐUN 03] Kiểm thử ranh giới TeX, Base64 math AST isolation & HTML escaping.
├── test_04_document_features.py # [MÔ-ĐUN 04 - v2.5.1] Bảng GFM, Bookmarks Cấp 6, Dynamic Callouts & Cascadia Code.
├── test_05_concurrency_stress.py# [MÔ-ĐUN 05] Kiểm thử ProcessPoolExecutor, tempfile bộ nhớ tạm & Playwright.
└── test_06_hybrid_math_engine.py# [MÔ-ĐUN 06] Kiểm thử DTO Routing, Python Mapping, MathJax SVG & Boundaries.

```

---

### 2. PHÂN TÍCH CHUYÊN SÂU TỪNG MÔ-ĐUN KIỂM THỬ

#### 2.1. `test_01_core_pipeline.py` (Core Engine & Batch Routing)

- **Mục tiêu kiểm toán:** Xác thực tính toàn vẹn của luồng I/O cơ sở và bộ điều phối quét hàng loạt.

- **Các kịch bản kiểm tra chính:**
- Kiểm thử hàm `execute_single_file_pipeline()` biên dịch thành công một tệp Markdown tiêu chuẩn sang định dạng PDF đích.

- Kiểm thử cơ chế quét đệ quy (`recursive_search: true`) thu thập chính xác toàn bộ các tệp `.md` nằm trong các nhánh thư mục con.

- Kiểm thử khả năng tự động bảo tồn và tái lập cây thư mục con (`preserve_subfolder_structure: true`) từ thư mục `input/` sang `output/`.

- Kiểm thử khả năng cô lập lỗi của Tầng 1: Đưa một tệp chứa chuỗi byte hỏng nhị phân vào thư mục quét; xác nhận tiến trình ghi nhận lỗi, bỏ qua tệp hỏng và hoàn thành xuất bản các tệp hợp lệ còn lại.

#### 2.2. `test_02_schema_layout.py` (Pydantic DTO & Layout Boundaries)

- **Mục tiêu kiểm toán:** Kiểm định tính đúng đắn của Lược đồ Cấu hình Pydantic DTO và các quy tắc hình học trang in.

- **Các kịch bản kiểm tra chính:**
- Kiểm thử hàm `load_configuration()` nạp và xác thực thành công tệp cấu hình thực tế `config/settings.yaml`.

- Kiểm thử rào chắn cứng `@field_validator("max_bookmark_level")`: Xác nhận Pydantic ném lỗi `ValidationError` trong dưới 500ms khi cấu hình giá trị vượt quá giới hạn (ví dụ: cấp 7) hoặc nhỏ hơn cấp 1.

- Kiểm thử tính toàn vẹn của cấu trúc `DocumentLayoutConfig` (kích thước A4, lề an toàn 20mm, và cơ chế bẻ dòng `break-word`).

#### 2.3. `test_03_math_base64.py` (KaTeX Syntax & AST Isolation)

- **Mục tiêu kiểm toán:** Kiểm tra màng lọc cú pháp LaTeX/KaTeX, cô lập biểu thức toán và mã hóa an toàn các thực thể HTML.

- **Các kịch bản kiểm tra chính:**
- Kiểm thử hàm `_unify_math_delimiters()` chuẩn hóa đồng bộ các dạng ranh giới Brackets `\[...\]` và `\(...\)` sang chuẩn Dollars `$$...$$` và `$...$`.

- Kiểm thử cơ chế mã hóa thực thể HTML an toàn (`&lt;` và `&gt;`) cho các toán tử so sánh nhỏ hơn/lớn hơn bên trong biểu thức toán học nhằm ngăn chặn Chromium nhận diện nhầm thành thẻ DOM.

- Kiểm thử cơ chế dán mặt nạ băm SHA-256 bảo vệ các khối mã nguồn (`code fence`) không bị biến dạng khi màng lọc toán học quét qua.

#### 2.4. `test_04_document_features.py` (Document Typography, Callouts & Bookmarks - MỞ RỘNG v2.5.1)

- **Mục tiêu kiểm toán:** Xác thực toàn diện các tính năng mỹ thuật tài liệu nâng cao, Cây Mục lục PyMuPDF Cấp 6, Động cơ Dynamic Obsidian Callouts và Typography Windows 11.

- **Phân tích Chi tiết 6 Kịch bản Kiểm toán:**
- **Scenario 2 (`test_scenario_2_heading_spoofing_simulation`):** Mô phỏng bẫy tiêu đề giả mạo nằm bên trong khối mã nguồn; xác nhận động cơ AST không sinh nhầm thẻ `<hX>` cho dòng mã giả mạo này.

- **Scenario 8 (`test_scenario_8_gfm_table_parsing_and_structure`):** Kiểm thử bóc tách bảng biểu GFM Markdown và xác nhận sự hiện diện của thẻ `<table>` trong HTML trung gian.

- **Scenario 10 (`test_scenario_10_academic_apa_profile_and_break_avoidance`):** Kiểm thử quy chuẩn in ấn học thuật APA và khả năng xuất bản PDF thực tế không lỗi.

- **Scenario 13 (`test_scenario_13_post_processing_metadata_outline_verification`):** Khởi tạo tài liệu Markdown có cấu trúc tiêu đề từ Cấp 1 đến Cấp 6; sử dụng PyMuPDF kiểm tra Cây Mục lục nhị phân của tệp PDF thành phẩm, xác nhận cấu trúc Bookmarks đạt độ sâu 6 cấp.

- **Scenario 14 (`test_scenario_14_orphaned_heading_tree_injection`):** Kiểm thử cơ chế chuẩn hóa Cây Mục lục khi tài liệu chứa tiêu đề mồ côi hoặc nhảy cấp bất thường (như H3 nhảy lên H5).

- **Scenario 15 (`test_scenario_15_gfm_alerts_semantic_parsing_and_isolation` - MỚI v2.5.1):** Kiểm toán Động cơ Can thiệp Vòng đời AST Callouts Động tại `src/html_renderer.py`. Khởi tạo văn bản Markdown chứa toàn bộ các biến thể `> [!Note]`, `> [!WARNING]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!CAUTION]`, và các trích dẫn thông thường. Màng lọc Assertions kiểm tra:

1. HTML thành phẩm phải chứa đầy đủ các thẻ ngữ nghĩa `<div class="markdown-alert markdown-alert-note">`, `<div class="markdown-alert markdown-alert-warning">`, v.v.

2. Tuyệt đối triệt tiêu toàn bộ các chuỗi tiền tố thô `[!Note]`, `[!WARNING]`, `[!TIP]` khỏi nội dung thẻ đoạn văn `<p>`.

3. Khối trích dẫn tiêu chuẩn (không chứa cú pháp Callout) phải được bảo toàn nguyên vẹn dưới dạng thẻ `<blockquote>`.

- **Scenario 16 (`test_scenario_16_inline_code_backtick_and_css_rules_verification` - MỚI v2.5.1):** Kiểm toán khả năng kết xuất chữ trong dấu Backtick và Ma trận CSS Paged Media tại `src/pdf_compiler.py`. Màng lọc Assertions kiểm tra:

1. Các đoạn mã nội dòng đan xen trong văn bản và trong tiêu đề phải sinh ra đúng thẻ `<code>`.

2. Ký tự phân cấp `>` nằm trong dấu nháy ngược (`>`) phải được mã hóa an toàn thành `<code>&gt;</code>`.

3. Bộ CSS Paged Media của `PDFCompiler` bắt buộc phải chứa các bộ chọn phân lập `:not(pre) > code`, `blockquote`, các lớp `.markdown-alert`, và chỉ thị phòng thủ in ấn `break-inside: avoid;`.

#### 2.5. `test_05_concurrency_stress.py` (Process Isolation & Ephemeral Memory)

- **Mục tiêu kiểm toán:** Ép tải đa tiến trình vật lý song song và xác thực tính an toàn của bộ nhớ tạm vô danh.

- **Các kịch bản kiểm tra chính:**
- Kích hoạt `ProcessPoolExecutor` phân bổ đồng thời 10 tác vụ biên dịch PDF trên 4 tiến trình Worker vật lý độc lập.

- Xác nhận mỗi Worker Playwright Chromium sở hữu một Vòng lặp Sự kiện (Event Loop) riêng biệt, không xảy ra xung đột bộ nhớ hay treo tiến trình.

- Kiểm tra việc cấp phát và dọn dẹp sạch sẽ 100% các tệp tạm thời `tempfile.NamedTemporaryFile` sau khi hoàn thành chu trình ép tải.

#### 2.6. `test_06_hybrid_math_engine.py` (Hybrid Math Engine & SVG Boundaries)

- **Mục tiêu kiểm toán:** Kiểm định toàn diện Kiến trúc Động cơ Toán học Lai KaTeX và MathJax v3 Vector SVG.

- **Các kịch bản kiểm tra chính:**
- Kiểm thử xác thực cờ DTO `math_engine_routing.active_engine` (chấp nhận `"katex_placeholder"` và `"mathjax_svg"`, chặn các giá trị không hợp lệ).

- Kiểm thử thuật toán **Server-Side Python Dictionary Mapping**: Xác minh các vĩ lệnh `\text{...}` chứa Tiếng Việt được bóc tách vào `self.vn_math_store`, thay bằng mã `VILANGMASK0001` và tiêm script Swap Hậu kỳ.

- Kiểm thử môi trường MathJax v3: Xác minh đối tượng `window.MathJax` (`fontCache: 'global'`) và tệp `tex-svg.js` được tiêm chính xác khi chọn nhánh `mathjax_svg`.

- Kiểm tra sự hiện diện của rào chắn CSS Paged Media `mjx-container[jax="SVG"] svg { max-width: 100% !important; }`.

- Thực hiện biên dịch End-to-End thực tế một tệp chứa công thức toán phức tạp sang PDF qua Playwright Chromium.

---

### 3. TỔNG HỢP CÂU LỆNH THỰC THI KIỂM THỬ (POWERSHELL COMMAND BLOCK)

Toàn bộ các câu lệnh kích hoạt môi trường ảo, thực thi toàn bộ ma trận kiểm thử, chạy chuyên biệt từng tệp hoặc lọc kịch bản trên Windows PowerShell được đóng gói trong duy nhất một khối mã dưới đây:

```powershell
# ==============================================================================
# HƯỚNG DẪN LỆNH THỰC THI BỘ KIỂM THỬ MÔ-ĐUN (WINDOWS 11 POWERSHELL)
# Dự án: markdown_to_pdf_engine (Phiên bản v2.5.1)
# ==============================================================================

# BƯỚC 1: Kích hoạt Môi trường ảo Python
.\venv\Scripts\Activate.ps1

# ------------------------------------------------------------------------------
# PHƯƠNG ÁN 1: THỰC THI TOÀN BỘ 6 MÔ-ĐUN KIỂM THỬ VỚI PYTEST
# ------------------------------------------------------------------------------
# Chạy toàn bộ bộ test với chế độ hiển thị chi tiết (Verbose):
pytest tests/ -v

# Chạy toàn bộ bộ test và cho phép xuất các dòng print ra màn hình Terminal:
pytest tests/ -v -s

# ------------------------------------------------------------------------------
# PHƯƠNG ÁN 2: THỰC THI CHUYÊN BIỆT TỪNG TỆP KIỂM THỬ (TARGETED TESTING)
# ------------------------------------------------------------------------------
# 1. Chạy Mô-đun 04 (GFM Tables, Bookmarks Cấp 6, Dynamic Callouts & Cascadia Code):
pytest tests/test_04_document_features.py -v

# 2. Chạy Mô-đun 06 (Kiến trúc Động cơ Toán học Lai KaTeX & MathJax v3):
pytest tests/test_06_hybrid_math_engine.py -v

# 3. Chạy Mô-đun 01 (Luồng xử lý I/O cơ sở và quét đệ quy hàng loạt):
pytest tests/test_01_core_pipeline.py -v

# 4. Chạy Mô-đun 02 (Xác thực Lược đồ Pydantic DTO và Bố cục Trang in):
pytest tests/test_02_schema_layout.py -v

# 5. Chạy Mô-đun 03 (Màng lọc Base64 và cô lập cú pháp công thức Toán):
pytest tests/test_03_math_base64.py -v

# 6. Chạy Mô-đun 05 (Ép tải Đa tiến trình ProcessPoolExecutor & Playwright):
pytest tests/test_05_concurrency_stress.py -v

# ------------------------------------------------------------------------------
# PHƯƠNG ÁN 3: LỌC KỊCH BẢN KIỂM TOÁN MỚI THEO TỪ KHÓA (PATTERN FILTERING)
# ------------------------------------------------------------------------------
# Chỉ chạy riêng Kịch bản 15 (Bóc tách cú pháp Dynamic Obsidian Callouts):
pytest tests/test_04_document_features.py -k "test_scenario_15" -v

# Chỉ chạy riêng Kịch bản 16 (Khối mã nội dòng Backtick và Ma trận CSS Paged Media):
pytest tests/test_04_document_features.py -k "test_scenario_16" -v

# ------------------------------------------------------------------------------
# PHƯƠNG ÁN 4: THỰC THI QUA TRÌNH THÔNG DỊCH PYTHON BẢN ĐỊA (UNITTEST DISCOVERY)
# ------------------------------------------------------------------------------
# Chạy trực tiếp tệp kiểm thử số 04 mà không cần cài đặt gói Pytest:
python tests/test_04_document_features.py

# Tự động quét và chạy toàn bộ thư mục tests/ bằng unittest:
python -m unittest discover -s tests -p "test_*.py" -v

```

---

## CHƯƠNG 7: LỊCH SỬ PHIÊN BẢN TOÀN DIỆN (CHANGELOG v2.0.0 - v2.5.1)

Chương này ghi nhận toàn bộ quá trình tiến hóa kiến trúc của dự án `markdown_to_pdf_engine`, từ giai đoạn chuẩn hóa DTO cơ sở đến kiến trúc động cơ toán học lai và hệ thống Obsidian Callouts động kết hợp Typography Windows 11 bản địa.

---

### Phiên bản v2.5.1 (Bản Vá Chuẩn Hóa Header Imports & Khử Cảnh Báo Linter - Hiện tại)

- **Tái cấu trúc Module-Level Imports (`src/pdf_compiler.py`):** Di chuyển toàn bộ các lệnh nạp thư viện `tempfile`, `pathlib.Path`, `typing.Any`, `PlaywrightTimeoutError` và `sync_playwright` lên phần đầu tệp ở phạm vi module level.

- **Triệt tiêu 100% Cảnh báo Phân tích Tĩnh (Zero-Warning Standard):** Xử lý dứt điểm các mã lỗi nghiêm trọng từ **Pylance** (`reportUndefinedVariable`, `reportPossiblyUnboundVariable`) và **Ruff** (`F821: undefined-name`, `I001: unsorted-imports`).

- **Bảo toàn Tính Toàn vẹn của Ephemeral Memory:** Duy trì cơ chế cấp phát và giải phóng tệp tạm thời vô danh qua `tempfile.NamedTemporaryFile` kết hợp khối `finally:`, bảo đảm không rò rỉ bộ nhớ hoặc tài nguyên tệp rác trên hệ điều hành.

---

### Phiên bản v2.5.0 (Bản Nâng Cấp Dynamic Obsidian Callouts & Hệ Nền Typography Windows 11)

- **Động cơ Dynamic Callout AST Interception (`src/html_renderer.py`):** Xóa bỏ hoàn toàn danh sách từ khóa tĩnh trong Biểu thức Chính quy, chuyển đổi sang mẫu Regex mở `r"^\[!([a-zA-Z0-9_-]+)\]([+-]?)[ \t]*(.*)"`. Động cơ có khả năng tự động nhận diện mọi định danh Callout theo chuẩn Obsidian và GFM mở rộng (`note`, `tip`, `warning`, `caution`, `important`, `quote`, `cite`, `abstract`, `todo`, `bug`, `example`, `faq`, `success`, `failure`).

- **Tách Lớp Tiêu Đề Ngữ Nghĩa (DOM Restructuring):** Tự động bóc tách tiêu đề tùy biến (`custom_title`) và cờ thu gọn (`fold_flag`), loại bỏ hoàn toàn dòng khai báo cú pháp thô khỏi thẻ con `<p>`, và sinh cấu trúc khối HTML ngữ nghĩa `<div class="markdown-alert markdown-alert-{type}" data-callout="{type}">` kèm thanh tiêu đề độc lập `<div class="markdown-alert-title"><span class="markdown-alert-icon"></span><span class="markdown-alert-label">{Tiêu đề}</span></div>`.

- **Hệ Thống Phông Chữ Bản Địa Windows 11 Song Ngữ (`src/pdf_compiler.py`):**
- Văn bản chính: Thiết lập Font Stack `"Segoe UI Variable Text"`, `"Segoe UI"`, `"Calibri"`, `"Arial"`, tối ưu hóa việc khử răng cưa và bảo toàn dấu thanh Tiếng Việt Unicode NFC.

- Khối mã & Inline Code: Trang bị bộ phông chữ bản địa thế hệ mới `"Cascadia Code"` và `"Cascadia Mono"` kết hợp `Consolas`, mang lại tỷ lệ Monospace chuẩn mực, nét chữ sắc nét trên bản in PDF.

- **Ma Trận CSS Callouts Phân Tầng:** Xây dựng kiểu dáng nền tảng cho bộ chọn toàn năng `[data-callout]` kết hợp 6 nhóm phối màu chuyên biệt, tích hợp chỉ thị phòng thủ in ấn `break-inside: avoid;` chống xẻ đôi khối hộp giữa hai trang in.

---

### Phiên bản v2.4.0 (Bản Cải Tiến Typography Patch & GFM Alerts Cơ Bản)

- **Cô lập và Nâng cấp Khối Mã Nội dòng (Backtick Typography):** Tách bộ chọn `:not(pre) > code` ra khỏi khối định dạng mã nhiều dòng, cấp phát màu nền xám mờ `rgba(175, 184, 193, 0.22)`, khoảng đệm `padding: 0.15em 0.45em`, bo góc `5px` và đường viền siêu mảnh, giải quyết triệt để hiện tượng chữ trong dấu Backtick bị chìm vào văn bản thô.

- **Định tuyến Lại Khối Trích dẫn Tiêu chuẩn (`blockquote`):** Giải phóng thẻ `blockquote` khỏi nhóm thẻ văn bản cơ sở, thiết lập đường viền trái `4px solid #d0d7de`, màu nền `#f6f8fa` và bo góc viền phải.

- **Mở rộng Ma trận Kiểm thử Mô-đun (`tests/test_04_document_features.py`):** Bổ sung Kịch bản 15 (`test_scenario_15`) kiểm toán bóc tách cú pháp Callouts/Alerts và Kịch bản 16 (`test_scenario_16`) kiểm toán kết xuất Inline Code Backtick cùng các quy tắc CSS Paged Media.

---

### Phiên bản v2.3.0 (Bản Nâng Cấp Hybrid Math Engine & Modular Pytest Suite)

- **Kiến trúc Động cơ Toán học Lai (Hybrid Math Engine):** Bổ sung phân khu `math_engine_routing` trong `config/settings.yaml` với cờ rẽ nhánh `active_engine` cho phép chuyển đổi linh hoạt giữa động cơ KaTeX (tốc độ cao) và động cơ MathJax v3 Vector SVG Offline (mỹ thuật hoàn hảo).

- **Thuật toán Server-Side Python Dictionary Mapping:** Bóc tách các chuỗi Tiếng Việt trong vĩ lệnh `\text{...}` sang từ điển `self.vn_math_store`, thay bằng mã giữ chỗ `VILANGMASK0001` và dùng script hoán đổi Text Nodes hậu kỳ để Chromium áp dụng bộ xếp chữ HarfBuzz bản địa, triệt tiêu 100% lỗi bay dấu Tiếng Việt.

- **Môi trường MathJax v3 Vector SVG Offline:** Tích hợp tệp nhị phân `assets/mathjax/tex-svg.js` và đối tượng `window.MathJax` (`fontCache: 'global'`).

- **Rào chắn CSS SVG Boundaries:** Bổ sung quy tắc `mjx-container[jax="SVG"] svg { max-width: 100% !important; height: auto !important; }` khống chế lề in A4 an toàn 170mm, loại bỏ lỗi tràn lề và ngắt mạch `PlaywrightTimeoutError`.

- **Đại phẫu Hạ tầng Kiểm thử:** Thay thế tệp đơn khối cũ bằng 6 mô-đun kiểm thử biệt lập (`test_01` đến `test_06`) vận hành bởi `pytest`.

---

### Phiên bản v2.2.0 (Bản Cải Tiến AST-Level Math Escape & Strict CSS Typography)

- **Thoát Ký tự Toán học Cấp AST:** Chuẩn hóa thực thể HTML (`&lt;` và `&gt;`) trực tiếp trên các Token AST toán học trong `src/html_renderer.py`, ngăn ngừa Chromium nhận diện nhầm toán tử so sánh thành thẻ DOM.

- **Chuẩn hóa Unicode NFC Toàn cục:** Tích hợp `unicodedata.normalize("NFC", ...)` tại `src/ast_parser.py` và `src/html_renderer.py`, gộp toàn bộ ký tự Tiếng Việt tổ hợp dạng NFD về dạng ký tự nguyên khối Unicode chuẩn.

- **Gia cố Lớp giáp Typography:** Cấu hình thuộc tính CSS `display: inline-block !important;` cho thẻ `.vietnamese-math-text` trong `src/pdf_compiler.py`.

---

### Phiên bản v2.0.0 (Bản Nâng Cấp Base64 AST Isolation & Context Architecture)

- **Kiến trúc ExecutionContext SSOT:** Khởi tạo lớp DTO `ExecutionContext` trong `main.py`, đóng gói toàn bộ `AppConfig` và thông tin đường dẫn I/O nhằm triệt tiêu sự cố trôi dạt tham số hạ nguồn.

- **Giải nén DTO Không Thất thoát (Zero-Loss Unpacking):** Sử dụng phương thức `.model_dump()` trích xuất từ điển cấu hình từ Pydantic DTO và truyền trực tiếp xuống các lớp xử lý hạ nguồn.

- **Mã hóa Base64 TeX AST Isolation:** Tích hợp tùy chọn mã hóa Base64 biểu thức toán học thô trong `src/ast_parser.py` để bảo vệ cú pháp TeX trước các trình cắm Markdown bổ trợ.

- **Mở rộng Dấu trang Cấp 6:** Nâng tham số `max_bookmark_level` trong Pydantic DTO từ 4 lên 6, cho phép PyMuPDF tiêm Cây Mục lục PDF sâu đến Heading Cấp 6.

---

## CHƯƠNG 8 (PHỤ LỤC): CẨM NANG CÚ PHÁP OBSIDIAN CALLOUTS VÀ BẢNG TRA CỨU MÃ MÀU MỸ THUẬT (SYNTAX & STYLE GUIDE v2.5.1)

Chương này đóng vai trò là tài liệu hướng dẫn thực hành dành cho người dùng soạn thảo tài liệu Markdown, chuẩn hóa quy tắc viết Callouts, mã nguồn nội dòng và biểu thức toán học song ngữ.

---

### 1. QUY TẮC CÚ PHÁP OBSIDIAN CALLOUTS VÀ EXTENDED GFM ALERTS

Động cơ `markdown_to_pdf_engine` v2.5.1 hỗ trợ trọn vẹn đặc tả Obsidian Callouts với 3 hình thái linh hoạt:

- **Cú pháp Khối Tiêu chuẩn (Standard Callout):**

```markdown
> [!NOTE]
> Đây là nội dung ghi chú thông thường.
```

- **Cú pháp Khối với Tiêu đề Tùy biến (Custom Title Callout):**

```markdown
> [!WARNING] CẢNH BÁO RỦI RO KIẾN TRÚC HỆ THỐNG
> Nội dung cảnh báo chi tiết đặt tại đây.
```

- **Cú pháp Khối Hỗ trợ Cờ Thu gọn (Foldable Callout Flag):**

```markdown
> [!TIP]+ Mẹo Tối Ưu Hóa Hiệu Năng
> Dấu cộng (+) hoặc trừ (-) sẽ được bộ bóc tách tự động chuẩn hóa mà không làm vỡ cấu trúc văn bản.
```

---

### 2. MA TRẬN 6 NHÓM PHỐI MÀU CALLOUTS VÀ BẢNG TRA CỨU CSS (CSS COLOR MATRIX)

Hệ thống CSS Paged Media tại `src/pdf_compiler.py` tự động ánh xạ các định danh Callout vào 6 nhóm phối màu chuyên nghiệp dưới đây:

| Nhóm Phân Loại | Định Danh Hỗ Trợ (`data-callout`) | Biểu Tượng Icon | Màu Viền Trái (`border-left`) | Màu Nền Hộp (`background-color`) | Mục Đích Ứng Dụng Thực Tế |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Note & Info** | `note`, `info` | ℹ️ | `#0969da` (Xanh lam) | `rgba(9, 105, 218, 0.05)` | Cung cấp thông tin bổ trợ, ngữ cảnh nền tảng hoặc giải thích thuật ngữ. |
| **2. Tip & Success** | `tip`, `success`, `done` | 💡 / ✅ | `#1a7f37` (Xanh lá) | `rgba(26, 127, 55, 0.05)` | Hướng dẫn mẹo vặt, gợi ý thực hành tốt nhất hoặc thông báo thành công. |
| **3. Important & Todo** | `important`, `todo` | 💬 / 📋 | `#8250df` (Tím) | `rgba(130, 80, 223, 0.05)` | Thông điệp tối quan trọng, quy tắc bắt buộc hoặc danh sách đầu việc cần làm. |
| **4. Warning & Attention** | `warning`, `attention` | ⚠️ | `#9a6700` (Vàng cam) | `rgba(154, 103, 0, 0.06)` | Cảnh báo rủi ro kỹ thuật, điểm mù logic hoặc lưu ý bảo mật nghiêm ngặt. |
| **5. Caution & Danger** | `caution`, `danger`, `error`, `bug` | 🛑 / 🪲 | `#d1242f` (Đỏ thẫm) | `rgba(209, 36, 47, 0.05)` | Cảnh báo nguy hiểm, hành vi phá hủy dữ liệu hoặc báo cáo lỗi hệ thống. |
| **6. Quote & Cite** | `quote`, `cite` | ❞ | `#57606a` (Xám tro) | `rgba(87, 96, 106, 0.06)` | Trích dẫn danh ngôn, trích đoạn tài liệu tham khảo hoặc lời phát biểu. |
| **7. Fallback Mặc Định** | _(Mọi từ khóa tùy biến khác)_ | _(Không icon)_ | `#6b7280` (Xám trung tính) | `rgba(243, 244, 246, 0.70)` | Tự động định hình khối hộp cho bất kỳ nhãn Callout tự tạo nào của người dùng. |

---

### 3. QUY CHUẨN SOẠN THẢO CÔNG THỨC TOÁN VÀ CHỮ TRONG DẤU BACKTICK

- **Chữ trong dấu nháy ngược (Inline Code):** Sử dụng cặp dấu Backtick đơn `doan_ma_nguon`. Trình biên dịch sẽ tự động áp dụng phông chữ `"Cascadia Code"`, màu chữ `#0969da` và nền xám mờ bo góc.

- **Công thức Toán học Nội dòng (Inline Math):** Đặt giữa cặp dấu `$...$` hoặc `\(...\)` (ví dụ: `$E = mc^2$`).

- **Công thức Toán học Dạng Khối (Display Block Math):** Đặt giữa cặp dấu `$$...$$` hoặc `\[...\]` (ví dụ: `$$\sum_{i=1}^n x_i$$`).

- **Văn bản Tiếng Việt bên trong Công thức Toán:** BẮT BUỘC đặt trong các vĩ lệnh `\text{...}`, `\textbf{...}` hoặc `\textit{...}` (ví dụ: `$$\text{Vận tốc } v = \frac{s}{t} \quad (\text{với } s \text{ là quãng đường})$$`). Thuật toán Server-Side Python Dictionary Mapping sẽ tự động bảo vệ tính nguyên vẹn của dấu thanh Tiếng Việt.

---

### 4. TÀI LIỆU MẪU THỰC HÀNH TOÀN DIỆN (COMPREHENSIVE MARKDOWN TEST SPECIFICATION)

Dưới đây là một tệp Markdown mẫu hoàn chỉnh chứa toàn bộ các thành phần cú pháp nâng cao của phiên bản v2.5.1. Bạn có thể sao chép toàn bộ khối mã duy nhất này và lưu thành tệp `input/demo_v251.md` để kiểm tra trực tiếp chất lượng xuất bản PDF:

```markdown
# I. TÀI LIỆU KIỂM TOÁN TỔNG THỂ HỆ THỐNG BIÊN DỊCH v2.5.1

Tài liệu này đóng vai trò là bản kiểm toán mẫu nhằm kiểm tra chất lượng kết xuất của Động cơ Obsidian Callouts, Hệ thống Typography Windows 11 bản địa và Động cơ Toán học Lai.

---

## 1.1. Thí nghiệm Chữ trong Dấu Nháy Ngược (Inline Code Typography)

Trong môi trường Windows 11, các đoạn mã nội dòng như `config.local.yaml`, `ProcessPoolExecutor`, hoặc lệnh khởi chạy `pytest tests/ -v` được tự động kết xuất bằng phông chữ `Cascadia Code` với tỷ lệ bo góc 5px và màu nền bán trong suốt.

Đoạn mã sau kiểm tra ký tự điều hướng phân cấp: `src/` > `html_renderer.py` > `pdf_compiler.py`.

---

## 1.2. Thí nghiệm Ma Trận 6 Nhóm Obsidian Callouts & GFM Alerts

> [!NOTE] MỤC TIÊU & CÂU HỎI KHAI PHÓNG
> Khối ghi chú màu xanh lam cung cấp các thông tin định hướng và bối cảnh nghiên cứu nền tảng.

> [!TIP] MẸO SOẠN THẢO VÀ TỐI ƯU HÓA
> Sử dụng phím tắt và các trình cắm tự động định dạng trên VSCode để tăng tốc độ soạn thảo Markdown.

> [!IMPORTANT] THÔNG ĐIỆP TỐI QUAN TRỌNG
> Mọi tham số cấu hình bắt buộc phải được kiểm định nghiêm ngặt qua mô hình Pydantic DTO trước khi chuyển hạ nguồn.

> [!WARNING] CẢNH BÁO RỦI RO BẢO MẬT & RÒ RỈ I/O
> Tuyệt đối không đẩy tệp cấu hình chứa thông tin nhạy cảm lên kho mã nguồn công khai.

> [!CAUTION] THẬN TRỌNG NGUY HIỂM KHI THAO TÁC BỘ NHỚ
> Lệnh `del` chỉ xóa liên kết danh định trong namespace hiện tại, không đảm bảo giải phóng bộ nhớ tức thì.

> [!QUOTE] TRÍCH DẪN KỸ THUẬT KINH ĐIỂN
> "Đơn giản là điều kiện tiên quyết cho sự tin cậy." — Edsger W. Dijkstra

> [!CUSTOM] KHỐI THÔNG BÁO VỚI TỪ KHÓA TỰ ĐỊNH NGHĨA
> Động cơ tự động áp dụng kiểu dáng Fallback nền xám trung tính cho mọi định danh Callout tùy biến.

> Đây là đoạn trích dẫn khối tiêu chuẩn (Standard Blockquote) sử dụng đường viền xám truyền thống.

---

## 1.3. Thí nghiệm Công Thức Toán Học Song Ngữ (Hybrid Math & Vietnamese Text)

Công thức toán học nội dòng: Năng lượng nghỉ của vật thể được tính theo phương trình Einstein $E = mc^2$, trong đó $m$ là khối lượng và $c$ là vận tốc ánh sáng trong chân không.

Công thức toán học dạng khối chứa Tiếng Việt nguyên khối qua thuật toán Server-Side Python Dictionary Mapping:

$$
\text{Độ lệch chuẩn mẫu } s = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2} \quad \text{với } \bar{x} \text{ là giá trị trung bình cộng}
$$

Phương trình tích phân vi phân phức tạp:

$$
\oint_{C} \mathbf{B} \cdot d\mathbf{l} = \mu_0 \left( I_{\text{dẫn}} + \varepsilon_0 \frac{d\Phi_{\text{E}}}{dt} \right)
$$

---

## 1.4. Thí nghiệm Bảng Biểu Khung Lưới GFM (Tables)

| STT | Tên Mô-đun Hệ Thống            | Trách Nhiệm Đơn Lẻ (SoC)                     | Trạng Thái Hoạt Động |
| :-: | :----------------------------- | :------------------------------------------- | :------------------: |
|  1  | `src/ast_parser.py`            | Quét AST CommonMark & Dán mặt nạ SHA-256     |       Sẵn sàng       |
|  2  | `src/html_renderer.py`         | Bóc tách Dynamic Callouts & Python Mapping   |       Sẵn sàng       |
|  3  | `src/pdf_compiler.py`          | CSS Paged Media Windows 11 & Playwright A4   |       Sẵn sàng       |
|  4  | `src/pdf_metadata_injector.py` | Quét nhị phân PyMuPDF & Tiêm Bookmarks Cấp 6 |       Sẵn sàng       |
```
