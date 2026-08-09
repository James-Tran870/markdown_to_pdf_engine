# MARKDOWN TO PDF ENGINE (Lõi Biên dịch Tài liệu Cục bộ & Chuẩn in ấn Học thuật - Phiên bản v1.4.3)

Một hệ thống đường ống dữ liệu (Data Pipeline) tự động hóa toàn diện, chuyên trách chuyển đổi hàng loạt tệp Markdown sang định dạng PDF chuẩn Typography xuất bản, đồ họa toán học sắc nét qua động cơ Chromium và bảng biểu GFM khung lưới hoàn chỉnh ngay trên môi trường Windows 11 cục bộ.

Dự án được xây dựng dựa trên tư duy phân tách hệ thống nghiêm ngặt, khép kín và độc lập ngoại tuyến (Offline-first). Hệ thống nói KHÔNG với các công nghệ đám mây (Cloud), máy chủ web hay cơ sở dữ liệu phức tạp. Mọi tiến trình biên dịch đều diễn ra trên máy cục bộ, bảo đảm tính bảo mật dữ liệu tuyệt đối và khả năng can thiệp tham số linh hoạt thông qua hệ thống cấu hình tách biệt.

---

### TRIẾT LÝ KIẾN TRÚC VÀ 6 TRỤ CỘT PHÒNG THỦ (ARCHITECTURAL PHILOSOPHY v1.4.3)

Để hình dung phương thức vận hành của hệ thống, hãy tưởng tượng dự án giống như một **Xưởng In ấn Đồ họa Hiện đại Khép kín**. Thay vì cho phép công nhân tự do can thiệp vào dây chuyền, xưởng vận hành dựa trên 6 trụ cột kiến trúc bất biến nhằm loại trừ hoàn toàn mọi rủi ro gián đoạn tiến trình:

#### 1. Phân tách Mối quan tâm (Separation of Concerns - SoC)

- **Ẩn dụ đời thực:** Trong một xưởng đúc phim điện ảnh, Trình chiếu phim (Mã logic Python) không bao giờ tự mình điều khiển độ sáng hay phông chữ của phụ đề; nó hoạt động dựa trên một tệp kịch bản định dạng do Đạo diễn thiết lập. Khi cần đổi kiểu chữ hay độ phân giải, Đạo diễn chỉ việc sửa kịch bản mà không cần thay máy chiếu.
- **Áp dụng vào hệ thống:** Tách rời hoàn toàn tham số điều khiển khỏi mã nguồn xử lý chính. Mọi tiến trình biên dịch đều nạp cấu hình từ tệp YAML chuyên biệt (`config/settings.yaml`). Toàn bộ thông số như lề giấy, chuẩn mã hóa, màu sắc từ khóa mã nguồn, độ sâu dấu trang (Bookmarks Palette), van điều khiển Chromium Headless và cấu hình KaTeX Offline đều được tập trung duy nhất tại đây.

#### 2. Chống Trôi dạt Mã hóa Luồng I/O (I/O Encoding Drift Defense)

- **Ẩn dụ đời thực:** Tưởng tượng nhà máy tiếp nhận đĩa phim từ nhiều quốc gia nhưng máy đọc mặc định chỉ đọc được ký tự tiếng Anh. Khi một bộ phim ghi nhãn Tiếng Việt đi qua, máy đọc sai mã và làm vỡ hình ảnh trên màn chiếu.
- **Áp dụng vào hệ thống:** Hệ điều hành Windows 11 vận hành mặc định với bảng mã `cp1252`. Khi nạp văn bản đa ngôn ngữ chứa ký tự Tiếng Việt, hệ thống sẽ ném ra ngoại lệ `UnicodeDecodeError` hoặc làm biến dạng ký tự có dấu nếu luồng nạp không được cưỡng chế chuẩn. Hệ thống xác lập hằng số `utf-8` làm kim chỉ nam bắt buộc cho toàn bộ giao thức Đọc (Read), Ghi (Write) và Kết xuất (Render).

#### 3. Phân tích Cây Cú pháp Trừu tượng (AST Engine - GFM Tables & Math - v1.4.3)

- **Ẩn dụ đời thực:** Dùng Biểu thức chính quy (Regex) để tìm và sửa văn bản giống như việc nhắm mắt dùng kéo cắt một bản vẽ kiến trúc dựa trên việc đếm số nét vẽ; nó rất dễ cắt nhầm vào dầm cột. Dùng AST giống như việc quét tia laser 3D toàn bộ tòa nhà, nhận diện rõ đâu là "Cửa sổ", đâu là "Bức tường", đâu là "Bàn ghế", sau đó mới tiến hành thi công.

- **Áp dụng vào hệ thống:** Hệ thống từ chối phương pháp thay thế chuỗi tuần tự (Regex) thiếu an toàn. Bắt buộc áp dụng cơ chế Cây cú pháp trừu tượng (Abstract Syntax Tree - AST) thông qua thư viện `markdown-it-py` với preset `gfm-like` tích hợp `linkify-it-py`. Các Nút mã nguồn (`fence`), Nút toán học (`math_inline`, `math_block`) và Nút bảng biểu (`table_open`, `tr_open`, `td_open`) được cô lập hoàn toàn, không cho phép rò rỉ định dạng ra ngoài.

#### 4. Động cơ Đúc Đồ họa Toán học Web DOM (Headless Browser & KaTeX Engine)

- **Ẩn dụ đời thực:** Thay vì dùng một máy dịch công thức thô sang ký tự sơ khai dễ bị sập khi gặp vĩ lệnh phức tạp, xưởng in sử dụng một **Rô-bốt Trình duyệt Ẩn danh (Chromium Headless Browser)**. Rô-bốt này mở tài liệu trong môi trường đồ họa ảo, chạy cỗ máy đúc KaTeX để vẽ ra từng đường nét vector, mũi tên và hộp khung sắc nét 100% trước khi chụp bản in PDF.
- **Áp dụng vào hệ thống:** Hệ thống loại bỏ hoàn toàn các thư viện dịch toán thuần Python. Module `src/html_renderer.py` tiêm trực tiếp bộ script KaTeX Offline (`assets/katex/`) vào tệp HTML trung gian. Module `src/pdf_compiler.py` khởi chạy trình duyệt Playwright Chromium ngầm, mở tệp tạm qua giao thức `file:///` và đợi KaTeX đúc xong toàn bộ các phần tử DOM `.katex` trước khi xuất bản bản in PDF chuẩn A4.

#### 5. Quản lý Tràn viền Bảng biểu và Cảnh báo Cắt Lề (Table Overflow Clipping & Warning - v1.4.3)

