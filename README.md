# 🖨️ MARKDOWN TO PDF ENGINE (Lõi Biên dịch Tài liệu Cục bộ)

**Một hệ thống đường ống dữ liệu (Data Pipeline) hoàn toàn tự động, chuyên trách việc chuyển đổi hàng loạt tệp Markdown sang định dạng PDF sắc nét ngay trên môi trường Windows 11 cục bộ.**

Dự án này được thiết kế dựa trên tư duy phân tích hệ thống nghiêm ngặt, từ chối sự phụ thuộc vào các công nghệ đám mây (Cloud), máy chủ web hay cơ sở dữ liệu phức tạp. Mọi tiến trình đều diễn ra ngoại tuyến (Offline-first), đảm bảo tính bảo mật dữ liệu tuyệt đối và khả năng tùy biến cao thông qua hệ thống tệp cấu hình tách biệt.

---

## 🏛️ TRIẾT LÝ KIẾN TRÚC VÀ CƠ CHẾ PHÒNG THỦ (ARCHITECTURAL PHILOSOPHY)

Để hiểu rõ cách hệ thống này vận hành, hãy hình dung dự án giống như một **Nhà máy In ấn Công nghiệp Khép kín**. Thay vì cho phép mọi công nhân tùy ý can thiệp vào dây chuyền, nhà máy này vận hành dựa trên 3 nguyên tắc bất biến nhằm loại trừ mọi rủi ro hỏng hóc:

### 1. Phân tách Mối quan tâm (Separation of Concerns - SoC)
* **Ẩn dụ đời thực:** Trong một nhà hàng, Bếp Trưởng (Mã logic Python) không bao giờ tự mình quyết định giá tiền hay tên món ăn; họ nấu ăn dựa trên một cuốn Thực Đơn (Tệp cấu hình) do Quản lý quy định. Nếu muốn đổi món, bạn đổi Thực Đơn, không phải thay Bếp Trưởng.
* **Áp dụng vào hệ thống:** Chúng ta tách rời hoàn toàn tham số điều khiển khỏi mã nguồn cốt lõi. Mọi tiến trình biên dịch đều phải nạp cấu hình từ một đối tượng YAML chuyên biệt (`settings.yaml`) để đảm bảo tính tái sử dụng. Toàn bộ các thông số như lề giấy, chuẩn mã hóa, màu sắc từ khóa mã nguồn, hay giới hạn độ sâu của dấu trang (Bookmarks) đều được khai báo tại đây. Điều này cho phép người dùng điều khiển toàn bộ nhà máy mà không cần chạm vào một dòng mã Python nào.

### 2. Chống Trôi dạt Mã hóa Luồng I/O (I/O Encoding Drift Defense)
* **Ẩn dụ đời thực:** Tưởng tượng nhà máy của bạn nhận nguyên liệu từ nhiều quốc gia nhưng băng chuyền mặc định chỉ hiểu được tiếng Anh. Khi một kiện hàng ghi nhãn tiếng Việt đi qua, hệ thống đọc sai và nghiền nát kiện hàng đó.
* **Áp dụng vào hệ thống:** Môi trường Windows 11 vận hành mặc định với bảng mã `cp1252`. Khi tiếp nhận các văn bản đa ngôn ngữ chứa ký tự tiếng Việt, hệ thống sẽ ném ra ngoại lệ `UnicodeDecodeError` hoặc phá vỡ hoàn toàn các ký tự có dấu nếu luồng nạp dữ liệu không bị cưỡng chế chuẩn. Để phòng thủ, hệ thống xác lập hằng số `utf-8` làm kim chỉ nam cho mọi giao thức Đọc (Read), Ghi (Write) và Kết xuất (Render). Thuộc tính này được khóa chặt từ tệp cấu hình YAML truyền xuống toàn bộ các module xử lý.

### 3. Cây Cú pháp Trừu tượng (AST) thay vì Chuỗi Tuần tự (Regex)
* **Ẩn dụ đời thực:** Dùng Regex (Biểu thức chính quy) để tìm và sửa định dạng văn bản giống như việc nhắm mắt dùng kéo cắt một bản vẽ kiến trúc dựa trên việc đếm số nét vẽ; nó rất dễ cắt nhầm vào dầm cột (lỗ hổng thoát ký tự). Dùng AST giống như việc quét tia laser 3D toàn bộ tòa nhà, nhận diện rõ đâu là "Cửa sổ", đâu là "Tường", sau đó mới tiến hành sơn màu.
* **Áp dụng vào hệ thống:** Hệ thống từ chối phương pháp thay thế chuỗi tuần tự (Regex) thiếu an toàn. Bắt buộc áp dụng cơ chế Cây cú pháp trừu tượng (Abstract Syntax Tree - AST) thông qua thư viện `markdown-it-py` để bảo chứng tính toàn vẹn của dữ liệu hỗn hợp. Tiến trình này bóc tách tài liệu thành các Nút (Node) độc lập. Việc trộn lẫn văn bản thường và các đoạn mã nguồn (Code snippets) tạo ra rủi ro nghiêm trọng (ví dụ: các toán tử logic `<` hay `>` bị đọc nhầm thành thẻ HTML), nhưng nhờ AST, các Nút mã nguồn (`fence`) được cô lập hoàn toàn, không cho phép rò rỉ định dạng ra ngoài.

---

## 📂 BẢN ĐỒ CẤU TRÚC THƯ MỤC (DIRECTORY BLUEPRINT)

