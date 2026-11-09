# BÀI TẬP LỚN PYTHON - NHÓM 13
## DANH SÁCH 07 CÂU HỎI PHÂN TÍCH DỮ LIỆU ĐỀ TÀI E-COMMERCE
**Chủ đề:** E-commerce Customer Purchasing Behavior  
**Bộ dữ liệu:** Giao dịch bán lẻ trực tuyến (E-commerce Transaction Data)  
**Mục tiêu:** Phân tích hành vi mua sắm, tần suất mua lặp lại và phân nhóm khách hàng (Tránh trùng lặp với nhóm 5 và 6).

---

### CÂU HỎI 1: BỨC TRANH TOÀN CẢNH KINH DOANH VÀ GIÁ TRỊ ĐƠN HÀNG TRUNG BÌNH (AOV)
* **Câu hỏi:** Tổng doanh thu hợp lệ, tổng số hóa đơn, số lượng khách hàng độc nhất và giá trị đơn hàng trung bình (Average Order Value - AOV) của sàn là bao nhiêu?
* **Ý nghĩa thực tiễn:** Giúp doanh nghiệp nắm bắt quy mô doanh thu cốt lõi và mức chi tiêu trung bình trên mỗi lượt mua hàng.
* **Kỹ thuật Pandas sử dụng:** Thống kê mô tả, `.sum()`, `.nunique()`, phép toán vector hóa kết hợp `.groupby("InvoiceNo")`.
* **Trạng thái:** 🟢 **ĐÃ HOÀN THÀNH** (Hàm `get_summary_metrics()` trong `src/customer_analyzer.py`).

---

### CÂU HỎI 2: TỶ LỆ KHÁCH HÀNG MUA LẠI (REPURCHASE RATE) VÀ TẦN SUẤT QUAY LẠI
* **Câu hỏi:** Tỷ lệ khách hàng mua lặp lại (>= 2 lần) chiếm bao nhiêu % so với khách hàng chỉ mua 1 lần? Trung bình mỗi khách hàng đặt bao nhiêu đơn?
* **Ý nghĩa thực tiễn:** Đo lường mức độ giữ chân khách hàng (Customer Retention) – yếu tố sống còn của sàn thương mại điện tử.
* **Kỹ thuật Pandas sử dụng:** `.groupby("CustomerID")["InvoiceNo"].nunique()`, đếm tần suất và tính tỷ lệ phần trăm.
* **Trạng thái:** 🟢 **ĐÃ HOÀN THÀNH** (Hàm `analyze_initial_repurchase()` trong `src/customer_analyzer.py`).

---

### CÂU HỎI 3: THỜI ĐIỂM VÀNG MUA SẮM (PEAK SHOPPING TIME PATTERNS)
* **Câu hỏi:** Các giao dịch mua sắm tập trung nhiều nhất vào những thứ mấy trong tuần và những khung giờ nào trong ngày?
* **Ý nghĩa thực tiễn:** Tối ưu hóa thời gian chạy quảng cáo (Flash Sale), phân bổ nhân sự chăm sóc khách hàng và vận hành kho bãi.
* **Kỹ thuật Pandas sử dụng:** `pivot_table(index="DayOfWeek", columns="Hour", values="InvoiceNo", aggfunc="nunique")`.
* **Trạng thái:** 🟢 **ĐÃ HOÀN THÀNH** (Hàm `analyze_shopping_time_patterns()`, đã vẽ biểu đồ Heatmap).

---

### CÂU HỎI 4: PHÂN KHÚC KHÁCH HÀNG THEO MÔ HÌNH RFM
* **Câu hỏi:** Cơ cấu khách hàng phân bổ như thế nào theo 3 tiêu chí: Mua gần đây (Recency), Tần suất mua (Frequency) và Tổng chi tiêu (Monetary)? Khách hàng được phân thành các nhóm nào (VIP/Champions, Tiềm năng, Cần chú ý, Nguy cơ rời bỏ)?
* **Ý nghĩa thực tiễn:** Giúp cá nhân hóa chiến lược marketing và chăm sóc khách hàng theo từng phân khúc.
* **Kỹ thuật Pandas sử dụng:** `.groupby("CustomerID").agg()`, tính khoảng cách ngày (`max_date - InvoiceDate`), phân vị `pd.qcut()` để gán điểm RFM Score.
* **Trạng thái:** 🟡 **CẦN TRIỂN KHAI CHO MỐC 04** (Hàm `compute_rfm_segments()`).

