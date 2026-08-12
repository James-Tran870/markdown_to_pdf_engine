# ==============================================================================
# TỆP: main.py (BỘ ĐIỀU PHỐI PIPELINE, HYBRID DTO & UNPACKING v2.3.0)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Single Source of Truth (SSOT), ExecutionContext & Hybrid Math DTO
# ==============================================================================

import sys
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from src.html_renderer import HTMLRenderer
from src.pdf_compiler import PDFCompiler
from src.pdf_metadata_injector import MetadataInjector

# ==============================================================================
# 1. ĐỊNH NGHĨA CÁC MÔ HÌNH DTO (DATA TRANSFER OBJECTS) QUA PYDANTIC V2
# ==============================================================================

class DirectoryRoutingConfig(BaseModel):
    """Lược đồ cấu hình điều hướng thư mục và xử lý hàng loạt."""
    input_directory: str = "input"
    output_directory: str = "output"
    recursive_search: bool = True
    allowed_extensions: list[str] = [".md", ".markdown", ".mdown"]
    overwrite_existing: bool = True
    auto_create_directories: bool = True
    preserve_subfolder_structure: bool = True


class HeadingRetentionDepthConfig(BaseModel):
    """Lược đồ cấu hình độ sâu dấu trang tiêu đề với rào chắn cứng mở rộng cấp 6."""
    max_bookmark_level: int = Field(default=6, ge=1, le=6)
    enable_heading_anchors: bool = True
    normalize_anchor_ascii: bool = True

    @field_validator("max_bookmark_level")
    @classmethod
    def validate_max_bookmark_level(cls, value: int) -> int:
        """Quy tắc chặn đứng: Cấm cấu hình max_bookmark_level vượt quá cấp 6."""
        if value > 6:
            raise ValueError(
                f"[VI_PHẠM_LƯỢC_ĐỒ] Tham số 'max_bookmark_level' ({value}) vượt quá "
                "giới hạn vật lý tối đa cho phép (Mức 6). Tiến trình bị hủy bỏ."
            )
        if value < 1:
            raise ValueError(
                f"[VI_PHẠM_LƯỢC_ĐỒ] Tham số 'max_bookmark_level' ({value}) nhỏ hơn "
                "ngưỡng tối thiểu cho phép (Mức 1)."
            )
        return value


class DocumentLayoutConfig(BaseModel):
    """Lược đồ cấu hình trang in vật lý."""
    page_size: str = "A4"
    margin: str = "20mm"
    code_overflow_handling: str = "break-word"


class TypographyConfiguration(BaseModel):
    """Lược đồ cấu hình mỹ thuật phông chữ."""
    font_family: str = '"Segoe UI", "Arial", "Calibri", "Tahoma", sans-serif'
    code_font_family: str = '"Consolas", "Courier New", monospace'
    base_font_size: str = "11pt"
    line_height: str = "1.6"
    text_color: str = "#1a1a1a"


class HeadingNumberingSystemConfig(BaseModel):
    """Lược đồ cấu hình hệ thống đánh số tiêu đề tự động."""
    enable_auto_numbering: bool = True
    h1_numbering_style: str = "roman"
    sub_heading_numbering_style: str = "decimal"
    number_separator: str = ". "


class HeadlessBrowserEngineConfig(BaseModel):
    """Lược đồ cấu hình trình duyệt ngầm Playwright Chromium."""
    browser_type: str = "chromium"
    headless: bool = True
    page_timeout_ms: int = Field(default=30000, ge=1000)
    wait_until_event: str = "networkidle"
    print_background: bool = True
    prefer_css_page_size: bool = True


class KaTeXDelimiterConfig(BaseModel):
    """Lược đồ ranh giới công thức toán KaTeX."""
    left: str
    right: str
    display: bool


