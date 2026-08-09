# MARKDOWN TO PDF ENGINE (Lõi Biên dịch Tài liệu Cục bộ & Chuẩn in ấn Học thuật - Phiên bản v1.3.2)

**Một hệ thống đường ống dữ liệu (Data Pipeline) tự động hóa toàn diện, chuyên trách chuyển đổi hàng loạt tệp Markdown sang định dạng PDF chuẩn Typography xuất bản, đồ họa toán học sắc nét và bảng biểu GFM khung lưới hoàn chỉnh ngay trên môi trường Windows 11 cục bộ.**

Dự án được xây dựng dựa trên tư duy phân tách hệ thống nghiêm ngặt, khép kín và độc lập ngoại tuyến (Offline-first). Hệ thống nói KHÔNG với các công nghệ đám mây (Cloud), máy chủ web hay cơ sở dữ liệu phức tạp. Mọi tiến trình biên dịch đều diễn ra trên máy cục bộ, bảo đảm tính bảo mật dữ liệu tuyệt đối và khả năng can thiệp tham số linh hoạt thông qua hệ thống cấu hình tách biệt.

---

## TRIẾT LÝ KIẾN TRÚC VÀ 6 TRỤ CỘT PHÒNG THỦ (ARCHITECTURAL PHILOSOPHY)

Để hình dung phương thức vận hành của hệ thống, hãy tưởng tượng dự án giống như một **Nhà máy In ấn Công nghiệp Khép kín**. Thay vì cho phép công nhân tự do can thiệp vào dây chuyền, nhà máy vận hành dựa trên 6 trụ cột kiến trúc bất biến nhằm loại trừ hoàn toàn mọi rủi ro gián đoạn tiến trình:

### 1. Phân tách Mối quan tâm (Separation of Concerns - SoC)

- **Ẩn dụ đời thực:** Trong một nhà hàng cao cấp, Bếp Trưởng (Mã logic Python) không bao giờ tự mình quyết định giá tiền hay danh sách món ăn; họ chế biến dựa trên một cuốn Thực Đơn (Tệp cấu hình) do Quản lý quy định. Khi cần đổi món hoặc điều chỉnh giá, Quản lý chỉ cần sửa Thực Đơn mà không phải thay thế Bếp Trưởng.
- **Áp dụng vào hệ thống:** Tách rời hoàn toàn tham số điều khiển khỏi mã nguồn xử lý chính. Mọi tiến trình biên dịch đều nạp cấu hình từ tệp YAML chuyên biệt (`config/settings.yaml`). Toàn bộ thông số như lề giấy, chuẩn mã hóa, màu sắc từ khóa mã nguồn, giới hạn độ sâu dấu trang (Bookmarks Palette), chế độ đánh số tiêu đề tự động (CSS Counters), van điều khiển toán học và ma trận học thuật đều được tập trung duy nhất tại đây.

### 2. Chống Trôi dạt Mã hóa Luồng I/O (I/O Encoding Drift Defense)

- **Ẩn dụ đời thực:** Tưởng tượng nhà máy tiếp nhận nguyên liệu từ nhiều quốc gia nhưng băng chuyền mặc định chỉ đọc được ký tự tiếng Anh. Khi một kiện hàng ghi nhãn Tiếng Việt đi qua, hệ thống đọc sai mã và làm nghiền nát kiện hàng.
- **Áp dụng vào hệ thống:** Hệ điều hành Windows 11 vận hành mặc định với bảng mã `cp1252`. Khi nạp văn bản đa ngôn ngữ chứa ký tự Tiếng Việt, hệ thống sẽ ném ra ngoại lệ `UnicodeDecodeError` hoặc làm biến dạng ký tự có dấu nếu luồng nạp không được cưỡng chế chuẩn. Hệ thống xác lập hằng số `utf-8` làm kim chỉ nam bắt buộc cho toàn bộ giao thức Đọc (Read), Ghi (Write) và Kết xuất (Render).

### 3. Phân tích Cây Cú pháp Trừu tượng (AST Engine - GFM Tables & Math - v1.3.2)

- **Ẩn dụ đời thực:** Dùng Biểu thức chính quy (Regex) để tìm và sửa văn bản giống như việc nhắm mắt dùng kéo cắt một bản vẽ kiến trúc dựa trên việc đếm số nét vẽ; nó rất dễ cắt nhầm vào dầm cột. Dùng AST giống như việc quét tia laser 3D toàn bộ tòa nhà, nhận diện rõ đâu là "Cửa sổ", đâu là "Bức tường", đâu là "Bàn ghế", sau đó mới tiến hành thi công.
- **Áp dụng vào hệ thống:** Hệ thống từ chối phương pháp thay thế chuỗi tuần tự (Regex) thiếu an toàn. Bắt buộc áp dụng cơ chế Cây cú pháp trừu tượng (Abstract Syntax Tree - AST) thông qua thư viện `markdown-it-py` với preset `gfm-like` tích hợp `linkify-it-py`. Các Nút mã nguồn (`fence`), Nút toán học (`math_inline`, `math_block`) và Nút bảng biểu (`table_open`, `tr_open`, `td_open`) được cô lập hoàn toàn, không cho phép rò rỉ định dạng ra ngoài.

### 4. Động cơ Biên dịch Toán học Ngoại tuyến (Offline MathML Translation Engine)

- **Ẩn dụ đời thực:** Thay vì gửi bản thảo chứa công thức toán lên một trung tâm tính toán trên đám mây rồi chờ gửi kết quả hình ảnh về, nhà máy trang bị một **Máy đúc chữ 3D cục bộ**. Máy này tự chuyển đổi các ký hiệu công thức thô thành khuôn kim loại sắc nét ngay tại chỗ mà không cần kết nối Internet.
- **Áp dụng vào hệ thống:** Hệ thống tích hợp bộ lọc `texmath` của `mdit-py-plugins` ở khâu phân tích AST để nhận diện dấu bọc `$` và `$$`. Module `src/html_renderer.py` sử dụng thư viện `latex2mathml` để dịch trực tiếp chuỗi LaTeX thành mã HTML MathML (`<math>...</math>`). Module `src/pdf_compiler.py` áp dụng lớp giáp CSS Paged Media với phông chữ `Cambria Math` và quy tắc `vertical-align: baseline` để cưỡng chế định dạng chỉ số mũ (`msup`) và chỉ số dưới (`msub`) căn chính xác theo đường cơ sở văn bản.

### 5. Quản lý Tràn viền Bảng biểu và Cảnh báo Cắt Lề (Table Overflow Clipping & Warning - NEW v1.3.2)

- **Ẩn dụ đời thực:** Khi chở một kiện hàng Bảng biểu khổng lồ có chiều rộng vượt quá thùng xe tải (khổ giấy A4), người tài xế thông minh sẽ dùng máy cắt gọt bỏ phần dư thừa thò ra ngoài thành xe để tránh gây tai nạn giao thông, đồng thời bấm còi báo động cho trung tâm điều phối biết kiện hàng đã bị xén bớt.
- **Áp dụng vào hệ thống:** Đối với các bảng biểu chứa lượng dữ liệu khổng lồ (nhiều cột) vượt quá độ rộng vùng in an toàn của khổ A4 (170mm), hệ thống kích hoạt chiến lược `clip_and_warn`. Lớp giáp CSS sẽ tự động cắt bỏ (clip) phần chữ bị tràn ngang lề giấy để bảo vệ thẩm mỹ chung của bản in, đồng thời bắn nhật ký cảnh báo màu vàng ra Terminal để người dùng nắm thông tin.

### 6. Ma trận In ấn Học thuật & Typography Tiêu đề Khóa Sàn (Academic Standards & Typography Floor - NEW v1.3.2)

- **Ẩn dụ đời thực:** Trong việc cắm biển chỉ dẫn giao thông, các biển báo đường lớn (H1-H4) được đánh số kilomet rõ ràng. Khi đi vào các ngõ hẻm nhỏ (H5-H6), người ta không đánh chuỗi số nhà dài ngoẵng như `1.1.1.1.1.1` để tránh gây rối mắt; thay vào đó, họ phủ một lớp **Sơn Phản Quang In Đậm (Bold & Italic)** lên biển báo. Người đi đường không cần đọc số dài vẫn nhận diện được ngay lập tức ranh giới khu vực.
- **Áp dụng vào hệ thống:** Tích hợp bộ quy chuẩn học thuật quốc tế (APA 7th, IEEE, Harvard). Giới hạn tự động đánh số bằng CSS Counters ở cấp 4 (`h1` đến `h4`) để giải phóng tải trọng nhận thức cho độc giả. Toàn bộ các tiêu đề từ `h1` đến `h6` được cưỡng chế In đậm (`font-weight: bold !important;`). Riêng `h5` và `h6` được khóa sàn kích thước phông chữ ở mức **11pt** (ngang bằng văn bản nội dung, xóa bỏ sự cố chữ H5/H6 bị bóp nhỏ hơn chữ thường) kết hợp định dạng In nghiêng (`font-style: italic;`) để đáp ứng chính xác quy định xuất bản học thuật.

