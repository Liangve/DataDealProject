import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline
import pandas as pd
from scipy.signal import find_peaks


class DataPlotter2:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def plot_data(self):
        try:
            x = self.X
            y = self.Y

            print("x:", x)
            print("y:", y)

            # 筛选极大值点
            # peaks = self.find_peaks(y)
            # if len(peaks) == 0:
            #     print("没有找到极大值点。")
            #     return
            #使用scipy.signal.find_peaks筛选极大值点
            peaks, _ = find_peaks(-y)
            if len(peaks) == 0:
                print("没有找到极大值点。")
                return
            # 提取极大值点的 x 和 y 值
            peak_x = x[peaks]
            peak_y = y[peaks]

            # 去重并排序
            unique_peaks = np.unique(peak_x)
            unique_peak_y = [peak_y[np.where(peak_x == p)[0][0]] for p in unique_peaks]
            peak_x, peak_y = unique_peaks, unique_peak_y

            # 样条插值
            cs = CubicSpline(peak_x, peak_y)

            # 生成样条插值曲线的 x 值
            x_spline = np.linspace(min(peak_x), max(peak_x), 100)
            y_spline = cs(x_spline)

            spline_data = pd.DataFrame({
                'x_spline': x_spline,
                'y_spline': y_spline
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