- **Ẩn dụ đời thực:** Khi chở một kiện hàng Bảng biểu khổng lồ có chiều rộng vượt quá thùng xe tải (khổ giấy A4), người tài xế thông minh sẽ dùng máy cắt gọt bỏ phần dư thừa thò ra ngoài thành xe để tránh gây tai nạn giao thông, đồng thời bấm còi báo động cho trung tâm điều phối biết kiện hàng đã bị xén bớt.

- **Áp dụng vào hệ thống:** Đối với các bảng biểu chứa lượng dữ liệu khổng lồ (nhiều cột) vượt quá độ rộng vùng in an toàn của khổ A4 (170mm), hệ thống kích hoạt chiến lược `clip_and_warn`. Lớp giáp CSS sẽ tự động cắt bỏ (clip) phần chữ bị tràn ngang lề giấy để bảo vệ thẩm mỹ chung của bản in, đồng thời bắn nhật ký cảnh báo màu vàng ra Terminal để người dùng nắm thông tin.

#### 6. Ma trận In ấn Học thuật & Lớp Giáp CSS Căn Lề Trái Cưỡng Chế (Academic Standards & Strict Align - v1.4.3)

- **Ẩn dụ đời thực:** Trong một xưởng in sách giáo khoa, toàn bộ chữ viết và tiêu đề bắt buộc phải gióng thẳng hàng dọc bên lề trái để tạo độ trang trọng. Nếu một công thức toán học ở giữa trang tỏa ra năng lượng làm đẩy toàn bộ văn bản xung quanh ra giữa, người thợ in sẽ lắp một **Thước Kẹp Bằng Thép (Strict Left-Align Rules)** giữ chặt toàn bộ khối chữ không cho xô lệch.
- **Áp dụng vào hệ thống:** Tích hợp bộ quy chuẩn học thuật quốc tế (APA 7th, IEEE, Harvard). Giới hạn tự động đánh số bằng CSS Counters ở cấp 4 (`h1` đến `h4`). Áp dụng triệt để thuộc tính `text-align: left !important;` cho toàn bộ `body`, `p`, `h1`-`h6`, `pre` và `.highlight` để triệt tiêu hoàn toàn sự cố rò rỉ căn giữa từ KaTeX, đồng thời khóa sàn kích thước phông chữ `h5`/`h6` ở mức **11pt** in đậm in nghiêng.

---

### BẢN ĐỒ CẤU TRÚC THƯ MỤC (DIRECTORY BLUEPRINT v1.4.3)

Dưới đây là sơ đồ không gian làm việc (Workspace) tiêu chuẩn trên VSCode. Mỗi thành phần đều giữ một vùng trách nhiệm duy nhất (Single Responsibility Principle):

```text
MARKDOWN_TO_PDF_ENGINE/
│
├── assets/                    # [Kho Tài Nguyên Tĩnh Offline] chứa tài nguyên kết xuất đồ họa.
│   └── katex/                 # Bảng CSS, thư viện JS và bộ phông chữ toán học .woff2 ngoại tuyến.
│       ├── fonts/             # Bộ phông chữ vector KaTeX (AMS, Main, Math, Size1).
│       ├── katex.min.css      # Định hình kiểu dáng và cấu trúc đồ họa công thức.
│       ├── katex.min.js       # Động cơ phân tích cú pháp LaTeX client-side.
│       └── auto-render.min.js # Script tự động quét và đúc DOM toán học ($/$$/\[/\]).
│
├── config/
│   └── settings.yaml          # [Bảng Điều Khiển Trung Tâm] Khai báo 11 phân khu tham số, Chromium Engine & KaTeX.
│
├── input/                     # [Kho Nguyên Liệu] Thư mục chứa các tệp .md đầu vào (Quét đệ quy).
│
├── output/                    # [Kho Thành Phẩm] Thư mục chứa các tệp .pdf thành phẩm (Tái tạo cây folder).
│
├── src/                       # [Lõi Động Cơ] Thư mục chứa các module mã nguồn xử lý logic.
│   ├── __init__.py
│   ├── ast_parser.py          # (Giai đoạn 1) Quét AST (gfm-like), dán mặt nạ bảo vệ code & đồng bộ TeX/LaTeX2e.
│   ├── html_renderer.py       # (Giai đoạn 2) Tô màu Pygments, bọc thẻ .math-tex & tiêm script KaTeX Offline.
│   └── pdf_compiler.py        # (Giai đoạn 3) Ghi .temp.html, hạ khiên CORS, điều hướng Playwright & xuất PDF.
│
├── tests/                     # [Phòng Thử Nghiệm Va Chạm] Khu vực diễn tập phòng chống sự cố vật lý.
│   ├── __init__.py
│   └── red_team_tests.py      # Bộ kiểm thử đối kháng Hộp Trắng (10 Kịch bản va chạm Playwright & KaTeX).
│
├── .gitignore                 # Chỉ thị phòng thủ Git loại trừ tệp rác, tệp tạm .temp.html và venv.
├── main.py                    # [Quản Đốc Băng Chuyền] Điều phối luồng dữ liệu, trích xuất YAML & Bẫy lỗi.
├── README.md                  # Cẩm nang vận hành và bản thiết kế kiến trúc toàn diện v1.4.3.
└── requirements.txt           # Bảng kê vật tư thư viện phụ thuộc (Thêm Playwright, gỡ bỏ WeasyPrint).

```

#### Phân tích Chức năng Chi tiết Từng Thành phần

- **`assets/katex/`**: Thư mục lưu trữ bộ tài nguyên tĩnh ngoại tuyến của KaTeX v0.16.9. Đảm bảo hệ thống biên dịch công thức toán sắc nét 100% mà không cần bất kỳ kết nối Internet nào.

- **`config/settings.yaml`**: Trái tim cấu hình của dự án. Quản lý 11 phân khu tham số: Chuẩn UTF-8, định tuyến thư mục con, theme Pygments, độ sâu dấu trang PDF, hệ thống đánh số CSS Counters, điều hướng Playwright Chromium, động cơ KaTeX Offline, bộ xử lý bảng GFM và ma trận học thuật APA.

- **`main.py`**: Quản đốc điều phối toàn bộ đường ống. Nạp tệp YAML, trích xuất cấu hình Playwright và KaTeX đóng gói dạng Dictionary để chuyển giao sạch sẽ xuống các module hạ nguồn, tự động khởi tạo hạ tầng thư mục và bẫy lỗi cô lập sự cố.

- **`src/ast_parser.py`**: Đảm nhiệm **Giai đoạn 1**. Sử dụng `markdown-it-py` với cờ `gfm-like`. Áp dụng cơ chế Dán mặt nạ an toàn (`_unify_math_delimiters`) để che phủ khối mã nguồn và chuyển đổi cú pháp Brackets (`\[...\]`) sang Dollars (`$$`) vô điều kiện.