---

## BẢN ĐỒ CẤU TRÚC THƯ MỤC (DIRECTORY BLUEPRINT v1.3.2)

Dưới đây là sơ đồ không gian làm việc (Workspace) tiêu chuẩn trên VSCode. Mỗi thành phần đều giữ một vùng trách nhiệm duy nhất (Single Responsibility Principle):

```text
MARKDOWN_TO_PDF_ENGINE/
│
├── config/
│   └── settings.yaml          # [Bảng Điều Khiển Trung Tâm] Khai báo 10 phân khu tham số vận hành, Bảng GFM & Chuẩn APA.
│
├── input/                     # [Kho Nguyên Liệu] Thư mục chứa các tệp .md đầu vào (Tự động khởi tạo & quét đệ quy).
│
├── output/                    # [Kho Thành Phẩm] Thư mục chứa các tệp .pdf thành phẩm (Tái tạo cây thư mục con).
│
├── src/                       # [Lõi Động Cơ] Thư mục chứa các module mã nguồn xử lý logic.
│   ├── __init__.py
│   ├── ast_parser.py          # (Giai đoạn 1) Quét AST đa chế độ (gfm-like), bóc tách Nút Toán TeX ($/$$) & Nút Bảng.
│   ├── html_renderer.py       # (Giai đoạn 2) Tô màu Pygments, đúc MathML & bọc khung HTML Bảng GFM.
│   └── pdf_compiler.py        # (Giai đoạn 3) Thảm CSS Paged Media, bóp viền Bảng, bám đường cơ sở & Khóa ngắt trang.
│
├── tests/                     # [Phòng Thử Nghiệm Va Chạm] Khu vực diễn tập phòng chống sự cố vật lý.
│   ├── __init__.py
│   └── red_team_tests.py      # Bộ kiểm thử đối kháng Hộp Trắng (10 Kịch bản bắn phá tải trọng).
│
├── .gitignore                 # Chỉ thị phòng thủ cho Git loại trừ tệp rác, môi trường ảo và tệp PDF nội bộ.
├── main.py                    # [Quản Đốc Băng Chuyền] Điều phối luồng dữ liệu, trích xuất cấu hình YAML & Bẫy lỗi.
├── README.md                  # Cẩm nang vận hành và bản thiết kế kiến trúc toàn diện.
└── requirements.txt           # Bảng kê vật tư thư viện phụ thuộc (Bổ sung linkify-it-py & mdit-py-plugins).
```

### Phân tích Chức năng Chi tiết Từng Thành phần

- **`config/settings.yaml`**: Trái tim cấu hình của dự án. Quản lý 10 phân khu tham số: Chuẩn mã hóa UTF-8, định tuyến thư mục con, theme Pygments, độ sâu dấu trang PDF, hệ thống đánh số CSS Counters, động cơ toán học MathML, bộ xử lý bảng GFM `clip_and_warn` và ma trận in ấn học thuật APA/IEEE.
- **`main.py`**: Quản đốc điều phối toàn bộ đường ống. Nạp tệp YAML, trích xuất cấu hình bảng biểu và quy chuẩn học thuật đóng gói dạng Dictionary để chuyển giao sạch sẽ xuống các module hạ nguồn, tự động khởi tạo hạ tầng thư mục và bẫy lỗi cô lập sự cố.
- **`src/ast_parser.py`**: Đảm nhiệm **Giai đoạn 1**. Sử dụng `markdown-it-py` với cờ `gfm-like` và plugin `texmath` để phân rã văn bản thô thành Cây cú pháp trừu tượng, cô lập chính xác các Nút toán học và Nút cấu trúc bảng.
- **`src/html_renderer.py`**: Đảm nhiệm **Giai đoạn 2**. Tiếp nhận các Nút AST, nhuộm màu mã nguồn qua `Pygments`, tạo mỏ neo tiêu đề ASCII, đúc công thức toán thành mã HTML MathML và kết xuất cấu trúc thẻ Bảng `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`.
- **`src/pdf_compiler.py`**: Đảm nhiệm **Giai đoạn 3**. Kích hoạt `WeasyPrint` biên dịch HTML/CSS Paged Media thành PDF. Nạp lớp giáp CSS phòng thủ: kẻ khung viền đen 1pt cho bảng, nhuộm xám tiêu đề `th`, khóa ngắt trang khối mã nguồn/bảng biểu (`break-inside: avoid;`), và khóa sàn kích thước chữ H5/H6 ở mức 11pt in đậm in nghiêng.
- **`tests/red_team_tests.py`**: Phòng thử nghiệm va chạm vật lý. Thực thi 10 kịch bản va chạm hộp trắng bao phủ toàn bộ các điểm gãy tiềm ẩn (Xung đột UTF-8, tràn viền mã nguồn, tệp hỏng nhị phân, hạ cấp lỗi LaTeX, nhận diện bảng GFM, và quy chuẩn APA).

---

## HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG VÀ HẠ TẦNG C-RUNTIME (ENVIRONMENT SETUP)

Nội dung phần này hướng dẫn chi tiết từng bước chuẩn bị hạ tầng phần mềm, khởi tạo môi trường thực thi cách ly trên VSCode và cài đặt danh mục vật tư phụ thuộc cho dự án.

---

### 1. YÊU CẦU HỆ THỐNG VÀ CÁC THÀNH PHẦN TIỀN ĐỀ (PREREQUISITES)

Để hệ thống chuyển đổi vận hành trơn tru và không gặp sự cố gián đoạn, máy tính cần đáp ứng các thành phần hạ tầng sau:

- **Hệ điều hành:** Microsoft Windows 10 hoặc Windows 11 (Tối ưu nhất trên Windows 11 64-bit).
- **Môi trường thực thi Python:** Python phiên bản 3.10 trở lên.
- **Trình biên tập mã nguồn (IDE):** Visual Studio Code (VSCode).
- **Thư viện đồ họa nền tảng C-Runtime:** GTK3-Runtime cho Windows (Thành phần bắt buộc để động cơ `WeasyPrint` kết xuất file PDF).

#### Ẩn dụ Ngữ nghĩa: "Vô-lăng Điều khiển và Hộp số Đồ họa C-Runtime"

Hãy tưởng tượng **Python** là **Vô-lăng và Cần số** (nơi người dùng ra lệnh logic), còn **GTK3-Runtime** là **Hộp số và Trục bánh xe** vật lý bên dưới gầm xe. Động cơ in ấn `WeasyPrint` sử dụng ngôn ngữ Python để nhận chỉ thị, nhưng khi cần vẽ phông chữ, tính toán khoảng cách lề in A4 hay xuất định dạng trang PDF, nó buộc phải gọi các thư viện đồ họa mã nguồn C của `GTK3-Runtime` (`Cairo`, `Pango`, `Fontconfig`). Nếu thiếu `GTK3-Runtime`, vô-lăng vẫn xoay nhưng xe không thể di chuyển (Python ném ra ngoại lệ `ImportError` hoặc `OSError`).

#### Hướng dẫn cài đặt GTK3-Runtime trên Windows 11

1. Tải bản cài đặt `GTK3-Runtime Win64` từ kho lưu trữ chính thức.
2. Thực thi tệp cài đặt `.exe` và chấp nhận đường dẫn mặc định: `C:\Program Files\GTK3-Runtime Win64\bin`.
3. Mã nguồn dự án trong tệp `src/pdf_compiler.py` đã tích hợp sẵn hàm `_register_gtk_dll_directories()` tự động tìm kiếm và đăng ký đường dẫn DLL này vào hệ thống (`os.add_dll_directory`), giúp bạn không cần phải cấu hình biến môi trường Environment Variables thủ công.

---

### 2. THIẾT LẬP KHÔNG GIAN LÀM VIỆC TRÊN VSCODE (VSCODE WORKFLOW)

Để đảm bảo các thư viện của dự án này không gây xung đột với các ứng dụng Python khác trên máy tính, chúng ta triển khai **Môi trường ảo (Virtual Environment - `venv`)**.

#### Ẩn dụ Ngữ nghĩa: "Hộp Dụng cụ Cách ly Công trình"