Dưới đây là sơ đồ không gian làm việc (Workspace) tiêu chuẩn trên VSCode. Mỗi thành phần đều có một vùng trách nhiệm duy nhất (Single Responsibility).

```text
MARKDOWN_TO_PDF_ENGINE/
│
├── config/
│   └── settings.yaml          # [Bảng Điều Khiển] Khai báo toàn bộ tham số vận hành.
│
├── input/                     # [Kho Nguyên Liệu] Thư mục chứa các tệp .md cần biên dịch.
│
├── output/                    # [Kho Thành Phẩm] Thư mục chứa các tệp .pdf sau biên dịch.
│
├── src/                       # [Lõi Động Cơ] Thư mục chứa mã nguồn xử lý logic.
│   ├── __init__.py
│   ├── ast_parser.py          # (Giai đoạn 1) Quét và phân rã văn bản thành Cây cú pháp.
│   ├── html_renderer.py       # (Giai đoạn 2) Nhuộm màu mã nguồn và kết xuất thẻ HTML.
│   └── pdf_compiler.py        # (Giai đoạn 3) Áp dụng Typography và đóng gói thành PDF.
│
├── tests/                     # [Sân Tập Trận] Khu vực diễn tập phòng chống lỗi.
│   ├── __init__.py
│   └── red_team_tests.py      # Kịch bản kiểm thử hộp trắng (White-Box Testing).
│
├── .gitignore                 # Chỉ thị cho Git bỏ qua các tệp rác hoặc tệp nhạy cảm.
├── main.py                    # [Trưởng Ban Điều Phối] Kịch bản khởi chạy băng chuyền chính.
├── README.md                  # Bản thiết kế và cẩm nang vận hành (Tệp bạn đang đọc).
└── requirements.txt           # Danh sách các thư viện vật tư bên ngoài cần thiết lập.

```

### Phân tích Chi tiết Từng Thành phần:

* **`config/settings.yaml`**: Trái tim cấu hình của dự án. Tệp này kiểm soát mọi thứ từ chuẩn mã hóa đa ngôn ngữ, định tuyến thư mục (`input`/`output`), giới hạn độ sâu cấp độ tiêu đề tối đa được ánh xạ thành Bookmark trong PDF (Cấp 1 đến Cấp 4), cho đến các thông số trang in vật lý (A4, lề 20mm) và bộ phông chữ phòng thủ chống lỗi hiển thị.


* **`main.py`**: Đóng vai trò là động cơ điều phối quét hàng loạt và phân loại tài liệu tự động. Nó nạp tệp cấu hình, tự động kiểm tra và khởi tạo các thư mục đầu vào/đầu ra, lọc các tệp hợp lệ (đuôi `.md`, `.markdown`) và đẩy chúng qua băng tải chuyển đổi.


* **`src/ast_parser.py`**: Module đảm nhiệm **Giai đoạn 1**. Sử dụng `markdown-it-py` để đọc tệp Markdown với chuẩn mã hóa được cưỡng chế, bóc tách tài liệu và xây dựng nên Cây cú pháp trừu tượng, đồng thời trực tiếp bắt các ngoại lệ `UnicodeDecodeError` nếu có luồng dữ liệu độc hại xâm nhập.


* **`src/html_renderer.py`**: Module đảm nhiệm **Giai đoạn 2**. Tiếp nhận các Nút (Nodes) từ AST để bơm giao diện mã nguồn thông qua động cơ `Pygments` (tô màu cú pháp). Đặc biệt, module này can thiệp vào các thẻ tiêu đề (Heading), tự động chuyển đổi chuỗi văn bản tiếng Việt có dấu thành dạng Slug ASCII chuẩn hóa để tạo các điểm neo dữ liệu (Data Anchor) bằng thuộc tính `id`.


* **`src/pdf_compiler.py`**: Module đảm nhiệm **Giai đoạn 3**. Kích hoạt thư viện `WeasyPrint` làm nhân lõi để hấp thụ mã HTML trung gian và bản đồ CSS Paged Media. Nó đọc toàn bộ các Mỏ neo Tiêu đề đã thiết lập và ra lệnh cho WeasyPrint kết xuất chúng thành bản đồ điều hướng tương tác bên lề PDF. Nó cũng bao gồm cơ chế triệt tiêu các cảnh báo nhiễu cấp hệ điều hành từ thư viện GLib/GIO/GTK3 trên Windows.


* **`tests/red_team_tests.py`**: Bộ kiểm thử đối kháng Hộp Trắng, thực thi 6 kịch bản khắc nghiệt (như thử nghiệm mã hóa tiếng Việt lồng toán tử, bẫy đánh lừa tiêu đề nằm trong khối mã, tràn viền vật lý, xử lý thư mục rỗng, và cô lập lỗi tệp hỏng) nhằm chứng minh hệ thống không bao giờ bị sập đổ trước các dữ liệu sai lệch.

-----

# 🛠️ HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG VÀ KHỞI TẠO CẤU HÌNH (ENVIRONMENT SETUP & CONFIGURATION)

Nội dung phần này hướng dẫn chi tiết từng bước chuẩn bị hạ tầng phần mềm, khởi tạo môi trường thực thi cách ly trên VSCode, cài đặt các vật tư thư viện phụ thuộc và thiết lập tệp điều khiển hệ thống `config/settings.yaml` cho dự án `markdown_to_pdf_engine` trên hệ điều hành Windows 11.

---

## 💻 1. YÊU CẦU HỆ THỐNG VÀ CÁC THÀNH PHẦN TIỀN ĐỀ (PREREQUISITES)