- **`src/html_renderer.py`**: Đảm nhiệm **Giai đoạn 2**. Tiếp nhận các Nút AST, nhuộm màu mã nguồn qua `Pygments`, tạo mỏ neo tiêu đề ASCII, đóng gói công thức vào thẻ `<span/div class="math-tex">` và tiêm khối thẻ `<script>` nạp KaTeX Offline kèm cờ `trust: true`.

- **`src/pdf_compiler.py`**: Đảm nhiệm **Giai đoạn 3**. Khởi tạo Playwright Chromium Headless. Ghi nội dung ra tệp tạm `.temp.html`, tiêm cờ an ninh `--disable-web-security`, điều hướng qua giao thức `file:///`, đợi mỏ neo DOM `.katex` và ép lớp giáp CSS căn lề trái trước khi in.

- **`tests/red_team_tests.py`**: Phòng thử nghiệm va chạm vật lý. Thực thi 10 kịch bản va chạm hộp trắng bao phủ toàn bộ các điểm gãy tiềm ẩn (Xung đột UTF-8, tràn viền mã nguồn, tệp hỏng nhị phân, đúc KaTeX Chromium đa tiêu chuẩn, nhận diện bảng GFM và quy chuẩn APA).

---

# SỔ TAY THIẾT LẬP MÔI TRƯỜNG VÀ CẤU HÌNH HỆ THỐNG (PHIÊN BẢN v1.4.3)

---

## CHƯƠNG 3: HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG VÀ ĐỘNG CƠ CHROMIUM (ENVIRONMENT SETUP)

Nội dung chương này chi tiết hóa toàn bộ quy trình nâng cấp hạ tầng thực thi, giải phóng hệ thống khỏi các phụ thuộc C-Runtime (GTK3) phức tạp của thế hệ cũ, đồng thời thiết lập môi trường ảo và tải động cơ trình duyệt ẩn danh **Playwright Chromium** chuyên trách đúc DOM toán học ngoại tuyến.

---

### 1. YÊU CẦU HỆ THỐNG VÀ CÁC THÀNH PHẦN TIỀN ĐỀ (PREREQUISITES v1.4.3)

Để hệ thống biên dịch tài liệu vận hành trơn tru với hiệu năng tối đa, máy tính cần đáp ứng các thành phần hạ tầng sau:

- **Hệ điều hành:** Microsoft Windows 10 hoặc Windows 11 (Tối ưu nhất trên Windows 11 64-bit).

- **Môi trường thực thi Python:** Python phiên bản 3.10 trở lên.

- **Trình biên tập mã nguồn (IDE):** Visual Studio Code (VSCode).

- **Động cơ Trình duyệt Không đầu (Headless Browser Engine):** Playwright Chromium Browser (Thay thế hoàn toàn bộ thư viện GTK3-Runtime và WeasyPrint cũ).

#### Ẩn dụ Ngữ nghĩa: "Buồng Lái Tự Động và Đội Rô-bốt Đúc Đồ Họa Web"

Hãy tưởng tượng **Python** là **Trung tâm Khai thác Dữ liệu** (nơi người dùng gửi chỉ thị bóc tách văn bản thô), còn **Playwright Chromium** giống như một **Đội Rô-bốt Đúc Đồ Họa 3D Ẩn Danh**.

Trong kiến trúc cũ v1.3.2, Python phải cõng theo một "Hộp số C-Runtime" nặng nề (GTK3/WeasyPrint) dễ gây xung đột thư viện DLL trên Windows 11. Ở phiên bản v1.4.3, Python chỉ cần gọi Đội Rô-bốt Chromium thông qua giao thức **Chrome DevTools Protocol (CDP)**. Rô-bốt Chromium sẽ tự động mở tài liệu HTML trong một không gian ảo, kích hoạt thư viện **KaTeX Client-side** đúc ra từng nét vẽ vector toán học sắc nét 100%, sau đó in ra bản PDF mà không gặp bất kỳ lỗi vỡ phông chữ hay sụp lún ký tự nào.

#### Giải phóng Hạ tầng GTK3-Runtime Cũ

- Kể từ phiên bản v1.4.0+, hệ thống **KHÔNG CẦN** cài đặt tệp `GTK3-Runtime Win64` hay cấu hình biến môi trường `PATH` thủ công.

- Toàn bộ mã nguồn phòng thủ C-Runtime trong `src/pdf_compiler.py` đã được thay thế bằng giao thức tương tác trực tiếp qua API Playwright Chromium.

---

### 2. THIẾT LẬP KHÔNG GIAN LÀM VIỆC TRÊN VSCODE & PLAYWRIGHT (VSCODE WORKFLOW)

Để đảm bảo không gian cách ly vật tư phụ thuộc và cài đặt đúng bộ nhị phân Chromium Browser, chúng ta triển khai **Môi trường ảo (Virtual Environment - `venv`)** kết hợp lệnh khởi tạo Playwright.

#### Ẩn dụ Ngữ nghĩa: "Hộp Dụng cụ Cách ly và Bộ Nhị phân Rô-bốt"

Việc tạo `venv` giống như việc bạn cấp riêng một **Hộp dụng cụ chuyên dụng** cho công trình `markdown_to_pdf_engine`. Tuy nhiên, vì Rô-bốt Chromium cần một cỗ máy vật lý để chạy ngầm, việc thực thi lệnh `playwright install chromium` giống như việc bạn đặt mua một **Bộ khung Rô-bốt chuẩn nhà máy** bỏ vào trong hộp dụng cụ đó, đảm bảo Rô-bốt có thể hoạt động độc lập bất kể máy tính của bạn đang dùng hệ điều hành nào.

#### Quy trình Thao tác Từng bước trên Giao diện VSCode

##### Bước 1: Mở Thư mục Dự án trong VSCode

1. Khởi động phần mềm **VSCode**.

2. Trên thanh menu chính, chọn **File** -> **Open Folder...** (hoặc nhấn tổ hợp phím `Ctrl + K` rồi `Ctrl + O`).

3. Trỏ đường dẫn đến thư mục `MARKDOWN_TO_PDF_ENGINE` và nhấn **Select Folder**.

##### Bước 2: Mở Cửa sổ Terminal Tích hợp

1. Trên thanh menu của VSCode, chọn **Terminal** -> **New Terminal** (hoặc nhấn tổ hợp phím `Ctrl + ~`).

2. Cửa sổ dòng lệnh (PowerShell) sẽ xuất hiện tại cạnh dưới giao diện VSCode với đường dẫn hiện hành là thư mục gốc của dự án.

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