---

### CÂU HỎI 5: KIỂM CHỨNG NGUYÊN LÝ PARETO (QUY LUẬT 80/20) TRONG DOANH THU
* **Câu hỏi:** Nhóm khách hàng VIP (top chi tiêu) chiếm bao nhiêu % về số lượng và đóng góp bao nhiêu % tổng doanh thu của toàn bộ cửa hàng?
* **Ý nghĩa thực tiễn:** Xác định mức độ phụ thuộc của doanh nghiệp vào nhóm khách hàng chủ lực để có chính sách tri ân và giữ chân đặc biệt.
* **Kỹ thuật Pandas sử dụng:** `pd.merge()` ghép bảng phân khúc RFM với bảng doanh thu, `.groupby("Segment")["TotalAmount"].sum()`, tính tỷ lệ tích lũy (Cumulative %).
* **Trạng thái:** 🟡 **CẦN TRIỂN KHAI CHO MỐC 04** (Hàm `analyze_segment_revenue_contribution()`).

---

### CÂU HỎI 6: HÀNH VI HỦY ĐƠN VÀ HOÀN TRẢ HÀNG THEO TỪNG NHÓM KHÁCH HÀNG
* **Câu hỏi:** Nhóm khách hàng nào có tỷ lệ hủy đơn/hoàn trả hàng cao nhất và giá trị các đơn hủy ảnh hưởng như thế nào đến doanh số?
* **Ý nghĩa thực tiễn:** Nhận diện rủi ro vận hành, phát hiện nhóm khách hàng hay đổi trả hoặc các mã hàng có tỷ lệ lỗi cao.
* **Kỹ thuật Pandas sử dụng:** Lọc tập dữ liệu `InvoiceNo.str.startswith('C')`, ghép bảng `pd.merge()` với danh sách phân khúc khách hàng, tính tỷ lệ hủy đơn trên tổng số đơn.
* **Trạng thái:** 🟡 **CẦN TRIỂN KHAI CHO MỐC 04** (Hàm `analyze_cancellation_by_segment()`).

---

### CÂU HỎI 7: SỰ KHÁC BIỆT HÀNH VI GIỮA THỊ TRƯỜNG NỘI ĐỊA (UK) VÀ THỊ TRƯỜNG QUỐC TẾ
* **Câu hỏi:** Khách hàng tại thị trường nội địa (United Kingdom) và khách hàng tại các quốc gia khác có sự khác biệt như thế nào về giá trị trung bình mỗi đơn (AOV) và tần suất mua sắm?
* **Ý nghĩa thực tiễn:** Đánh giá tiềm năng mở rộng ra thị trường nước ngoài (Cross-border E-commerce) so với thị trường nội địa.
* **Kỹ thuật Pandas sử dụng:** Phân nhóm `np.where(df['Country'] == 'United Kingdom', 'Domestic', 'International')`, dùng `.groupby()` so sánh AOV, quy mô giỏ hàng và tổng doanh thu.
* **Trạng thái:** 🟡 **CẦN TRIỂN KHAI CHO MỐC 04** (Hàm `analyze_geographic_behavior()`).

---

## TỔNG KẾT ĐÁNH GIÁ SO VỚI YÊU CẦU BÀI TẬP LỚN (PTIT):
1. Đủ tối thiểu **07 câu hỏi phân tích** gắn liền trực tiếp với bài toán kinh doanh.
2. Có đầy đủ các thao tác kỹ thuật bắt buộc: **`groupby()`**, **`pivot_table()`** (Câu 3), và **`merge()`** (Câu 5, Câu 6).
3. Đủ điều kiện để trực quan hóa ra **4 loại biểu đồ** cho Mốc 04 (Heatmap, Donut/Pie, Boxplot, Bar chart kép).