Để hệ thống chuyển đổi vận hành trơn tru và không gặp sự cố gián đoạn, máy tính cần đáp ứng các thành phần hạ tầng sau:

* **Hệ điều hành:** Microsoft Windows 10 hoặc Windows 11 (Tối ưu nhất trên Windows 11 64-bit).
* **Môi trường thực thi Python:** Python phiên bản 3.10 trở lên.
* **Trình biên tập mã nguồn (IDE):** Visual Studio Code (VSCode).
* **Thư viện đồ họa nền tảng C-Runtime:** GTK3-Runtime cho Windows (Thành phần bắt buộc để động cơ `WeasyPrint` kết xuất file PDF).

### Ẩn dụ Ngữ nghĩa: "Động cơ và Bộ truyền động C-Runtime"
Hãy tưởng tượng **Python** là **Vô-lăng và Cần số** (nơi điều khiển logic), còn **GTK3-Runtime** là **Hộp số và Trục bánh xe** vật lý bên dưới gầm xe. Động cơ in ấn `WeasyPrint` sử dụng ngôn ngữ Python để nhận lệnh, nhưng khi cần vẽ phông chữ, chia khoảng cách lề in A4 hay xuất định dạng trang PDF, nó buộc phải gọi các thư viện đồ họa mã nguồn C của `GTK3-Runtime` (`Cairo`, `Pango`, `Fontconfig`). Nếu thiếu `GTK3-Runtime`, vô-lăng vẫn xoay nhưng xe không thể di chuyển (Python ném ra ngoại lệ `ImportError` hoặc `OSError`).

### Hướng dẫn cài đặt GTK3-Runtime trên Windows 11:
1. Tải bản cài đặt `GTK3-Runtime Win64` từ kho lưu trữ chính thức.
2. Thực thi tệp cài đặt `.exe` và chấp nhận đường dẫn mặc định: `C:\Program Files\GTK3-Runtime Win64\bin`.
3. Mã nguồn của dự án trong tệp `src/pdf_compiler.py` đã tích hợp sẵn cơ chế tự động tìm kiếm và đăng ký đường dẫn DLL này vào hệ thống (`os.add_dll_directory`), giúp bạn không cần phải cấu hình biến môi trường Environment Variables thủ công.

---

## 🧰 2. THIẾT LẬP KHÔNG GIAN LÀM VIỆC TRÊN VSCODE (VSCODE WORKFLOW)

Để đảm bảo các thư viện của dự án này không gây xung đột với các ứng dụng Python khác trên máy tính, chúng ta triển khai **Môi trường ảo (Virtual Environment - `venv`)**.

### Ẩn dụ Ngữ nghĩa: "Hộp Dụng cụ Cách ly Công trình"
Thay vì vứt tất cả đinh, ốc, búa vào một kho chung của cả ngôi nhà (môi trường Python toàn cục của Windows), việc tạo `venv` giống như việc bạn cấp riêng một **Hộp dụng cụ chuyên dụng** cho công trình `markdown_to_pdf_engine`. Mọi vật tư (thư viện) mua về chỉ nằm trong hộp này, khi xong công trình, bạn có thể cất đi mà không làm bẩn kho chung.

### Quy trình Thao tác Từng bước trên Giao diện VSCode:

#### Bước 1: Mở Thư mục Dự án trong VSCode
1. Khởi động phần mềm **VSCode**.
2. Trên thanh menu chính, chọn **File** -> **Open Folder...** (hoặc nhấn tổ hợp phím `Ctrl + K` rồi `Ctrl + O`).
3. Trỏ đường dẫn đến thư mục `MARKDOWN_TO_PDF_ENGINE` và nhấn **Select Folder**.

#### Bước 2: Mở Cửa sổ Terminal Tích hợp
1. Trên thanh menu của VSCode, chọn **Terminal** -> **New Terminal** (hoặc nhấn tổ hợp phím `Ctrl + ~`).
2. Màn hình Cửa sổ dòng lệnh (PowerShell) sẽ xuất hiện tại cạnh dưới giao diện VSCode với đường dẫn hiện hành là thư mục gốc của dự án.

#### Bước 3: Khởi tạo Môi trường Ảo `venv`
Tại cửa sổ Terminal, gõ lệnh sau và nhấn `Enter`:
```powershell
python -m venv venv

```

*Hệ thống sẽ tạo ra một thư mục ẩn tên là `venv/` chứa trình thông dịch Python độc lập.*

#### Bước 4: Kích hoạt Môi trường Ảo

Tại cửa sổ Terminal, gõ lệnh sau và nhấn `Enter`:

```powershell
.\venv\Scripts\Activate.ps1

```

* **Dấu hiệu nhận biết thành công:** Đầu dòng lệnh của Terminal sẽ xuất hiện tiền tố `(venv)` màu xanh lá cây (Ví dụ: `(venv) PS D:\vscode_run\markdown_to_pdf_engine>`).

#### Bước 5: Cài đặt Các Thư viện Vật tư Phụ thuộc (`requirements.txt`)

Tệp `requirements.txt` trong dự án khai báo danh sách các thư viện mã nguồn mở bắt buộc bao gồm:

* **`markdown-it-py>=3.0.0`**: Động cơ bóc tách văn bản thô thành Cây cú pháp trừu tượng (AST).

* **`pygments>=2.17.0`**: Động cơ phân tích cú pháp mã nguồn và nhuộm màu từ khóa (Syntax Highlighting).