Thay vì vứt tất cả đinh, ốc, búa vào một kho chung của cả ngôi nhà (môi trường Python toàn cục của Windows), việc tạo `venv` giống như việc bạn cấp riêng một **Hộp dụng cụ chuyên dụng** cho công trình `markdown_to_pdf_engine`. Mọi vật tư (thư viện) mua về chỉ nằm trong hộp này; khi hoàn thành công trình, bạn có thể cất đi mà không làm bẩn kho chung.

#### Quy trình Thao tác Từng bước trên Giao diện VSCode

##### Bước 1: Mở Thư mục Dự án trong VSCode

1. Khởi động phần mềm **VSCode**.
2. Trên thanh menu chính, chọn **File** -> **Open Folder...** (hoặc nhấn tổ hợp phím `Ctrl + K` rồi `Ctrl + O`).
3. Trỏ đường dẫn đến thư mục `MARKDOWN_TO_PDF_ENGINE` và nhấn **Select Folder**.

##### Bước 2: Mở Cửa sổ Terminal Tích hợp

1. Trên thanh menu của VSCode, chọn **Terminal** -> **New Terminal** (hoặc nhấn tổ hợp phím `Ctrl + ~`).
2. Màn hình Cửa sổ dòng lệnh (PowerShell) sẽ xuất hiện tại cạnh dưới giao diện VSCode với đường dẫn hiện hành là thư mục gốc của dự án.

##### Bước 3: Khởi tạo Môi trường Ảo `venv`

Tại cửa sổ Terminal, gõ lệnh sau và nhấn `Enter`:

```powershell
python -m venv venv

```

Hệ thống sẽ tạo ra một thư mục ẩn tên là `venv/` chứa trình thông dịch Python độc lập.

##### Bước 4: Kích hoạt Môi trường Ảo

Tại cửa sổ Terminal, gõ lệnh sau và nhấn `Enter`:

```powershell
.\venv\Scripts\Activate.ps1

```

- **Dấu hiệu nhận biết thành công:** Đầu dòng lệnh của Terminal sẽ xuất hiện tiền tố `(venv)` màu xanh lá cây.

##### Bước 5: Cài đặt Danh mục Vật tư Phụ thuộc (`requirements.txt`)

Tệp `requirements.txt` trong dự án v1.3.2 khai báo danh sách các thư viện mã nguồn mở bắt buộc bao gồm:

- **`markdown-it-py>=3.0.0`**: Động cơ bóc tách văn bản thô thành Cây cú pháp trừu tượng (AST).
- **`pygments>=2.17.0`**: Động cơ phân tích cú pháp mã nguồn và nhuộm màu từ khóa.
- **`weasyprint>=61.0`**: Động cơ chuyển đổi HTML/CSS Paged Media thành tệp PDF.
- **`pyyaml>=6.0.1`**: Động cơ đọc và phân tích tệp cấu hình `settings.yaml`.
- **`mdit-py-plugins>=0.4.0`**: Plugin mở rộng cho `markdown-it-py` để nhận diện ký hiệu toán học `$`/`$$`.
- **`latex2mathml>=3.77.0`**: Động cơ dịch thuật mã LaTeX sang định dạng HTML MathML ngoại tuyến.
- **`linkify-it-py>=2.0.0`** _(MỚI v1.3.2)_: Thư viện vệ tinh bắt buộc đi kèm khi kích hoạt preset `gfm-like` để hỗ trợ phân tích bảng GFM và tự động nhận diện liên kết web.

Thực thi lệnh cài đặt hàng loạt bằng cách gõ lệnh sau vào Terminal:

```powershell
pip install -r requirements.txt

```

Chờ tiến trình tải xuống và giải nén hoàn tất cho đến khi Terminal hiển thị thông báo `Successfully installed...`.

---

# SỔ TAY CẤU HÌNH TOÀN CỤC VÀ HƯỚNG DẪN VẬN HÀNH (PHIÊN BẢN v1.3.2)

---

## CHƯƠNG 4: SỔ TAY CẤU HÌNH TOÀN CỤC (config/settings.yaml)

Thực hiện đúng triết lý **Phân tách Mối quan tâm (Separation of Concerns - SoC)**, toàn bộ tham số vận hành của hệ thống được tập trung duy nhất tại tệp `config/settings.yaml`. Tệp cấu hình này đóng vai trò là "Bảng Điều Khiển Center Panel" của nhà máy, cho phép tùy chỉnh hành vi biên dịch mà không cần chỉnh sửa mã nguồn Python.

### Mã nguồn Cấu hình Mẫu Chuẩn mực cho config/settings.yaml (v1.3.2)

