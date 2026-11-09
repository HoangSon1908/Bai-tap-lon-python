"""
Module: customer_analyzer.py
Lớp CustomerBehaviorAnalyzer đảm nhận phân tích hành vi mua sắm của khách hàng.

Hiện trạng (Mốc 03 - Ngày 10/11/2026):
- Đã hoàn thiện: Thống kê mô tả tổng quan (Summary Metrics).
- Đã hoàn thiện: Kết quả phân tích ban đầu về tần suất mua lại sơ bộ và thời điểm mua sắm (pivot_table).
- Khung mã nguồn (TODO): Các câu hỏi phân tích chuyên sâu (RFM, Pareto, Hủy đơn...)
  được để sẵn khung hàm để các thành viên trong nhóm tiếp tục triển khai cho Mốc 04 (Hạn 17/11).
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple


class CustomerBehaviorAnalyzer:
    """
    Lớp phân tích hành vi mua sắm, tần suất mua lại và phân nhóm khách hàng thương mại điện tử.
    """

    def __init__(self, df: pd.DataFrame, cancelled_df: pd.DataFrame = None):
        """
        Khởi tạo với DataFrame đã được làm sạch từ EcommerceDataProcessor.
        """
        if df is None or len(df) == 0:
            raise ValueError("[LỖI] Dữ liệu truyền vào phân tích rỗng.")
        self.df = df.copy()
        self.cancelled_df = cancelled_df.copy() if cancelled_df is not None else pd.DataFrame()
        self.rfm_df: pd.DataFrame = None

    # =========================================================================
    # KẾT QUẢ PHÂN TÍCH BAN ĐẦU (ĐÁP ỨNG MỐC 03 - 10/11/2026)
    # =========================================================================

    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        [MỐC 03] Thống kê mô tả tổng quan các chỉ số kinh doanh cốt lõi.
        """
        total_revenue = float(self.df["TotalAmount"].sum())
        total_orders = int(self.df["InvoiceNo"].nunique())
        total_customers = int(self.df["CustomerID"].nunique())
        aov = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0
        avg_items_per_order = round(self.df.groupby("InvoiceNo")["Quantity"].sum().mean(), 2)

        metrics = {
            "Total_Revenue": total_revenue,
            "Total_Orders": total_orders,
            "Total_Customers": total_customers,
            "Average_Order_Value": aov,
            "Avg_Items_Per_Order": avg_items_per_order,
            "Date_Min": self.df["InvoiceDate"].min(),
            "Date_Max": self.df["InvoiceDate"].max()
        }
        return metrics

    def analyze_initial_repurchase(self) -> Dict[str, Any]:
        """
        [MỐC 03] Phân tích sơ bộ tần suất mua lại (Repurchase Rate ban đầu):
        Đo lường tỷ lệ khách hàng mua 1 lần so với khách hàng quay lại mua sắm.
        """
        # Đếm số hóa đơn của từng khách hàng
        orders_per_customer = self.df.groupby("CustomerID")["InvoiceNo"].nunique()
        total_customers = len(orders_per_customer)
        repeat_customers = int((orders_per_customer > 1).sum())
        one_time_customers = int((orders_per_customer == 1).sum())
        repurchase_rate = round((repeat_customers / total_customers) * 100, 2)

        return {
            "total_customers": total_customers,
            "one_time_customers": one_time_customers,
            "repeat_customers": repeat_customers,
            "repurchase_rate_pct": repurchase_rate,
            "max_orders_by_single_customer": int(orders_per_customer.max()),
            "avg_orders_per_customer": round(float(orders_per_customer.mean()), 2)
        }

    def analyze_shopping_time_patterns(self) -> pd.DataFrame:
        """
        [MỐC 03] Phân tích thời điểm mua sắm phổ biến bằng pivot_table (Thứ trong tuần x Khung giờ).
        Đáp ứng yêu cầu kỹ thuật: sử dụng phương thức pivot_table() của Pandas.
        """
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        pivot = self.df.pivot_table(
            index="DayOfWeek",
            columns="Hour",
            values="InvoiceNo",
            aggfunc="nunique",
            fill_value=0
        )
        existing_days = [d for d in day_order if d in pivot.index]
        pivot = pivot.reindex(existing_days)
        return pivot

    # =========================================================================
    # CÁC MỤC PHÂN CÔNG THÀNH VIÊN TIẾP TỤC TRIỂN KHAI CHO MỐC 04 (HẠN 17/11)
    # =========================================================================

    def compute_rfm_segments(self) -> pd.DataFrame:
        """
        # TODO (Phân công Thành viên phụ trách Mốc 04 - Hạn 17/11):
        Tính toán mô hình phân khúc RFM (Recency, Frequency, Monetary):
        - Recency: Số ngày kể từ ngày mua hàng gần nhất đến mốc kết thúc dữ liệu.
        - Frequency: Tổng số đơn hàng duy nhất của khách hàng.
        - Monetary: Tổng số tiền khách hàng đã chi tiêu.
        Gợi ý: Dùng groupby('CustomerID') để tính R, F, M; sau đó dùng pd.qcut() chia điểm.
        """
        pass

    def analyze_segment_revenue_contribution(self) -> pd.DataFrame:
        """
        # TODO (Phân công Thành viên phụ trách Mốc 04 - Hạn 17/11):
        Đo lường mức độ đóng góp doanh thu theo từng phân khúc khách hàng (Kiểm chứng nguyên lý Pareto 80/20).
        Gợi ý: Dùng pd.merge() ghép bảng RFM với dữ liệu doanh thu, sau đó groupby('Segment').
        """
        pass

    def analyze_cancellation_by_segment(self) -> pd.DataFrame:
        """
        # TODO (Phân công Thành viên phụ trách Mốc 04 - Hạn 17/11):
        Đo lường tỷ lệ đơn hủy/hoàn trả (cancelled_df) theo từng phân khúc khách hàng.
        """
        pass

    def analyze_geographic_behavior(self, top_n: int = 5) -> pd.DataFrame:
        """
        # TODO (Phân công Thành viên phụ trách Mốc 04 - Hạn 17/11):
        So sánh hành vi mua hàng giữa thị trường nội địa (UK) và các thị trường quốc tế.
        """
        pass
