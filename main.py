# ==============================================================================
# TỆP 1: main.py (BỘ ĐIỀU PHỐI PIPELINE PLAYWRIGHT & KATEX v1.4.0)
# Dự án: markdown_to_pdf_engine
# Kiến trúc: Separation of Concerns (SoC) & Defensive Pipeline Orchestration
# ==============================================================================

import sys
from pathlib import Path

import yaml

from src.ast_parser import ASTParser
from src.html_renderer import HTMLRenderer
from src.pdf_compiler import PDFCompiler


def load_configuration(config_path: Path) -> dict:
    """Nạp tệp cấu hình YAML với cơ chế kiểm soát lỗi cấu trúc phòng thủ."""
    if not config_path.exists():
        raise FileNotFoundError(
            f"[LỖI_CẤU_HÌNH] Không tìm thấy tệp cấu hình tại đường dẫn: {config_path}"
        )

    try:
        with open(config_path, "r", encoding="utf-8") as file_stream:
            config_data = yaml.safe_load(file_stream)
            if not isinstance(config_data, dict):
                raise TypeError(
                    "[LỖI_CẤU_HÌNH] Cấu trúc tệp YAML không hợp lệ (Phải là dạng Dictionary)."
                )
            return config_data
    except yaml.YAMLError as error:
        raise ValueError(
            f"[LỖI_CÚ_PHÁP_YAML] Phân tích tệp cấu hình thất bại: {error}"
        ) from error


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


def execute_single_file_pipeline(
    input_md_path: Path, output_pdf_path: Path, config: dict
) -> bool:
    """Biên dịch một tệp Markdown duy nhất sang PDF qua Playwright và KaTeX Engine."""
    try:
        # 1. Trích xuất các tham số cấu hình cơ bản từ YAML
        encoding_standard = config.get("global_encoding_standard", "utf-8")
        theme_profile = config.get("syntax_highlighting_profile", "monokai")
        heading_config = config.get("heading_retention_depth", {})
        max_bookmark_level = heading_config.get("max_bookmark_level", 4)
        numbering_config = config.get("heading_numbering_system", {})

        # 2. Trích xuất khối cấu hình động cơ Playwright và KaTeX (Nâng cấp v1.4.0)
        browser_config = config.get("headless_browser_engine", {})
        katex_config = config.get("katex_offline_config", {})
        enable_math = katex_config.get("enable_katex", True)

        # 3. Trích xuất khối cấu hình động cơ xử lý bảng biểu GFM và học thuật
        table_config = config.get("table_rendering_system", {})
        enable_tables = table_config.get("enable_gfm_tables", True)
        academic_config = config.get("academic_standards_profile", {})

        # 4. Khởi tạo và nạp tệp qua bộ phân tích AST
        parser = ASTParser(
            encoding_standard=encoding_standard,
            enable_math=enable_math,
            enable_tables=enable_tables,
        )
        _ast_tokens = parser.parse_markdown_file(input_md_path)

        # 5. Đọc nội dung văn bản thô theo chuẩn UTF-8 cưỡng chế
        with open(input_md_path, "r", encoding=encoding_standard) as file_stream:
            markdown_text = file_stream.read()

        # 6. Kết xuất mã HTML ngữ nghĩa (Bơm katex_config để tiêm script KaTeX Offline)
        renderer = HTMLRenderer(
            theme_name=theme_profile,
            max_bookmark_level=max_bookmark_level,
            enable_math=enable_math,
            table_config=table_config,
            katex_config=katex_config,
        )
        pygments_css, rendered_html = renderer.convert_to_html(markdown_text)

        # 7. Đảm bảo thư mục cha của tệp đầu ra đã được tạo
        output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

        # 8. Biên dịch PDF qua Playwright Chromium Engine
        compiler = PDFCompiler(
            output_encoding=encoding_standard,
            numbering_config=numbering_config,
            academic_config=academic_config,
            browser_config=browser_config,
        )
        compiler.compile_to_pdf(
            html_content=rendered_html,
            pygments_css=pygments_css,
            output_path=output_pdf_path,
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
    """Động cơ điều phối quét hàng loạt và phân loại tài liệu tự động."""
    print("=== BẮT ĐẦU TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT (PLAYWRIGHT v1.4.0) ===")

    config_path = base_directory / "config" / "settings.yaml"
    config = load_configuration(config_path)

    routing_config = config.get("directory_routing", {})
    input_dir_name = routing_config.get("input_directory", "input")
    output_dir_name = routing_config.get("output_directory", "output")
    recursive_search = routing_config.get("recursive_search", True)
    allowed_extensions = set(
        routing_config.get("allowed_extensions", [".md", ".markdown"])
    )
    overwrite_existing = routing_config.get("overwrite_existing", True)
    auto_create_dirs = routing_config.get("auto_create_directories", True)
    preserve_subfolder = routing_config.get("preserve_subfolder_structure", True)

    input_dir = base_directory / input_dir_name
    output_dir = base_directory / output_dir_name

    ensure_directories_exist(
        input_dir=input_dir, output_dir=output_dir, auto_create=auto_create_dirs
    )

    if recursive_search:
        all_candidate_files = [path for path in input_dir.rglob("*") if path.is_file()]
    else:
        all_candidate_files = [path for path in input_dir.glob("*") if path.is_file()]

    target_files = [
        file_path
        for file_path in all_candidate_files
        if file_path.suffix.lower() in allowed_extensions
    ]

    if not target_files:
        print(
            f"[THÔNG_BÁO] Thư mục '{input_dir_name}' không chứa tệp Markdown hợp lệ nào."
        )
        return

    print(
        f"[THÔNG_TIN] Phát hiện {len(target_files)} tệp Markdown hợp lệ trong danh sách chờ biên dịch.\n"
    )

    success_count = 0
    failure_count = 0
    skipped_count = 0

    for index, input_file_path in enumerate(target_files, start=1):
        if preserve_subfolder:
            relative_path = input_file_path.relative_to(input_dir)
            target_output_pdf_path = (output_dir / relative_path).with_suffix(".pdf")
        else:
            target_output_pdf_path = (output_dir / input_file_path.name).with_suffix(
                ".pdf"
            )

        print(
            f"[{index}/{len(target_files)}] Đang xử lý: {input_file_path.relative_to(base_directory)}"
        )

        if target_output_pdf_path.exists() and not overwrite_existing:
            print(
                "    -> [BỎ_QUA] Tệp PDF thành phẩm đã tồn tại và chế độ ghi đè bị tắt."
            )
            skipped_count += 1
            continue

        is_successful = execute_single_file_pipeline(
            input_md_path=input_file_path,
            output_pdf_path=target_output_pdf_path,
            config=config,
        )

        if is_successful:
            print(
                f"    -> [THÀNH_CÔNG] Xuất bản: {target_output_pdf_path.relative_to(base_directory)}"
            )
            success_count += 1
        else:
            failure_count += 1

    print("\n================ TỔNG KẾT TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT ================")
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
    except (FileNotFoundError, ValueError, TypeError, OSError) as error:
        print(f"[SỰ_CỐ_HỆ_THỐNG] {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