* **`weasyprint>=61.0`**: Động cơ chuyển đổi HTML/CSS Paged Media thành tệp PDF.

* **`pyyaml>=6.0.1`**: Động cơ đọc và phân tích tệp cấu hình `settings.yaml`.

Thực thi lệnh cài đặt hàng loạt bằng cách gõ lệnh sau vào Terminal:

```powershell
pip install -r requirements.txt

```

*Chờ tiến trình tải xuống và giải nén hoàn tất cho đến khi Terminal hiển thị thông báo `Successfully installed...`.*

---

## ⚙️ 3. SỔ TAY CẤU HÌNH TOÀN CỤC (`config/settings.yaml`)

Thực hiện đúng triết lý **Phân tách Mối quan tâm (Separation of Concerns - SoC)**, toàn bộ tham số vận hành của hệ thống được tập trung duy nhất tại tệp `config/settings.yaml`. Tệp cấu hình này đóng vai trò là "Bảng Điều Khiển" của nhà máy, cho phép tùy chỉnh hành vi biên dịch mà không cần chỉnh sửa mã nguồn Python.

### Mã nguồn Cấu hình Mẫu Chuẩn mực cho `config/settings.yaml`:

```yaml
# ==============================================================================
# BẢNG ĐIỀU KHUYỂN VÀ QUY HOẠCH PIPELINE (MARKDOWN TO PDF ENGINE SCHEMA)
# Dự án: markdown_to_pdf_engine
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
  code_overflow_handling: "break-all"

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
```

---

## 🔍 PHÂN TÍCH CHI TIẾT CÁC THAM SỐ CẤU HÌNH BẮT BUỘC

1. **`global_encoding_standard: "utf-8"`**: Đóng vai trò là bức tường phòng thủ nguyên nhân gốc rễ gây ra lỗi mã hóa ký tự. Nó buộc toàn bộ các hàm mở tệp (`open()`) trong Python phải sử dụng chuẩn `utf-8` thay vì bảng mã mặc định `cp1252` của hệ điều hành Windows 11.
2. **`directory_routing`**: Quản lý chiến lược định tuyến tài liệu. Tính năng `preserve_subfolder_structure: true` giúp người dùng quản lý tri thức dạng cây folder phức tạp (như Obsidian hay Zettelkasten) bên trong thư mục `input/` mà khi xuất sang `output/` không bị dồn tất cả file PDF ra một thư mục phẳng.
3. **`syntax_highlighting_profile: "monokai"`**: Khai báo theme giao diện nhuộm màu khối mã. Bạn có thể thay đổi tham số này thành `"github-dark"`, `"dracula"`, hoặc `"solarized-light"` tùy theo sở thích thẩm mỹ.
4. **`heading_retention_depth`**: Khóa độ sâu của cây Bookmark điều hướng trong file PDF. Bằng việc đặt `max_bookmark_level: 4`, hệ thống chỉ đưa các tiêu đề từ H1 đến H4 vào danh sách Dấu trang (Bookmarks Palette), giữ cho thanh điều hướng PDF gọn gàng, tránh bị rác bởi các tiêu đề quá nhỏ như H5 hay H6.
5. **`typography_configuration`**: Danh sách phông chữ dự phòng (Font Stack). Chuỗi `"Segoe UI", "Arial", "Calibri", "Tahoma"` đảm bảo luôn có ít nhất một phông chữ hệ thống hỗ trợ trọn vẹn bảng mã tiếng Việt Unicode trên bất kỳ máy tính Windows nào, triệt tiêu hoàn toàn nguy cơ biến dạng ký tự hoặc lỗi ô vuông.

---

# 🚀 SÁCH HƯỚNG DẪN VẬN HÀNH VÀ CƠ CHẾ CHỐNG LỖI (OPERATIONAL MANUAL & FAULT TOLERANCE)

Tài liệu này cung cấp toàn bộ quy trình vận hành đường ống biên dịch tài liệu tự động `markdown_to_pdf_engine`, chi tiết hóa các thao tác thực thi trên giao diện Terminal của VSCode, cùng phân tích kỹ thuật chuyên sâu về cơ chế chống lỗi (Fault-tolerance) và tự bảo tồn cấu trúc dữ liệu của hệ thống.

---

## 🔄 1. QUY TRÌNH VẬN HÀNH ĐƯỜNG ỐNG BIÊN DỊCH (OPERATIONAL WORKFLOW)

### Ẩn dụ Ngữ nghĩa: "Băng chuyền Tự động hóa của Nhà máy"
Hãy tưởng tượng tệp `main.py` đóng vai trò là **Quản Đốc Băng Chuyền**.
* Bạn nạp nguyên liệu thô (các tệp `.md`) vào **Máng Đón Đầu Vào** (Thư mục `input/`).
* Bạn gạt cầu giao khởi động băng chuyền (Thực thi lệnh `python main.py`).
* Quản Đốc sẽ tự động phân loại tệp, kiểm tra tính hợp lệ, đẩy từng tệp qua các công đoạn chế tác (AST Parser -> HTML Renderer -> PDF Compiler) và đưa sản phẩm đóng gói sắc nét (tệp `.pdf`) vào **Kho Thành Phẩm** (Thư mục `output/`).

