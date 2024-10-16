import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline
import pandas as pd
from scipy.signal import find_peaks


class DataPlotter3:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def plot_data(self):
        try:
            x = self.X
            y = self.Y

            print("x:", x)
            print("y:", y)

            # 筛选极大值点和极小值点
            peaks, _ = find_peaks(y)
            troughs, _ = find_peaks(-y)

            if len(peaks) == 0 or len(troughs) == 0:
                print("没有找到足够的极值点。")
                return

            # 提取极大值点的 x 和 y 值
            peak_x = x[peaks]
            peak_y = y[peaks]
            trough_x = x[troughs]
            trough_y = y[troughs]

            # 去重并排序
            unique_peak_x, indices = np.unique(peak_x, return_index=True)
            unique_peak_y = peak_y[indices]

            unique_trough_x, indices = np.unique(trough_x, return_index=True)
            unique_trough_y = trough_y[indices]

            # 样条插值
            cs_peaks = CubicSpline(unique_peak_x, unique_peak_y)
            cs_troughs = CubicSpline(unique_trough_x, unique_trough_y)

            # 生成样条插值曲线的 x 值
            x_spline = np.linspace(min(x), max(x), 100)
            y_upper = cs_peaks(x_spline)
            y_lower = cs_troughs(x_spline)
            # 计算均值包络线
            y_mean = (y_upper + y_lower) / 2

            spline_data = pd.DataFrame({
                'x_spline': x_spline,
                'y_mean': y_mean
            })
            return spline_data


        except Exception as e:
            print("出现错误:", e)

    # def find_peaks(self, data):
    #     """ 筛选极大值点 """
    #     peaks = []
    #     for i in range(1, len(data) - 1):
    #         if data[i] > data[i - 1] and data[i] > data[i + 1]:
    #             peaks.append(i)
    #     return peaks


