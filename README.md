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
- Xử lý làm sạch 541,909 dòng dữ liệu thô, giữ lại 392,692 giao dịch hợp lệ của 4,338 khách hàng độc nhất.
- Tạo các đặc trưng mới: `TotalAmount` ($Quantity \times UnitPrice$), `DayOfWeek`, `Hour`.
- Đưa ra các phát hiện ban đầu:
  + Tỷ lệ khách hàng mua lại sơ bộ (Repurchase Rate): **65.58%**.
  + Giá trị đơn hàng trung bình (AOV): **$479.56 USD**.
  + Thời điểm mua sắm cao điểm nhất: **Thứ Năm**, lúc **12:00 trưa**.
- Xuất biểu đồ mật độ giao dịch ban đầu tại `outputs/figures/01_shopping_time_heatmap.png`.