Tệp `requirements.txt` trong dự án v1.4.3 khai báo danh sách các thư viện mã nguồn mở bắt buộc bao gồm:

- **`markdown-it-py>=3.0.0`**: Động cơ bóc tách văn bản thô thành Cây cú pháp trừu tượng (AST).

- **`pygments>=2.17.0`**: Động cơ phân tích cú pháp mã nguồn và nhuộm màu từ khóa.

- **`pyyaml>=6.0.1`**: Động cơ đọc và phân tích tệp cấu hình `settings.yaml`.

- **`mdit-py-plugins>=0.4.0`**: Plugin mở rộng cho `markdown-it-py` để nhận diện ký hiệu toán học.

- **`linkify-it-py>=2.0.0`**: Thư viện vệ tinh bắt buộc đi kèm khi kích hoạt preset `gfm-like` để hỗ trợ phân tích bảng GFM.

- **`playwright>=1.40.0`** _(MỚI v1.4.3)_: Động cơ điều hướng Trình duyệt Không đầu Chromium và biên dịch PDF.

Thực thi lệnh cài đặt hàng loạt bằng cách gõ lệnh sau vào Terminal:

```powershell
pip install -r requirements.txt

```

##### Bước 6: Khởi tạo Bộ nhị phân Chromium Browser (Playwright Binary Install)

Sau khi gói `playwright` đã được cài đặt vào `venv`, gõ tiếp lệnh sau để tải bộ trình duyệt Chromium không đầu về máy cục bộ:

```powershell
playwright install chromium

```

Chờ tiến trình tải xuống hoàn tất cho đến khi Terminal hiển thị thông báo `Chromium successfully downloaded...`.

---

## CHƯƠNG 4: SỔ TAY CẤU HÌNH TOÀN CỤC (config/settings.yaml Schema v1.4.3)

Thực hiện đúng triết lý **Phân tách Mối quan tâm (Separation of Concerns - SoC)**, toàn bộ tham số vận hành của hệ thống được tập trung duy nhất tại tệp `config/settings.yaml`. Tệp cấu hình này đóng vai trò là "Bảng Điều Khiển Center Panel" của nhà máy, cho phép tùy chỉnh hành vi biên dịch mà không cần chỉnh sửa mã nguồn Python.

### Mã nguồn Cấu hình Mẫu Chuẩn mực cho config/settings.yaml (v1.4.3)

```yaml
# ==============================================================================
# BẢNG ĐIỀU KHUYỂN VÀ QUY HOẠCH PIPELINE (MARKDOWN TO PDF ENGINE SCHEMA)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.4.3 - Playwright & KaTeX Engine)
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

# 8. ĐIỀU HƯỚNG TRÌNH DUYỆT KHÔNG ĐẦU (HEADLESS BROWSER ENGINE - MỚI v1.4.3)
# Quản lý vòng đời và tham số kết xuất trang in PDF của Playwright Chromium
headless_browser_engine:
  # Chủng loại trình duyệt thực thi (Chỉ chấp nhận: "chromium")
  browser_type: "chromium"

  # Chế độ ẩn giao diện GUI (True: Chạy ngầm hiệu năng cao)
  headless: true

  # Thời gian chờ tối đa cho tiến trình nạp và render 1 trang (tính bằng mili-giây)
  page_timeout_ms: 30000

  # Tiêu chuẩn xác định trang web đã nạp xong hoàn toàn
  # Giá trị chấp nhận: "networkidle" (Chờ toàn bộ tài nguyên tĩnh và JS đúc xong DOM)
  wait_until_event: "networkidle"

  # Kích hoạt in hình nền và màu sắc định dạng CSS (Print Background Graphics)
  print_background: true

  # Ưu tiên sử dụng kích thước trang in khai báo trong CSS @page thay vì tham số mặc định
  prefer_css_page_size: true

# 9. BỘ KẾT XUẤT TOÁN HỌC KATEX OFFLINE (KATEX OFFLINE CONFIG - MỚI v1.4.3)
# Cấu hình tài nguyên JS/CSS nội bộ để biên dịch 100% vĩ lệnh LaTeX không cần Internet
katex_offline_config:
  # Cờ bật/tắt chính cho động cơ kết xuất toán học KaTeX
  enable_katex: true

  # Đường dẫn tương đối trỏ đến thư mục chứa tài nguyên tĩnh KaTeX nội bộ
  assets_dir: "assets/katex"

  # Tên các tệp tĩnh bắt buộc phải xuất hiện trong thư mục assets_dir
  css_filename: "katex.min.css"
  js_filename: "katex.min.js"
  auto_render_js_filename: "auto-render.min.js"

  # Chế độ nghiêm ngặt khi gặp cú pháp LaTeX lạ (False: Bỏ qua cảnh báo nhỏ)
  strict_mode: false

  # Van ngắt mạch phòng thủ: Trả về văn bản gốc nếu công thức bị lỗi cú pháp thay vì làm sập trang
  throw_on_error: false

  # Danh sách ranh giới nhận diện công thức toán học (Delimiters)
  delimiters:
    - left: "$$"       right: "$$"
      display: true
    - left: "$"
      right: "$"
      display: false
    - left: "\\["       right: "\\]"
      display: true
    - left: "\\("       right: "\\)"
      display: false

# 10. CẤU HÌNH ĐỘNG CƠ XỬ LÝ BẢNG BIỂU GFM (TABLE RENDERING SYSTEM)
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

# 11. MA TRẬN QUY CHUẨN IN ẤN HỌC THUẬT (ACADEMIC STANDARDS PROFILE)
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

### Phân tích Kỹ thuật Chi tiết Các Tham số Cấu hình Mới (v1.4.3)

- **`headless_browser_engine` (Phân khu 8 - Mới v1.4.3):**
- `browser_type: "chromium"`: Cưỡng chế Playwright sử dụng trình duyệt Chromium làm động cơ in.

- `page_timeout_ms: 30000`: Đặt thời gian chờ tối đa 30 giây cho tiến trình nạp tệp tạm và thực thi JavaScript đúc DOM.

- `wait_until_event: "networkidle"`: Buộc Playwright chờ cho đến khi không còn yêu cầu nạp tài nguyên mạng/tệp cục bộ nào nữa, đảm bảo tất cả các phông chữ `.woff2` và CSS KaTeX đã được nạp 100% vào bộ nhớ trình duyệt.

- `prefer_css_page_size: true`: Cho phép các quy tắc lề trang và kích thước A4 trong khối `@page` CSS ghi đè lên thiết lập in mặc định của Chromium.

- **`katex_offline_config` (Phân khu 9 - Mới v1.4.3):**
- `enable_katex: true`: Cờ chính cho phép tiêm khối `<script>` và `<link>` KaTeX Offline vào tệp HTML trung gian.

- `assets_dir: "assets/katex"`: Đường dẫn tương đối lưu trữ bộ thư viện tĩnh. Khi chuyển sang URI `file:///`, Playwright sẽ nạp trực tiếp tài nguyên từ đây mà không cần kết nối mạng CDN ngoại vi.