```yaml
# ==============================================================================
# BẢNG ĐIỀU KHUYỂN VÀ QUY HOẠCH PIPELINE (MARKDOWN TO PDF ENGINE SCHEMA)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.3.2 - Academic & Table Engine)
# Kiến trúc: Separation of Concerns (SoC) - Configuration Layer
# ==============================================================================

# 1. CHUẨN MÃ HÓA TOÀN CỤC (GLOBAL ENCODING STANDARD)
# Cưỡng chế luồng Đọc (Read), Ghi (Write) và Render theo UTF-8
# Triệt tiêu hoàn toàn sự cố trôi dạt mã hóa cp1252 trên Windows 11
global_encoding_standard: "utf-8"

# 2. ĐIỀU HƯỚNG THƯ MỤC VÀ XỬ LÝ HÀNG LOẠT (DIRECTORY ROUTING & BATCH PROCESSING)
# Cấu hình dây chuyền tự động quét và phân loại tài liệu đầu vào/đầu ra
directory_routing:
  # Tên thư mục chứa các tệp Markdown cần chuyển đổi
  input_directory: "input"

  # Tên thư mục chứa các tệp PDF thành phẩm sau biên dịch
  output_directory: "output"

  # Kích hoạt quét đệ quy (Recursive Search) vào tất cả các thư mục con bên trong input/
  recursive_search: true

  # Danh sách các đuôi tệp văn bản được phép nạp vào đường ống xử lý
  allowed_extensions:
    - ".md"
    - ".markdown"
    - ".mdown"

  # Cho phép tự động ghi đè tệp PDF thành phẩm nếu đã tồn tại bên thư mục output/
  overwrite_existing: true

  # Tự động kiểm tra và khởi tạo thư mục input/ và output/ nếu chưa tồn tại
  auto_create_directories: true

  # Bảo tồn nguyên vẹn cấu trúc thư mục con từ input/ sang output/
  # Ví dụ: input/du_an_a/baocao.md -> output/du_an_a/baocao.pdf
  preserve_subfolder_structure: true

# 3. NHUỘM MÀU CÚ PHÁP MÃ NGUỒN (SYNTAX HIGHLIGHTING PROFILE)
# Định danh chủ đề (Theme) Pygments dùng để tô màu từ khóa, biến và hàm trong Code Block
syntax_highlighting_profile: "monokai"

# 4. GIỚI HẠN ĐỘ SÂU DẤU TRANG TIÊU ĐỀ (HEADING RETENTION & ANCHORS)
# Quy định ranh giới phân cấp cấu hình Dấu trang (Bookmarks) và Mỏ neo HTML
heading_retention_depth:
  # Cấp độ tiêu đề tối đa được ánh xạ thành Bookmark trong PDF (Cấp 1 đến Cấp 4)
  max_bookmark_level: 4

  # Kích hoạt tự động gắn thuộc tính id mỏ neo vào các thẻ tiêu đề HTML
  enable_heading_anchors: true

  # Cưỡng chế chuẩn hóa chuỗi id tiêu đề về dạng ASCII không dấu chuẩn SEO/HTML
  normalize_anchor_ascii: true

# 5. THÔNG SỐ TRANG IN VẬT LÝ (DOCUMENT LAYOUT CONFIGURATION)
# Cấu hình kích thước trang in, lề văn bản và cơ chế xử lý khối mã tràn viền
document_layout:
  # Kích thước khổ giấy in tiêu chuẩn
  page_size: "A4"

  # Khoảng cách lề trang in (Top, Right, Bottom, Left)
  margin: "20mm"

  # Quy tắc bẻ dòng tự động cho khối mã nguồn vượt quá độ rộng trang in
  code_overflow_handling: "break-word"

# 6. CẤU HÌNH MỸ THUẬT CHỮ VÀ PHÔNG CHỮ HỆ THỐNG (TYPOGRAPHY CONFIGURATION)
# Bộ phông chữ phòng thủ chống lỗi hiển thị, vỡ font, bóp mỏng chữ Tiếng Việt trên Windows 11
typography_configuration:
  # Chuỗi ưu tiên phông chữ văn bản (Font Stack) hỗ trợ trọn vẹn Tiếng Việt Unicode
  font_family: '"Segoe UI", "Arial", "Calibri", "Tahoma", sans-serif'

  # Phông chữ cố định chiều rộng (Monospace) dành cho khối mã nguồn và code nội dòng
  code_font_family: '"Consolas", "Courier New", monospace'

  # Kích thước chữ cơ sở cho đoạn văn bản
  base_font_size: "11pt"

  # Khoảng cách giữa các dòng văn bản (Tối ưu độ đọc)
  line_height: "1.6"

  # Mã màu văn bản chuẩn (Tránh màu đen tuyệt đối gây mỏi mắt)
  text_color: "#1a1a1a"

# 7. CẤU HÌNH ĐÁNH SỐ TIÊU ĐỀ TỰ ĐỘNG (HEADING NUMBERING CONFIGURATION)
# Điều khiển tính năng tự động đếm và chèn ký tự số vào trước tiêu đề trong bản in PDF
heading_numbering_system:
  # Kích hoạt tính năng tự động đánh số tiêu đề (True: Bật, False: Tắt)
  enable_auto_numbering: true

  # Định dạng đánh số cho tiêu đề Cấp 1 (H1)
  # Giá trị chấp nhận: "roman" (Chữ số La Mã: I, II, III) hoặc "decimal" (Chữ số tự nhiên: 1, 2, 3)
  h1_numbering_style: "roman"

  # Định dạng đánh số cho tiêu đề Cấp con (H2, H3, H4)
  # Giới hạn ở cấp 4 để tránh chuỗi số quá dài (e.g., 1.1.1.1.1) theo chuẩn APA/IEEE
  # Giá trị chấp nhận: "decimal" (Phân cấp tự nhiên: 1.1, 1.2, 1.1.1) hoặc "none" (Không đánh số cấp con)
  sub_heading_numbering_style: "decimal"

  # Ký tự phân cách giữa chỉ số thứ tự và nội dung tiêu đề
  number_separator: ". "

# 8. CẤU HÌNH ĐỘNG CƠ DỊCH THUẬT TOÁN HỌC (MATH RENDERING SYSTEM)
# Điều khiển tính năng nhận diện và chuyển đổi công thức LaTeX sang MathML/SVG
math_rendering_system:
  # Cờ bật/tắt chính cho toàn bộ luồng xử lý toán học (True: Bật, False: Tắt)
  enable_math_rendering: true

  # Chế độ tự động hạ cấp an toàn: Nếu chuỗi LaTeX bị lỗi cú pháp, trả về văn bản gốc thay vì làm sập chương trình
  fallback_to_raw_on_error: true

# 9. CẤU HÌNH ĐỘNG CƠ XỬ LÝ BẢNG BIỂU GFM (TABLE RENDERING SYSTEM - NEW v1.3.2)
# Điều khiển tính năng phân tích cú pháp bảng Markdown và quản lý tràn viền vật lý
table_rendering_system:
  # Kích hoạt bộ phân tích bảng biểu GFM trong AST Parser (True: Bật, False: Tắt)
  enable_gfm_tables: true

  # Chiến lược xử lý khi bảng biểu vượt quá độ rộng vùng in A4
  # Giá trị chấp nhận: "clip_and_warn" (Cắt bỏ phần thừa tràn ngang và xuất cảnh báo ra Terminal)
  overflow_strategy: "clip_and_warn"

  # Tự động lặp lại hàng tiêu đề của bảng (Table Header) khi bảng bị ngắt sang trang mới
  repeat_header_on_page_break: true

  # Ngưỡng độ rộng chiều ngang tối đa của vùng in A4 (tính bằng mm) dùng để kích hoạt cảnh báo
  max_printable_width_mm: 170

# 10. MA TRẬN QUY CHUẨN IN ẤN HỌC THUẬT (ACADEMIC STANDARDS PROFILE - NEW v1.3.2)
# Định hình phong cách trình bày văn bản theo các tiêu chuẩn xuất bản quốc tế
academic_standards_profile:
  # Tiêu chuẩn học thuật đang kích hoạt
  # Giá trị chấp nhận: "none" (Mặc định), "apa" (APA 7th), "ieee" (IEEE), "harvard" (Harvard)
  active_standard: "apa"

  # Bật tính năng chống dòng mồ côi (Orphans) và dòng góa phụ (Widows)
  # Đảm bảo không có dòng văn bản đơn lẻ trơ trọi ở đầu hoặc cuối trang in
  prevent_orphans_and_widows: true

  # Quy tắc ngắt trang cho khối mã nguồn và bảng biểu
  # Giá trị chấp nhận: "avoid" (Ngăn ngắt trang giữa khối), "auto" (Cho phép ngắt tự nhiên)
  code_block_page_break_inside: "avoid"
  table_page_break_inside: "avoid"
```

---

### Phân tích Kỹ thuật Chi tiết Các Tham số Cấu hình Bắt buộc

- **`global_encoding_standard: "utf-8"`**: Đóng vai trò là bức tường phòng thủ nguyên nhân gốc rễ gây ra lỗi mã hóa ký tự. Nó buộc toàn bộ các hàm mở tệp (`open()`) trong Python phải sử dụng chuẩn `utf-8` thay vì bảng mã mặc định `cp1252` của hệ điều hành Windows 11.

- **`directory_routing`**: Quản lý chiến lược định tuyến tài liệu. Tính năng `preserve_subfolder_structure: true` giúp người dùng quản lý tri thức dạng cây folder phức tạp bên trong thư mục `input/` mà khi xuất sang `output/` không bị dồn tất cả tệp PDF ra một thư mục phẳng.

- **`syntax_highlighting_profile: "monokai"`**: Khai báo theme giao diện nhuộm màu khối mã. Người dùng có thể thay đổi tham số này thành `"github-dark"`, `"dracula"`, hoặc `"solarized-light"` tùy theo sở thích thẩm mỹ.

- **`heading_retention_depth`**: Khóa độ sâu của cây Bookmark điều hướng trong tệp PDF. Bằng việc đặt `max_bookmark_level: 4`, hệ thống chỉ đưa các tiêu đề từ H1 đến H4 vào danh sách Dấu trang (Bookmarks Palette), giữ cho thanh điều hướng PDF gọn gàng, tránh bị rác bởi các tiêu đề quá nhỏ như H5 hay H6.

- **`document_layout`**: Thiết lập tham số trang in vật lý. Quy tắc `code_overflow_handling: "break-word"` bảo vệ văn bản không bị cắt ngang giữa từ ngữ, đồng thời tự động bẻ dòng an toàn đối với các chuỗi mã nguồn siêu dài.

- **`typography_configuration`**: Danh sách phông chữ dự phòng (Font Stack). Chuỗi `"Segoe UI", "Arial", "Calibri", "Tahoma"` đảm bảo luôn có ít nhất một phông chữ hệ thống hỗ trợ trọn vẹn bảng mã tiếng Việt Unicode trên bất kỳ máy tính Windows nào, triệt tiêu hoàn toàn nguy cơ biến dạng ký tự hoặc lỗi ô vuông.

- **`heading_numbering_system`**: Điều khiển tính năng nhảy số tự động hoàn toàn bằng cơ chế CSS Counters của WeasyPrint mà không làm thay đổi văn bản Markdown gốc. Tham số `enable_auto_numbering: true` kích hoạt toàn bộ khối lệnh. Tham số `h1_numbering_style: "roman"` sẽ tự động chèn số La Mã (`I, II, III`) trước các thẻ `<h1>`. Tham số `sub_heading_numbering_style: "decimal"` tạo ra các chuỗi số phân cấp tự nhiên (`1.1`, `1.2`) nối tiếp từ tiêu đề cha xuống các thẻ `<h2>`, `<h3>` và `<h4>`.

- **`math_rendering_system`**: Van điều khiển động cơ dịch thuật toán học ngoại tuyến. Tham số `enable_math_rendering: true` ra lệnh cho `ASTParser` nạp plugin `texmath` và `HTMLRenderer` kích hoạt bộ đúc MathML. Tham số `fallback_to_raw_on_error: true` kích hoạt Aptomat ngắt mạch phòng thủ, tự động chuyển hướng công thức lỗi về dạng thẻ văn bản thô để bảo vệ tiến trình biên dịch.

- **`table_rendering_system` (Mới trong v1.3.2)**: Van điều khiển động cơ xử lý bảng GFM. Tham số `enable_gfm_tables: true` cho phép `ASTParser` nạp preset `gfm-like` để cấu trúc hóa dữ liệu bảng. Tham số `overflow_strategy: "clip_and_warn"` kích hoạt cơ chế cắt gọn chiều ngang bảng biểu quá khổ A4 và bắn nhật ký cảnh báo màu vàng lên Terminal. Tham số `repeat_header_on_page_break: true` tự động tái tạo hàng tiêu đề bảng ở đầu trang mới khi bảng bị cắt đôi theo chiều dọc.