```text
[Thư mục input/] ---> (Quét tệp .md) ---> [main.py: Quản đốc Điều phối]
                                                    │
       ┌────────────────────────────────────────────┴──────────────────────────────────────────┐
       ▼                                            ▼                                           ▼
[Giai đoạn 1: AST Parser]              [Giai đoạn 2: HTML Renderer]               [Giai đoạn 3: PDF Compiler]
(Phân rã Cây cú pháp UTF-8)           (Tô màu Pygments & Gắn Mỏ neo)            (Hấp thụ CSS & Bơm Bookmarks)
       │                                            │                                           │
       └────────────────────────────────────────────┬──────────────────────────────────────────┘
                                                    ▼
                                    [Thư mục output/ (File .pdf)]
```

---

### Quy trình Thao tác Chi tiết Từng bước trên VSCode:

#### Bước 1: Chuẩn bị Văn bản Đầu vào (Input Preparation)
1. Trong cửa sổ **Explorer** bên cánh trái của VSCode, tìm đến thư mục `input/` (Nếu chưa có, hệ thống sẽ tự động khởi tạo ở lần chạy đầu tiên).
2. Sao chép hoặc tạo mới các tệp Markdown cần chuyển đổi vào trong thư mục `input/`.
3. **Các định dạng đuôi tệp được hỗ trợ mặc định:** `.md`, `.markdown`, `.mdown` (Có thể tùy chỉnh trong `config/settings.yaml`).

#### Bước 2: Thực thi Tiến trình Biên dịch Hàng loạt (Batch Execution)
1. Mở cửa sổ **Terminal** trong VSCode bằng tổ hợp phím `Ctrl + ~` (Đảm bảo môi trường ảo `(venv)` đang được kích hoạt).
2. Gõ câu lệnh thực thi sau và nhấn `Enter`:
   ```powershell
   python main.py
   ```

#### Bước 3: Đọc Nhật ký Vận hành Terminal (Log Inspection)
Khi lệnh được kích hoạt, hệ thống sẽ in ra màn hình nhật ký tiến trình thời gian thực (Real-time Console Logs):

```text
=== BẮT ĐẦU TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT (BATCH PROCESSING) ===
[THÔNG_TIN] Phát hiện 2 tệp Markdown hợp lệ trong danh sách chờ biên dịch.

[1/2] Đang xử lý: input\input_sample.md
    -> [THÀNH_CÔNG] Xuất bản: output\input_sample.pdf
[2/2] Đang xử lý: input\learn_python_programming.md
    -> [THÀNH_CÔNG] Xuất bản: output\learn_python_programming.pdf

================ TỔNG KẾT TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT ================
- Tổng số tệp phát hiện : 2
- Biên dịch thành công : 2
- Biên dịch thất bại   : 0
- Bỏ qua (Đã tồn tại)  : 0
========================================================================
```

#### Bước 4: Kiểm tra Sản phẩm Đầu ra
1. Truy cập thư mục `output/` trên cây thư mục VSCode.
2. Nhấp chuột phải vào tệp `.pdf` vừa xuất bản và chọn **Reveal in File Explorer** để mở và kiểm tra chất lượng hiển thị, bản đồ Bookmark và màu sắc mã nguồn.

---

## 🛡️ 2. PHÂN TÍCH CƠ CHẾ BẢO TỒN VÀ QUẢN LÝ CẤU TRÚC (SELF-PRESERVATION)

Hệ thống được trang bị các tính năng tự bảo tồn không gian lưu trữ và duy trì cấu trúc dữ liệu nguyên vẹn:

### 1. Tự động Khởi tạo Hạ tầng Thư mục (`auto_create_directories`)
* Nếu người dùng lần đầu tải mã nguồn về và chưa tạo hai thư mục `input/` và `output/`, hàm `ensure_directories_exist()` trong `main.py` sẽ phát hiện sự thiếu hụt này.
* Hệ thống sẽ tự động kích hoạt lệnh tạo thư mục an toàn (`mkdir(parents=True, exist_ok=True)`) mà không gây ra bất kỳ lỗi dừng chương trình nào.

### 2. Tái tạo và Bảo tồn Cấu trúc Thư mục Con (`preserve_subfolder_structure`)
* **Thách thức:** Khi người dùng lưu trữ ghi chú dạng cây phân tầng phức tạp (Ví dụ: `input/du_an_a/chuyen_de_1/bao_cao.md`), nhiều công cụ chuyển đổi thô sẽ dồn tất cả các file PDF ra một thư mục phẳng `output/bao_cao.pdf`, làm mất hoàn toàn bối cảnh phân loại.
* **Giải pháp:** Trong `main.py`, hệ thống tính toán đường dẫn tương đối (`relative_to(input_dir)`).[cite: 3] Khi tính năng `preserve_subfolder_structure: true` được bật trong `settings.yaml`, hệ thống sẽ tự động dựng lại cây thư mục con tương ứng bên phía `output/` (Ví dụ: `output/du_an_a/chuyen_de_1/bao_cao.pdf`).

### 3. Kiểm soát Chế độ Ghi đè Tệp Thành phẩm (`overwrite_existing`)
* Khi `overwrite_existing: true`, hệ thống sẽ ghi đè tệp PDF mới lên tệp PDF cũ để luôn cập nhật nội dung mới nhất.
* Khi `overwrite_existing: false`, hệ thống sẽ kiểm tra `target_output_pdf_path.exists()`. Nếu tệp PDF đã tồn tại, nó sẽ tự động bỏ qua (`skipped_count += 1`) để tiết kiệm tài nguyên tính toán và bảo vệ tài liệu đã biên dịch trước đó.

---

## ⚡ 3. CƠ CHẾ PHÒNG THỦ VÀ CÔ LẬP NGOẠI LỆ (FAULT ISOLATION)

