"""
Module: visualizer.py
Lớp CustomerVisualizer phục vụ trực quan hóa dữ liệu bằng Matplotlib và Seaborn.

Hiện trạng (Mốc 03 - Ngày 10/11/2026):
- Đã hoàn thiện khung kết nối và 01 biểu đồ sơ bộ (Heatmap khung giờ mua sắm).
- Các biểu đồ còn lại (Phân bố mua lại, AOV, Phân khúc RFM, Tỷ lệ hủy đơn)
  để sẵn khung hàm TODO để thành viên phụ trách mảng Trực quan hóa triển khai cho Mốc 04 (17/11).
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class CustomerVisualizer:
    """
    Lớp vẽ và xuất các biểu đồ trực quan hóa dữ liệu hành vi khách hàng.
    """

    def __init__(self, output_dir: str = "outputs/figures"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        sns.set_theme(style="whitegrid")

    def plot_shopping_heatmap(self, pivot_df: pd.DataFrame, filename: str = "01_shopping_time_heatmap.png") -> str:
        """
        [MỐC 03] Biểu đồ sơ bộ: Heatmap mật độ giao dịch theo Giờ trong ngày và Ngày trong tuần.
        """
        plt.figure(figsize=(12, 6))
        sns.heatmap(
            pivot_df,
            cmap="YlGnBu",
            linewidths=0.5,
            annot=True,
            fmt="d",
            cbar_kws={"label": "Số lượng đơn hàng (Đơn)"}
        )
        plt.title("HÀNH VI MUA SẮM: SỐ LƯỢNG ĐƠN HÀNG THEO KHUNG GIỜ VÀ THỨ TRONG TUẦN", fontsize=13, fontweight="bold", pad=15)
        plt.xlabel("Khung giờ trong ngày (0h - 23h)", fontsize=11, labelpad=10)
        plt.ylabel("Ngày trong tuần", fontsize=11, labelpad=10)
        plt.tight_layout()

        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300)
        plt.close()
        print(f"[+] Đã lưu biểu đồ ban đầu: {filepath}")
        return filepath

    # =========================================================================
    # CÁC BIỂU ĐỒ TODO DÀNH CHO THÀNH VIÊN TRỰC QUAN HÓA (MỐC 04 - HẠN 17/11)
    # =========================================================================

    def plot_repurchase_distribution(self, repurchase_data: dict):
        """
        # TODO (Thành viên phụ trách Trực quan hóa - Mốc 04):
        Vẽ biểu đồ hình tròn (Donut chart) hoặc biểu đồ cột thể hiện tỷ lệ khách mua 1 lần vs khách mua lặp lại.
        """
        pass

    def plot_order_value_distribution(self, order_values: pd.Series):
        """
        # TODO (Thành viên phụ trách Trực quan hóa - Mốc 04):
        Vẽ Boxplot kết hợp Histogram/KDE phân bố giá trị đơn hàng (AOV).
        """
        pass

    def plot_rfm_segments_comparison(self, seg_summary: pd.DataFrame):
        """
        # TODO (Thành viên phụ trách Trực quan hóa - Mốc 04):
        Vẽ biểu đồ cột kép so sánh % khách hàng vs % doanh thu của các nhóm RFM (kiểm chứng Pareto).
        """
        pass