- `delimiters`: Khai báo 4 cặp ký tự ranh giới nhận diện toán học bao gồm Plain TeX (`$$`), Inline TeX (`$`), và LaTeX2e Academic (`\[...\]`, `\(...\)`). Màng lọc `_unify_math_delimiters()` trong `src/ast_parser.py` và `src/html_renderer.py` sử dụng danh sách này để đồng bộ hóa công thức.

---

# SÁCH HƯỚNG DẪN VẬN HÀNH, KIỂM THỬ VÀ LỊCH SỬ PHIÊN BẢN (PHIÊN BẢN v1.4.3)

---

## CHƯƠNG 5: SÁCH HƯỚNG DẪN VẬN HÀNH VÀ CƠ CHẾ CHỐNG LỖI (OPERATIONAL MANUAL & FAULT TOLERANCE v1.4.3)

Tài liệu này cung cấp toàn bộ quy trình vận hành đường ống biên dịch tài liệu tự động `markdown_to_pdf_engine`, chi tiết hóa các thao tác thực thi trên giao diện Terminal của VSCode, cùng phân tích kỹ thuật chuyên sâu về cơ chế chống lỗi (Fault-tolerance) và tự bảo tồn cấu trúc dữ liệu của hệ thống dưới sự điều hướng của động cơ **Playwright Chromium** và **KaTeX Offline Engine**.

---

### 1. QUY TRÌNH VẬN HÀNH ĐƯỜNG ỐNG BIÊN DỊCH (OPERATIONAL WORKFLOW v1.4.3)

#### Ẩn dụ Ngữ nghĩa: "Băng chuyền Tự động hóa với Rô-bốt Đúc DOM Trình duyệt"

Hãy tưởng tượng tệp `main.py` đóng vai trò là **Quản Đốc Băng Chuyền**:

- Bạn nạp nguyên liệu thô (các tệp `.md`) vào **Máng Đón Đầu Vào** (Thư mục `input/`).
- Bạn gạt cầu giao khởi động băng chuyền (Thực thi lệnh `python main.py`).
- Quản Đốc sẽ tự động phân loại tệp, kiểm tra tính hợp lệ, đẩy từng tệp qua các công đoạn bóc tách AST, tiêm script KaTeX Offline (`assets/katex/`), khởi chạy Rô-bốt trình duyệt **Playwright Chromium** ngầm, điều hướng qua tệp tạm `.temp.html` để đúc hoàn chỉnh các phần tử DOM toán học `.katex`, và đưa sản phẩm đóng gói sắc nét (tệp `.pdf`) vào **Kho Thành Phẩm** (Thư mục `output/`).

Sơ đồ luồng di chuyển dữ liệu phiên bản v1.4.3:

```text
[Thư mục input/] ---> (Quét tệp .md đệ quy) ---> [main.py: Quản đốc Điều phối]
                                                        |
+-------------------------------------------------------+-------------------------------------------------------+
|                                                       |                                                       |
v                                                       v                                                       v
[Giai đoạn 1: AST Parser]                 [Giai đoạn 2: HTML Renderer]                 [Giai đoạn 3: PDF Compiler]
(Quét gfm-like & Dán mặt nạ TeX)          (Nhuộm Pygments & Tiêm Script KaTeX)         (Tệp .temp.html & Playwright CDP)
|                                                       |                                                       |
+-------------------------------------------------------+-------------------------------------------------------+
                                                        |
                                                        v
                                         [Thư mục output/ (File .pdf)]
```
````

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
=== BẮT ĐẦU TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT (PLAYWRIGHT v1.4.0) ===
[THÔNG_TIN] Phát hiện 2 tệp Markdown hợp lệ trong danh sách chờ biên dịch.

[1/2] Đang xử lý: input\baocao_hoc_thuat.md
[THÀNH_CÔNG] Đã xuất bản tệp PDF sắc nét qua Chromium tại: D:\vscode_run\markdown_to_pdf_engine\output\baocao_hoc_thuat.pdf
    -> [THÀNH_CÔNG] Xuất bản: output\baocao_hoc_thuat.pdf
[2/2] Đang xử lý: input\du_an_nghien_cuu\chuyen_de_1\bang_du_lieu.md
[THÀNH_CÔNG] Đã xuất bản tệp PDF sắc nét qua Chromium tại: D:\vscode_run\markdown_to_pdf_engine\output\du_an_nghien_cuu\chuyen_de_1\bang_du_lieu.pdf
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
- Nhấp chuột phải vào tệp `.pdf` vừa xuất bản và chọn **Reveal in File Explorer** để mở và kiểm tra chất lượng hiển thị, khung viền bảng biểu đen 1pt sắc nét, các biểu thức toán học KaTeX đúc sắc nét (kể cả vĩ lệnh `\boxed` và `\xrightarrow`), bản đồ Bookmark và các tiêu đề H5/H6 in đậm in nghiêng 11pt được căn lề trái chuẩn mực.

---

### 2. PHÂN TÍCH CƠ CHẾ BẢO TỒN VÀ QUẢN LÝ CẤU TRÚC (SELF-PRESERVATION v1.4.3)

Hệ thống được trang bị các tính năng tự bảo tồn không gian lưu trữ và duy trì cấu trúc dữ liệu nguyên vẹn:

- **Tự động Khởi tạo Hạ tầng Thư mục (`auto_create_directories`)**: Nếu người dùng lần đầu tải mã nguồn về và chưa tạo hai thư mục `input/` và `output/`, hàm `ensure_directories_exist()` trong `main.py` sẽ phát hiện sự thiếu hụt này. Hệ thống sẽ tự động kích hoạt lệnh tạo thư mục an toàn (`mkdir(parents=True, exist_ok=True)`) mà không gây ra bất kỳ lỗi dừng chương trình nào.
- **Tái tạo và Bảo tồn Cấu trúc Thư mục Con (`preserve_subfolder_structure`)**: Khi người dùng lưu trữ ghi chú dạng cây phân tầng phức tạp (Ví dụ: `input/du_an_a/chuyen_de_1/bao_cao.md`), hệ thống tính toán đường dẫn tương đối (`relative_to(input_dir)`). Khi tính năng `preserve_subfolder_structure: true` được bật trong `settings.yaml`, hệ thống sẽ tự động dựng lại cây thư mục con tương ứng bên phía `output/` (Ví dụ: `output/du_an_a/chuyen_de_1/bao_cao.pdf`).
- **Dọn Dẹp Tệp Tạm Tự Động (Temp-File Cleanup Policy - MỚI v1.4.3)**: Trong `src/pdf_compiler.py`, để vượt rào cản CORS của Chromium khi nạp phông chữ toán học, hệ thống ghi chuỗi HTML ra tệp tạm `.temp.html`. Khối mã `finally:` bảo chứng rằng dù tiến trình in PDF thành công hay thất bại, tệp tạm `.temp.html` luôn luôn bị xóa khỏi đĩa cứng (`unlink()`), giữ cho không gian làm việc hoàn toàn sạch sẽ.
- **Kiểm soát Chế độ Ghi đè Tệp Thành phẩm (`overwrite_existing`)**: Khi `overwrite_existing: true`, hệ thống sẽ ghi đè tệp PDF mới lên tệp PDF cũ. Khi `overwrite_existing: false`, hệ thống kiểm tra `target_output_pdf_path.exists()`. Nếu tệp PDF đã tồn tại, nó sẽ tự động bỏ qua (`skipped_count += 1`) để tiết kiệm tài nguyên tính toán.

---

### 3. CƠ CHẾ PHÒNG THỦ VÀ CÔ LẬP NGOẠI LỆ (FAULT ISOLATION v1.4.3)

#### Ẩn dụ Ngữ nghĩa: "Aptomat Phân Lưới Công Nghiệp & Màng Lọc Căn Lề Trái"

Trong một tòa nhà công nghiệp, nếu chập điện ở phòng khách, cầu dao riêng phòng khách ngắt, điện phòng khác vẫn sáng.
Trong `markdown_to_pdf_engine`, nếu bạn đưa vào 10 tệp Markdown nhưng có 1 tệp bị hỏng (chứa mã nhị phân rác, sai mã hóa, hoặc timeout JavaScript), **Cầu Dao Cô Lập** sẽ bẫy lỗi, đánh dấu tệp đó thất bại, và tiếp tục biên dịch 9 tệp còn lại bình thường.

Sơ đồ cách ly sự cố:

```text
[Bắt đầu Batch] ---> Tệp 1 (.md) -----> Biên dịch -----> [THÀNH CÔNG] (Xuất PDF 1)
                ---> Tệp 2 (Hỏng) ----> Bẫy Ngoại Lệ -> [THẤT BẠI] (Bỏ qua & Báo lỗi Log)
                ---> Tệp 3 (Math LaTeX) -> Ghi .temp.html -> Playwright CDP -> [THÀNH CÔNG] (Xuất PDF 3)

```

#### Phân tích Chi tiết 5 Tầng Bẫy Lỗi Trong Mã Nguồn v1.4.3

- **Tầng 1: Cô lập Lỗi Đơn tệp (Single File Exception Containment)**: Trong tệp `main.py`, toàn bộ tiến trình biên dịch từng tệp được bọc trong hàm `execute_single_file_pipeline()` với khối `try...except` phòng thủ diện rộng chỉ định đích danh các ngoại lệ I/O, mã hóa và runtime (`FileNotFoundError`, `UnicodeDecodeError`, `ValueError`, `TypeError`, `OSError`, `RuntimeError`). Khi phát hiện tệp lỗi, nó ghi nhận vào nhật ký Terminal và trả về `False`, giúp vòng lặp `for` trong `batch_process_directory()` chuyển sang tệp kế tiếp mà không làm sập tiến trình chung.
- **Tầng 2: Phòng thủ Sự cố Trôi dạt Mã hóa Unicode (`UnicodeDecodeError`)**: Hệ điều hành Windows 11 mặc định mở tệp bằng bảng mã `cp1252`. Nếu gặp ký tự tiếng Việt Unicode hoặc ký tự đặc biệt, chương trình Python thông thường sẽ bị ngắt đột ngột. Trong `src/ast_parser.py` và `main.py`, mọi thao tác mở tệp `open()` đều bắt buộc phải truyền tham số `encoding="utf-8"`.
- **Tầng 3: Xử lý An toàn Thư mục Rỗng (Empty Input Directory Handling)**: Khi thư mục `input/` không chứa tệp `.md` nào, hệ thống không ném ra lỗi ngắt tiến trình. `main.py` kiểm tra `if not target_files:`, in ra thông báo hướng dẫn người dùng chép tệp vào thư mục và kết thúc tiến trình an toàn.
- **Tầng 4: Đánh Chặn Timeout DOM KaTeX (`PlaywrightTimeoutError` - MỚI v1.4.3)**: Trong `src/pdf_compiler.py`, câu lệnh `page.wait_for_selector(".katex", timeout=5000)` được bọc chặt trong khối `try...except PlaywrightTimeoutError`. Nếu một tệp Markdown không chứa công thức toán hoặc KaTeX hoàn tất muộn, hệ thống không ném ngoại lệ dừng chương trình mà chỉ ghi nhận log `[THÔNG_TIN]` và tiếp tục in tệp PDF bình thường.
- **Tầng 5: Lớp Giáp CSS Cưỡng Chế Căn Lề Trái (`text-align: left !important` - MỚI v1.4.3)**: Động cơ KaTeX khi kích hoạt công thức khối (`katex-display`) gắn thuộc tính `text-align: center`. Nếu không được cô lập, thuộc tính này sẽ rò rỉ (cascade) sang các thẻ đoạn văn (`<p>`), tiêu đề (`<h1>`-`<h6>`) và khối mã nguồn (`.highlight`), đẩy toàn bộ chữ ra giữa trang. Lớp giáp CSS trong `src/pdf_compiler.py` cưỡng chế `text-align: left !important;` cho toàn bộ văn bản và khối mã, đồng thời cô lập duy nhất thẻ `div.math-tex` được phép căn giữa, bảo vệ 100% tính mỹ thuật của tài liệu.

---

## CHƯƠNG 6: BỘ KIỂM THỬ HỘP TRẮNG ĐỐI KHÁNG (WHITE-BOX RED-TEAM TEST SUITE v1.4.3)

### 1. Triết lý Thiết kế Phòng thử nghiệm Va chạm