### Ẩn dụ Ngữ nghĩa: "Aptomat (Cầu Dao Tự Động) Phân Lưới"
Trong một tòa nhà, nếu bóng đèn ở phòng khách bị chập điện, cầu dao riêng của phòng khách sẽ ngắt. Điện ở phòng bếp và phòng ngủ vẫn sáng bình thường. 
Trong `markdown_to_pdf_engine`, nếu bạn đưa vào 10 tệp Markdown nhưng có 1 tệp bị hỏng (chứa mã nhị phân rác hoặc sai mã hóa), **Cầu Dao Cô Lập** `execute_single_file_pipeline` sẽ lập tức bẫy lỗi, đánh dấu tệp đó thất bại, và tiếp tục biên dịch 9 tệp còn lại một cách bình thường.

```text
[Bắt đầu Batch] ───> Tệp 1 (.md) ───> Biên dịch ───> [THÀNH CÔNG] (Xuất PDF 1)
                 ───> Tệp 2 (Hỏng) ───> Bẫy Ngoại Lệ ───> [THẤT BẠI] (Bỏ qua & Báo lỗi Log)
                 ───> Tệp 3 (.md) ───> Biên dịch ───> [THÀNH CÔNG] (Xuất PDF 3)
```

---

### Phân tích Chi tiết Các Tầng Bẫy Lỗi Trong Mã Nguồn:

#### Tầng 1: Cô lập Lỗi Đơn tệp (Single File Exception Containment)
Trong tệp `main.py`, toàn bộ tiến trình biên dịch từng tệp được bọc trong hàm `execute_single_file_pipeline()` với khối `try...except` phòng thủ diện rộng:

```python
try:
    # Tiến trình 5 bước biên dịch AST -> HTML -> PDF
    ...
    return True
except (
    FileNotFoundError,
    UnicodeDecodeError,
    ValueError,
    TypeError,
    OSError,
    RuntimeError,
) as error:
    print(f"    -> [THẤT_BẠI_TỆP] Bỏ qua tệp {input_md_path.name} do xuất hiện lỗi: {error}")
    return False
```

* **Chức năng:** Chỉ định đích danh các ngoại lệ I/O, mã hóa và runtime. Khi phát hiện tệp lỗi, nó ghi nhận vào nhật ký Terminal và trả về `False`, giúp vòng lặp `for` trong `batch_process_directory()` chuyển sang tệp kế tiếp mà không làm sập tiến trình chung.

#### Tầng 2: Phòng thủ Sự cố Trôi dạt Mã hóa Unicode (`UnicodeDecodeError`)
* **Sự cố:** Hệ điều hành Windows 11 mặc định mở tệp bằng bảng mã `cp1252`. Nếu gặp ký tự tiếng Việt Unicode hoặc ký tự đặc biệt, chương trình Python thông thường sẽ bị ngắt đột ngột.
* **Giải pháp phòng thủ:** Trong `src/ast_parser.py` và `main.py`, mọi thao tác mở tệp `open()` đều bắt buộc phải truyền tham số `encoding="utf-8"`. Đồng thời, `ASTParser` bắt riêng `UnicodeDecodeError` và đóng gói lại thành thông điệp lỗi rõ ràng cho người dùng.

#### Tầng 3: Xử lý An toàn Thư mục Rỗng (Empty Input Directory Handling)
* Khi thư mục `input/` không chứa tệp `.md` nào, hệ thống không ném ra lỗi ngắt tiến trình.[cite: 3, 9] 
* `main.py` kiểm tra `if not target_files:`, in ra thông báo hướng dẫn người dùng chép tệp vào thư mục và kết thúc tiến trình một cách êm đẹp (Exit Code 0).

#### Tầng 4: Triệt tiêu Cảnh báo Nhiễu C-Runtime của GTK3 trên Windows
* **Sự cố:** Khi `WeasyPrint` gọi thư viện C gốc `GLib/GIO` trên Windows 11, hệ thống thường đẩy các cảnh báo nhiễu dạng `GLib-GIO-WARNING` ra luồng xuất lỗi Terminal (`stderr`).
* **Giải pháp phòng thủ:** Trong `src/pdf_compiler.py`, hệ thống tự động đăng ký đường dẫn DLL của GTK3 (`_register_gtk_dll_directories`) và thiết lập các biến môi trường dập tắt log nhiễu trước khi nạp thư viện `WeasyPrint`:
  ```python
  os.environ["G_MESSAGES_DEBUG"] = "none"
  os.environ["GLIB_LOG_LEVEL"] = "4"
  ```
  Việc này giữ cho nhật ký giao diện Terminal của người dùng luôn sạch sẽ, dễ quan sát.

-----

# 🧪 BỘ KIỂM THỬ ĐỐI KHÁNG (RED-TEAM TESTING) VÀ QUẢN LÝ MÃ NGUỒN (VERSION CONTROL)

Tài liệu này chi tiết hóa toàn bộ kịch bản kiểm thử hộp trắng (White-Box Red-Teaming) nhằm thử thách độ bền vững của hệ thống `markdown_to_pdf_engine`, cùng hướng dẫn thiết lập tệp loại trừ `.gitignore` và quy trình quản lý mã nguồn bằng Git/GitHub trên VSCode.[cite: 3]

---

## 🛡️ 1. BỘ KIỂM THỬ HỘP TRẮNG ĐỐI KHÁNG (WHITE-BOX RED-TEAM TEST SUITE)