- **`academic_standards_profile` (Mới trong v1.3.2)**: Ma trận quy chuẩn in ấn học thuật. Tham số `active_standard: "apa"` kích hoạt phong cách định dạng Times New Roman, dãn dòng chuẩn và viền bảng kẻ ngang. Tham số `prevent_orphans_and_widows: true` áp dụng chỉ thị `orphans: 2; widows: 2;` chống dòng mồ côi ở ranh giới ngắt trang. Các tham số `code_block_page_break_inside: "avoid"` và `table_page_break_inside: "avoid"` tiêm chỉ thị CSS Paged Media ép buộc máy in giữ nguyên khối mã nguồn và bảng biểu không bị xẻ đôi giữa hai trang.

---

## CHƯƠNG 5: SÁCH HƯỚNG DẪN VẬN HÀNH VÀ CƠ CHẾ CHỐNG LỖI (OPERATIONAL MANUAL & FAULT TOLERANCE v1.3.2)

Tài liệu này cung cấp toàn bộ quy trình vận hành đường ống biên dịch tài liệu tự động `markdown_to_pdf_engine`, chi tiết hóa các thao tác thực thi trên giao diện Terminal của VSCode, cùng phân tích kỹ thuật chuyên sâu về cơ chế chống lỗi (Fault-tolerance) và tự bảo tồn cấu trúc dữ liệu của hệ thống.

---

### 1. QUY TRÌNH VẬN HÀNH ĐƯỜNG ỐNG BIÊN DỊCH (OPERATIONAL WORKFLOW)

#### Ẩn dụ Ngữ nghĩa: "Băng chuyền Tự động hóa của Nhà máy In ấn"

Hãy tưởng tượng tệp `main.py` đóng vai trò là **Quản Đốc Băng Chuyền**.

- Bạn nạp nguyên liệu thô (các tệp `.md`) vào **Máng Đón Đầu Vào** (Thư mục `input/`).

- Bạn gạt cầu giao khởi động băng chuyền (Thực thi lệnh `python main.py`).

- Quản Đốc sẽ tự động phân loại tệp, kiểm tra tính hợp lệ, đẩy từng tệp qua các công đoạn chế tác (AST Parser -> HTML Renderer -> PDF Compiler) và đưa sản phẩm đóng gói sắc nét (tệp `.pdf`) vào **Kho Thành Phẩm** (Thư mục `output/`).

Sơ đồ luồng di chuyển dữ liệu phiên bản v1.3.2:

```text
[Thư mục input/] ---> (Quét tệp .md đệ quy) ---> [main.py: Quản đốc Điều phối]
                                                        |
+-------------------------------------------------------+-------------------------------------------------------+
|                                                       |                                                       |
v                                                       v                                                       v
[Giai đoạn 1: AST Parser]                 [Giai đoạn 2: HTML Renderer]                 [Giai đoạn 3: PDF Compiler]
(Cảm biến gfm-like & TeX)                (Nhuộm Pygments, MathML & Bảng)              (CSS Paged Media, APA & Frame)
|                                                       |                                                       |
+-------------------------------------------------------+-------------------------------------------------------+
                                                        |
                                                        v
                                         [Thư mục output/ (File .pdf)]

```

#### Quy trình Thao tác Chi tiết Từng bước trên VSCode

- **Bước 1: Chuẩn bị Văn bản Đầu vào (Input Preparation)**
- Trong cửa sổ **Explorer** bên cánh trái của VSCode, tìm đến thư mục `input/` (Nếu chưa có, hệ thống sẽ tự động khởi tạo ở lần chạy đầu tiên).

- Sao chép hoặc tạo mới các tệp Markdown cần chuyển đổi vào trong thư mục `input/`.

- Các định dạng đuôi tệp được hỗ trợ mặc định: `.md`, `.markdown`, `.mdown` (Có thể tùy chỉnh trong `config/settings.yaml`).

- **Bước 2: Thực thi Tiến trình Biên dịch Hàng loạt (Batch Execution)**
- Mở cửa sổ **Terminal** trong VSCode bằng tổ hợp phím `Ctrl + ~` (Đảm bảo môi trường ảo `(venv)` đang được kích hoạt).

- Gõ câu lệnh thực thi sau và nhấn `Enter`:

```powershell
python main.py

```

- **Bước 3: Đọc Nhật ký Vận hành Terminal (Log Inspection)**
- Khi lệnh được kích hoạt, hệ thống sẽ in ra màn hình nhật ký tiến trình thời gian thực (Real-time Console Logs):

```text
=== BẮT ĐẦU TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT (BATCH PROCESSING v1.3.2) ===
[THÔNG_TIN] Phát hiện 2 tệp Markdown hợp lệ trong danh sách chờ biên dịch.

[1/2] Đang xử lý: input\baocao_hoc_thuat.md
    -> [THÀNH_CÔNG] Xuất bản: output\baocao_hoc_thuat.pdf
[2/2] Đang xử lý: input\du_an_nghien_cuu\chuyen_de_1\bang_du_lieu.md
    -> [THÀNH_CÔNG] Xuất bản: output\du_an_nghien_cuu\chuyen_de_1\bang_du_lieu.pdf

================ TỔNG KẾT TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT ================
- Tổng số tệp phát hiện : 2
- Biên dịch thành công : 2
- Biên dịch thất bại   : 0
- Bỏ qua (Đã tồn tại)  : 0
========================================================================

```

- **Bước 4: Kiểm tra Sản phẩm Đầu ra**
- Truy cập thư mục `output/` trên cây thư mục VSCode.

- Nhấp chuột phải vào tệp `.pdf` vừa xuất bản và chọn **Reveal in File Explorer** để mở và kiểm tra chất lượng hiển thị, khung viền bảng biểu đen 1pt sắc nét, công thức toán học MathML, bản đồ Bookmark và các tiêu đề H5/H6 in đậm in nghiêng 11pt.

---

### 2. PHÂN TÍCH CƠ CHẾ BẢO TỒN VÀ QUẢN LÝ CẤU TRÚC (SELF-PRESERVATION)

Hệ thống được trang bị các tính năng tự bảo tồn không gian lưu trữ và duy trì cấu trúc dữ liệu nguyên vẹn:

- **Tự động Khởi tạo Hạ tầng Thư mục (`auto_create_directories`)**: Nếu người dùng lần đầu tải mã nguồn về và chưa tạo hai thư mục `input/` và `output/`, hàm `ensure_directories_exist()` trong `main.py` sẽ phát hiện sự thiếu hụt này. Hệ thống sẽ tự động kích hoạt lệnh tạo thư mục an toàn (`mkdir(parents=True, exist_ok=True)`) mà không gây ra bất kỳ lỗi dừng chương trình nào.

- **Tái tạo và Bảo tồn Cấu trúc Thư mục Con (`preserve_subfolder_structure`)**: Khi người dùng lưu trữ ghi chú dạng cây phân tầng phức tạp (Ví dụ: `input/du_an_a/chuyen_de_1/bao_cao.md`), nhiều công cụ chuyển đổi thô sẽ dồn tất cả tệp PDF ra một thư mục phẳng `output/bao_cao.pdf`, làm mất hoàn toàn bối cảnh phân loại. Trong `main.py`, hệ thống tính toán đường dẫn tương đối (`relative_to(input_dir)`). Khi tính năng `preserve_subfolder_structure: true` được bật trong `settings.yaml`, hệ thống sẽ tự động dựng lại cây thư mục con tương ứng bên phía `output/` (Ví dụ: `output/du_an_a/chuyen_de_1/bao_cao.pdf`).

- **Kiểm soát Chế độ Ghi đè Tệp Thành phẩm (`overwrite_existing`)**: Khi `overwrite_existing: true`, hệ thống sẽ ghi đè tệp PDF mới lên tệp PDF cũ để luôn cập nhật nội dung mới nhất. Khi `overwrite_existing: false`, hệ thống sẽ kiểm tra `target_output_pdf_path.exists()`. Nếu tệp PDF đã tồn tại, nó sẽ tự động bỏ qua (`skipped_count += 1`) để tiết kiệm tài nguyên tính toán và bảo vệ tài liệu đã biên dịch trước đó.

---

### 3. CƠ CHẾ PHÒNG THỦ VÀ CÔ LẬP NGOẠI LỆ (FAULT ISOLATION v1.3.2)

#### Ẩn dụ Ngữ nghĩa: "Aptomat (Cầu Dao Tự Động) Phân Lưới Công Nghiệp"