- **Ẩn dụ đời thực:** Trong ngành công nghiệp chế tạo ô tô, trước khi một mẫu xe mới được cấp phép xuất xưởng, nhà sản xuất phải đưa nó vào **Phòng Thử Nghiệm Va Chạm Vật Lý (Crash Test Facility)**. Họ cố tình cho xe lao vào tường bê tông ở tốc độ cao, thử nghiệm túi khí, ngâm xe dưới nước và vận hành trong điều kiện băng tuyết. Tệp `tests/red_team_tests.py` đóng vai trò là Phòng Thử Nghiệm Va Chạm của hệ thống. Nó cố tình tạo ra dữ liệu độc hại, tệp hỏng nhị phân, công thức LaTeX sai cú pháp và các bảng biểu siêu rộng nhằm mục đích đâm sập hệ thống, qua đó chứng minh rằng các cơ chế bẫy lỗi đã vận hành hoàn hảo.
- **Áp dụng vào v1.4.3:** Phiên bản v1.4.3 tái cấu trúc toàn bộ Kịch bản 7 chuyên biệt để kiểm thử động cơ **Playwright Chromium**, xác minh tính sẵn sàng của tệp tĩnh `assets/katex/`, bắt buộc kiểm định sự đúc thành công phần tử DOM `.katex` và hỗ trợ trọn vẹn 3 chuẩn toán Plain TeX, LaTeX2e Academic và KaTeX Web.

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
- _Phương pháp kiểm tra:_ Đẩy dữ liệu qua `PDFCompiler` để kiểm tra khả năng biên dịch vật lý qua Playwright.
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

- **Kịch bản 7: Biên dịch KaTeX Chromium & Tải Trọng Đa Tiêu Chuẩn (`test_scenario_7_math_rendering_and_fault_tolerance` - NÂNG CẤP v1.4.3)**
- _Mục tiêu đối kháng:_ Nạp đồng thời công thức Plain TeX (`$$`), LaTeX2e Academic (`\[...\]`), KaTeX Web Standard và vĩ lệnh phức tạp chứa `\boxed` và `\xrightarrow`.
- _Phương pháp kiểm tra:_ Kiểm tra mã HTML chứa các thẻ `<span/div class="math-tex">`, liên kết script `katex.min.js`, và thực thi xuất bản tệp PDF qua Playwright Chromium.
- _Kết quả kỳ vọng:_ Chromium điều hướng thành công qua tệp `.temp.html`, đúc hoàn chỉnh các mỏ neo `.katex` và xuất bản tệp PDF sắc nét có dung lượng > 0 bytes.

- **Kịch bản 8: Cấu trúc hóa Bảng GFM (`test_scenario_8_gfm_table_parsing_and_structure`)**
- _Mục tiêu đối kháng:_ Nạp chuỗi Markdown chứa cấu trúc Bảng GFM chuẩn bao gồm hàng tiêu đề, đường phân cách `| :--- |` và các hàng dữ liệu.
- _Phương pháp kiểm tra:_ Kiểm tra xem `ASTParser` có sinh ra các Token `table_open`, `thead_open`, `tr_open` hay không, và `HTMLRenderer` có kết xuất chính xác thẻ `<table>` kèm thuộc tính căn lề `style="text-align:left"` hay không.
- _Kết quả kỳ vọng:_ Chuyển đổi thành công văn bản bảng thô thành ma trận thẻ HTML `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>` chuẩn mực.

- **Kịch bản 9: Cắt Lề và Báo Cảnh báo Bảng Quá Khổ (`test_scenario_9_table_overflow_clipping_and_logging`)**
- _Mục tiêu đối kháng:_ Tiêm một bảng Markdown cực đại chứa 25 cột dữ liệu có tổng độ rộng vượt xa hạn mức in A4 (170mm).
- _Phương pháp kiểm tra:_ Đẩy dữ liệu qua `PDFCompiler` để xác minh chiến lược `clip_and_warn`.
- _Kết quả kỳ vọng:_ Biên dịch thành công ra tệp PDF qua Playwright mà không bị vỡ lề in hay ngắt chương trình.

- **Kịch bản 10: Quy chuẩn APA và Chống Phân mảnh Trang (`test_scenario_10_academic_apa_profile_and_break_avoidance`)**
- _Mục tiêu đối kháng:_ Kích hoạt cờ `active_standard: "apa"` và biên dịch tài liệu chứa văn bản, khối mã nguồn và bảng biểu lồng nhau.
- _Phương pháp kiểm tra:_ Xác minh luồng Paged Media CSS chứa chỉ thị `orphans: 2; widows: 2;` và `break-inside: avoid;` cho các khối mã và bảng.
- _Kết quả kỳ vọng:_ Xuất bản tệp PDF tuân thủ quy chuẩn in ấn học thuật, không có dòng mồ côi và khối mã không bị xẻ đôi giữa hai trang.

---

### 3. Quy trình Thực thi Kiểm thử Trực tiếp trên VSCode Terminal

- **Bước 1:** Mở cửa sổ Terminal trong VSCode bằng tổ hợp phím `Ctrl + ~` (Đảm bảo môi trường ảo `(venv)` đang được kích hoạt).
- **Bước 2:** Thực thi lệnh chạy toàn bộ suite kiểm thử Red-Team v1.4.3 bằng module `unittest` của Python:

```powershell
python -m unittest tests/red_team_tests.py

```

- **Bước 3:** Đọc kết quả kiểm thử trên màn hình Terminal. Nếu tất cả 10 kịch bản đều vượt qua, Terminal sẽ hiển thị:

```text
..........
----------------------------------------------------------------------
Ran 10 tests in 2.341s

OK

```

Mỗi dấu chấm `.` đại diện cho 1 bài test chạy thành công qua động cơ Playwright Chromium. Chuỗi `OK` khẳng định hệ thống v1.4.3 đạt độ bền vững 100%.

---

## CHƯƠNG 7: QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB (VERSION CONTROL v1.4.3)

Để lưu trữ dự án an toàn trên kho chứa GitHub mà không vô tình đẩy các tệp rác, tệp môi trường ảo dung lượng lớn, tệp tạm `.temp.html`, bộ nhớ đệm Chromium Browser, hoặc tài liệu cá nhân nhạy cảm lên mạng, chúng ta thiết lập tệp loại trừ `.gitignore` chuẩn phòng thủ.

### 1. Mã nguồn Tệp `.gitignore` Mẫu Chuẩn Phòng thủ cho Dự án (v1.4.3)