### Ẩn dụ Ngữ nghĩa: "Phòng Thử Nghiệm Va Chạm Ô Tô (Crash Test Lab)"
Trong ngành sản xuất ô tô, trước khi một chiếc xe được phép lăn bánh ra thị trường, nhà sản xuất phải đưa nó vào phòng thử nghiệm va chạm: cho xe đâm vào tường bê tông, thử nghiệm trong bão tuyết, hay cho chạy trên đường ngập nước. 
Tệp `tests/red_team_tests.py` đóng vai trò là **Phòng Thử Nghiệm Va Chạm** của hệ thống.[cite: 3] Nó tạo ra các dữ liệu "độc hại" và khắc nghiệt nhất nhằm mục đích cố tình làm sập hệ thống, qua đó chứng minh rằng các cơ chế phòng thủ đã vận hành hoàn hảo.[cite: 3]

---

### Phân tích Chi tiết 6 Kịch bản Kiểm thử Đối kháng (`tests/red_team_tests.py`):

```text
                                ┌──────────────────────────────────────────────┐
                                │     Kịch bản 1: Xung đột Mã hóa Đa ngôn ngữ   │
                                ├──────────────────────────────────────────────┤
                                │     Kịch bản 2: Bẫy Đánh lừa Tiêu đề (Spoof) │
                                ├──────────────────────────────────────────────┤
  [Bộ Kiểm thử Red-Team] ─────> │     Kịch bản 3: Tràn Viền Vật lý Chuỗi Dài   │
   (red_team_tests.py)          ├──────────────────────────────────────────────┤
                                │     Kịch bản 4: Thư mục Đầu vào Rỗng       │
                                ├──────────────────────────────────────────────┤
                                │     Kịch bản 5: Cô lập Tệp Hỏng Nhị phân   │
                                ├──────────────────────────────────────────────┤
                                │     Kịch bản 6: Tái tạo Cấu trúc Folder Con  │
                                └──────────────────────────────────────────────┘

```

#### Kịch bản 1: Rào chắn Xung đột Ký tự Đa ngôn ngữ (`test_scenario_1_bilingual_encoding_stress_test`)

* **Mục tiêu đối kháng:** Tiêm một khối dữ liệu phức tạp chứa văn bản Tiếng Việt có dấu (`# Thử nghiệm Mã hóa Tiếng Việt...`) lồng ghép trực tiếp với các biểu thức logic (`a < b && c > d`) và ký tự điều khiển biểu thức chính quy (`^[a-zA-Z0-9_]+$`).

* **Phương pháp kiểm tra:** Ép `ASTParser` nạp tệp và kiểm tra `HTMLRenderer` có giữ nguyên văn bản Tiếng Việt mà không biến dạng ký tự hay ném ra ngoại lệ `UnicodeDecodeError`.

* **Kết quả kỳ vọng:** Bộ phân tích AST giữ nguyên 100% hình thái văn bản Tiếng Việt và render thành công các thẻ HTML trung gian.

#### Kịch bản 2: Bẫy Đánh lừa Cấu trúc Phân cấp (`test_scenario_2_heading_spoofing_simulation`)

* **Mục tiêu đối kháng:** Cố tình đưa chuỗi định dạng tiêu đề giả mạo (Ví dụ: `## Tiêu đề Giả mạo Cấp 2 Trong Code Block`) nằm chìm bên trong một khối mã nguồn (````python ... ````).

* **Phương pháp kiểm tra:** Quét mã HTML trung gian để xác nhận tiêu đề thật (`# Tiêu đề Hợp lệ Cấp 1`) được chuyển thành `<h1 id="tieu-de-hop-le-cap-1" data-level="1">`, còn tiêu đề giả mạo nằm trong khối mã KHÔNG bao giờ được tạo thẻ `<h2>` hay gắn thuộc tính `data-level="2"`.
* **Kết quả kỳ vọng:** Động cơ `markdown-it-py` cô lập hoàn toàn khối mã nguồn `fence`, triệt tiêu nguy cơ rác bản đồ Dấu trang (Bookmarks) trong PDF.

#### Kịch bản 3: Thử nghiệm Tràn Viền Vật lý (`test_scenario_3_physical_overflow_destructive_test`)

* **Mục tiêu đối kháng:** Ép hệ thống xử lý một chuỗi mã nguồn liên tục gồm 1.500 ký tự `X` không có khoảng trắng, vượt gấp nhiều lần độ rộng trang A4.

* **Phương pháp kiểm tra:** Đẩy dữ liệu qua `PDFCompiler` để kiểm tra khả năng biên dịch vật lý.
* **Kết quả kỳ vọng:** Lớp CSS Paged Media với thuộc tính `word-break: break-all` phản ứng thành công, tự động bẻ gãy chuỗi xuống dòng mà không làm sập tiến trình in ấn của `WeasyPrint`.

#### Kịch bản 4: Xử lý Thư mục Đầu vào Rỗng (`test_scenario_4_empty_directory_handling`)

* **Mục tiêu đối kháng:** Kích hoạt tiến trình quét hàng loạt `batch_process_directory()` khi thư mục `input/` không chứa bất kỳ tệp Markdown nào.

* **Phương pháp kiểm tra:** Bẫy toàn bộ các ngoại lệ `FileNotFoundError`, `ValueError`, `TypeError`, `OSError`, `RuntimeError`.

* **Kết quả kỳ vọng:** Chương trình hiển thị thông báo hướng dẫn nhẹ nhàng và kết thúc an toàn mà không ném ra ngoại lệ dừng đột ngột.

#### Kịch bản 5: Cô lập Tệp Hỏng Nhị phân (`test_scenario_5_batch_fault_isolation`)