class KaTeXOfflineConfig(BaseModel):
    """Lược đồ cấu hình động cơ KaTeX Offline Mở rộng (v2.3.0)."""
    enable_katex: bool = True
    assets_dir: str = "assets/katex"
    css_filename: str = "katex.min.css"
    js_filename: str = "katex.min.js"
    auto_render_js_filename: str = "auto-render.min.js"
    strict_mode: bool = False
    throw_on_error: bool = False
    enable_base64_math_encoding: bool = True
    enable_vietnamese_math_isolation: bool = True
    vietnamese_font_family: str = '"Times New Roman", "Segoe UI", Arial, sans-serif'
    enable_base64_font_embedding: bool = True
    hybrid_typography_fallback: str = '"Cambria Math", "Times New Roman", serif'
    delimiters: list[KaTeXDelimiterConfig] = []


class MathEngineRoutingConfig(BaseModel):
    """Lược đồ điều hướng công tắc động cơ toán học (NÂNG CẤP KIẾN TRÚC LAI v2.3.0)."""
    active_engine: str = "katex_placeholder"

    @field_validator("active_engine")
    @classmethod
    def validate_active_engine(cls, value: str) -> str:
        """Xác thực cờ active_engine chỉ nhận các giá trị động cơ được hỗ trợ."""
        allowed_engines = {"katex_placeholder", "mathjax_svg"}
        clean_value = value.strip().lower()
        if clean_value not in allowed_engines:
            # Sửa lỗi Ruff C414: Bỏ hàm list() dư thừa bên trong sorted()
            raise ValueError(
                f"[VI_PHẠM_LƯỢC_ĐỒ] Động cơ toán học '{value}' không được hỗ trợ. "
                f"Giá trị hợp lệ phải là một trong các tùy chọn: {sorted(allowed_engines)}."
            )
        return clean_value


class MathJaxOfflineConfig(BaseModel):
    """Lược đồ cấu hình động cơ MathJax v3 Offline (NÂNG CẤP KIẾN TRÚC LAI v2.3.0)."""
    enable_mathjax: bool = True
    assets_dir: str = "assets/mathjax"
    js_filename: str = "tex-svg.js"
    font_cache: str = "global"
    scale: float = Field(default=1.0, ge=0.1, le=5.0)
    inline_math_delimiters: list[list[str]] = Field(
        default_factory=lambda: [["$", "$"], ["\\(", "\\)"]]
    )
    display_math_delimiters: list[list[str]] = Field(
        default_factory=lambda: [["$$", "$$"], ["\\[", "\\]"]]
    )


class TableRenderingSystemConfig(BaseModel):
    """Lược đồ cấu hình bộ xử lý bảng biểu GFM."""
    enable_gfm_tables: bool = True
    overflow_strategy: str = "clip_and_warn"
    repeat_header_on_page_break: bool = True
    max_printable_width_mm: int = 170


class AcademicStandardsProfileConfig(BaseModel):
    """Lược đồ cấu hình ma trận học thuật APA/IEEE."""
    active_standard: str = "apa"
    prevent_orphans_and_widows: bool = True
    code_block_page_break_inside: str = "avoid"
    table_page_break_inside: str = "avoid"


class AppConfig(BaseModel):
    """Lược đồ tổng thể cho toàn bộ ứng dụng (Global Engine Schema v2.3.0)."""
    global_encoding_standard: str = "utf-8"
    directory_routing: DirectoryRoutingConfig = Field(default_factory=DirectoryRoutingConfig)
    syntax_highlighting_profile: str = "monokai"
    heading_retention_depth: HeadingRetentionDepthConfig = Field(default_factory=HeadingRetentionDepthConfig)
    document_layout: DocumentLayoutConfig = Field(default_factory=DocumentLayoutConfig)
    typography_configuration: TypographyConfiguration = Field(default_factory=TypographyConfiguration)
    heading_numbering_system: HeadingNumberingSystemConfig = Field(default_factory=HeadingNumberingSystemConfig)
    headless_browser_engine: HeadlessBrowserEngineConfig = Field(default_factory=HeadlessBrowserEngineConfig)
    math_engine_routing: MathEngineRoutingConfig = Field(default_factory=MathEngineRoutingConfig)
    katex_offline_config: KaTeXOfflineConfig = Field(default_factory=KaTeXOfflineConfig)
    mathjax_offline_config: MathJaxOfflineConfig = Field(default_factory=MathJaxOfflineConfig)
    table_rendering_system: TableRenderingSystemConfig = Field(default_factory=TableRenderingSystemConfig)
    academic_standards_profile: AcademicStandardsProfileConfig = Field(default_factory=AcademicStandardsProfileConfig)