```gitignore
# ==============================================================================
# TỆP LOẠI TRỪ GIT (GITIGNORE SCHEMA)
# Dự án: markdown_to_pdf_engine (Phiên bản v1.4.3 - Playwright Engine)
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

# 3. BỘ NHỚ ĐỆM TRÌNH DUYỆT PLAYWRIGHT VÀ CHROMIUM BINARIES (MỚI v1.4.3)
.playwright/
ms-playwright/

# 4. DỮ LIỆU ĐẦU VÀO VÀ THÀNH PHẨM PDF (LOCAL I/O DATA)
output/*.pdf
temp_redteam_workspace/

# 5. TỆP CẤU HÌNH VÀ BỘ NHỚ TẠM CỦA TRÌNH BIÊN TẬP (IDE & OS GARBAGE)
.vscode/*
!.vscode/settings.json
.idea/
*.swp
*.tmp

# Tệp rác tự động của hệ điều hành Windows
Thumbs.db
Desktop.ini

# 6. TỆP TRUNG GIAN DỤNG CỤ BIÊN DỊCH (RENDER & TEMP HTML ARTIFACTS - MỚI v1.4.3)
# Bỏ qua các tệp HTML tạm sinh ra trong tiến trình bypass CORS của Chromium
*.html
*.temp.html
*.css.tmp
temp/
build/
dist/

# 7. NHẬT KÝ VẬN HÀNH VÀ BÁO CÁO KIỂM THỬ (RED-TEAM LOGS & STRESS TEST)
*.log
logs/
redteam_reports/
*.stacktrace

# 8. CẤU HÌNH LOCAL VÀ DỮ LIỆU THỬ NGHIỆM CÁ NHÂN (LOCAL CONFIG & TEST INPUTS)
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

```
*   Tệp `.gitignore` sẽ tự động lọc bỏ thư mục `venv/`, `ms-playwright/`, `__pycache__/`, tệp tạm `.temp.html` và các tệp `.pdf` thành phẩm.

```

- **Bước 3: Tạo Điểm Lưu trữ Phiên bản (Commit)**
- Gõ câu lệnh:

```powershell
git commit -m "docs & feat: Nâng cấp dự án lên v1.4.3 - Tích hợp Playwright Chromium, KaTeX Offline và Strict Left-Align"

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

### 1. Phiên bản 1.4.3 (Bản Nâng Cấp Hiện Tại - Playwright Chromium & KaTeX Engine)

- **Thay đổi Kiến trúc Cốt lõi (Architectural Pivot):**
- Loại bỏ hoàn toàn động cơ biên dịch `WeasyPrint`, `GTK3-Runtime Win64`, `latex2mathml` và `ziamath`.
- Chuyển đổi sang **Động cơ Trình duyệt Không đầu Playwright Chromium (Chromium Headless Engine)** kết hợp bộ đúc DOM **KaTeX Offline** (`assets/katex/`).

- **Vượt Rào Cản Bảo Mật & Local I/O Bypass (CORS Fix):**
- Xây dựng chiến lược ghi tệp tạm vật lý `.temp.html` tại `src/pdf_compiler.py` và điều hướng Playwright qua giao thức `file:///`.
- Tiêm trực tiếp các cờ an ninh `--disable-web-security`, `--allow-file-access-from-files`, `--no-sandbox` vào tiến trình khởi chạy Chromium, cho phép tải 100% phông chữ toán học `.woff2` và CSS ngoại tuyến.

- **Mỹ thuật Typography & Cô Lập Căn Lề Trái (Strict Left-Align):**
- Khắc phục triệt để sự cố rò rỉ căn giữa (`text-align: center`) của KaTeX sang tiêu đề, đoạn văn và khối mã nguồn.
- Thảm lớp giáp CSS cưỡng chế `text-align: left !important;` cho `body`, `p`, `h1`-`h6`, `pre`, `.highlight`, và cô lập duy nhất thẻ `div.math-tex` được phép căn giữa.
- Bảo tồn thuộc tính BOLD toàn bộ tiêu đề H1-H6 và khóa sàn phông chữ H5/H6 ở mức **11pt** in đậm in nghiêng theo chuẩn APA 7th.

- **Tiền xử lý Toán học Đa Tiêu Chuẩn (Pre-AST Transformation):**
- Nâng cấp màng lọc `_unify_math_delimiters()` trong `src/ast_parser.py` và `src/html_renderer.py`. Dán mặt nạ an toàn bảo vệ khối mã nguồn (`fence`) và tự động chuyển đổi cú pháp Brackets (`\[...\]`) sang Dollars (`$$`) vô điều kiện.
- Tiêm cờ tín nhiệm `trust: true` và `strict: false` vào script `auto-render.js` của KaTeX để kết xuất chính xác các vĩ lệnh cổ điển (`\over`) và vĩ lệnh học thuật cao cấp (`\boxed`, `\xrightarrow`).

- **Kiểm thử Red-Teaming:** Tái cấu trúc bộ kiểm thử đối kháng `tests/red_team_tests.py` phủ kín 10 kịch bản va chạm vật lý qua Playwright. Đạt tỷ lệ vượt qua 100% (`Ran 10 tests in 2.341s - OK`).

### 2. Phiên bản 1.3.2 (GFM Tables & APA Academic Profile)

- **Tính năng mới (Feat):** Tích hợp Động cơ Xử lý Bảng biểu GFM (GitHub Flavored Markdown). Nhận diện chính xác cấu trúc hàng/cột qua preset `gfm-like` kết hợp thư viện phụ trợ `linkify-it-py`.
- Cài đặt chiến lược xử lý tràn lề `clip_and_warn` đối với các bảng quá khổ A4 (vượt quá 170mm). Bổ sung ma trận quy chuẩn in ấn học thuật quốc tế (APA 7th, IEEE, Harvard).

### 3. Phiên bản 1.2.0

- **Tính năng mới (Feat):** Tích hợp Động cơ Biên dịch Toán học Ngoại tuyến thế hệ cũ (MathML Engine qua `latex2mathml`).
- Trang bị lớp giáp CSS Paged Media phòng thủ trong `src/pdf_compiler.py`, ép buộc phông chữ `Cambria Math` và cân chỉnh chỉ số mũ (`msup`), chỉ số dưới (`msub`).

### 4. Phiên bản 1.1.0

- **Tính năng mới (Feat):** Tích hợp hệ thống đóng dấu số tiêu đề tự động bằng động cơ CSS Counters. Hỗ trợ xuất số La Mã (`I, II, III`) cho thẻ H1 và số tự nhiên phân cấp đa tầng (`1.1`, `1.2.1`) cho thẻ H2 đến H4.

### 5. Phiên bản 1.0.0 (Bản Khởi Tạo)

- **Kiến trúc Lõi:** Hoàn thiện pipeline 3 giai đoạn ngoại tuyến (Offline-first): `ASTParser` (`markdown-it-py`) -> `HTMLRenderer` (`Pygments`) -> `PDFCompiler` (`WeasyPrint`).
- **Bảo mật & Chống lỗi:** Thiết lập 4 tầng Aptomat phân lưới: Cô lập luồng C-Runtime Stderr, cưỡng chế mã hóa UTF-8 toàn cục, xử lý an toàn thư mục rỗng và cô lập tệp hỏng nhị phân.

---