Trong một tòa nhà công nghiệp, nếu bóng đèn ở phòng khách bị chập điện, cầu dao riêng của phòng khách sẽ ngắt. Điện ở phòng bếp và phòng ngủ vẫn sáng bình thường.
Trong `markdown_to_pdf_engine`, nếu bạn đưa vào 10 tệp Markdown nhưng có 1 tệp bị hỏng (chứa mã nhị phân rác, sai mã hóa, công thức toán hỏng hoặc bảng biểu vượt kích thước), **Cầu Dao Cô Lập** sẽ lập tức bẫy lỗi, đánh dấu tệp đó thất bại, và tiếp tục biên dịch 9 tệp còn lại một cách bình thường.

Sơ đồ cách ly sự cố:

```text
[Bắt đầu Batch] ---> Tệp 1 (.md) -----> Biên dịch -----> [THÀNH CÔNG] (Xuất PDF 1)
                ---> Tệp 2 (Hỏng) ----> Bẫy Ngoại Lệ -> [THẤT BẠI] (Bỏ qua & Báo lỗi Log)
                ---> Tệp 3 (Bảng cực rộng) -> Cắt lề & Warn -> [THÀNH CÔNG] (Xuất PDF 3)

```

#### Phân tích Chi tiết 5 Tầng Bẫy Lỗi Trong Mã Nguồn

- **Tầng 1: Cô lập Lỗi Đơn tệp (Single File Exception Containment)**: Trong tệp `main.py`, toàn bộ tiến trình biên dịch từng tệp được bọc trong hàm `execute_single_file_pipeline()` với khối `try...except` phòng thủ diện rộng chỉ định đích danh các ngoại lệ I/O, mã hóa và runtime (`FileNotFoundError`, `UnicodeDecodeError`, `ValueError`, `TypeError`, `OSError`, `RuntimeError`). Khi phát hiện tệp lỗi, nó ghi nhận vào nhật ký Terminal và trả về `False`, giúp vòng lặp `for` trong `batch_process_directory()` chuyển sang tệp kế tiếp mà không làm sập tiến trình chung.

- **Tầng 2: Phòng thủ Sự cố Trôi dạt Mã hóa Unicode (`UnicodeDecodeError`)**: Hệ điều hành Windows 11 mặc định mở tệp bằng bảng mã `cp1252`. Nếu gặp ký tự tiếng Việt Unicode hoặc ký tự đặc biệt, chương trình Python thông thường sẽ bị ngắt đột ngột. Trong `src/ast_parser.py` và `main.py`, mọi thao tác mở tệp `open()` đều bắt buộc phải truyền tham số `encoding="utf-8"`. Đồng thời, `ASTParser` bắt riêng `UnicodeDecodeError` và đóng gói lại thành thông điệp lỗi rõ ràng cho người dùng.

- **Tầng 3: Xử lý An toàn Thư mục Rỗng (Empty Input Directory Handling)**: Khi thư mục `input/` không chứa tệp `.md` nào, hệ thống không ném ra lỗi ngắt tiến trình. `main.py` kiểm tra `if not target_files:`, in ra thông báo hướng dẫn người dùng chép tệp vào thư mục và kết thúc tiến trình một cách êm đẹp (Exit Code 0).

- **Tầng 4: Triệt tiêu Cảnh báo Nhiễu C-Runtime của GTK3 trên Windows**: Khi `WeasyPrint` gọi thư viện C gốc `GLib/GIO` trên Windows 11, hệ thống thường đẩy các cảnh báo nhiễu dạng `GLib-GIO-WARNING` ra luồng xuất lỗi Terminal (`stderr`). Trong `src/pdf_compiler.py`, hệ thống tự động đăng ký đường dẫn DLL của GTK3 (`_register_gtk_dll_directories`) và thiết lập bộ cô lập `_suppress_c_stderr()` dập tắt log nhiễu trước khi nạp thư viện `WeasyPrint`, giữ cho nhật ký Terminal của người dùng luôn sạch sẽ.

- **Tầng 5: Hạ cấp An toàn Toán học & Cắt Viền Bảng Tràn Lề (Math Fallback & Table Overflow Engine - NEW v1.3.2)**:
- _Xử lý Toán học:_ Trong `src/html_renderer.py`, hai hàm `_render_math_inline` và `_render_math_block` được bọc chặt trong khối `try...except Exception`. Khi cờ `fallback_to_raw_on_error: true` bật, nó sẽ in log cảnh báo `[CẢNH_BÁO_MATH]` ra Terminal và tự động hạ cấp công thức LaTeX lỗi về dạng thẻ HTML văn bản thô `<span class="math-error">` để tài liệu PDF vẫn được xuất bản an toàn.

- _Xử lý Bảng biểu:_ Khi gặp bảng GFM cực rộng chứa hàng chục cột, hệ thống áp dụng cơ chế `overflow_strategy: "clip_and_warn"`. Lớp CSS Paged Media sẽ xén gọn phần tràn ngang lề A4, bảo vệ tài liệu không bị vỡ lề in, đồng thời bắn thông báo màu vàng cảnh báo người dùng trên Terminal mà không ngắt mạch biên dịch.

---

# BỘ KIỂM THỬ ĐỐI KHÁNG, QUẢN LÝ MÃ NGUỒN VÀ LỊCH SỬ PHIÊN BẢN (PHIÊN BẢN v1.3.2)

---

## CHƯƠNG 6: BỘ KIỂM THỬ HỘP TRẮNG ĐỐI KHÁNG (WHITE-BOX RED-TEAM TEST SUITE v1.3.2)

### 1. Triết lý Thiết kế Phòng thử nghiệm Va chạm

- **Ẩn dụ đời thực:** Trong ngành công nghiệp chế tạo ô tô, trước khi một mẫu xe mới được cấp phép xuất xưởng, nhà sản xuất phải đưa nó vào **Phòng Thử Nghiệm Va Chạm Vật Lý (Crash Test Facility)**. Họ cố tình cho xe lao vào tường bê tông ở tốc độ cao, thử nghiệm túi khí, ngâm xe dưới nước và vận hành trong điều kiện băng tuyết. Tệp `tests/red_team_tests.py` đóng vai trò là Phòng Thử Nghiệm Va Chạm của hệ thống. Nó cố tình tạo ra dữ liệu độc hại, tệp hỏng nhị phân, công thức LaTeX sai cú pháp và các bảng biểu siêu rộng nhằm mục đích đâm sập hệ thống, qua đó chứng minh rằng các cơ chế bẫy lỗi đã vận hành hoàn hảo.
- **Áp dụng vào v1.3.2:** Bên cạnh 7 kịch bản kiểm thử nền tảng, phiên bản v1.3.2 bổ sung 3 kịch bản va chạm mới (Kịch bản 8, 9, 10) chuyên biệt để kiểm thử động cơ phân tích Bảng GFM, cơ chế cắt lề bảng cực đại và quy chuẩn in ấn học thuật APA.

---

### 2. Phân tích Chi tiết 10 Kịch bản Kiểm thử Đối kháng (`tests/red_team_tests.py`)

- **Kịch bản 1: Rào chắn Xung đột Ký tự Đa ngôn ngữ (`test_scenario_1_bilingual_encoding_stress_test`)**
  - _Mục tiêu đối kháng:_ Tiêm khối dữ liệu chứa văn bản Tiếng Việt có dấu lồng ghép trực tiếp với các biểu thức logic (`a < b && c > d`) và chuỗi Regex.
  - _Phương pháp kiểm tra:_ Ép `ASTParser` nạp tệp và kiểm tra `HTMLRenderer` có giữ nguyên văn bản Tiếng Việt mà không biến dạng ký tự hay ném ra ngoại lệ `UnicodeDecodeError`.
  - _Kết quả kỳ vọng:_ Bộ phân tích AST giữ nguyên hình thái văn bản Tiếng Việt và render thành công các thẻ HTML trung gian.

- **Kịch bản 2: Bẫy Đánh lừa Cấu trúc Phân cấp (`test_scenario_2_heading_spoofing_simulation`)**
  - _Mục tiêu đối kháng:_ Cố tình đưa chuỗi định dạng tiêu đề giả mạo (ví dụ `## Tiêu đề Giả mạo`) nằm chìm bên trong một khối mã nguồn Python.
  - _Phương pháp kiểm tra:_ Quét mã HTML trung gian để xác nhận tiêu đề thật được chuyển thành `<h1 id="..." data-level="1">`, còn tiêu đề giả mạo nằm trong khối mã không bao giờ được tạo thẻ `<h2>`.
  - _Kết quả kỳ vọng:_ Động cơ `markdown-it-py` cô lập hoàn toàn khối mã nguồn `fence`, triệt tiêu nguy cơ rác bản đồ Dấu trang (Bookmarks) trong PDF.

