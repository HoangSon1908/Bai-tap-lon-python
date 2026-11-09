# BÀI TẬP LỚN LẬP TRÌNH PYTHON - NHÓM 13
**Chủ đề:** E-commerce customer purchasing behavior  
**Tiến độ:** Mốc 03 (10/11/2026) - Tiền xử lý dữ liệu & Phân tích ban đầu

---

## 1. HƯỚNG DẪN CÀI ĐẶT
Mở terminal tại thư mục dự án và chạy lệnh:
```bash
pip install -r requirements.txt
```

## 2. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH
Chạy toàn bộ luồng xử lý và phân tích Mốc 03:
```bash
python main.py
```

## 3. CẤU TRÚC THƯ MỤC
- `data/raw/`              : Chứa tệp dữ liệu thô ban đầu (`ecommerce_data.csv`).
- `data/processed/`        : Chứa dữ liệu sạch sau khi tiền xử lý (`ecommerce_cleaned.csv`).
- `src/data_processor.py`  : Lớp OOP `EcommerceDataProcessor` kiểm tra cấu trúc, làm sạch và tạo đặc trưng mới.
- `src/customer_analyzer.py`: Lớp OOP `CustomerBehaviorAnalyzer` phân tích các chỉ số hành vi khách hàng.
- `src/visualizer.py`      : Lớp OOP `CustomerVisualizer` vẽ và xuất biểu đồ trực quan.
- `outputs/`               : Chứa biểu đồ (`figures/`) và tệp báo cáo nghiệm thu Mốc 03 (`Bao_cao_tien_do_Moc03.txt`).
- `main.py`                : Tệp kịch bản điều phối chương trình chính.
- `requirements.txt`       : Danh sách các thư viện ngoài cần cài đặt.

## 4. KẾT QUẢ ĐẠT ĐƯỢC (MỐC 03 - 10/11/2026)
- **Quy mô dữ liệu:** Đạt chuẩn yêu cầu BTL (> 300 bản ghi, > 6 thuộc tính), xử lý làm sạch **1,811 dòng dữ liệu thô (8 thuộc tính)**, loại bỏ trùng lặp và bản ghi khuyết thiếu, giữ lại **1,704 giao dịch hợp lệ** của **55 khách hàng độc nhất** (tỷ lệ giữ lại: 94.09%).
- **Kỹ thuật dữ liệu:**
  + Xây dựng module hướng đối tượng (`EcommerceDataProcessor`) đọc, kiểm tra cấu trúc, chuẩn hóa thời gian và làm sạch dữ liệu.
  + Tạo các đặc trưng mới phục vụ phân tích: `TotalAmount` ($Quantity \times UnitPrice$), `DayOfWeek` (thứ trong tuần), `Hour` (khung giờ mua sắm).
- **Phát hiện ban đầu:**
  + Tỷ lệ khách hàng mua lại sơ bộ (Repurchase Rate): **49.09%** (27/55 khách hàng phát sinh từ 2 đơn hàng trở lên).
  + Giá trị đơn hàng trung bình (AOV): **$452.40 USD**.
  + Thời điểm mua sắm cao điểm nhất: **Thứ Tư (Wednesday)**, khung giờ **12:00 trưa**.
- **Trực quan hóa:** Xuất biểu đồ nhiệt phân bố thời gian mua sắm tại `outputs/figures/01_shopping_time_heatmap.png`.
- **Nghiệm thu:** Báo cáo chi tiết mốc 03 được xuất tự động tại `outputs/Bao_cao_tien_do_Moc03.txt`.