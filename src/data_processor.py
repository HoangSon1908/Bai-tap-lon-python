"""
Module data_processor.py
Chứa lớp EcommerceDataProcessor chịu trách nhiệm:
1. Đọc dữ liệu thô (raw data) từ file CSV/Excel.
2. Kiểm tra cấu trúc dữ liệu, các trường khuyết thiếu, trùng lặp.
3. Làm sạch dữ liệu:
   - Loại bỏ các bản ghi không có CustomerID (vì bài toán tập trung vào hành vi khách hàng).
   - Loại bỏ trùng lặp (duplicates).
   - Xử lý các giao dịch hủy (InvoiceNo bắt đầu bằng 'C') và các giá trị số lượng/đơn giá bất thường.
   - Chuẩn hóa kiểu dữ liệu datetime cho cột InvoiceDate.
4. Kỹ thuật tạo biến (Feature Engineering):
   - Tính TotalAmount = Quantity * UnitPrice.
   - Trích xuất InvoiceYearMonth, DayOfWeek, Hour.
5. Xuất dữ liệu đã làm sạch ra thư mục data/processed.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple


class EcommerceDataProcessor:
    """
    Lớp xử lý và làm sạch dữ liệu thương mại điện tử phục vụ phân tích hành vi khách hàng.
    """

    def __init__(self, raw_path: str = "data/raw/ecommerce_data.csv",
                 processed_path: str = "data/processed/ecommerce_cleaned.csv"):
        """
        Khởi tạo processor với đường dẫn dữ liệu đầu vào và đầu ra.
        """
        self.raw_path = raw_path
        self.processed_path = processed_path
        self.df_raw: pd.DataFrame = None
        self.df_cleaned: pd.DataFrame = None
        self.cancelled_df: pd.DataFrame = None

    def load_data(self, nrows: int = None) -> pd.DataFrame:
        """
        Đọc dữ liệu thô từ file CSV với xử lý ngoại lệ.
        :param nrows: Số dòng đọc (nếu muốn lấy mẫu để chạy nhanh, mặc định đọc toàn bộ).
        :return: DataFrame thô.
        """
        if not os.path.exists(self.raw_path):
            raise FileNotFoundError(f"[LỖI] Không tìm thấy tệp dữ liệu thô tại: {self.raw_path}")

        print(f"[*] Đang đọc dữ liệu từ: {self.raw_path} ...")
        try:
            # Thử đọc với encoding latin1 (chuẩn cho Online Retail dataset) hoặc utf-8
            try:
                self.df_raw = pd.read_csv(self.raw_path, encoding="latin1", nrows=nrows)
            except UnicodeDecodeError:
                self.df_raw = pd.read_csv(self.raw_path, encoding="utf-8", nrows=nrows)

            print(f"[+] Đọc thành công: {len(self.df_raw):,} dòng và {len(self.df_raw.columns)} cột.")
            return self.df_raw
        except Exception as e:
            raise RuntimeError(f"[LỖI NGOẠI LỆ] Quá trình đọc dữ liệu thất bại: {e}")

    def inspect_structure(self) -> Dict[str, Any]:
        """
        Kiểm tra cấu trúc và hiện trạng dữ liệu thô.
        :return: Từ điển chứa các thông tin kiểm tra dữ liệu.
        """
        if self.df_raw is None:
            raise ValueError("[LỖI] Chưa tải dữ liệu thô. Hãy gọi hàm load_data() trước.")

        info = {
            "total_rows": len(self.df_raw),
            "total_columns": len(self.df_raw.columns),
            "columns": list(self.df_raw.columns),
            "missing_values": self.df_raw.isnull().sum().to_dict(),
            "duplicate_rows": int(self.df_raw.duplicated().sum()),
            "dtypes": {col: str(dtype) for col, dtype in self.df_raw.dtypes.items()}
        }
        return info

    def clean_data(self) -> pd.DataFrame:
        """
        Quy trình làm sạch dữ liệu:
        - Xóa trùng lặp
        - Xử lý thiếu CustomerID
        - Tách riêng các đơn hủy (InvoiceNo bắt đầu bằng 'C') để phục vụ phân tích câu hỏi tỷ lệ hủy đơn
        - Lọc các dòng giao dịch hợp lệ: Quantity > 0, UnitPrice > 0
        - Chuẩn hóa cột thời gian & kiểu dữ liệu
        - Tạo các trường mới: TotalAmount, YearMonth, DayOfWeek, Hour
        """
        if self.df_raw is None:
            self.load_data()

        print("[*] Bắt đầu quá trình tiền xử lý và làm sạch dữ liệu...")
        df = self.df_raw.copy()

        # 1. Loại bỏ các dòng trùng lặp hoàn toàn
        initial_count = len(df)
        df.drop_duplicates(inplace=True)
        dropped_duplicates = initial_count - len(df)
        print(f"  - Đã loại bỏ {dropped_duplicates:,} dòng trùng lặp.")

        # 2. Xử lý giá trị khuyết CustomerID
        missing_customers = df["CustomerID"].isnull().sum()
        df = df[df["CustomerID"].notnull()].copy()
        print(f"  - Đã loại bỏ {missing_customers:,} dòng không có CustomerID (để phục vụ phân tích hành vi khách hàng).")

        # Chuẩn hóa CustomerID thành kiểu số nguyên rồi chuyển thành chuỗi định danh
        df["CustomerID"] = df["CustomerID"].astype(int).astype(str)

        # 3. Chuẩn hóa thời gian InvoiceDate
        try:
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="mixed")
        except Exception:
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

        # 4. Tách các đơn hủy (Cancellations)
        # Các hóa đơn bắt đầu bằng chữ 'C' là đơn hủy hoặc trả hàng
        df["InvoiceNo"] = df["InvoiceNo"].astype(str)
        is_cancelled = df["InvoiceNo"].str.startswith("C") | (df["Quantity"] < 0)
        self.cancelled_df = df[is_cancelled].copy()
        print(f"  - Đã ghi nhận {len(self.cancelled_df):,} dòng đơn hủy/trả hàng (lưu riêng để phân tích hành vi hoàn trả).")

        # 5. Dữ liệu giao dịch mua hàng thành công
        df_valid = df[~is_cancelled].copy()
        df_valid = df_valid[(df_valid["Quantity"] > 0) & (df_valid["UnitPrice"] > 0)].copy()

        # 6. Kỹ thuật tạo đặc trưng mới (Feature Engineering)
        # Biến đổi 1: Tổng tiền từng mục hàng = Số lượng * Đơn giá
        df_valid["TotalAmount"] = (df_valid["Quantity"] * df_valid["UnitPrice"]).round(2)
        # Biến đổi 2: Trích xuất năm-tháng, ngày trong tuần, giờ mua hàng
        df_valid["InvoiceYearMonth"] = df_valid["InvoiceDate"].dt.to_period("M").astype(str)
        df_valid["DayOfWeek"] = df_valid["InvoiceDate"].dt.day_name()
        df_valid["Hour"] = df_valid["InvoiceDate"].dt.hour
        # Thứ tự ngày trong tuần để thuận tiện sắp xếp (Thứ 2 -> Chủ nhật)
        df_valid["DayOfWeekNum"] = df_valid["InvoiceDate"].dt.dayofweek

        # Làm sạch chuỗi Description
        if "Description" in df_valid.columns:
            df_valid["Description"] = df_valid["Description"].astype(str).str.strip().str.upper()

        self.df_cleaned = df_valid
        print(f"[+] Hoàn tất làm sạch! Dữ liệu sẵn sàng phân tích: {len(self.df_cleaned):,} dòng, {self.df_cleaned['CustomerID'].nunique():,} khách hàng duy nhất.")
        return self.df_cleaned

    def save_processed_data(self, output_path: str = None) -> str:
        """
        Lưu dữ liệu sạch ra tệp CSV.
        """
        if self.df_cleaned is None:
            raise ValueError("[LỖI] Chưa có dữ liệu sạch để lưu. Hãy gọi clean_data() trước.")

        save_to = output_path or self.processed_path
        os.makedirs(os.path.dirname(save_to), exist_ok=True)
        
        print(f"[*] Đang lưu dữ liệu sạch vào: {save_to} ...")
        self.df_cleaned.to_csv(save_to, index=False, encoding="utf-8-sig")
        print(f"[+] Lưu thành công vào {save_to}")
        return save_to

    def get_summary_report(self) -> str:
        """
        Tạo báo cáo tóm tắt quy trình làm sạch dữ liệu.
        """
        if self.df_cleaned is None:
            return "Chưa có dữ liệu làm sạch."

        report = [
            "=" * 60,
            "BÁO CÁO TỔNG KẾT TIỀN XỬ LÝ VÀ LÀM SẠCH DỮ LIỆU",
            "=" * 60,
            f"Số dòng thô ban đầu       : {len(self.df_raw):,}",
            f"Số dòng sau khi làm sạch  : {len(self.df_cleaned):,}",
            f"Tỷ lệ giữ lại             : {len(self.df_cleaned) / len(self.df_raw) * 100:.2f}%",
            f"Số khách hàng duy nhất    : {self.df_cleaned['CustomerID'].nunique():,}",
            f"Số hóa đơn mua thành công : {self.df_cleaned['InvoiceNo'].nunique():,}",
            f"Tổng số mặt hàng khác nhau: {self.df_cleaned['StockCode'].nunique():,}",
            f"Khoảng thời gian giao dịch: {self.df_cleaned['InvoiceDate'].min().strftime('%Y-%m-%d')} đến {self.df_cleaned['InvoiceDate'].max().strftime('%Y-%m-%d')}",
            f"Tổng doanh thu hợp lệ     : {self.df_cleaned['TotalAmount'].sum():,.2f} USD",
            "=" * 60
        ]
        return "\n".join(report)

