"""
Tệp điều phối chương trình chính (main.py)
Đề tài: E-commerce customer purchasing behavior
Học phần: Lập trình Python - PTIT | Nhóm 13

MỤC TIÊU MỐC 03 (HẠN 10/11/2026):
1. Đọc và kiểm tra cấu trúc dữ liệu thô.
2. Tiền xử lý, làm sạch và tạo đặc trưng mới (OOP: EcommerceDataProcessor).
3. Xuất dữ liệu sạch vào data/processed/ecommerce_cleaned.csv.
4. Thống kê mô tả tổng quan & đưa ra các kết quả phân tích ban đầu (CustomerBehaviorAnalyzer).
5. Xuất báo cáo tiến độ Mốc 03 để giảng viên kiểm tra.
"""

import os
import sys
import time

from src.data_processor import EcommerceDataProcessor
from src.customer_analyzer import CustomerBehaviorAnalyzer
from src.visualizer import CustomerVisualizer


def print_header(title: str):
    print("\n" + "=" * 75)
    print(f" {title.upper()} ")
    print("=" * 75)


def run_milestone_03():
    start_time = time.time()
    print_header("BÀI TẬP LỚN LẬP TRÌNH PYTHON - NHÓM 13")
    print("ĐỀ TÀI: E-COMMERCE CUSTOMER PURCHASING BEHAVIOR")
    print("TIẾN ĐỘ: MỐC 03 (10/11/2026) - LÀM SẠCH DỮ LIỆU & PHÂN TÍCH BAN ĐẦU\n")

    os.makedirs("outputs", exist_ok=True)
    os.makedirs("outputs/figures", exist_ok=True)

    # -------------------------------------------------------------------------
    # BƯỚC 1: ĐỌC VÀ LÀM SẠCH DỮ LIỆU (OOP: EcommerceDataProcessor)
    # -------------------------------------------------------------------------
    print_header("1. ĐỌC VÀ LÀM SẠCH DỮ LIỆU (EcommerceDataProcessor)")
    processor = EcommerceDataProcessor(
        raw_path="data/raw/ecommerce_data.csv",
        processed_path="data/processed/ecommerce_cleaned.csv"
    )

    try:
        # Tải dữ liệu thô
        processor.load_data()

        # Kiểm tra cấu trúc ban đầu
        info = processor.inspect_structure()
        print(f"  - Số lượng bản ghi thô       : {info['total_rows']:,}")
        print(f"  - Số dòng trùng lặp          : {info['duplicate_rows']:,}")
        print(f"  - Số bản ghi thiếu CustomerID: {info['missing_values'].get('CustomerID', 0):,}")

        # Làm sạch dữ liệu và tạo đặc trưng mới
        df_cleaned = processor.clean_data()

        # Lưu dữ liệu sạch
        saved_path = processor.save_processed_data()

        # In tóm tắt tiền xử lý
        print("\n" + processor.get_summary_report())

    except Exception as e:
        print(f"[LỖI XỬ LÝ DỮ LIỆU]: {e}", file=sys.stderr)
        return

    # -------------------------------------------------------------------------
    # BƯỚC 2: KẾT QUẢ PHÂN TÍCH BAN ĐẦU (CustomerBehaviorAnalyzer)
    # -------------------------------------------------------------------------
    print_header("2. KẾT QUẢ PHÂN TÍCH BAN ĐẦU (CustomerBehaviorAnalyzer)")
    analyzer = CustomerBehaviorAnalyzer(df=df_cleaned, cancelled_df=processor.cancelled_df)

    # 2.1 Thống kê mô tả tổng quan
    metrics = analyzer.get_summary_metrics()
    print("A. THỐNG KÊ MÔ TẢ TỔNG QUAN:")
    print(f"  * Tổng doanh thu hợp lệ        : ${metrics['Total_Revenue']:,.2f} USD")
    print(f"  * Tổng số đơn hàng thành công  : {metrics['Total_Orders']:,} hóa đơn")
    print(f"  * Tổng số khách hàng duy nhất  : {metrics['Total_Customers']:,} người")
    print(f"  * Giá trị đơn hàng TB (AOV)    : ${metrics['Average_Order_Value']:.2f} USD")
    print(f"  * Số sản phẩm TB trên mỗi đơn  : {metrics['Avg_Items_Per_Order']:.1f} sản phẩm")
    print(f"  * Khoảng thời gian khảo sát     : {metrics['Date_Min'].strftime('%d/%m/%Y')} -> {metrics['Date_Max'].strftime('%d/%m/%Y')}")

    # 2.2 Kết quả sơ bộ về Tần suất mua lại (Repurchase Rate)
    print("\nB. KẾT QUẢ PHÂN TÍCH SƠ BỘ VỀ TẦN SUẤT MUA LẠI:")
    repurchase_init = analyzer.analyze_initial_repurchase()
    print(f"  * Số khách hàng chỉ mua 1 lần   : {repurchase_init['one_time_customers']:,} ({100 - repurchase_init['repurchase_rate_pct']:.2f}%)")
    print(f"  * Số khách hàng mua lặp lại (>=2): {repurchase_init['repeat_customers']:,} ({repurchase_init['repurchase_rate_pct']}%)")
    print(f"  * Tỷ lệ khách mua lại (Repurchase Rate): {repurchase_init['repurchase_rate_pct']}% (Mức độ giữ chân tốt)")
    print(f"  * Số đơn hàng TB mỗi khách hàng: {repurchase_init['avg_orders_per_customer']} đơn")

    # 2.3 Kết quả sơ bộ về Thời điểm mua sắm (sử dụng pivot_table)
    print("\nC. KẾT QUẢ SƠ BỘ VỀ THỜI ĐIỂM MUA SẮM (pivot_table):")
    time_pivot = analyzer.analyze_shopping_time_patterns()
    peak_day = time_pivot.sum(axis=1).idxmax()
    peak_hour = time_pivot.sum(axis=0).idxmax()
    print(f"  * Ngày có nhiều đơn đặt nhất    : {peak_day} ({time_pivot.sum(axis=1).max():,} đơn)")
    print(f"  * Khung giờ cao điểm nhất       : {peak_hour}:00 ({time_pivot.sum(axis=0).max():,} đơn)")

    # -------------------------------------------------------------------------
    # BƯỚC 3: XUẤT 01 BIỂU ĐỒ SƠ BỘ (CustomerVisualizer)
    # -------------------------------------------------------------------------
    print_header("3. TRỰC QUAN HÓA BAN ĐẦU (CustomerVisualizer)")
    visualizer = CustomerVisualizer(output_dir="outputs/figures")
    visualizer.plot_shopping_heatmap(time_pivot)

    # -------------------------------------------------------------------------
    # BƯỚC 4: XUẤT BÁO CÁO TIẾN ĐỘ MỐC 03
    # -------------------------------------------------------------------------
    report_file = "outputs/Bao_cao_tien_do_Moc03.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("BÁO CÁO TIẾN ĐỘ MỐC 03 (10/11/2026) - NHÓM 13\n")
        f.write("Chủ đề: E-commerce customer purchasing behavior\n")
        f.write("=" * 70 + "\n\n")
        f.write(processor.get_summary_report() + "\n\n")
        f.write("KẾT QUẢ PHÂN TÍCH BAN ĐẦU:\n")
        f.write("-" * 70 + "\n")
        f.write(f"- Khách hàng độc nhất: {metrics['Total_Customers']:,}\n")
        f.write(f"- Tỷ lệ khách mua lại sơ bộ: {repurchase_init['repurchase_rate_pct']}%\n")
        f.write(f"- Giá trị đơn hàng trung bình (AOV): ${metrics['Average_Order_Value']:.2f}\n")
        f.write(f"- Thời điểm mua sắm cao điểm: {peak_day} lúc {peak_hour}:00\n")
        f.write("\nKẾ HOẠCH BÀN GIAO CHO CÁC THÀNH VIÊN TRIỂN KHAI MỐC 04 (HẠN 17/11):\n")
        f.write("- Thành viên phụ trách RFM: Xây dựng compute_rfm_segments().\n")
        f.write("- Thành viên phụ trách Doanh thu & Hủy đơn: analyze_segment_revenue_contribution(), analyze_cancellation_by_segment().\n")
        f.write("- Thành viên phụ trách Trực quan hóa: Hoàn thiện 04 biểu đồ còn lại trong visualizer.py.\n")
        f.write("- Thành viên phụ trách Báo cáo: Soạn thảo bản nháp báo cáo 5-8 trang.\n")

    elapsed = round(time.time() - start_time, 2)
    print_header(f"HOÀN THÀNH MỤC TIÊU MỐC 03 (Thời gian: {elapsed}s)")
    print(f"[+] Dữ liệu sạch đã lưu tại       : data/processed/ecommerce_cleaned.csv")
    print(f"[+] Biểu đồ ban đầu lưu tại       : outputs/figures/01_shopping_time_heatmap.png")
    print(f"[+] Báo cáo nghiệm thu Mốc 03     : {report_file}")
    print("[*] Sẵn sàng bàn giao cho các thành viên trong nhóm làm tiếp Mốc 04 (17/11)!")


if __name__ == "__main__":
    run_milestone_03()