# ==============================================================================
# 2. ĐỐI TƯỢNG NGỮ CẢNH THỰC THI TRUNG TÂM (EXECUTION CONTEXT SSOT)
# ==============================================================================

class ExecutionContext(BaseModel):
    """Vùng chứa Ngữ cảnh Thực thi Toàn cục (Single Source of Truth - SSOT DTO v2.3.0).
    
    Đóng gói cấu hình gốc và thông tin tệp I/O đang xử lý nhằm triệt tiêu
    hoàn toàn sự cố trôi dạt tham số hạ nguồn. Chuẩn hóa cú pháp PEP 604.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: AppConfig
    input_md_path: Path | None = None
    output_pdf_path: Path | None = None


# ==============================================================================
# 3. HÀM NẠP CẤU HÌNH VÀ TẠO NGỮ CẢNH THỰC THI
# ==============================================================================

def load_configuration(config_path: Path) -> AppConfig:
    """Nạp tệp YAML và thực thi xác thực qua Pydantic DTO Model."""
    if not config_path.exists():
        raise FileNotFoundError(
            f"[LỖI_CẤU_HÌNH] Không tìm thấy tệp cấu hình tại đường dẫn: {config_path}"
        )

    try:
        with open(config_path, "r", encoding="utf-8") as file_stream:
            raw_yaml_data = yaml.safe_load(file_stream)
            if not isinstance(raw_yaml_data, dict):
                raise TypeError(
                    "[LỖI_CẤU_HÌNH] Cấu trúc tệp YAML không hợp lệ (Phải là dạng Dictionary)."
                )

        validated_config = AppConfig.model_validate(raw_yaml_data)
        return validated_config

    except yaml.YAMLError as error:
        raise ValueError(
            f"[LỖI_CÚ_PHÁP_YAML] Phân tích tệp cấu hình thất bại: {error}"
        ) from error
    except ValidationError as error:
        print("\n================ [SỰ CỐ VI PHẠM LƯỢC ĐỒ TẢI CẤU HÌNH] ================")
        print(f"Phát hiện lỗi định dạng nghiêm trọng trong tệp: {config_path.name}")
        for err in error.errors():
            location = " -> ".join([str(loc) for loc in err['loc']])
            print(f"  - Vị trí khóa : [{location}]")
            print(f"  - Lỗi phát hiện : {err['msg']}")
        print("======================================================================\n")
        raise


def ensure_directories_exist(
    input_dir: Path, output_dir: Path, auto_create: bool = True
) -> None:
    """Tự động kiểm tra và khởi tạo các thư mục đầu vào và đầu ra."""
    if not input_dir.exists():
        if auto_create:
            input_dir.mkdir(parents=True, exist_ok=True)
            print(f"[KHỞI_TẠO] Đã tự động tạo thư mục đầu vào tại: {input_dir}")
        else:
            raise FileNotFoundError(
                f"[LỖI_I/O] Thư mục đầu vào không tồn tại: {input_dir}"
            )

    if not output_dir.exists():
        if auto_create:
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"[KHỞI_TẠO] Đã tự động tạo thư mục đầu ra tại: {output_dir}")
        else:
            raise FileNotFoundError(
                f"[LỖI_I/O] Thư mục đầu ra không tồn tại: {output_dir}"
            )


# ==============================================================================
# 4. ĐIỀU PHỐI ĐƯỜNG ỐNG XỬ LÝ ĐƠN TỆP VÀ HÀNG LOẠT
# ==============================================================================

def execute_single_file_pipeline(
    input_md_path: Path,
    output_pdf_path: Path,
    config: AppConfig | ExecutionContext,
) -> bool:
    """Biên dịch Markdown sang PDF sử dụng ExecutionContext DTO chuẩn hóa (v2.3.0)."""
    try:
        # 1. Trích xuất hoặc khởi tạo ExecutionContext từ tham số đầu vào
        if isinstance(config, ExecutionContext):
            context = config
            app_config = context.config
        else:
            app_config = config
            context = ExecutionContext(
                config=app_config,
                input_md_path=input_md_path,
                output_pdf_path=output_pdf_path,
            )

        # 2. Truy xuất các khối cấu hình chuẩn DTO
        encoding_standard = app_config.global_encoding_standard
        theme_profile = app_config.syntax_highlighting_profile
        enable_math = app_config.katex_offline_config.enable_katex

        # Trích xuất đầy đủ các khối DTO dưới dạng từ điển phục vụ truyền dẫn hạ nguồn
        layout_config = app_config.document_layout.model_dump()
        retention_config = app_config.heading_retention_depth.model_dump()
        browser_config = app_config.headless_browser_engine.model_dump()
        math_routing_config = app_config.math_engine_routing.model_dump()
        katex_config = app_config.katex_offline_config.model_dump()
        mathjax_config = app_config.mathjax_offline_config.model_dump()
        table_config = app_config.table_rendering_system.model_dump()
        numbering_config = app_config.heading_numbering_system.model_dump()
        academic_config = app_config.academic_standards_profile.model_dump()

        # 3. Đọc nội dung văn bản thô theo chuẩn UTF-8
        with open(input_md_path, "r", encoding=encoding_standard) as file_stream:
            markdown_text = file_stream.read()

        # 4. Kết xuất mã HTML ngữ nghĩa (Giai đoạn 2 - Truyền dẫn DTO Routing & MathJax v2.3.0)
        renderer = HTMLRenderer(
            theme_name=theme_profile,
            **retention_config,
            enable_math=enable_math,
            table_config=table_config,
            katex_config=katex_config,
            math_routing_config=math_routing_config,
            mathjax_config=mathjax_config,
            encoding_standard=encoding_standard,
        )
        pygments_css, rendered_html = renderer.convert_to_html(markdown_text)

        # 5. Đảm bảo thư mục cha của tệp đầu ra đã được khởi tạo
        output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

        # 6. Biên dịch PDF qua Playwright Chromium Engine (Giai đoạn 3)
        compiler = PDFCompiler(
            output_encoding=encoding_standard,
            layout_config=layout_config,
            numbering_config=numbering_config,
            academic_config=academic_config,
            browser_config=browser_config,
            table_config=table_config,
        )
        compiler.compile_to_pdf(
            html_content=rendered_html,
            pygments_css=pygments_css,
            output_path=output_pdf_path,
        )

        # 7. Tiêm Siêu Dữ Liệu Hậu Kỳ bằng PyMuPDF (Giai đoạn 4)
        print("    -> [ĐIỀU_PHỐI] Đang kích hoạt động cơ tiêm siêu dữ liệu Bookmarks...")
        injector = MetadataInjector(
            max_bookmark_level=app_config.heading_retention_depth.max_bookmark_level
        )
        is_metadata_injected = injector.inject_metadata(
            pdf_path=output_pdf_path,
            html_content=rendered_html,
        )

        if not is_metadata_injected:
            print(
                f"    -> [CẢNH_BÁO_ĐIỀU_PHỐI] Tệp PDF '{input_md_path.name}' được in thành công nhưng tiến trình tiêm Bookmarks gặp sự cố."
            )

        return True

    except (
        FileNotFoundError,
        UnicodeDecodeError,
        ValueError,
        TypeError,
        OSError,
        RuntimeError,
    ) as error:
        print(
            f"    -> [THẤT_BẠI_TỆP] Bỏ qua tệp {input_md_path.name} do xuất hiện lỗi: {error}"
        )
        return False


def batch_process_directory(base_directory: Path) -> None:
    """Động cơ điều phối quét hàng loạt dựa trên ExecutionContext SSOT Schema (v2.3.0)."""
    print("=== BẮT ĐẦU TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT (HYBRID MATH ENGINE ARCHITECTURE v2.3.0) ===")

    config_path = base_directory / "config" / "settings.yaml"
    config = load_configuration(config_path)

    routing = config.directory_routing
    input_dir = base_directory / routing.input_directory
    output_dir = base_directory / routing.output_directory

    ensure_directories_exist(
        input_dir=input_dir, output_dir=output_dir, auto_create=routing.auto_create_directories
    )

    allowed_exts = set(routing.allowed_extensions)
    if routing.recursive_search:
        all_candidate_files = [path for path in input_dir.rglob("*") if path.is_file()]
    else:
        all_candidate_files = [path for path in input_dir.glob("*") if path.is_file()]

    target_files = [
        file_path
        for file_path in all_candidate_files
        if file_path.suffix.lower() in allowed_exts
    ]

    if not target_files:
        print(
            f"[THÔNG_BÁO] Thư mục '{routing.input_directory}' không chứa tệp Markdown hợp lệ nào."
        )
        return

    print(
        f"[THÔNG_TIN] Phát hiện {len(target_files)} tệp Markdown hợp lệ trong danh sách chờ biên dịch.\n"
    )

    success_count = 0
    failure_count = 0
    skipped_count = 0

    for index, input_file_path in enumerate(target_files, start=1):
        if routing.preserve_subfolder_structure:
            relative_path = input_file_path.relative_to(input_dir)
            target_output_pdf_path = (output_dir / relative_path).with_suffix(".pdf")
        else:
            target_output_pdf_path = (output_dir / input_file_path.name).with_suffix(".pdf")

        print(
            f"[{index}/{len(target_files)}] Đang xử lý: {input_file_path.relative_to(base_directory)}"
        )

        if target_output_pdf_path.exists() and not routing.overwrite_existing:
            print(
                "    -> [BỎ_QUA] Tệp PDF thành phẩm đã tồn tại và chế độ ghi đè bị tắt."
            )
            skipped_count += 1
            continue

        file_context = ExecutionContext(
            config=config,
            input_md_path=input_file_path,
            output_pdf_path=target_output_pdf_path,
        )

        is_successful = execute_single_file_pipeline(
            input_md_path=input_file_path,
            output_pdf_path=target_output_pdf_path,
            config=file_context,
        )

        if is_successful:
            print(
                f"    -> [THÀNH_CÔNG] Xuất bản hoàn chỉnh: {target_output_pdf_path.relative_to(base_directory)}\n"
            )
            success_count += 1
        else:
            failure_count += 1
            print("\n")

    print("================ TỔNG KẾT TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT ================")
    print(f"- Tổng số tệp phát hiện : {len(target_files)}")
    print(f"- Biên dịch thành công : {success_count}")
    print(f"- Biên dịch thất bại   : {failure_count}")
    print(f"- Bỏ qua (Đã tồn tại)  : {skipped_count}")
    print("========================================================================")


def main() -> None:
    """Hàm khởi chạy chính của ứng dụng."""
    base_directory = Path(__file__).parent.resolve()

    try:
        batch_process_directory(base_directory=base_directory)
    except (FileNotFoundError, ValueError, TypeError, OSError, ValidationError) as error:
        print(f"[SỰ_CỐ_HỆ_THỐNG_DỪNG_LUỒNG] Tiến trình kết thúc do lỗi: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
