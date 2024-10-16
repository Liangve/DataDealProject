import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, ifft, fftfreq
import pandas as pd


class DataPlotter:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def plot_data(self):
        try:
            x = self.X
            y = self.Y

            print("x:", x)
            print("y:", y)

            # 执行傅里叶变换
            N = len(y)
            T = x[1] - x[0]  # 采样间隔
            yf = fft(y)
            xf = fftfreq(N, T)[:N//2]  # 频率范围

            # 提取傅里叶变换结果的幅值
            amplitudes = 2.0/N * np.abs(yf[0:N//2])

            # 选择显著频率成分（这里选择前几个最高的频率成分）
            num_significant_frequencies = 5
            significant_indices = np.argsort(amplitudes)[-num_significant_frequencies:]
            significant_frequencies = xf[significant_indices]

            print("显著频率成分:", significant_frequencies)

            # 构建显著频率成分的信号
            significant_yf = np.zeros_like(yf)
            for idx in significant_indices:
                significant_yf[idx] = yf[idx]

            # 进行逆傅里叶变换得到滤波后的信号
            filtered_signal = ifft(significant_yf)

            # 构建傅里叶变换数据
            fourier_data = pd.DataFrame({
                'x': x,
                'filtered_signal': np.real(filtered_signal)
            })

            # 绘制原始信号和滤波后的信号
            plt.figure(figsize=(14, 6))
            plt.subplot(2, 1, 1)
            plt.plot(fourier_data['x'], y, label='Original Signal')
            plt.plot(fourier_data['x'], fourier_data['filtered_signal'], label='Filtered Signal (Fourier)')
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('Amplitude')
            plt.title('Original Signal and Filtered Signal using Fourier Transform')

            # 绘制频谱图
            plt.subplot(2, 1, 2)
            plt.stem(xf, amplitudes, use_line_collection=True)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')
            plt.title('Frequency Spectrum')
            plt.show()

            return fourier_data

        except Exception as e:
            print("出现错误:", e)