- **Kịch bản 3: Thử nghiệm Tràn Viền Vật lý Khối Mã (`test_scenario_3_physical_overflow_destructive_test`)**
  - _Mục tiêu đối kháng:_ Ép hệ thống xử lý một chuỗi mã nguồn liên tục gồm 1.500 ký tự `X` không có khoảng trắng, vượt gấp nhiều lần độ rộng trang A4.
  - _Phương pháp kiểm tra:_ Đẩy dữ liệu qua `PDFCompiler` để kiểm tra khả năng biên dịch vật lý.
  - _Kết quả kỳ vọng:_ Lớp CSS Paged Media với thuộc tính `overflow-wrap: break-word` phản ứng thành công, tự động bẻ gãy chuỗi xuống dòng mà không làm sập tiến trình in.

- **Kịch bản 4: Xử lý Thư mục Đầu vào Rỗng (`test_scenario_4_empty_directory_handling`)**
  - _Mục tiêu đối kháng:_ Kích hoạt tiến trình quét hàng loạt `batch_process_directory()` khi thư mục `input/` không chứa bất kỳ tệp Markdown nào.
  - _Phương pháp kiểm tra:_ Bẫy toàn bộ các ngoại lệ `FileNotFoundError`, `ValueError`, `TypeError`, `OSError`, `RuntimeError`.
  - _Kết quả kỳ vọng:_ Chương trình hiển thị thông báo hướng dẫn và kết thúc an toàn mà không ném ra ngoại lệ dừng đột ngột.

- **Kịch bản 5: Cô lập Tệp Hỏng Nhị phân (`test_scenario_5_batch_fault_isolation`)**
  - _Mục tiêu đối kháng:_ Tạo một thư mục thử nghiệm chứa 3 tệp: Tệp A (Hợp lệ), Tệp B (Tệp hỏng chứa chuỗi byte nhị phân không hợp lệ `\x80\x81\xfe\xff\xff`), và Tệp C (Hợp lệ).
  - _Phương pháp kiểm tra:_ Chạy kịch bản qua `execute_single_file_pipeline()`.
  - _Kết quả kỳ vọng:_ Tệp A và C trả về `True` và xuất hiện trong `output/`. Tệp B bị bẫy lỗi, trả về `False`, không sinh ra PDF nhưng không làm ngắt tiến trình biên dịch của A và C.

- **Kịch bản 6: Tái tạo Cấu trúc Thư mục Con (`test_scenario_6_subfolder_structure_preservation`)**
  - _Mục tiêu đối kháng:_ Tạo cấu trúc thư mục phân tầng nhiều cấp: `input/du_an_nghien_cuu/chuyen_de_1/bao_cao.md`.
  - _Phương pháp kiểm tra:_ Thực thi tiến trình quét hàng loạt `batch_process_directory()`.
  - _Kết quả kỳ vọng:_ Hệ thống tự động tái tạo đúng cây thư mục con tương ứng bên phía `output/` và xuất bản tệp tại: `output/du_an_nghien_cuu/chuyen_de_1/bao_cao.pdf`.

- **Kịch bản 7: Biên dịch MathML và Cơ chế Hạ cấp Lỗi LaTeX (`test_scenario_7_math_rendering_and_fault_tolerance`)**
  - _Mục tiêu đối kháng:_ Nạp đồng thời tệp Markdown chứa công thức toán hợp lệ (`$2^{30}$`, `$$\frac{a}{b}$$`) và công thức LaTeX bị lỗi cú pháp nghiêm trọng (`$\invalidlatex_command{{{$`).
  - _Phương pháp kiểm tra:_ Kiểm tra mã HTML trung gian xem công thức chuẩn có chứa các thẻ `<math>` hay không, và công thức lỗi có được chuyển hướng an toàn về thẻ `<span class="math-error">` hay không.
  - _Kết quả kỳ vọng:_ Công thức chuẩn đúc thành công mã MathML sắc nét, công thức lỗi bị cô lập tại chỗ mà không gây ngắt chương trình.

- **Kịch bản 8: Cấu trúc hóa Bảng GFM (`test_scenario_8_gfm_table_parsing_and_structure` - MỚI v1.3.2)**
  - _Mục tiêu đối kháng:_ Nạp chuỗi Markdown chứa cấu trúc Bảng GFM chuẩn bao gồm hàng tiêu đề, đường phân cách `| :--- |` và các hàng dữ liệu.
  - _Phương pháp kiểm tra:_ Kiểm tra xem `ASTParser` có sinh ra các Token `table_open`, `thead_open`, `tr_open` hay không, và `HTMLRenderer` có kết xuất chính xác thẻ `<table>` kèm thuộc tính căn lề `style="text-align:left"` hay không.
  - _Kết quả kỳ vọng:_ Chuyển đổi thành công văn bản bảng thô thành ma trận thẻ HTML `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>` chuẩn mực.

- **Kịch bản 9: Cắt Lề và Báo Cảnh báo Bảng Quá Khổ (`test_scenario_9_table_overflow_clipping_and_logging` - MỚI v1.3.2)**
  - _Mục tiêu đối kháng:_ Tiêm một bảng Markdown cực đại chứa 25 cột dữ liệu có tổng độ rộng vượt xa hạn mức in A4 (170mm).
  - _Phương pháp kiểm tra:_ Đẩy dữ liệu qua `PDFCompiler` để xác minh chiến lược `clip_and_warn`.
  - _Kết quả kỳ vọng:_ Biên dịch thành công ra tệp PDF mà không bị vỡ lề in hay ngắt chương trình, bảo đảm tính toàn vẹn của trang giấy.

- **Kịch bản 10: Quy chuẩn APA và Chống Phân mảnh Trang (`test_scenario_10_academic_apa_profile_and_break_avoidance` - MỚI v1.3.2)**
  - _Mục tiêu đối kháng:_ Kích hoạt cờ `active_standard: "apa"` và biên dịch tài liệu chứa văn bản, khối mã nguồn và bảng biểu lồng nhau.
  - _Phương pháp kiểm tra:_ Xác minh luồng Paged Media CSS chứa chỉ thị `orphans: 2; widows: 2;` và `break-inside: avoid;` cho các khối mã và bảng.
  - _Kết quả kỳ vọng:_ Xuất bản tệp PDF tuân thủ quy chuẩn in ấn học thuật, không có dòng mồ côi và khối mã không bị xẻ đôi giữa hai trang.

---

### 3. Quy trình Thực thi Kiểm thử Trực tiếp trên VSCode Terminal

- **Bước 1:** Mở cửa sổ Terminal trong VSCode bằng tổ hợp phím `Ctrl + ~` (Đảm bảo môi trường ảo `(venv)` đang được kích hoạt).
- **Bước 2:** Thực thi lệnh chạy toàn bộ suite kiểm thử Red-Team v1.3.2 bằng module `unittest` của Python:

  ```powershell
  python -m unittest tests/red_team_tests.py
  ```

- **Bước 3:** Đọc kết quả kiểm thử trên màn hình Terminal. Nếu tất cả 10 kịch bản đều vượt qua, Terminal sẽ hiển thị:

```text
..........
----------------------------------------------------------------------
Ran 10 tests in 2.854s

OK

```

Mỗi dấu chấm `.` đại diện cho 1 bài test chạy thành công. Chuỗi `OK` khẳng định hệ thống v1.3.2 đạt độ bền vững 100%.

---

## CHƯƠNG 7: QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB (VERSION CONTROL v1.3.2)

Để lưu trữ dự án an toàn trên kho chứa GitHub mà không vô tình đẩy các tệp rác, tệp môi trường ảo dung lượng lớn, hoặc tài liệu cá nhân nhạy cảm lên mạng, chúng ta thiết lập tệp loại trừ `.gitignore` chuẩn phòng thủ.

### 1. Mã nguồn Tệp `.gitignore` Mẫu Chuẩn Phòng thủ cho Dự án (v1.3.2)