* **Mục tiêu đối kháng:** Tạo một thư mục thử nghiệm chứa 3 tệp: Tệp A (Hợp lệ), Tệp B (Tệp hỏng chứa chuỗi byte nhị phân không hợp lệ `\x80\x81\xfe\xff\xff` gây lỗi mã hóa UTF-8), và Tệp C (Hợp lệ).
* **Phương pháp kiểm tra:** Chạy kịch bản qua `execute_single_file_pipeline()`.

* **Kết quả kỳ vọng:** Tệp A và C trả về `True` và xuất hiện trong `output/`. Tệp B bị bẫy lỗi, trả về `False`, không sinh ra PDF nhưng không làm ngắt tiến trình biên dịch của A và C.

#### Kịch bản 6: Tái tạo Cấu trúc Thư mục Con (`test_scenario_6_subfolder_structure_preservation`)

* **Mục tiêu đối kháng:** Tạo cấu trúc thư mục phân tầng nhiều cấp: `input/du_an_nghien_cuu/chuyen_de_1/bao_cao.md`.
* **Phương pháp kiểm tra:** Thực thi tiến trình quét hàng loạt `batch_process_directory()`.

* **Kết quả kỳ vọng:** Hệ thống tự động tái tạo đúng cây thư mục con bên phía `output/` và xuất bản tệp tại: `output/du_an_nghien_cuu/chuyen_de_1/bao_cao.pdf`.

---

### Quy trình Thực thi Kiểm thử Trực tiếp trên VSCode Terminal:

1. Mở Cửa sổ Terminal trong VSCode (`Ctrl + ~`) và đảm bảo môi trường ảo `(venv)` đang bật.


2. Thực thi lệnh chạy toàn bộ suite kiểm thử Red-Team bằng module `unittest` của Python:
```powershell
python -m unittest tests/red_team_tests.py

```


3. **Đọc kết quả kiểm thử trên màn hình:**
* Nếu tất cả 6 kịch bản đều vượt qua, Terminal sẽ hiển thị:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 2.154s

OK

```

* Ký tự `.` đại diện cho 1 bài test chạy thành công. Chuỗi `OK` khẳng định hệ thống đạt độ bền vững 100%.

---

## 📦 2. QUY TRÌNH QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB (VERSION CONTROL)

Để lưu trữ dự án an toàn trên GitHub mà không vô tình đẩy các tệp rác, tệp môi trường ảo dung lượng lớn, hoặc tài liệu cá nhân nhạy cảm lên mạng, chúng ta thiết lập tệp loại trừ `.gitignore`.

### Mã nguồn Tệp `.gitignore` Mẫu Chuẩn Phòng thủ cho Dự án:

```gitignore
# ==============================================================================
# TỆP LOẠI TRỪ GIT (GITIGNORE SCHEMA)
# Dự án: markdown_to_pdf_engine
# ==============================================================================

# 1. BỘ NHỚ ĐỆM VÀ TỆP TRÌNH THÔNG DỊCH PYTHON (PYTHON CACHE)
__pycache__/
*.py[cod]
*$py.class
.Python

# 2. MÔI TRƯỜNG ẢO (VIRTUAL ENVIRONMENTS)
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

```

---

### Quy trình Đồng bộ Mã nguồn lên GitHub Từng bước:

#### Bước 1: Khởi tạo Kho lưu trữ Git Cục bộ (Local Repository)

Tại cửa sổ Terminal của VSCode, gõ lệnh:

```powershell
git init

```

#### Bước 2: Thêm Tất cả Tệp vào Hàng chờ Lưu trữ (Staging Area)

```powershell
git add .

```

*(Tệp `.gitignore` sẽ tự động lọc bỏ thư mục `venv/`, `__pycache__/` và các tệp `.pdf` thành phẩm).*

#### Bước 3: Tạo Điểm Lưu trữ Phiên bản (Commit)

```powershell
git commit -m "feat: Hoàn thiện lõi động cơ markdown_to_pdf_engine v1.0.0 đạt chuẩn Red-Team"

```

#### Bước 4: Liên kết với Kho lưu trữ GitHub Trực tuyến (Remote Repository)

1. Truy cập GitHub, tạo một Repository mới đặt tên là `markdown_to_pdf_engine`.
2. Sao chép đường dẫn URL của Repository (Ví dụ: `https://github.com/user/markdown_to_pdf_engine.git`).
3. Dán lệnh liên kết vào Terminal:
```powershell
git branch -M main
git remote add origin [https://github.com/user/markdown_to_pdf_engine.git](https://github.com/user/markdown_to_pdf_engine.git)
git push -u origin main

```

---

## 📜 3. LỊCH SỬ PHIÊN BẢN (CHANGELOG & VERSION HISTORY)

### Phiên bản 1.0.0 (Hiện tại)

* **Kiến trúc Lõi:** Hoàn thiện pipeline 3 giai đoạn: `ASTParser` (`markdown-it-py`) -> `HTMLRenderer` (`Pygments`) -> `PDFCompiler` (`WeasyPrint`).

* **Bảo mật & Chống lỗi:** Tích hợp bộ cô lập luồng `C-Runtime Stderr` trên Windows 11, cưỡng chế mã hóa UTF-8 toàn cục, và hoàn tất 100% bài test trong Red-Team Suite.

* **Cấu hình Tách biệt:** Điều khiển toàn bộ hệ thống thông qua tệp YAML chuẩn SoC (`config/settings.yaml`).
