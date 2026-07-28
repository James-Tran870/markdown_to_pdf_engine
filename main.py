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
    """Biên dịch một tệp Markdown duy nhất sang PDF với cơ chế cô lập ngoại lệ cụ thể."""
    try:
        encoding_standard = config.get("global_encoding_standard", "utf-8")
        theme_profile = config.get("syntax_highlighting_profile", "monokai")
        heading_config = config.get("heading_retention_depth", {})
        max_bookmark_level = heading_config.get("max_bookmark_level", 4)

        # 1. Khởi tạo và nạp tệp qua bộ phân tích Cây Cú Pháp Trừu Tượng (AST)
        parser = ASTParser(encoding_standard=encoding_standard)
        _ast_tokens = parser.parse_markdown_file(input_md_path)

        # 2. Đọc nội dung văn bản thô theo chuẩn UTF-8 cưỡng chế
        with open(input_md_path, "r", encoding=encoding_standard) as file_stream:
            markdown_text = file_stream.read()

        # 3. Kết xuất mã HTML ngữ nghĩa kèm Stylesheet Pygments CSS
        renderer = HTMLRenderer(
            theme_name=theme_profile, max_bookmark_level=max_bookmark_level
        )
        pygments_css, rendered_html = renderer.convert_to_html(markdown_text)

        # 4. Đảm bảo thư mục cha của tệp đầu ra đã được tạo trước khi xuất bản
        output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

        # 5. Biên dịch Paged Media CSS và xuất tệp PDF hoàn chỉnh
        compiler = PDFCompiler(output_encoding=encoding_standard)
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
    print("=== BẮT ĐẦU TIẾN TRÌNH BIÊN DỊCH HÀNG LOẠT (BATCH PROCESSING) ===")

    # 1. Nạp tệp cấu hình hệ thống
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

    # 2. Đảm bảo các thư mục đầu vào và đầu ra đã sẵn sàng
    ensure_directories_exist(
        input_dir=input_dir, output_dir=output_dir, auto_create=auto_create_dirs
    )

    # 3. Thu gom danh sách toàn bộ các tệp cần xử lý
    if recursive_search:
        all_candidate_files = [path for path in input_dir.rglob("*") if path.is_file()]
    else:
        all_candidate_files = [path for path in input_dir.glob("*") if path.is_file()]

    # Lọc danh sách chỉ giữ lại các tệp có đuôi mở rộng hợp lệ
    target_files = [
        file_path
        for file_path in all_candidate_files
        if file_path.suffix.lower() in allowed_extensions
    ]

    if not target_files:
        print(
            f"[THÔNG_BÁO] Thư mục '{input_dir_name}' không chứa tệp Markdown hợp lệ nào."
        )
        print(
            f"[HƯỚNG_DẪN] Hãy chép các tệp {list(allowed_extensions)} vào thư mục '{input_dir}' và thực thi lại."
        )
        return

    print(
        f"[THÔNG_TIN] Phát hiện {len(target_files)} tệp Markdown hợp lệ trong danh sách chờ biên dịch.\n"
    )

    success_count = 0
    failure_count = 0
    skipped_count = 0

    # 4. Duyệt qua từng tệp để đẩy qua băng tải chuyển đổi
    for index, input_file_path in enumerate(target_files, start=1):
        # Tái tạo cấu trúc thư mục con nếu tính năng preserve_subfolder_structure bật
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

        # Kiểm tra điều kiện ghi đè tệp thành phẩm
        if target_output_pdf_path.exists() and not overwrite_existing:
            print(
                "    -> [BỎ_QUA] Tệp PDF thành phẩm đã tồn tại và chế độ ghi đè bị tắt."
            )
            skipped_count += 1
            continue

        # Kích hoạt biên dịch đơn tệp
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

    # 5. In báo cáo tổng kết tiến trình vận hành
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