```gitignore
# ==============================================================================
# TỆP LOẠI TRỪ GIT (GITIGNORE SCHEMA)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.3.2)
# ==============================================================================

# 1. BỘ NHỚ ĐỆM VÀ TỆP TRÌNH THÔNG DỊCH PYTHON (PYTHON CACHE)
__pycache__/
*.py[cod]
*$py.class
.Python

# 2. MÔI TRƯỜNG ẢO (VIRTUAL ENVIRONMENTS)
# Bỏ qua thư mục venv/ chứa hàng ngàn tệp thư viện nặng
venv/
.venv/
env/
ENV/

# 3. DỮ LIỆU ĐẦU VÀO VÀ THÀNH PHẨM PDF (LOCAL I/O DATA)
# Bỏ qua các tệp PDF thành phẩm và dữ liệu thử nghiệm cá nhân
output/*.pdf
temp_redteam_workspace/

# 4. TỆP CẤU HÌNH VÀ BỘ NHỚ TẠM CỦA TRÌNH BIÊN TẬP (IDE & OS GARBAGE)
.vscode/*
!.vscode/settings.json
.idea/
*.swp
*.tmp

# Tệp rác tự động của hệ điều hành Windows
Thumbs.db
Desktop.ini

# 5. TỆP TRUNG GIAN DỤNG CỤ BIÊN DỊCH (RENDER & AST INTERMEDIATE ARTIFACTS)
*.html
*.css.tmp
temp/
build/
dist/

# 6. NHẬT KÝ VẬN HÀNH VÀ BÁO CÁO KIỂM THỬ (RED-TEAM LOGS & STRESS TEST)
*.log
logs/
redteam_reports/
*.stacktrace

# 7. CẤU HÌNH LOCAL VÀ DỮ LIỆU THỬ NGHIỆM CÁ NHÂN (LOCAL CONFIG & TEST INPUTS)
.env
config.local.yaml
input/*
!input/input_sample.md
!input/.gitkeep

```

---

### 2. Quy trình Đồng bộ Mã nguồn lên GitHub Từng bước trên VSCode

- **Bước 1: Khởi tạo Kho lưu trữ Git Cục bộ (Local Repository)**
- Tại cửa sổ Terminal của VSCode, gõ lệnh:

```powershell
git init

```

- **Bước 2: Thêm Tất cả Tệp vào Hàng chờ Lưu trữ (Staging Area)**
- Gõ câu lệnh:

```powershell
git add .

```

- Tệp `.gitignore` sẽ tự động lọc bỏ thư mục `venv/`, `__pycache__/` và các tệp `.pdf` thành phẩm.

- **Bước 3: Tạo Điểm Lưu trữ Phiên bản (Commit)**
- Gõ câu lệnh:

```powershell
git commit -m "docs & feat: Nâng cấp dự án lên v1.3.2 - Tích hợp Bảng GFM, Chuẩn APA và Typography H1-H6 Bold/Italic"

```

- **Bước 4: Liên kết và Đẩy Mã nguồn lên GitHub (Remote Repository)**
- Truy cập trang web GitHub, tạo một Repository mới đặt tên là `markdown_to_pdf_engine`.
- Sao chép đường dẫn URL của Repository và dán chuỗi lệnh sau vào Terminal:

```powershell
git branch -M main
git remote add origin [https://github.com/user/markdown_to_pdf_engine.git](https://github.com/user/markdown_to_pdf_engine.git)
git push -u origin main

```

---

## CHƯƠNG 8: LỊCH SỬ PHIÊN BẢN (CHANGELOG & VERSION HISTORY)

### 1. Phiên bản 1.3.2 (Bản Nâng Cấp Hiện Tại - Academic & Table Engine)

- **Tính năng mới (Feat):**
- Tích hợp Động cơ Xử lý Bảng biểu GFM (GitHub Flavored Markdown). Nhận diện chính xác cấu trúc hàng/cột qua preset `gfm-like` kết hợp thư viện phụ trợ `linkify-it-py`.

- Cài đặt chiến lược xử lý tràn lề `clip_and_warn` đối với các bảng quá khổ A4 (vượt quá 170mm).

- Bổ sung ma trận quy chuẩn in ấn học thuật quốc tế (APA 7th, IEEE, Harvard).

- **Mỹ thuật Typography (Style):**
- **Định dạng Khung Bảng:** Bổ sung lưới viền đen 1pt (`border: 1pt solid #1a1a1a;`), hợp nhất viền ô (`border-collapse: collapse;`), tạo khoảng đệm ô 8px/12px và nhuộm màu xám nhạt (`#f2f2f2`) cho hàng tiêu đề `th`.

- **Chống Cắt Phân Mảnh Khối Mã & Bảng:** Tiêm chỉ thị CSS Paged Media `break-inside: avoid;` và `page-break-inside: avoid;` cho khối mã `.highlight`, `<pre>` và `table`, loại bỏ triệt để hiện tượng khối mã hoặc bảng bị xẻ đôi ngang trang.

- **Typography Tiêu đề H1-H6:** Cưỡng chế thuộc tính In đậm (`font-weight: bold !important;`) toàn bộ tiêu đề từ H1 đến H6. Khóa sàn kích thước phông chữ cho Heading 5 và 6 ở mức **11pt** (bằng văn bản nội dung, xóa bỏ sự cố H5/H6 bị bóp nhỏ) kết hợp định dạng In nghiêng (`font-style: italic;`) theo chuẩn APA 7th.

- **Bẫy lỗi An toàn (Fault-Tolerance):** Tích hợp kiểm soát dòng mồ côi (`orphans: 2; widows: 2;`) ở ranh giới trang in.

- **Kiểm thử (Test):** Nâng cấp bộ kiểm thử Red-Team lên 10 kịch bản va chạm vật lý (bổ sung test bóc tách bảng GFM, test cắt lề bảng cực rộng và test chỉ thị APA CSS). Đạt tỷ lệ vượt qua 100% (`Ran 10 tests - OK`).

- **Cấu hình (Config):** Bổ sung phân khu 9 (`table_rendering_system`) và phân khu 10 (`academic_standards_profile`) vào `config/settings.yaml`.

### 2. Phiên bản 1.2.0

- **Tính năng mới (Feat):** Tích hợp Động cơ Biên dịch Toán học Ngoại tuyến (MathML Engine). Nhận diện các ký hiệu toán học `$`/`$$` qua plugin `texmath` và dịch trực tiếp sang định dạng HTML MathML bằng thư viện `latex2mathml`.

- **Mỹ thuật Typography (Style):** Trang bị lớp giáp CSS Paged Media phòng thủ trong `src/pdf_compiler.py`. Ép buộc phông chữ `Cambria Math`, tự động cân chỉnh chỉ số mũ (`msup`), chỉ số dưới (`msub`) và cưỡng chế bám dính đường cơ sở văn bản (`vertical-align: baseline`) để triệt tiêu hoàn toàn sự cố sụp lún chữ.

- **Bẫy lỗi An toàn (Fault-Tolerance):** Tích hợp cờ `fallback_to_raw_on_error`. Khi công thức LaTeX bị lỗi cú pháp, hệ thống tự động ngắt mạch và hạ cấp về dạng thẻ văn bản thô `<span class="math-error">` mà không làm dừng tiến trình biên dịch tệp PDF.

- **Kiểm thử (Test):** Bổ sung Kịch bản 7 (`test_scenario_7_math_rendering_and_fault_tolerance`) vào bộ kiểm thử Red-Team. Đạt tỷ lệ vượt qua 100% cho toàn bộ 7 kịch bản.

- **Cấu hình (Config):** Khai báo khối `math_rendering_system` trong `config/settings.yaml` cho phép người dùng chủ động đóng/mở van xử lý toán học.

### 3. Phiên bản 1.1.0

- **Tính năng mới (Feat):** Tích hợp hệ thống đóng dấu số tiêu đề tự động bằng động cơ CSS Counters. Hỗ trợ xuất số La Mã (`I, II, III`) cho thẻ H1 và số tự nhiên phân cấp đa tầng (`1.1`, `1.2.1`) cho thẻ H2 đến H4.
- **Cấu hình (Config):** Bổ sung mục `heading_numbering_system` vào `config/settings.yaml`.
- **Kiến trúc (Arch):** Mở rộng Trạm trung chuyển `main.py` để trích xuất cấu hình đánh số và truyền xuống `PDFCompiler`.

### 4. Phiên bản 1.0.0 (Bản Khởi Tạo)

- **Kiến trúc Lõi:** Hoàn thiện pipeline 3 giai đoạn ngoại tuyến (Offline-first): `ASTParser` (`markdown-it-py`) -> `HTMLRenderer` (`Pygments`) -> `PDFCompiler` (`WeasyPrint`).
- **Bảo mật & Chống lỗi:** Thiết lập 4 tầng Aptomat phân lưới: Cô lập luồng C-Runtime Stderr, cưỡng chế mã hóa UTF-8 toàn cục, xử lý an toàn thư mục rỗng và cô lập tệp hỏng nhị phân.
- **Cấu hình Tách biệt:** Điều khiển toàn bộ hệ thống thông qua tệp YAML chuẩn Separation of Concerns (`config/settings.yaml`).

---
